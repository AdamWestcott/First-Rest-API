from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name":"My store",
        "items":[
            {
                "name":"chair",
                "price": 15.99
            }
        ]
    }
]

#Gets All Stores
@app.get("/store") #http://127.0.0.1:5000/store - this tells the code to run the get_stores function when you access this url
def get_stores():
    return {"stores":stores}

#Creates a Store
@app.post("/store") #http://127.0.0.1:5000/store - this tells the code to run the create_stores function when you access this url
def create_stores():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items":[]}
    stores.append(new_store)
    return new_store, 201

#Allows you to update a stores items - accepts the store name to access it
@app.post("/store/<string:name>/item") #http://127.0.0.1:5000/store/<string:name>/item - this tells the code to run the create_item function when you access this url
def create_Item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name":request_data["name"],"price":request_data["price"]}
            store["items"].append(new_item)
            return new_item,201
    return {"message":"Store Not Found"},404

#Gets A specific Store
@app.get("/store/<string:name>") #http://127.0.0.1:5000/store/<string:name> - this tells the code to run the get_store function when you access this url
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message":"Store Not Found"},404

#Gets the items of a specific Store
@app.get("/store/<string:name>/item") #http://127.0.0.1:5000/store/<string:name>/items - this tells the code to run the get_store_items function when you access this url
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items":store["items"]}
    return {"message":"Store Not Found"},404