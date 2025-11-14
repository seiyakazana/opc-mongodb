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
```
project/
│── migration.py
│── auth_app.py
│── create_user.py
│── integrity.py
│── docker-compose.yml
│── Dockerfile
└── data/healthcare_dataset.csv
```
