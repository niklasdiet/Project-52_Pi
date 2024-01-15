from pymongo import MongoClient

def connectToDB(username, password):
    connection_string = f"mongodb+srv://{username}:{password}@cluster0.qgruyjo.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    return client


def uploadData(client, collection_name, d1, d2 = {}, d3 = {}):
    data = d1 | d2 | d3
    
    db = client['cluster0']
    print(f"Files to upload:\n{data}")

    # Get the reference to the collection and upload the data
    collection_ref = db[collection_name]
    id = collection_ref.insert_one(data)
    print(f"Data uploaded with id: {id}")

