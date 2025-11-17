# auth_app.py
from getpass import getpass

from pymongo import MongoClient
import bcrypt

MONGO_URI = "mongodb://mongo:27017"  
DB_NAME = "mydb"
PATIENT_COLLECTION = "mycollection"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]
patients = db[PATIENT_COLLECTION]

ROLE_PERMISSIONS = {
    "admin": {
        "read_patients",
        "update_patients",
        "create_patients",
        "delete_patients",
        "search_patients",
    },
    "doctor": {
        "read_patients",
        "update_patients",
        "search_patients",
    },
}

def verify_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)

def login():
    print("=== Login ===")
    while True:
        username = input("Username: ").strip()
        password = getpass("Password: ")

        user = users.find_one({"username": username})
        if not user:
            print("Invalid username or password.\n")
            continue

        if not verify_password(password, user["password_hash"]):
            print("Invalid username or password.\n")
            continue

        print(f"\nLogged in as {user['username']} (role: {user['role']})\n")
        return user

def has_permission(user, action: str) -> bool:
    role = user.get("role")
    allowed_actions = ROLE_PERMISSIONS.get(role, set())
    return action in allowed_actions

REQUIRED_COLS = [
    'Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition',
    'Date of Admission', 'Doctor', 'Hospital', 'Insurance Provider',
    'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date',
    'Medication', 'Test Results'
]


def list_patients(user):
    if not has_permission(user, "read_patients"):
        print("Access denied.\n")
        return

    print("=== Patients ===")
    for p in patients.find():
        line = " | ".join(f"{col}={p.get(col)}" for col in REQUIRED_COLS)
        print(f"- id={p['_id']} | {line}")
    print()


def search_patient(user):
    if not has_permission(user, "search_patients"):
        print("Access denied.\n")
        return

    print("=== Search patient ===")
    name = input("Enter patient name to search: ").strip()
    patient = patients.find_one({"Name": name})

    if not patient:
        print("No patient found with that name.\n")
        return

    print("Found patient:")
    print(f"  id={patient['_id']}")
    for col in REQUIRED_COLS:
        print(f"  {col}: {patient.get(col)}")
    print()


def create_patient(user):
    if not has_permission(user, "create_patients"):
        print("Access denied.\n")
        return

    print("=== Create patient ===")
    doc = {}

    for col in REQUIRED_COLS:
        value = input(f"{col}: ").strip()
        doc[col] = value

    result = patients.insert_one(doc)
    print(f"Patient created with _id={result.inserted_id}\n")


def update_patient(user):
    if not has_permission(user, "update_patients"):
        print("Access denied.\n")
        return

    print("=== Update patient ===")
    name = input("Enter patient name to search: ").strip()
    patient = patients.find_one({"Name": name})

    if not patient:
        print("No patient found with that name.\n")
        return

    print("Found patient:")
    print(f"  id={patient['_id']}")
    for col in REQUIRED_COLS:
        print(f"  {col}: {patient.get(col)}")

    print("\nAvailable fields to update:")
    print(", ".join(REQUIRED_COLS))

    field = input("Field to update (exact name): ").strip()
    if field not in REQUIRED_COLS:
        print("Invalid field name. Update aborted.\n")
        return

    new_value = input("New value: ").strip()

    patients.update_one(
        {"_id": patient["_id"]},
        {"$set": {field: new_value}}
    )
    print("Patient updated.\n")


def delete_patient(user):
    if not has_permission(user, "delete_patients"):
        print("Access denied.\n")
        return

    print("=== Delete patient ===")
    name = input("Enter patient name to delete: ").strip()
    result = patients.delete_one({"Name": name})
    if result.deleted_count:
        print("Patient deleted.\n")
    else:
        print("No patient found with that name.\n")

def main_menu(user):
    while True:
        print("=== Main menu ===")
        print("1 - List patients")
        print("2 - Update a patient")
        print("3 - Create a new patient (admin only)")
        print("4 - Delete a patient (admin only)")
        print("5 - Search a patient")
        print("0 - Exit")

        choice = input("Your choice: ").strip()

        if choice == "1":
            list_patients(user)
        elif choice == "2":
            update_patient(user)
        elif choice == "3":
            create_patient(user)
        elif choice == "4":
            delete_patient(user)
        elif choice == "5":
            search_patient(user)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Unknown choice.\n")

def main():
    user = login()
    main_menu(user)
    client.close()

if __name__ == "__main__":
    main()
