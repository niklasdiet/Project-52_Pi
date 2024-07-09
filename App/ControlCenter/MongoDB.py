from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING
from datetime import datetime
import os
from gridfs import GridFS
from bson import ObjectId



def uploadData(client, dbName, collection_name, data):

    db = client[dbName]

    # Get the reference to the collection and upload the data
    collection_ref = db[collection_name]
    id = collection_ref.insert_one(data)
    print(f"Data uploaded with id: {id}")
    return id

def updateStock(data, client, collection, db = 'Stock'):
    try:
        uploadData(client, db, collection, data)
    except:
        print("Error updating stock {culture}")
        uploadData(client, 'ErrorLogs', 'Logs', {'errorMessage': "Error updating stock {culture}", 'time': datetime.now()})


def getData(client, dbName, collection_name):
    db = client[dbName]
    collection = db[collection_name]
    return collection.find({})

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


def download_image_from_mongodb(client, file_id, db_name, file_name):
    IMAGE_SAVE_DIR = "downloadedImages/"
    # Connect to the specified database
    db = client[db_name]
    
    # Initialize GridFS
    fs = GridFS(db, collection="imageData")
    
    # Find the file by its ID
    file_data = fs.get(ObjectId(file_id))

    with open(os.path.join(IMAGE_SAVE_DIR, file_name), "wb") as image_file:
        image_file.write(file_data.read())
    
    print(f"Image downloaded from MongoDB and saved to: {file_name}")


# Function to convert ObjectId to a datetime object
def get_datetime_from_objectid(objectid):
    return objectid.generation_time


def downloadAllImages(client, db_name, collection_name):
    # Query to fetch the images
    db = client[db_name]
    fs = GridFS(db, collection=collection_name)
    
    # Fetching and saving the images
    for document in fs.find({}):
        object_id = document._id
        image_data = document.read() # Change 'image_field' to your specific field name
        
        if image_data:
            date_time = get_datetime_from_objectid(ObjectId(object_id))

            # Getting date and time from ObjectId
            formatted_date_time = date_time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{formatted_date_time}.jpg"  # Assuming the image is in JPEG format
            download_image_from_mongodb(client, object_id, db_name, file_name)
        else:
            print(f"No image data found for document with ID: {object_id}")

    print("Images downloaded successfully.")

    # Close the MongoDB connection
