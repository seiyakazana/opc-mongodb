from pymongo import MongoClient
import bcrypt

MONGO_URI = "mongodb://mongo:27017"
DB_NAME = "mydb"

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
