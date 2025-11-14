# 🩺 Projet : Migration CSV & Authentification (MongoDB + Python + Docker)

Ce projet permet :

1. **D’importer automatiquement un fichier CSV dans MongoDB** via `migration.py`.  
2. **D’accéder et de modifier les données** avec un système d’authentification simple (`auth_app.py`).  
3. **De créer des utilisateurs** (admin ou doctor) via `create_user.py`.  

---

## 🚀 Fonctionnement général

### 🔄 Migration des données

Le script `migration.py` :

- lit le fichier CSV,  
- vérifie l’intégrité des données,  
- insère les documents dans MongoDB (collection `mycollection`).  

La migration s’exécute automatiquement via Docker Compose (service `loader`).

---

## 🔐 Authentification & rôles utilisateurs

Le script `auth_app.py` propose un **menu interactif** après connexion.

Les utilisateurs sont stockés dans MongoDB sous la collection `users`, avec :

- un **nom d’utilisateur**,  
- un **mot de passe hashé** (bcrypt),  
- un **rôle** attribué.  

### Rôles disponibles

#### 🟦 Admin
- Lire les patients  
- Mettre à jour des patients  
- Créer des patients  
- Supprimer des patients  

#### 🟩 Doctor
- Lire les patients  
- Mettre à jour des patients  
- ❌ Ne peut pas créer  
- ❌ Ne peut pas supprimer  

---

## 🗄️ Schéma de la base de données

La base de données MongoDB utilisée s’appelle **`mydb`** et contient deux collections principales : `mycollection` (patients) et `users` (authentification).

```text
mydb
├─ mycollection   (données patients)
└─ users          (utilisateurs et rôles)
```

### 📂 Collection `mycollection` (patients)

Chaque document de la collection `mycollection` représente un patient, par exemple :

```json
{
  "_id": ObjectId("..."),
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

Principaux champs :

| Champ                | Type       | Description                          |
|----------------------|-----------|--------------------------------------|
| `_id`                | ObjectId  | Identifiant unique MongoDB          |
| `Name`               | String    | Nom du patient                      |
| `Age`                | Number    | Âge du patient                      |
| `Gender`             | String    | Sexe du patient                     |
| `Blood Type`         | String    | Groupe sanguin                      |
| `Medical Condition`  | String    | Pathologie principale               |
| `Date of Admission`  | String    | Date d’admission                    |
| `Doctor`             | String    | Médecin en charge                   |
| `Hospital`           | String    | Nom de l’hôpital                    |
| `Insurance Provider` | String    | Assurance du patient                |
| `Billing Amount`     | Number    | Montant facturé                     |
| `Room Number`        | Number    | Numéro de chambre                   |
| `Admission Type`     | String    | Type d’admission (Urgent, etc.)     |
| `Discharge Date`     | String    | Date de sortie                      |
| `Medication`         | String    | Médication principale               |
| `Test Results`       | String    | Résultats des examens               |

### 👤 Collection `users` (authentification)

Chaque document de la collection `users` représente un compte utilisateur :

```json
{
  "_id": ObjectId("..."),
  "username": "admin123",
  "password_hash": "<hash bcrypt>",
  "role": "admin"
}
```

Champs :

| Champ           | Type      | Description                                      |
|-----------------|-----------|--------------------------------------------------|
| `_id`           | ObjectId  | Identifiant unique MongoDB                      |
| `username`      | String    | Identifiant de connexion                        |
| `password_hash` | Binary / String | Mot de passe hashé avec bcrypt         |
| `role`          | String    | Rôle de l’utilisateur (`admin` ou `doctor`)     |

---

## 🐳 Déploiement avec Docker

### 1️⃣ Lancer MongoDB et la migration CSV
```bash
docker compose up --build mongo loader
```

### 2️⃣ Créer un utilisateur (admin ou doctor)
```bash
docker compose run --rm auth_app python create_user.py
```

### 3️⃣ Lancer l’application d’authentification
```bash
docker compose run --rm auth_app
```

---

## 📁 Structure du projet

```text
project/
│── migration.py
│── auth_app.py
│── create_user.py
│── integrity.py
│── docker-compose.yml
│── Dockerfile
└── data/healthcare_dataset.csv
```
