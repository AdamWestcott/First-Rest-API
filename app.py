import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items,stores

app = Flask(__name__)

#Gets All Stores
@app.get("/store") #http://127.0.0.1:5000/store - this tells the code to run the get_stores function when you access this url
def get_stores():
    return {"stores":list(stores.values())}

#Gets All Items
@app.get("/item") #http://127.0.0.1:5000/item - this tells the code to run the get_items function when you access this url
def get_items():
    return {"items":list(items.values())}

#Creates a Store
@app.post("/store") #http://127.0.0.1:5000/store - this tells the code to run the create_stores function when you access this url
def create_stores():
    store_data = request.get_json()
    #Checks name has been passed to API
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    
    #Checks if Store already exists
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")
    
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id":store_id}
    stores[store_id] = new_store
    return new_store, 201

#Allows you to update a stores items - accepts the store name to access it
@app.post("/item") #http://127.0.0.1:5000/store/<string:name>/item - this tells the code to run the create_item function when you access this url
def create_Item():
    item_data = request.get_json()
    #Checks if all values have been passed to API
    if(
        "price" not in item_data 
        or "store_id" not in item_data
        or "name" not in item_data

    ):
        abort(
            400,
            message = "Bad Request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload"
        )

    #Checks if Item Already Exists
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
           abort(400, message=f"Item already exists.")
    
    #Checks if store that items are being added to exists
    if item_data["store_id"] not in stores:
        abort(404, message = "Store not found.")
    
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id":item_id}
    items[item_id] = new_item
    return new_item,201

#Gets A specific Store
@app.get("/store/<string:store_id>") #http://127.0.0.1:5000/store/<string:name> - this tells the code to run the get_store function when you access this url
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message = "Store not found.")

#Deletes A Store
@app.delete("/store/<string:store_id>") #http://127.0.0.1:5000/store/<string:name>/items - this tells the code to run the get_item function when you access this url
def del_store(store_id):
    try:
        del[stores[store_id]]
        return {"message": "Store has been deleted"}
    except KeyError:
        abort(404, message = "Store not found.")

#Updates a Store
@app.put("/store/<string:store_id>") #http://127.0.0.1:5000/store/<string:name>/items - this tells the code to run the get_item function when you access this url
def update_store(store_id):
    store_data = request.get_json()
    if "price" not in store_data or "name" not in store_data:
        abort(404, message = "Bad Request. Ensure 'price' and 'name' are included in JSON payload")
    try:
        store = stores[store_id]
        store |= store_data
        return store
    except KeyError:
        abort(404, message = "Item not found.")

#Gets a specific Item
@app.get("/item/<string:item_id>") #http://127.0.0.1:5000/store/<string:name>/items - this tells the code to run the get_item function when you access this url
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message = "Item not found.")

#Deletes an Item
@app.delete("/item/<string:item_id>") #http://127.0.0.1:5000/store/<string:item_id> - this tells the code to run the del_item function when you access this url
def del_item(item_id):
    try:
        del[items[item_id]]
        return {"message": "Item has been deleted"}
    except KeyError:
        abort(404, message = "Item not found.")

#Updates an Item
@app.put("/item/<string:item_id>") #http://127.0.0.1:5000/store/<string:name>/items - this tells the code to run the get_item function when you access this url
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(404, message = "Bad Request. Ensure 'price' and 'name' are included in JSON payload")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message = "Item not found.")