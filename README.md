# 🩺 Projet : Migration CSV & Authentification (MongoDB + Python + Docker)

Ce projet permet :

1. **D’importer automatiquement un fichier CSV dans MongoDB** via `migration.py`.  
2. **D’accéder et de modifier les données patients** via une application Python (`auth_app.py`).  
3. **De gérer des utilisateurs applicatifs** (admin / doctor) stockés dans MongoDB (`create_user.py`).  
4. **D’utiliser deux types d'utilisateurs MongoDB** pour sécuriser l’architecture.

---

# 🔐 Architecture des utilisateurs

Le projet utilise **deux niveaux d’utilisateurs**, chacun ayant un rôle différent :

---

## 1️⃣ **Utilisateurs MongoDB (techniques – niveau base de données)**

Créés automatiquement au lancement grâce à `mongo-init.js`.

| Utilisateur MongoDB | Rôle | Utilisation |
|---------------------|------|-------------|
| **root** | Accès total au serveur MongoDB | Administrateur système |
| **db_admin** | `dbOwner` sur `mydb` | Exécute la migration CSV |
| **app_user** | `readWrite` sur `mydb` | Utilisé par l’application (`auth_app.py`) |

➡️ Ces utilisateurs *n’apparaissent pas* dans vos collections MongoDB.  
➡️ Ils servent uniquement à autoriser vos scripts Python à se connecter.

---

## 2️⃣ **Utilisateurs de l’application (stockés dans MongoDB)**

Stockés dans `mydb.users`, créés via `create_user.py`.

| Rôle applicatif | Actions autorisées |
|------------------|--------------------|
| **admin** | Lire, créer, modifier, supprimer des patients |
| **doctor** | Lire et modifier des patients uniquement |

➡️ Ces utilisateurs se connectent à **l’application Python**, pas à MongoDB directement.

---

# 🔄 Migration des données (loader)

Le service Docker **loader** exécute automatiquement :

- `migration.py`
- en utilisant le compte MongoDB **db_admin**
- pour écrire dans `mydb.mycollection`

Le script :

- lit le fichier CSV dans `/data`
- nettoie et transforme les données
- vérifie l’intégrité (`integrity.py`)
- insère les documents dans MongoDB

---

# 🗄️ Structure de la base de données

Base : **`mydb`**

```
mydb
├─ mycollection   → données patients
└─ users          → comptes applicatifs (admin/doctor)
```

---

## 📂 Collection `mycollection` (patients)

Chaque document contient les champs du CSV (nom, âge, médecin, assurance, etc.). Exemple :

```json
{
  "_id": "ObjectId(...)",
  "Name": "Bobby Jackson",
  "Age": 30,
  "Gender": "Male",
  "Blood Type": "B-",
  "Medical Condition": "Cancer",
  "Date of Admission": "2024-01-31",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.28,
  "Room Number": 328,
  "Admission Type": "Urgent",
  "Discharge Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
```

---

## 👤 Collection `users` (utilisateurs applicatifs)

Exemple :

```json
{
  "_id": "ObjectId(...)",
  "username": "admin123",
  "password_hash": "<hash bcrypt>",
  "role": "admin"
}
```

---

# 🧑‍💻 Application d’authentification (`auth_app.py`)

Après connexion, l’application propose un menu permettant :

| Action | admin | doctor |
|--------|--------|---------|
| Lire les patients | ✔ | ✔ |
| Modifier un patient | ✔ | ✔ |
| Créer un patient | ✔ | ❌ |
| Supprimer un patient | ✔ | ❌ |
| Rechercher un patient | ✔ | ✔ |

L'application utilise **l’utilisateur MongoDB `app_user`**, avec un accès limité au strict nécessaire.

---

# 🐳 Déploiement avec Docker

## 1️⃣ Démarrer MongoDB + migration CSV

```bash
docker compose up --build mongo loader
```

MongoDB démarre → `mongo-init.js` crée les comptes →  
Le loader importe le CSV automatiquement.

---

## 2️⃣ Créer un utilisateur applicatif (admin OU doctor)

```bash
docker compose run --rm auth_app python create_user.py
```

---

## 3️⃣ Lancer l’application d’authentification

```bash
docker compose run --rm auth_app
```

---

# 📁 Structure du projet

```
project/
│── migration.py
│── auth_app.py
│── create_user.py
│── integrity.py
│── mongo-init.js
│── docker-compose.yml
│── Dockerfile
└── data/
    └── healthcare_dataset.csv
```
