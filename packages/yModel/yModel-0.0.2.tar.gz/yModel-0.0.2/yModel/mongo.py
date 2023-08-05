from datetime import datetime
from json import JSONEncoder
from pathlib import PurePath

import bson
from pymongo.errors import InvalidOperation

from marshmallow import fields, ValidationError, missing
from marshmallow.validate import Range

from yModel import Schema, Tree

class MongoJSONEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, (bson.ObjectId, bson.decimal128.Decimal128)):
      return str(obj)
    elif isinstance(obj, datetime):
      return obj.isoformat(timespec = 'milliseconds')

    return JSONEncoder.default(self, obj)

class ObjectId(fields.Field):
  def _deserialize(self, value, attr, data):
    try:
      return bson.ObjectId(value)
    except Exception:
      raise ValidationError('invalid ObjectId `%s`' % value)

  def _serialize(self, value, attr, obj):
    if value is None:
      return missing
    return str(value)

class Decimal(fields.Field):
  def _deserialize(self, value, attr, data):
    try:
      return bson.decimal128.Decimal128(str(value))
    except Exception:
      raise ValidationError('invalid Decimal `%s`' % value)

  def _serialize(self, value, attr, obj):
    if value is None:
      return missing

    return str(value)

class Decimal128Range(Range):
  def __call__(self, value):
    if self.min is not None and value.to_decimal() < self.min.to_decimal():
      message = self.message_min if self.max is None else self.message_all
      raise ValidationError(self._format_error(value, message))

    if self.max is not None and value.to_decimal() > self.max.to_decimal():
      message = self.message_max if self.min is None else self.message_all
      raise ValidationError(self._format_error(value, message))

    return value

class NotFound(Exception):
  pass

class MongoSchema(Schema):
  encoder = MongoJSONEncoder

  async def create(self):
    if not self.table:
      raise InvalidOperation("No table")

    data = self.get_data()
    if not data:
      raise InvalidOperation("No data")

    result = await self.table.insert_one(data)

    if result.inserted_id:
      self.__data__["_id"] = result.inserted_id

  async def get(self, **kwargs):
    if not self.table:
      raise InvalidOperation("No table")

    query = kwargs.pop("query", kwargs)
    many = kwargs.pop("many", False)

    data = await self.table.find(query).to_list(None) if many else await self.table.find_one(query)
    if not data:
      raise NotFound(query)

    self.load(data, many)

  async def update(self, data = None):
    if not self.table:
      raise InvalidOperation("No table")

    if "_id" not in self.__data__:
      raise InvalidOperation("The object hasn't been saved {}".format(self.get_data()))

    if data is None:
      data = self.get_data().copy()

    model = self.__class__(self.table, only = tuple(data.keys()))
    model.load(data)
    errors = model.get_errors()
    if errors:
      raise ValidationError(errors)

    if "_id" in data:
      del data["_id"]

    result = self.table.update_one({"_id": self._id}, {"$set": data})
    self.__data__.update(data)

    return model

  async def remove_field(self, field):
    if not self.table:
      raise InvalidOperation("No table")

    if not self._id:
      raise InvalidOperation("The object hasn't been saved {}".format(self.get_data()))

    await self.table.update_one({"_id": self._id}, {"$unset": {field: 1}})
    del self.__data__[field]

  async def delete(self):
    if not self.table:
      raise InvalidOperation("No table")

    if not self._id:
      raise InvalidOperation("The object hasn't been saved {}".format(self.get_data()))

    await self.table.delete_one({"_id": self._id})

class MongoTree(MongoSchema, Tree):
  async def ancestors(self, models, parent = False):
    if not self.table:
      raise InvalidOperation("No table")

    purePath = PurePath(self.path)
    elements = []
    while purePath.name != '' and purePath.parent != '/':
      doc = await self.table.find_one({"path": str(purePath.parent), "slug": purePath.name})
      if doc:
        model = getattr(models, doc["type"])(self.table)
        model.load(doc)
        if not model.get_errors():
          if parent:
            return model
          else:
            elements.append(model)

      purePath = purePath.parent

    elements.reverse()
    return elements

  async def create_child(self, child, as_, indexer = "slug"):
    if not self.table:
      raise InvalidOperation("No table")

    if child.__class__.__name__ == self.children_models[as_]:
      child.table = self.table
      # start transaction
      async with await self.table.database.client.start_session() as s:
        async with s.start_transaction():
          await child.create()
          items = getattr(self, as_, None)
          if items is not None:
            items.append(getattr(child, "_id" if isinstance(self.fields[as_].container, ObjectId) else indexer))
            query = {}
            query[as_] = items
            await self.table.update_one({"_id": self._id}, {"$set": query})
      # end transaction
      return child.to_plain_dict()
    else:
      ValidationError("Unexpected child model: {} vs {}".format(child.__name__, self.children_models[as_]))

  async def children(self, member, models, sort = None):
    if not self.table:
      raise InvalidOperation("No table")

    if isinstance(member, str):
      type_ = self.children_models[member]
      if not sort:
        sort = {"$sort": {"__order": 1}}
      order = getattr(self, member)
      if isinstance(self.fields[member].container, ObjectId):
        match = {"$match": {"_id": {"$in": order}}}
        addOrder = {"$addFields": {"__order": {"$indexOfArray": [order, "$_id"]}}}
      else:
        match = {"$match": {"path": self.get_url(), "type": type_}}
        addOrder = {"$addFields": {"__order": {"$indexOfArray": [order, "$slug"]}}}

      docs = await self.table.aggregate([match, addOrder, sort]).to_list(None)
    else:
      type_ = member.__name__
      aggregation = [{"$match": {"path": self.get_url(), "type": type_}}]
      if sort:
        aggregation.append(sort)

      docs = await self.table.aggregate(aggregation).to_list(None)

    model_class = getattr(models, type_)
    children = model_class(self.table, many = True)
    children.load(docs, many = True)

    return children

  async def update(self, data, models = None):
    if not self.table:
      raise InvalidOperation("No table")
 
    # Start mongo transaction
    async with await self.table.database.client.start_session() as s:
      async with s.start_transaction():
        if "slug" in data and data["slug"] and self.slug != data["slug"]:
          # update parent
          parent = await self.ancestors(models, True)
          # look_at is the list of members of self of type model_name (everyone where I can put of this type)
          look_at = parent.children_of_type(self.__class__.__name__)

          if look_at:
            # search on them to see if self is there and annotate to update the new slug
            to_set = {}
            for child in look_at:
              try:
                orig = getattr(parent, child)
                # if self is not indexed in this parent's member it will crash with ValueError (which is ok cause we only care when it's found)
                # when we put _id instead of slug we don't need to update the index so its ok too that will crash
                index = orig.index(self.slug)
                orig[index] = data["slug"]
                to_set[child] = orig
              except ValueError:
                pass

            if to_set:
              await parent.table.update_one({"_id": parent._id}, {"$set": to_set})

          # update children
          url = self.get_url()
          new_url = "{}/{}".format(("" if self.path == "/" else self.path), data["slug"])
          async for child in self.table.find({"path": {"$regex": "^{}".format(url)}}):
            path = child["path"].replace(url, new_url)
            # TODO: can we bulk this, please?
            await self.table.update_one({"_id": child["_id"]}, {"$set": {"path": path}})

        # update itself
        model = await super().update(data)

    return model

  async def delete(self, models = None):
    if not self.table:
      raise InvalidOperation("No table")

    path = self.get_url()
    async with await self.table.database.client.start_session() as s:
      async with s.start_transaction():
        # start transaction
        # update parent
        parent = await self.ancestors(models, True)
        if parent:
          # look_at is the list of members of self of type model_name (everyone where I can put of this type)
          look_at = parent.children_of_type(self.__class__.__name__)

          if look_at:
            # search on them to see if self is there and annotate to update the new slug
            to_set = {}
            for child in look_at:
              try:
                orig = getattr(parent, child)
                # if self is not indexed in this parent's member it will crash with ValueError (which is ok cause we only care when it's found)
                # when we put _id instead of slug we don't need to update the index so its ok too that will crash
                index = orig.index(self.slug)
                orig.pop(index)
                to_set[child] = orig
              except ValueError:
                pass

            if to_set:
              await parent.table.update_one({"_id": parent._id}, {"$set": to_set})
        # delete children
        await self.table.delete_many({"path": {"$regex": "^{}".format(path)}})
        # delete itself
        await super().delete()
        # end transaction
