"""
Fonctions metier du chatbot.

Ce fichier contient la logique "locale", c'est-a-dire la partie qui ne depend
pas directement d'un LLM. C'est ici qu'on :

- charge les produits depuis le JSON
- detecte quel produit est mentionne par l'utilisateur
- genere une suggestion de vin
- peut analyser le sentiment d'un texte

L'idee importante :
la route HTTP appelle ces fonctions, mais la logique metier reste separee.
"""

# Permet de lire les variables d'environnement et de manipuler les chemins.
import os

# Permet de convertir le fichier products.json en objets Python.
import json

# Importe les outils de machine learning utilises pour l'analyse de sentiment.
import torch
from transformers import pipeline

from core.prompt_manager import load_prompt
from llama_cpp import Llama


# Active un mode de demonstration pour la logique produit.
# Si USE_DEMO_TEXT=1 dans l'environnement, on renverra une reponse fictive.
USE_DEMO_TEXT = os.environ.get("USE_DEMO_TEXT", "0") == "1"

# Meme idee pour la partie analyse de sentiment.
USE_DEMO_SENTIMENT = os.environ.get(
    "USE_DEMO_SENTIMENT",
    "0"
) == "1"

# Au lancement du programme, le pipeline de sentiment n'est pas encore charge.
# On le chargera seulement au premier besoin.
_sentiment_pipeline = None


PROMPT_UPSELL = 'upsell_prompt_v1.0.txt'
MODEL_PATH = os.path.join(
os.path.dirname(__file__),
'..',
'models',
'mistral-7b-q4_k_m.gguf')
llm = Llama(model_path=MODEL_PATH, n_gpu_layers=16, n_threads=4)


# Construction du chemin du fichier JSON de produits.
# __file__ correspond au chemin de ce fichier Python.
# On remonte ensuite vers ../data/products.json
DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "../data/products.json"
)

def load_products():
    """
    Charge le fichier products.json et retourne la liste des produits.

    Retour:
    - une liste de dictionnaires Python

    Exemple de produit:
    {
        "name": "Brie",
        "category": "Fromage",
        "description": "Fromage cremeux au lait de vache."
    }
    """
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Les donnees sont chargees une seule fois au demarrage.
# Cela evite de rouvrir le fichier JSON a chaque requete.
PRODUCTS_DATA = load_products()

def find_product_by_name(query: str):
    """
    Cherche si un produit connu apparait dans le message utilisateur.

    Parametre:
    - query: texte brut saisi par l'utilisateur

    Retour:
    - le dictionnaire du produit trouve
    - ou None si aucun produit connu n'est present dans le texte
    """
    # On normalise en minuscules pour comparer sans se soucier de la casse.
    query = query.lower()

    for product in PRODUCTS_DATA:
        if product["name"].lower() in query:
            return product

    return None


def suggest_wine_for_product(product):
    """
    Retourne une suggestion de vin a partir de la categorie du produit.

    Parametre:
    - product: dictionnaire representant un produit

    Retour:
    - une phrase prete a etre affichee a l'utilisateur
    """
    # Table de correspondance tres simple entre categorie et recommandation.
    pairing = {
        "Fromage": "Un vin blanc sec, type Sancerre ou Chablis.",
        "Poisson": "Un vin blanc fruite, type Sauvignon ou Chardonnay.",
        "Charcuterie": "Un vin rouge leger, type Pinot Noir.",
        "Dessert": "Un vin moelleux, type Sauternes."
    }

    # Si la categorie n'existe pas dans le dictionnaire, on utilise le message
    # par defaut fourni en second argument de .get().
    suggestion = pairing.get(
        product["category"],
        "Un vin adapte a ce plat, a voir selon vos gouts !"
    )

    return (
        f"Pour {product['name']}, "
        f"je te recommande : {suggestion}"
    )


def get_product_info(user_message: str):
    """
    Analyse le message utilisateur et choisit une reponse metier.

    Cette fonction sert de point d'entree "intelligent" pour la logique locale.

    Cas possibles:
    - mode demo active -> reponse fictive
    - aucun produit connu detecte -> None
    - demande de description -> description du produit
    - sinon -> suggestion de vin
    """
    if USE_DEMO_TEXT:
        return (
            "MODE DEMO : "
            "Produit detecte + suggestion fictive."
        )

    product = find_product_by_name(user_message)

    # Si aucun produit n'est trouve, on laisse l'appelant decider de la suite.
    # Dans notre cas, l'API bascule ensuite vers le LLM.
    if not product:
        return None

    message_lower = user_message.lower()

    # Si le message ressemble a une demande d'explication du produit,
    # on renvoie sa description plutot qu'un accord vin.
    if any(x in message_lower for x in [
        "que contient",
        "description",
        "qu'y a-t-il dans",
        "c'est quoi",
        "qu'est-ce que"
    ]):
        return (
            f"{product['name']} : "
            f"{product['description']}"
        )

    return suggest_wine_for_product(product)


def get_sentiment_pipeline():
    """
    Charge le pipeline HuggingFace d'analyse de sentiment si besoin.

    Pourquoi faire comme ca:
    - le modele peut etre lourd a charger
    - on evite de le recharger a chaque appel

    Retour:
    - le pipeline pret a etre utilise
    """
    global _sentiment_pipeline

    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline("sentiment-analysis")

    return _sentiment_pipeline


def analyze_sentiment(text):
    """
    Analyse le sentiment d'un texte.

    Parametre:
    - text: texte a analyser

    Retour:
    - un tuple (label, score)
      exemple: ("positive", 0.998)
    """
    if USE_DEMO_SENTIMENT:
        return "neutral", 0.5

    pipe = get_sentiment_pipeline()

    # Le pipeline renvoie une liste de resultats.
    # Ici on prend le premier, car on analyse une seule phrase a la fois.
    result = pipe(text)[0]

    label = result["label"].lower()
    score = result["score"]

    return label, score
#-----Fonction upsell ----#
def get_upsell(cart_items: list[str]) -> dict:
    prompt_template = load_prompt(PROMPT_UPSELL)
    prompt = prompt_template.replace("{cart_items}", ", ".join(cart_items))
    result = llm(prompt, max_tokens=50)
    return {"suggestion": result["choices"][0]["text"].strip()}
