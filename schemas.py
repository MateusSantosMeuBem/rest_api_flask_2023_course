from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    # dump_only=True means we will not give a request with "id"
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)


class ItemUpdateSchema(Schema):
    # dump_only=True means we will not give a request with "id"
    name = fields.String()
    price = fields.Float()


