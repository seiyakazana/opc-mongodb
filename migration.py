import pandas as pd
from pymongo import MongoClient
from integrity import check_integrity

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
    df = df.drop_duplicates()
    df['Name'] = df['Name'].str.title()
    check_integrity(df)
    records = df.to_dict(orient="records")

    result = coll.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} documents into {DB_NAME}.{COLLECTION_NAME}")

    df_after = pd.DataFrame(list(coll.find({}, {"_id": 0})))
    check_integrity(df_after)

def main():
    migrate_csv_to_mongo()

if __name__ == "__main__":
    main()