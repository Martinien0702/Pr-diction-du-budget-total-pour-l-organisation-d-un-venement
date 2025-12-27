README.md
Projet IA – Prédiction du budget total pour l'organisation d'un évenement


1. Description

    Cette application fournit une API FastAPI pour prédire le budget total d’un événement en fonction de plusieurs paramètres (type d’événement, capacité du lieu, budget marketing, coûts, etc.).
    L’API peut être exécutée localement mais est  déployée sur Google Cloud Run également ( accessible https://api-model-prediction-budget-871459561848.us-central1.run.app/predict)

    Dans le formulaire, c'est seulement quelque caractéristiques qui seront saisies ( les plus importants suivant MUTUAL INFO)


2. Structure du projet


        ├─ app/projet IA #Jupiter notebook 
        projet_ia/
        ├─ app/
        │  ├─ main.py           # Point d’entrée de l’API FastAPI
        │  ├─ model_loader.py   # Chargement du modèle ML
        │  ├─ preprocessing.py  # Pré-traitement des données
        │  ├─ logger.py         # Logging des prédictions et erreurs
        │  └─ templates/
        │      └─ form.html     # Formulaire HTML pour les tests
        ├─ models/
        │  └─ model.pkl      # Modèle ML entraîné
        ├─ tests/
        │  └─ test_api.py       # Tests unitaires (optionnel)
        ├─ Dockerfile           # Instructions pour containeriser l’API
        ├─ requirements.txt     # Dépendances Python
        ├─ .env                 # Variables d’environnement 
        └─ README.md            # Ce fichier


3. Exécution locale de l’API

    3.1 Prérequis

        Python 3.10+

        pip installé

    3.2 Installer les dépendances

        pip install -r requirements.txt (commande dans terminal)

    3.3 Lancer le serveur FastAPI
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 (commande dans terminal)

    3.4 Tester

        Accéder au formulaire HTML : http://localhost:8000

        Documentation Swagger : http://localhost:8000/docs


4. Dockerisation

    4.1 Construire l’image Docker

    docker build -t api-model-prediction-budget (commande dans terminal)

    4.2 Exécuter le container Docker localement

    docker run -p 8000:8080 api-model-prediction-budget (commande dans terminal)


    NB : L’API écoute sur le port 8080 à l’intérieur du container (Cloud Run standard).


5. Rôle des fichiers principaux

    Dockerfile : décrit comment construire l’image Docker (base Python, installation dépendances, copie du projet, lancement d’Uvicorn)

    requirements.txt : liste des packages Python nécessaires pour exécuter l’API

    main.py : point d’entrée FastAPI

    model_loader.py / preprocessing.py : chargement du modèle et traitement des entrées

    templates/form.html : interface utilisateur pour tester les prédictions

6. Déploiement sur Google Cloud Run

    6.1 Créer un compte et un projet Google Cloud

        Crée un compte Google Cloud : https://console.cloud.google.com/

        Crée un nouveau projet depuis la console :

        Clique sur “Sélectionner un projet” → Nouveau projet

        Donne un nom (ex : projet-ia-prediction-budget)

        Note l’ID du projet (ex : projet-ia-prediction-budget)

    6.2 Installer et configurer Google Cloud SDK

        Télécharge et installe le SDK : https://cloud.google.com/sdk/docs/install

        Authentification  dans le terminal :

        gcloud auth login

        Sélection du projet actif :

        gcloud config set project <ID_DU_PROJET>

    6.3 Construire l’image et l’envoyer sur Google Container Registry (GCR)

        gcloud builds submit --tag gcr.io/projet-ia-prediction-budget/api-model-prediction-budget (commande dans terminal)

    6.4 Déployer sur Cloud Run
    
    gcloud run deploy api-model-prediction-budget \
    --image gcr.io/projet-ia-prediction-budget/api-model-prediction-budget \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated              (commande dans terminal)


    --platform managed : Cloud Run géré par Google

    --region : région la plus proche

    --allow-unauthenticated : rend l’API accessible publiquement

    6.5 Accéder à l’API en ligne

    Une URL sera générée par Cloud Run, par exemple :

    https://api-model-prediction-budget-xxxxx-uc.a.run.app 

    Formulaire HTML et Swagger disponibles via cette URL

     test de  /predict avec un POST ou via le formulaire

     Notre API est disponible sur https://api-model-prediction-budget-871459561848.us-central1.run.app/predict

7.  Erreurs rencontrées / Ajustements

Problème de port Cloud Run : initialement, Uvicorn utilisait le port 8000.
Solution : modification du Dockerfile pour écouter le port 8080 (--port 8080)

Conflits de dépendances : suppression de pywin32 et ajustement de protobuf pour compatibilité Linux et Cloud Run

Exécution gcloud : ajout du SDK et configuration PATH sous Windows

