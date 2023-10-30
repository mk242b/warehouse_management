from fastapi import FastAPI
from typing import Union

myItemList = ["weather","kmp","sayaGyi"]
app = FastAPI()

@app.get("/")
def read_root():
    return {"Data" : "This is somedata"}

@app.get("/items/{item_id}")

def read_items(item_id : int , q:Union[str,None] = None ):
    return({"item_id" : item_id , "q" : q})



@app.get("/name/{item_name}")

def find_item(item_name : str):
    for i in myItemList:
        if item_name == i:
            return {"Your Item" : i}
    else:
            return {"Your item" : "Invalid"}