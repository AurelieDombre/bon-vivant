"""
Client minimal pour dialoguer avec Ollama.

Ce fichier isole l'appel au modele dans une classe dediee.
L'avantage est simple :
- la route FastAPI reste lisible
- si on change de fournisseur plus tard, on modifie surtout ce fichier
"""

import ollama


class LLMClient:
    """
    Encapsulation tres simple d'un appel a un modele local Ollama.
    """

    def complete(self, prompt: str):
        """
        Envoie un prompt texte au modele et retourne la reponse.

        Parametre:
        - prompt: texte deja prepare par le backend

        Retour:
        - le contenu textuel de la reponse du modele

        En cas d'erreur reseau ou si Ollama n'est pas lance,
        on retourne un message explicite plutot que de faire planter l'API.
        """
        try:
            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        except Exception:
            return (
                "Je n'ai pas pu joindre le modele local Ollama. "
                "Verifie que le service Ollama tourne et que le modele "
                "'llama3' est installe."
            )

        # La librairie Ollama renvoie une structure plus grande.
        # Ici on ne garde que le texte utile de la reponse.
        return response["message"]["content"]
