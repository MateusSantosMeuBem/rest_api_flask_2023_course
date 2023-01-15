import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import (
    items,
    stores,
)

from schemas import (
    ItemSchema,
    ItemUpdateSchema
)

blp = Blueprint('items', __name__, description='Operations on items')

@blp.route('/item/<item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if item := items.get(item_id, None):
            return item, 200

        return abort(404, message='Item not found!')

    def delete(self, item_id):
        if items.get(item_id):
            del items[item_id]
            return {'message': 'Item deleted.'}

        return abort(404, message='Item not found!')

    # Decorators order matters
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        if item := items.get(item_id):
            item |= item_data
        else:
            abort(404, message='Item not found.')

        return item, 201
    

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return list(items.values())

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, new_item):
        for item in items.values():
            if new_item.get('name') == item.get('name')\
            and new_item.get('store_id') == item.get('store_id'):
                abort(
                    404,
                    message=f'Item already exists.'
                )

        if new_item.get('store_id') in stores:
            item_id = uuid.uuid4().hex
            items[item_id] = {
                **new_item,
                'id': item_id,
            }

            return items.get(item_id)
        
        return abort(404, message='Store not found!')