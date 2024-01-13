import firebase_admin
from firebase_admin import credentials, firestore
def initializeApp():
    # Initialize Firebase with the configuration file
    cred = credentials.Certificate("firebaseConfig.json")
    firebase_admin.initialize_app(cred)


def uploadData(collection_name, d1, d2 = {}, d3 = {}):
    data = d1 | d2 | d3
    # Get the Firestore database instance
    db = firestore.client()
    
    print(f"Files to upload:\n{data}")

    # Get the reference to the collection and upload the data
    collection_ref = db.collection(collection_name)
    collection_ref.add(data)