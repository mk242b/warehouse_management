from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import psycopg2
myData = {}

class Item(BaseModel):
    
    name : str
    price : float
    model : str
    discription : str

app = FastAPI()
@app.get("/get_item/{item_name}")
def get_item():
    returnData = {}
    connection = psycopg2.connect(   
    database="garage_data",
    user="postgres",
    password="8920",
    host="localhost",
    port="5432")

    cur = connection.cursor()
    cur.execute("SELECT * FROM myData")
    rows = cur.fetchall()

    # Process the fetched rows here
    for row in rows:
        newDict = {row[0] :{"name" : row[1]  , "price" : row[2]  ,"model" : row[3]  , "discription" : row[4] }}
        returnData.update(newDict)
    


    # Close the cursor and connection
    cur.close()
    connection.close()
    return returnData

@app.put("/update/{item_id}")
def update_item(item_id : int , item : Item):
    item_dict = item.dict()
    
    update_to_postgre(item_id,item_dict)
    return item

@app.put("/put/{item_id}")
def put_item(item_id : int , item : Item):
    item_dict = item.dict()
    
    put_to_postgre(item_id,item_dict)
    return item
    
@app.get("/find/{model_name}")
def find_model(model_name: str):

    toReturn = {}
    connection = psycopg2.connect(   
    database="garage_data",
    user="postgres",
    password="8920",
    host="localhost",
    port="5432")

    cur = connection.cursor()
    cur.execute("SELECT * FROM myData")
    rows = cur.fetchall()

    for row in rows:
        if row[3] == model_name:
            newDict = {row[0] :{"name" : row[1]  , "price" : row[2]  ,"model" : row[3]  , "discription" : row[4] }}

            toReturn.update(newDict)
    if not toReturn:
        return None
    cur.close()
    connection.close()
    return toReturn
    
@app.put("/delete/{item_id}")
def delete_model(item_id : int):
    try:
        connection = psycopg2.connect(   
        database="garage_data",
        user="postgres",
        password="8920",
        host="localhost",
        port="5432")

        cur = connection.cursor()
        cur.execute("DELETE FROM myData WHERE id=%s",(item_id,))
        connection.commit()
        return "Deletion Successful"
    except Exception as error:
    # Handle any exceptions that occur during deletion
        print("Error:", error)

    finally:
        # Close the cursor and connection
        cur.close()
        connection.close()
def update_to_postgre(id,data):
    connection = psycopg2.connect(   
    database="garage_data",
    user="postgres",
    password="8920",
    host="localhost",
    port="5432")

    update_query = """
    UPDATE myData
    SET name = %s, price = %s, model = %s, discription = %s
    WHERE id = %s;
    """
    cur = connection.cursor()
    print(data)
    cur.execute( update_query,(data["name"],data["price"],data["model"],data["discription"],id))

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cur.close()
    connection.close()


def put_to_postgre(id,data):
    connection = psycopg2.connect(   
    database="garage_data",
    user="postgres",
    password="8920",
    host="localhost",
    port="5432")

    cur = connection.cursor()
    print(data)
    cur.execute("INSERT INTO myData (id, name, price , model , discription) VALUES (%s, %s ,%s,%s,%s)", (id,data["name"],data["price"],data["model"],data["discription"]))

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cur.close()
    connection.close()
