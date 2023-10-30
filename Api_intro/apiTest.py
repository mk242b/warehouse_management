import requests

print("API Testing")
print("-------")
while True:
    option = input("1 to put or update::\n2 to get::\n3 to find::\n4 to delete::")
    if option == "1":
        id = int(input("Enter your id::"))
        name = input("Enter your name::")
        price = int(input("Enter your price::"))
        model = input("Enter your model::")
        disc = input("Enter your discription::")
        data = {"name" : name , "price" : price ,"model" : model , "discription" : disc}
        response = requests.put("http://127.0.0.1:8000/put/{}".format(id),json=data)

    if option == "2":
        response = requests.get("http://127.0.0.1:8000/get_item/{item_name}")
        if response.status_code == 200:
            print(response.json())
    if option == "3":
        model_name = input("Enter your model name::")
        response = requests.get("http://127.0.0.1:8000/find/{}".format(model_name))
        if response.status_code == 200:
            print("Found : " , response.json() )
        else:
            print("Error")
    if option == "4":
        item_id = int(input("Enter your id::"))
        response = requests.put("http://127.0.0.1:8000/delete/{}".format(item_id))
        if response.status_code == 200:
            print(response.text)
        else:
            print("Invalid")