# P7_Modele_de_scoring.

Ce projet est dedié au développement d’un modèle de scoring selon la probabilité de défaut de paiement d'un client, et son implémentation sous forme d'API web. 

Il s'agit d'un modèle d'apprentissage supervisée pour la prédiction de la probabilité assoicée à la classification d'un client comme défaut, à partir des données variées sur les clients (ex. socio-démographiques, historique de demandes de prêt, etc), disponilbes sur [Kaggle](https://www.kaggle.com/c/home-credit-default-risk/data). 

L'API web, déployé sur la platforme Heroku, est acessible [ici](https://app-credit-dashboard.herokuapp.com/), permettant de visualiser les résultats du modèle et sont intrepretation à travers du dashboard interactif.

### Contenu:

- [P7_01_modelisation.ipynb](https://github.com/arbarbeiro/P7_Modele_de_scoring/blob/main/P7_01_modelisation.ipynb) comprend l'analyse, prétraitement et modélisation des données. 
- [app_dash.py](https://github.com/arbarbeiro/P7_Modele_de_scoring/blob/main/P7_app-credit-dashboard/app_dash.py) et [Dashboard_functions.py](https://github.com/arbarbeiro/P7_Modele_de_scoring/blob/main/P7_app-credit-dashboard/Dashboard_functions.py): contientent le code pour implementer le modèle sous forme d’API (backend) avec Dash et générant le dashboard (frontend), aussi en Dash.
- [P7_app-credit-dashboard](https://github.com/arbarbeiro/P7_Modele_de_scoring/tree/main/P7_app-credit-dashboard) contient tous les fichiers nécesaires au déploiement de l'API sur Heroku.


### Packages requis:
- `environment_P7.yml` permet de créer le même environnement utilisé avec `P7_01_modelisation.ipynb`. Exécutez la commande:
```
conda env create -f environment_P7.yml
```
- `P7_app_dash/requirements.txt` contient les requis pour l'API web et dashboard, ainsi que pour son déploiement sur Heroku. Exécutez la commande pour son installation:
```
pip install -r requirements.txt
```