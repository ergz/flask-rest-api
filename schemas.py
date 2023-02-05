from marshmallow import Schema, fields

class BaseItemSchema(Schema):
    id = fields.Int(dump_only=True) # not used for validation
    price = fields.Str(required=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Str()
    store_id = fields.Int()

class BaseStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class BaseTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(BaseItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(BaseStoreSchema(), dump_only=True)

class StoreSchema(BaseStoreSchema):
    items = fields.List(fields.Nested(BaseItemSchema()), dump_only=True) 
    tags = fields.List(fields.Nested(BaseTagSchema()), dump_only=True)

class TagSchema(BaseTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(BaseStoreSchema(), dump_only=True)
