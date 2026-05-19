import os
import ollama

# Active ou non le mode demo pour la vision.
# Si la variable vaut "1", on ne contacte pas le modele.
USE_DEMO_IMAGE = os.environ.get("USE_DEMO_IMAGE", "0") == "1"

def analyze_image(path: str) -> str:
    """
    Analyse une image et retourne une description textuelle.

    Parametre:
    - path: chemin absolu de l'image a analyser

    Retour:
    - une description reelle ou simulee selon le mode actif
    """
    if USE_DEMO_IMAGE:
        return (
            "Ceci est une description simulee (mode demo active). "
            "Aucune analyse reelle de l'image n'a ete effectuee."
        )
    try:

        # Sinon, appel reel au modele vision d'Ollama.
        # Le champ "images" recoit une liste de chemins locaux.
        resp = ollama.chat(
            model="llama3.2-vision:latest",
            messages=[{
                "role": "user",
                "content": "Decris cette image en detail.",
                "images": [path]
            }]
        )
    except Exception:
        return (
            "Je n'ai pas pu analyser l'image avec Ollama Vision. "
            "Verifie que le service Ollama tourne et que le modele "
            "'llama3.2-vision:latest' est installe."
        )

    # On recupere uniquement le texte de la reponse du modele.
    return resp["message"]["content"].strip()

