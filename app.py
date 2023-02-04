from flask import Flask, request
from flask_smorest import abort
from db import ITEMS, STORES

import uuid

app = Flask(__name__)

# list all stores
@app.get("/store")
def get_all_stores():
    return {"stores": list(STORES.values())}, 200

# list all items
@app.get("/item")
def get_all_items():
    return {"items": list(ITEMS.values())}, 200

# create a store
@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex

    new_store = {"id": store_id, **store_data}
    STORES[store_id] = new_store
    return new_store, 201

# get a single store
@app.get("/store/<string:store_id>")
def get_store_detail(store_id):
    try:
        return STORES[store_id], 200
    except KeyError:
        abort(404, message="store not found.")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del STORES[store_id]
        return {"message": "store deleted"}
    except KeyError:
        abort(404, "could not find store for deletion")


# create an item
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in STORES:
        abort(404, message="store not found.")
    
    item_id = uuid.uuid4().hex
    item = {"id": item_id, **item_data}
    ITEMS[item_id] = item
    return item, 201

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return ITEMS[item_id]
    except KeyError:
        abort(404, message="item not found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del ITEMS[item_id]
        return {"message": "item deleted"}
    except KeyError:
        abort(404, "item not found for deletion")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="bad request")
    
    try:
        item = ITEMS[item_id]
        item |= item_data
        return item, 201
    except KeyError:
        abort(404, "item not found")



    