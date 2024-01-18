from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def uploadData(device, username, password, dbName, collection_name, d1, d2 = {}, d3 = {}):
    d4 = {"device": device}
    data = d1 | d2 | d3 | d4
    
    client = connectToDB(username, password)
    db = client[dbName]
    print(f"Files to upload:\n{data}")

    # Get the reference to the collection and upload the data
    collection_ref = db[collection_name]
    id = collection_ref.insert_one(data)
    print(f"Data uploaded with id: {id}")



def connectToDB(username, password):
    connection_string = f"mongodb+srv://{username}:{password}@cluster0.qgruyjo.mongodb.net/?retryWrites=true&w=majority"
    
    # Create a new client and connect to the server
    client = MongoClient(connection_string, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
    