from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING
from datetime import datetime
import os
from gridfs import GridFS
from bson import ObjectId


def round_to_5_minutes(dt):
    # Round the minutes to the nearest 5
    rounded_minutes = (dt.minute // 5) * 5
    # Set seconds to 0
    dt = dt.replace(minute=rounded_minutes, second=0, microsecond=0)
    return dt


def uploadData(client, dbName, collection_name, d1):
    # Get the current time
    current_time = datetime.now()

    # Round to the nearest 5 minutes
    rounded_time = round_to_5_minutes(current_time)

    d4 = {"device_id": "hub0001","time": rounded_time}
    d1.update(d4)
    
    db = client[dbName]

    # Get the reference to the collection and upload the data
    collection_ref = db[collection_name]
    id = collection_ref.insert_one(d1)
    print(f"Data uploaded with id: {id}")
    return id



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


def upload_image_to_mongodb(client, image_path, db_name, collection_name, device_info):
    current_time = datetime.now()

    # Round to the nearest 5 minutes
    rounded_time = round_to_5_minutes(current_time)

    # Connect to the specified database
    db = client[db_name]

    
    # Initialize GridFS
    fs = GridFS(db, collection=collection_name)
    
    # Open the image file
    with open(image_path, 'rb') as image_file:
        # Create a document with additional metadata
        metadata = {
            'timestamp': rounded_time,
            'device_id': device_info
        }
        
        # Store the image and metadata in GridFS
        file_id = fs.put(image_file, filename=image_path, metadata=metadata)
    

    
    print(f"Image uploaded to MongoDB with file ID: {file_id}")
    os.remove(image_path)

    #return file_id

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
