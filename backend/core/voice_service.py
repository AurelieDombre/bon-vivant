"""
Services locaux pour la voix.

Ce module gere deux choses :
- la transcription d'un fichier audio vers du texte avec Vosk
- la synthese d'un texte vers un fichier audio avec pyttsx3

Point important :
- la transcription actuelle est prevue pour des fichiers WAV lisibles
  par le module standard `wave`
- un fichier .ogg ne peut donc pas etre traite directement ici
  sans etape de conversion ou bibliotheque supplementaire
"""

import json
import os
import wave

import pyttsx3
from vosk import KaldiRecognizer, Model


# Active le mode demo pour la partie voix.
USE_DEMO_VOICE = os.environ.get("USE_DEMO_VOICE", "0") == "1"

# Chemin local du modele Vosk.
# On calcule un chemin absolu et normalise.
# Le "/" en tete aurait force un faux chemin absolu sur Windows,
# ce qui expliquait ton crash au demarrage.
MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "vosk-model-small-en-us-0.15",
    )
)

# Chargement paresseux du modele.
# On le charge au premier besoin plutot qu'a l'import du module.
_model = None

# Initialisation du moteur de synthese vocale.
engine = pyttsx3.init()


def transcribe_audio(wav_path: str) -> str:
    """
    Transcrit un fichier audio WAV en texte.

    Parametre:
    - wav_path: chemin local d'un fichier .wav

    Retour:
    - la transcription complete detectee par Vosk
    """
    global _model

    # Si le modele n'est pas encore charge, on l'initialise ici.
    # Cela permet d'avoir un message d'erreur plus lisible si le dossier
    # du modele est absent.
    if _model is None:
        if not os.path.isdir(MODEL_PATH):
            raise FileNotFoundError(
                "Modele Vosk introuvable. "
                f"Chemin attendu : {MODEL_PATH}"
            )
        _model = Model(MODEL_PATH)

    # `wave` ne sait lire que des WAV valides.
    # Si le fichier est un .ogg, cette ouverture echouera.
    with wave.open(wav_path, "rb") as wf:
        rec = KaldiRecognizer(_model, wf.getframerate())
        text = ""

        # On lit l'audio par blocs pour alimenter Vosk progressivement.
        while True:
            data = wf.readframes(4000)
            if not data:
                break

            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text += " " + res.get("text", "")

        res = json.loads(rec.FinalResult())
        return (text + " " + res.get("text", "")).strip()


def speak_text(text: str, out_path: str) -> None:
    """
    Genere un fichier audio a partir d'un texte.

    Parametres:
    - text: texte a prononcer
    - out_path: chemin du fichier audio de sortie
    """
    engine.save_to_file(text, out_path)
    engine.runAndWait()
