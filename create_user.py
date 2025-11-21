from pymongo import MongoClient
import bcrypt
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://app_user:app_user_pwd@mongo:27017/mydb?authSource=mydb")
DB_NAME = os.getenv("DB_NAME", "mydb")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]

username = input("Username: ").strip()
password = input("Password: ").strip()
role = input("Role (admin/doctor): ").strip()

password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

users.insert_one({
    "username": username,
    "password_hash": password_hash,
    "role": role,
})

print("User created successfully!")
client.close()
