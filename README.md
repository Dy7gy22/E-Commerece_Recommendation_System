# E-Commerece_Recommendation_System

### Description
Ce projet est un système de recommandation de produits pour une plateforme de commerce électronique. L'objectif est de fournir des recommandations personnalisées à chaque utilisateur en fonction de ses préférences et de ses interactions.

### Fonctionnalités principales
- **Scraping de données** : Extraction des données à partir du site Amazon pour collecter des informations sur les produits.
- **Interface utilisateur** : Une application web développée avec Flask, HTML, CSS et JavaScript.
- **Stockage de données** : Utilisation de SQL pour stocker les données des utilisateurs et des produits.
- **Recommandations personnalisées** : Génération de recommandations basées sur les données collectées.

### Technologies utilisées
- **Backend** : Flask (Python)
- **Frontend** : HTML, CSS, JavaScript
- **Base de données** : SQL
- **Scraping** : Bibliothèques Python telles que BeautifulSoup et/ou Selenium

### Prérequis
- Python 3.x
- Flask
- SQLite/MySQL
- BeautifulSoup et/ou Selenium
- Un navigateur compatible avec les technologies modernes

### Installation
1. **Cloner le dépôt** :
   ```bash
   git clone <url_du_dépôt>
   cd <nom_du_projet>
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer la base de données** :
   - Créez une base de données SQL.
   - Importez les tables fournies dans le fichier `schema.sql`.

4. **Exécuter l'application** :
   ```bash
   flask run
   ```

5. **Accéder à l'application** :
   - Ouvrez votre navigateur et accédez à `http://127.0.0.1:5000`.

### Structure du projet
- **/static** : Contient les fichiers CSS, JS et images.
- **/templates** : Contient les fichiers HTML.
- **app.py** : Point d'entrée principal de l'application.
- **scraper.py** : Script pour scraper les données depuis Amazon.
- **database/** : Fichiers relatifs à la base de données.
- **requirements.txt** : Liste des dépendances Python.

### Fonctionnement du scraping
Le script `scraper.py` utilise BeautifulSoup et/ou Selenium pour extraire les données des pages produits d'Amazon. Les données collectées incluent :
- Nom du produit
- Prix
- Catégorie
- Note des utilisateurs

### Limites et améliorations possibles
- **Problèmes de scraping** : Amazon limite le scraping, ce qui peut nécessiter l'utilisation de proxies ou des techniques avancées.
- **Précision des recommandations** : Amélioration à l'aide de modèles de machine learning.
- **Interface utilisateur** : Ajout de fonctionnalités interactives pour une meilleure expérience utilisateur.

### Licence
Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

---

N'hésitez pas à contribuer à ce projet ou à signaler des problèmes !

