import pandas as pd
from pymongo import MongoClient

CSV_PATH = "/app/data/healthcare_dataset.csv"
MONGO_URI      = "mongodb://mongo:27017"
DB_NAME        = "mydb"
COLLECTION_NAME= "mycollection"

def main():
    #import csv
    df = pd.read_csv(CSV_PATH)

    #transform
    df['Name'] = df['Name'].str.title()
    records = df.to_dict(orient="records")

    #insert in mongodb
    client = MongoClient(MONGO_URI)
    coll = client[DB_NAME][COLLECTION_NAME]

    result = coll.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} documents into {DB_NAME}.{COLLECTION_NAME}")

if __name__ == "__main__":
    main()