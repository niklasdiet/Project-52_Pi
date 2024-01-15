from pymongo import MongoClient


def uploadData(username, password, dbName, collection_name, d1, d2 = {}, d3 = {}):
    data = d1 | d2 | d3
    
    connection_string = f"mongodb+srv://{username}:{password}@cluster0.qgruyjo.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client[dbName]
    print(f"Files to upload:\n{data}")

    # Get the reference to the collection and upload the data
    collection_ref = db[collection_name]
    id = collection_ref.insert_one(data)
    print(f"Data uploaded with id: {id}")

