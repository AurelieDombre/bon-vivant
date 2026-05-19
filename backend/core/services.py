# ==============================
# IMPORTS
# ==============================

# Permet de travailler avec :
# - les fichiers
# - les chemins
# - les variables d'environnement
import os

# Permet de lire les fichiers JSON
import json

# Bibliothèque d'expressions régulières
# (pas utilisée ici, mais importée)
import re
# framework de deep learning utilisé par HuggingFace Transformers
import torch
# HuggingFace Transformers
# pipeline() permet d'utiliser facilement une IA pré-entraînée
from transformers import pipeline



# ==============================
# VARIABLES D'ENVIRONNEMENT
# ==============================

# Lit une variable système nommée USE_DEMO_TEXT
#
# Si la variable vaut "1" :
# -> USE_DEMO_TEXT = True
#
# Sinon :
# -> False
#
# Exemple terminal :
# export USE_DEMO_TEXT=1
USE_DEMO_TEXT = os.environ.get("USE_DEMO_TEXT", "0") == "1"


# Même principe pour le mode démo sentiment
USE_DEMO_SENTIMENT = os.environ.get(
    "USE_DEMO_SENTIMENT",
    "0"
) == "1"


# ==============================
# LAZY LOADING DU MODÈLE IA
# ==============================

# Au démarrage :
# le pipeline IA n'est PAS chargé
#
# None = "vide"
#
# Le modèle sera chargé uniquement
# quand on en aura besoin
_sentiment_pipeline = None


# ==============================
# CHEMIN DU FICHIER JSON
# ==============================

# __file__
# = chemin du fichier Python actuel
#
# os.path.dirname(__file__)
# = dossier du fichier actuel
#
# "../data/products.json"
# = remonte d'un dossier puis va dans data/
#
# os.path.join(...)
# construit un chemin propre selon l'OS
DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "../data/products.json"
)


# ==============================
# CHARGEMENT DES PRODUITS
# ==============================

def load_products():
    """
    Ouvre le fichier JSON
    et retourne les données Python.
    """

    # with open(...)
    # ouvre le fichier en lecture
    #
    # "r" = read
    # utf-8 = gestion des accents
    with open(DATASET_PATH, "r", encoding="utf-8") as f:

        # json.load(f)
        # transforme le JSON
        # en objets Python
        return json.load(f)


# Chargement immédiat des données
#
# Le fichier JSON est lu UNE seule fois
# au démarrage du programme
PRODUCTS_DATA = load_products()


# ==============================
# RECHERCHE D'UN PRODUIT
# ==============================

def find_product_by_name(query: str):
    """
    Cherche un produit dans le message utilisateur.
    """

    # Passage en minuscules
    # pour éviter les problèmes de casse
    #
    # Exemple :
    # "BRIE" -> "brie"
    query = query.lower()

    # Boucle sur tous les produits
    for product in PRODUCTS_DATA:

        # Vérifie si le nom du produit
        # est contenu dans le message
        #
        # Exemple :
        # product["name"] = "Brie"
        #
        # query = "je veux du brie"
        #
        # => True
        if product["name"].lower() in query:

            # On retourne le produit trouvé
            return product

    # Aucun produit trouvé
    return None


# ==============================
# SUGGESTION DE VIN
# ==============================

def suggest_wine_for_product(product):
    """
    Associe un type de produit
    à un conseil de vin.
    """

    # Dictionnaire Python
    #
    # clé -> valeur
    pairing = {

        "Fromage":
            "Un vin blanc sec, type Sancerre ou Chablis.",

        "Poisson":
            "Un vin blanc fruité, type Sauvignon ou Chardonnay.",

        "Charcuterie":
            "Un vin rouge léger, type Pinot Noir.",

        "Dessert":
            "Un vin moelleux, type Sauternes."
    }

    # .get()
    #
    # Cherche la catégorie
    #
    # Si elle n'existe pas :
    # retourne le texte par défaut
    suggestion = pairing.get(
        product["category"],
        "Un vin adapté à ce plat, à voir selon vos goûts !"
    )

    # f-string
    #
    # Permet d'injecter des variables
    # dans du texte
    return (
        f"Pour {product['name']}, "
        f"je te recommande : {suggestion}"
    )


# ==============================
# FONCTION PRINCIPALE
# ==============================

def get_product_info(user_message: str):
    """
    Analyse le message utilisateur
    et retourne une réponse adaptée.
    """

    # MODE DEMO
    #
    # Permet de simuler une réponse
    # sans exécuter la vraie logique
    if USE_DEMO_TEXT:

        return (
            "MODE DEMO : "
            "Produit détecté + suggestion fictive."
        )

    # Recherche du produit
    product = find_product_by_name(user_message)

    # Aucun produit trouvé
    if not product:
        return None

    # Message en minuscules
    message_lower = user_message.lower()

    # any(...)
    #
    # Retourne True
    # si AU MOINS une condition est vraie
    #
    # Ici :
    # on cherche si le message
    # demande une description du produit
    if any(x in message_lower for x in [

        "que contient",
        "description",
        "qu'y a-t-il dans",
        "c'est quoi",
        "qu'est-ce que"

    ]):

        # Retourne la description du produit
        return (
            f"{product['name']} : "
            f"{product['description']}"
        )

    # Sinon :
    # retourne un conseil de vin
    return suggest_wine_for_product(product)


# ==============================
# ANALYSE DE SENTIMENT
# ==============================

def get_sentiment_pipeline():
    """
    Charge le modèle HuggingFace
    UNE seule fois.

    Singleton + Lazy Loading
    Evite de recharger après chaque requête
    """

    # On utilise la variable globale
    global _sentiment_pipeline

    # Si le modèle n'est pas chargé
    if _sentiment_pipeline is None:

        # Chargement du modèle IA
        #
        # sentiment-analysis
        # = modèle de classification
        #
        # Il détecte :
        # - positif
        # - négatif
        # - neutre
        _sentiment_pipeline = pipeline(
            "sentiment-analysis"
        )

    # Retourne le pipeline
    return _sentiment_pipeline


# ==============================
# ANALYSE D'UN TEXTE
# ==============================

def analyze_sentiment(text):
    """
    Analyse le sentiment d'un texte.
    """

    # MODE DEMO
    if USE_DEMO_SENTIMENT:

        # Retourne un résultat fictif
        return "neutral", 0.5

    # Récupération du pipeline IA
    pipe = get_sentiment_pipeline()

    # Analyse du texte
    #
    # pipe(text)
    # retourne une liste
    #
    # Exemple :
    # [
    #   {
    #       "label": "POSITIVE",
    #       "score": 0.998
    #   }
    # ]
    #
    # [0]
    # récupère le premier résultat
    result = pipe(text)[0]

    # Extraction du label
    #
    # .lower()
    # transforme :
    #
    # "POSITIVE"
    # ->
    # "positive"
    label = result["label"].lower()

    # Score de confiance du modèle
    score = result["score"]

    # Retour final
    return label, score