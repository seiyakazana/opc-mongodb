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

def migrate_csv_to_mongo():
    #import csv
    df = pd.read_csv(CSV_PATH)

    #transform
    df['Name'] = df['Name'].str.title()
    records = df.to_dict(orient="records")

    result = coll.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} documents into {DB_NAME}.{COLLECTION_NAME}")

def create(document):
    result = coll.insert_one(document)
    return result.inserted_id

def read_one(filter):
    return coll.find_one(filter)

def update_one(filter, update, upsert):
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
    migrate_csv_to_mongo()
    #Create one
    new_id = create({"Name": "New Person", "Age": 99, "City": "Paris"})
    print("Inserted one document with _id:", new_id)

    #Read one (by id)
    one = read_one({"_id": new_id})
    print("Read one by _id:", one)

    #Update one
    upd = update_one({"_id": new_id}, {"$set": {"Age": 100}})
    print("Update result:", upd)

    #Delete one
    upd = update_one({"_id": new_id}, {"$set": {"Age": 100}})
    print("Update result:", upd)

if __name__ == "__main__":
    main()