Description
Ce projet est une application en Python avec une interface graphique (Tkinter) qui permet :

D'enregistrer et d'authentifier des utilisateurs.
D'afficher les données météorologiques pour une ville donnée en utilisant l'API OpenWeatherMap.
L'application permet à l'utilisateur de choisir entre s'inscrire ou se connecter. Après une connexion réussie, l'utilisateur peut saisir le nom d'une ville pour récupérer les données météorologiques actuelles.

Fonctionnalités
Authentification des utilisateurs : Les utilisateurs peuvent s'inscrire et se connecter.
Recherche de météo : Les utilisateurs connectés peuvent rechercher des informations météorologiques en fonction de la ville saisie.
Stockage des données météo : Les données météorologiques sont enregistrées dans une base de données MySQL.
Prérequis
Avant de lancer l'application, assurez-vous d'avoir les prérequis suivants installés :

Python 3.x
Tkinter : Inclus avec Python pour les systèmes Windows. Pour Linux, vous pouvez l'installer avec la commande suivante :

sudo apt-get install python3-tk


MySQL Server : Utilisé pour stocker les utilisateurs et les données météorologiques.
mysql-connector-python : Pour interagir avec la base de données MySQL.

pip install mysql-connector-python






Installation et Configuration
1. Cloner le dépôt
Clonez ce projet depuis GitHub :

git clone <URL_DU_DEPOT>
cd <nom_du_repertoire_du_projet>


2. Créer la base de données
Avant de lancer l'application, vous devez créer la base de données et les tables nécessaires dans MySQL.

Connectez-vous à MySQL et exécutez les commandes suivantes :

CREATE DATABASE api;

USE api;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE weatherdata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    weather_main VARCHAR(100),
    weather_description VARCHAR(255),
    temperature FLOAT,
    humidity INT,
    wind_speed FLOAT,
    timestamp DATETIME
);

3. Ajouter votre clé API OpenWeatherMap
Vous devez avoir une clé API pour récupérer les données météorologiques. Si vous n'en avez pas encore, inscrivez-vous sur OpenWeatherMap.

Remplacez la clé API dans le fichier WeatherApp par votre propre clé :

API_key = "VOTRE_CLE_API"


4. Lancer l'application
Après avoir configuré la base de données et ajouté la clé API, vous pouvez lancer l'application :

python <nom_du_fichier_principal>.py


5. Utilisation
Connexion : Si vous êtes déjà inscrit, connectez-vous avec votre nom d'utilisateur et votre mot de passe.
Inscription : Si vous êtes un nouvel utilisateur, cliquez sur "S'inscrire" et créez un compte.
Recherche de météo : Après la connexion, saisissez le nom d'une ville pour récupérer et afficher les informations météorologiques.
Exemple de flux utilisateur
Lancez l'application.
Choisissez de vous connecter ou de vous inscrire.
Après l'inscription, vous êtes redirigé vers l'écran de connexion.
Une fois connecté, accédez à l'application météo.
Saisissez une ville pour obtenir les données météo.
Technologies Utilisées
Python : Langage de programmation principal.
Tkinter : Pour l'interface graphique.
MySQL : Base de données pour stocker les utilisateurs et les données météo.
OpenWeatherMap API : Pour obtenir les données météorologiques en temps réel.
Améliorations possibles
Ajouter un hachage pour les mots de passe des utilisateurs.
Ajouter plus de fonctionnalités météorologiques (prévisions, historique).
Améliorer l'interface utilisateur pour la rendre plus intuitive et attrayante.
Auteur
Nom : JAMMAA Mohamed Ali
Email : mohamedali.jammaa2@gmail.com
GitHub : CHAMA9A