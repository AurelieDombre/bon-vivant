# Synthèse pédagogique du cours : “Les analyses techniques”

Ce cours explique **comment concevoir un projet IA moderne**, centré sur un **chatbot multimodal** (texte + image + voix), tout en gardant :

* un **budget limité**,
* une architecture propre,
* et un projet évolutif dans le temps.

L’idée générale est simple :

> On construit d’abord une **V1 simple mais fonctionnelle (POC)**, puis on améliore progressivement le système.

---

# 1. L’idée centrale du cours

Le projet “Bon Vivant” veut créer un chatbot intelligent pour un site e-commerce.

Le chatbot doit pouvoir :

* répondre par texte,
* analyser les émotions,
* comprendre des images,
* comprendre la voix,
* proposer des recommandations produits.

Le cours montre surtout :

1. **comment organiser techniquement un projet IA**,
2. **quels outils utiliser**,
3. **pourquoi ces choix sont pertinents**.

---

# 2. Le concept le plus important : le POC

Le mot-clé du cours est :

## POC = Proof Of Concept

Un POC est :

* une **première version rapide**,
* qui sert à vérifier :

  * si l’idée fonctionne,
  * si les utilisateurs sont intéressés,
  * si c’est techniquement faisable.

Le but n’est PAS de créer un produit parfait.

👉 Le cours insiste beaucoup là-dessus :

> “faire simple, rapide, peu coûteux”.

---

# 3. La philosophie technique du projet

Le cours suit une logique très professionnelle :

## a) Utiliser des modèles IA locaux

Au lieu d’utiliser OpenAI/API cloud coûteuse :

on utilise :

* Meta → modèle Llama
* Mistral AI → Mistral 7B

Pourquoi ?

### Avantages :

* gratuit,
* open source,
* fonctionne sans Internet,
* pas de coût API,
* parfait pour une startup.

### Inconvénient :

* parfois moins puissant,
* plus lent en local.

👉 Mais pour une V1, c’est largement suffisant.

---

# 4. Le chatbot multimodal

“Multimodal” = plusieurs types d’entrée.

Le chatbot comprend :

| Mode  | Exemple                      |
| ----- | ---------------------------- |
| Texte | “Quel vin avec du fromage ?” |
| Image | photo d’un fromage           |
| Voix  | message vocal                |

---

# 5. Le fonctionnement du chatbot texte

Le fonctionnement est très important à comprendre.

## Étape 1 : l’utilisateur pose une question

Exemple :

> “Quel vin va avec du chèvre ?”

## Étape 2 : le backend vérifie une base de données

Le projet utilise un fichier :

```json
products.json
```

Si le produit existe :
→ le backend répond directement.

Sinon :
→ le LLM (Llama) génère une réponse.

---

# 6. Le cycle de vie d’un projet IA

Le cours donne une structure essentielle :

## Les 5 étapes d’un projet IA

### 1. Collecte de données

On récupère les données utiles.

Exemple :

* produits,
* descriptions,
* images.

---

### 2. Entraînement

Normalement on entraîne un modèle.

Mais ici :

* PAS de fine-tuning,
* on utilise un modèle déjà entraîné.

👉 gain de temps énorme.

---

### 3. Inférence

C’est le moment où l’IA répond réellement.

Exemple :

* l’utilisateur pose une question,
* le modèle génère une réponse.

---

### 4. Validation

On teste :

* les cas normaux,
* les erreurs,
* les cas non prévus.

---

### 5. Ré-entraînement / amélioration

On améliore progressivement le système.

---

# 7. Analyse de sentiment

Très important dans le cours.

Le chatbot doit détecter :

* positif,
* neutre,
* négatif.

Exemple :

* “Je suis satisfait” → positif
* “Je suis déçu” → négatif

---

## Comment ça fonctionne ?

Le cours montre une progression intelligente :

### V1 simple

Détection par mots-clés.

Exemple :

* “déçu”
* “nul”
* “problème”

---

### V2 plus intelligente

Utilisation de :

* PyTorch
* Hugging Face

Le pipeline classe automatiquement :

* positif,
* neutre,
* négatif.

avec un score de confiance.

---

## Pourquoi c’est utile ?

Le chatbot adapte son comportement :

* ton empathique,
* aide humaine,
* support client.

👉 Très important en e-commerce.

---

# 8. Fonction image

Le chatbot peut analyser une photo.

Exemple :

* photo d’un plateau de fromage.

L’IA :

* décrit l’image,
* reconnaît certains éléments.

---

## Outil utilisé

Le cours utilise :

* Ollama
* modèle Llama Vision.

Pourquoi ?

* léger,
* local,
* gratuit.

---

## Idée essentielle à retenir

Le backend :

1. reçoit l’image,
2. la stocke temporairement,
3. l’analyse,
4. renvoie une description.

---

# 9. Fonction voix (Speech-to-Text)

Le chatbot comprend la voix.

Le processus :

## Étapes

1. utilisateur envoie un fichier audio,
2. backend reçoit l’audio,
3. conversion voix → texte,
4. chatbot traite le texte.

---

## Outil utilisé

Vosk

Pourquoi ?

* open source,
* rapide,
* hors ligne.

Le modèle anglais est choisi car :

* plus léger,
* plus stable.

---

# 10. L’upsell

Concept marketing important.

## Upsell = proposer un produit complémentaire

Exemple :

* utilisateur achète du fromage,
* IA propose un vin adapté.

---

## Fonctionnement

1. frontend envoie le panier,
2. backend analyse le panier,
3. LLM + prompt génèrent une suggestion,
4. affichage dans le frontend.

---

## Point TRÈS important du cours

Les prompts sont versionnés.

Exemple :

```txt
prompt_v1.txt
prompt_v1.1.txt
```

Pourquoi ?

Parce qu’en IA :

> la manière de poser la question change énormément la qualité de la réponse.

---

# 11. Newsletter générée par IA

L’utilisateur indique ses centres d’intérêt.

Le backend :

* construit un prompt,
* génère une newsletter personnalisée.

Exemple :

* amateur de fromage,
* amateur de vin rouge,
* amateur de gastronomie.

👉 newsletter adaptée à la personne.

---

# 12. Le mono repository

Très important techniquement.

## Monorepo = tout dans un seul projet

On met ensemble :

* frontend,
* backend,
* modèles IA,
* données,
* prompts,
* tests.

---

## Pourquoi ?

### Avantages

* plus simple à maintenir,
* moins d’erreurs,
* plus cohérent,
* plus scalable.

---

# 13. La stack technique à mémoriser

Voici le “kit technique” du cours :

| Outil        | Rôle                        |
| ------------ | --------------------------- |
| FastAPI      | backend API                 |
| React        | frontend                    |
| Vite         | frontend rapide             |
| Tailwind CSS | design                      |
| Router       | navigation SPA              |
| Docker       | environnement identique     |
| Git          | versioning code             |
| DVC          | versioning datasets/modèles |
| MLflow       | suivi expérimentations      |

---

# 14. Git ≠ suffisant pour l’IA

Point fondamental du cours.

Git versionne bien :

* le code.

Mais PAS :

* gros modèles IA,
* datasets,
* expériences ML.

---

## Donc :

### Git

→ code

### DVC

→ datasets + modèles lourds

### MLflow

→ expériences IA

C’est une idée TRÈS importante.

---

# 15. La logique globale du cours

Le cours enseigne surtout cette méthode :

## Construire un projet IA proprement

### Étapes mentales :

1. faire une V1 simple,
2. utiliser de l’open source,
3. organiser le projet proprement,
4. prévoir les futures versions,
5. versionner :

   * code,
   * prompts,
   * données,
   * modèles.

---

# 16. Ce qu’il faut ABSOLUMENT retenir

Si tu dois retenir seulement 10 idées :

## Les 10 idées-clés

1. Un POC sert à tester rapidement une idée.
2. Un chatbot multimodal combine texte + image + voix.
3. Les modèles locaux réduisent les coûts.
4. Llama/Mistral = modèles open source.
5. FastAPI = backend IA simple et efficace.
6. React + Vite + Tailwind = frontend moderne.
7. Le versioning des prompts est essentiel.
8. Git seul ne suffit pas pour l’IA.
9. DVC versionne datasets et modèles.
10. Un monorepo centralise tout le projet.

---

# 17. Méthode mnémotechnique pour retenir le cours

Utilise cette phrase :

## “POC → Multi → Local → Versionné → Scalable”

### POC

on teste vite.

### Multi

texte + image + voix.

### Local

Llama/Vosk/Ollama en local.

### Versionné

Git + DVC + MLflow + prompts.

### Scalable

architecture propre et évolutive.

---

# 18. La vision globale (ultra simple)

Imagine le projet comme ceci :

```text
Utilisateur
   ↓
Frontend React
   ↓
Backend FastAPI
   ↓
Modules IA :
- texte
- sentiment
- image
- voix
- upsell
- newsletter
   ↓
LLM local (Llama/Mistral)
```

---

# 19. Comment vraiment mémoriser ce cours

Le meilleur moyen :

## Méthode en 3 niveaux

### Niveau 1 — Comprendre

Pose-toi :

> “Pourquoi ce choix technique ?”

Pas “quoi”.

---

### Niveau 2 — Reformuler

Explique le cours avec tes mots.

Exemple :

> “DVC sert à versionner les gros fichiers IA.”

---

### Niveau 3 — Visualiser

Imagine le flow :

* frontend,
* backend,
* IA,
* réponse.

Le cerveau retient mieux les systèmes que les listes.

---

# 20. Résumé ultra-court (30 secondes)

Le cours explique comment créer un chatbot IA multimodal à faible coût grâce à des modèles open source locaux. Le projet est organisé dans un monorepo avec FastAPI côté backend et React/Vite/Tailwind côté frontend. Le chatbot peut gérer texte, image, voix et analyse de sentiment. Le cours insiste aussi sur le versioning IA avec Git, DVC, MLflow et le versioning des prompts pour construire un projet maintenable et évolutif.
