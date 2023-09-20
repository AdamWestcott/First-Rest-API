from flask import Flask

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
@app.get("/store") #http://127.0.0.1:5000/store - this tells the code to run the get_stores function when you access this url
def get_stores():
    return {"stores":stores}