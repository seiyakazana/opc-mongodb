import pandas as pd
from pymongo import MongoClient

#config
CSV_PATH = "/app/data/healthcare_dataset.csv"
MONGO_URI      = "mongodb://mongo:27017"
DB_NAME        = "mydb"
COLLECTION_NAME= "mycollection"

#mongodb config
client = MongoClient(MONGO_URI)
coll = client[DB_NAME][COLLECTION_NAME]

def create(document):
    result = coll.insert_one(document)
    return result.inserted_id

def read_one(filter):
    return coll.find_one(filter)

def update_one(filter, update, upsert=False):
    res = coll.update_one(filter, update, upsert=upsert)
    return {
        "matched_count": res.matched_count,
        "modified_count": res.modified_count,
        "upserted_id": str(res.upserted_id) if res.upserted_id else None,
    }

def delete_one(filter) :
    res = coll.delete_one(filter)
    return res.deleted_count


def main():

    new_patient = {
        "Name": "Marco Alvarez",
        "Age": 54,
        "Gender": "Male",
        "Blood Type": "A+",
        "Medical Condition": "Hypertension",
        "Date of Admission": "2023-11-12",
        "Doctor": "Sarah Thompson",
        "Hospital": "St. Helena General Hospital",
        "Insurance Provider": "United Health",
        "Billing Amount": 6220.55,
        "Room Number": 208,
        "Admission Type": "Emergency",
        "Discharge Date": "2023-11-18",
        "Medication": "Lisinopril",
        "Test Results": "Normal",
    }


    # Create one
    new_id = create(new_patient)
    print("Inserted one document with _id:", new_id)

    # Read one (by id)
    one = read_one({"_id": new_id})
    print("Read one by _id:", one)

    # Update one (for example, change test result)
    upd = update_one({"_id": new_id}, {"$set": {"Test Results": "Abnormal"}})
    print("Update result:", upd)

    # Delete one
    deleted = delete_one({"_id": new_id})
    print("Deleted documents:", deleted)

if __name__ == "__main__":
    main()