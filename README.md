# Bon vivant projet contenant l'IA

Monorepo IA modulaire :
- chabot (text, image, voix, sentiment),
- upsell
- newsletter

Stack :
- FastAPI,
- React / Vite/ Tailwind
- Router,
- Llama,
- openAI
- DVC
- MLflow,
- Docker
- GitHub Actions


# Exercice : Partie 1 : Cas pratique
Vous êtes développeur full-stack dans une entreprise technologique française.

Votre mission est de soutenir l'équipe marketing lors de la présentation d'un chatbot multimodal à des investisseurs.

L'enjeu est double. Vous devez prouver la faisabilité technique du projet et argumenter sur sa capacité à être robuste, évolutif et durable. Vous devrez à la fois maîtriser les fondamentaux de l'IA et savoir les vulgariser mais aussi justifier des choix techniques stratégiques qui démontrent la performance, la pertinence et la crédibilité de votre solution.

1. Lors de la présentation, un investisseur vous demande : « Qu'entendez-vous par IA symbolique ? » Comment expliquez-vous simplement ce concept ?
C'est-à-dire une intelligence artificielle capable de s'adapter à des conditions comme "si.. alors".

2. Un investisseur visiblement sceptique vous interpelle : « Comment pouvez-vous garantir que le chatbot ne donnera pas de réponses hors sujet face aux questions des utilisateurs ? »
Nous avons intégré une phase de testing lors de la création du projet. Tout d’abord, nous avons soumis des questions dans le périmètre au chatbot. Il s’agissait de questions directement liées à la base de données produits de l'entreprise. Puis nous avons confronté le chatbot à des questions hors périmètre, à savoir non couvertes par cette même base. Dans ce cas, l'IA prend le relais afin de générer une réponse pertinente. Cette étape de validation et d'évaluation nous a permis de mesurer précisément les performances de la solution et les résultats obtenus ont été très satisfaisants.

3. Vous avez évoqué le terme « Apprentissage par renforcement ». Un investisseur vous demande d’expliquer vos propos.
C'est-à-dire que l'on entraine le modèle comme on entrainerait un étudiant. On lui donne un certain nombre de données qui a été récolté et traiter précédemment puis on le test pour savoir comment il réagit
>Solution
Le terme « apprentissage par renforcement » fait référence au cas où l’intelligence artificielle apprend par essais, erreurs, victoires et récompenses.

4. Et si l'entreprise traite des données très sensibles, quelle méthode privilégierez-vous ?
Afin de respecter les conventions RGPD, nous n'utiliserons pas les données sensibles telles quel, nous anonymiserons ces dernières, voir si certaines ne sont pas utiles pour certaines actiosn elles ne seront pas sauvegarder.
De plus, si nous devions les utiliser, nous demanderions le consentement à l'utilisateur.
>Solution
Le développement sur-mesure car il est plus flexible et adapté aux données sensibles, bien que plus long et plus couteux.

5. Comment les profils techniques et non techniques s'entendent. Parlent-ils le même langage autour du projet ?
Nos objectifs sont les mêmes, une fois la logique métier définie et comprise par les techniques, tout le monde se comprend.
>Solution
Il y a une entente est une compréhension naturelle dans l'équipe car nous avons la logique métier comme point commun. Cela signifie que les choix techniques sont immédiatement traduits en impacts concrets pour l'entreprise. Ainsi, les solutions IA développées sont alignées avec les objectifs stratégiques et les contraintes réelles de l'entreprise.

6. Quel est le socle technique de votre projet ?
>Solution
Nous avons choisi FastAPI côté backend car il s'agit d'une API rapide et adaptée à l'IA. 
Puis nous avons choisi React, Vite, Router et Tailwind côté frontend pour un rendu moderne et modulaire.

7. Vous expliquez que votre projet est flexible grâce aux variables d'environnement ?
Nous avons des environement différent afin de répondre quoi qu'il arrive.
Par exemple, nous pouvons passer de l'IA local à l'API de openAi en cas de blocage
>Solution
En effet ! Nous avons mis en place plusieurs variables d’environnement. Ces dernières nous permettent de modifier le comportement de l’application sans modifier le code. Par exemple, grâce à une de nos variables d’environnement, nous pouvons basculer en mode API afin d’utiliser OpenAI plutôt que notre modèle d’intelligence artificielle local.

8. Dans le projet, quel est l'intérêt d'Ollama + Llama 3.2 Vision ?
C'est légé et moins couteux car local 
>Solution
Ollama et Llama 3.2 Vision sont des modèles IA légers, open-source, gratuits et qui tournent en local. Dans le cadre de notre proof of concept, 
c’est l’idéal car l'utilisation de ces outils permet un coût zéro pour l'application.

9. Pourquoi Vosk est-il choisi pour le speech-to-text ?
Vosk est utilisé afin de respecter les objectifs de la V1 locale à savoir un modèle local, gratuit, et léger.

10. Pourquoi l'équipe a-t-elle choisi FastAPI plutôt que Flask ?
En règle générale, FastAPI est privilégié par les développeurs IA pour sa rapidité et son adaptation aux API basées sur l'IA. 
C’est donc très naturellement que nous avons fait ce choix.


# Exercice : Partie 2 : Cas pratique

Avec le pic des fêtes, la direction veut augmenter la fidélisation des clients et maintenir un lien régulier avec eux. Après la réussite du chatbot multimodal, elle vous confie la création d'une newsletter IA personnalisée, ainsi qu'une fonction Upsell IA. Vous êtes en charge de la réalisation de ce projet

1. Lors d’une phase de testing, comment organiser les différents prompts sans modifier le code ?
Le prompt est versionné afin de pouvoir naviguer entre eux voir revenir en arrière s'il y en a un qui n'est pas adapté.
>Solution
Tout d’abord, nous allons créer plusieurs fichiers de prompts : newsletter_v1.0.txt, newsletter_v1.1.txt, ainsi de suite. Deuxièmement, nous allons centraliser le chargement des prompts dans un fichier prompt_manager.py. Cela permettra à l'équipe marketing de choisir une version à utiliser du prompt sans avoir à modifier l'entièreté du code. 
Seul le nom du fichier à charger devra être modifié.

2. En cas de forte affluence, le serveur local met trop de temps à générer les suggestions d'upsell. 
Quelles solutions techniques proposeriez-vous pour améliorer la performance ?
La solution serait de switcher sur l'API d'une IA
>Solution
Il est possible de mettre en place une fonction switch to API tel que OpenAI, migrer la fonction Upsell sur un serveur GPU cloud ou encore ajouter une file d'attente (queue) pour traiter les requêtes sans saturer le serveur.

3. Un bug est signalé, certains utilisateurs obtiennent une newsletter vide. Quelles vérifications techniques allez-vous effectuer pour identifier la cause ?
En premier, je verifierais l'envoi des données dans le back. Puis le prompt.
>Solution
Tout d'abord, il faut vérifier que le frontend envoie bien la liste interests. Ensuite, il est important de vérifier que le schéma Pydantic reçoit bien les données, ensuite, il faut contrôler la construction du prompt et s'assurer que {interests} est bien remplacé. 
Enfin, nous pourrions ajouter des logs backend pour tracer les inputs et outputs du modèle IA.

4. Quels éléments doivent être définis dans le fichier schemas.py pour supporter l'endpoint Upsell ?
>Solution
Il faut créer 2 classes Pydantic. Une première qui définit la structure des données envoyées (ici une liste d'articles) et
une seconde qui définit la structure de la réponse (donc une suggestion d’achat).
````python
class UpsellRequest(BaseModel):
    cart_items: List[str]
 
class UpsellResponse(BaseModel):
    suggestion: str
````

5. Comment écrire un endpoint FastAPI complet qui reçoit une requête UpsellRequest, appelle le fonction get_upsell et renvoie UpsellResponse ?
````python
@app.post("/upsell", response_model=UpsellResponse) 
async def upsell(request: UpsellRequest): 
result = get_upsell(request.cart_items) 
return UpsellResponse(**result)
````
`UpsellResponse` et `UpsellRequest` sont définit dans un fichier schema.py, la oute dans le frontend et la function get_upsell() dans un fichier services.

6. Comment versionner les modèles IA ?
En utilisant DVC
>Solution
Les modèles IA ne doivent pas être stockés dans Git car il s'agit de fichiers volumineux. Pour ce faire, nous allons utiliser DVC (Data Version Control) qui est bien plus adapté à ce contexte.

7. Quelles sont les bonnes pratiques à respecter pour garantir la conformité RGPD des fonctionnalités Upsell IA et Newsletter IA ?
- Ne pas stocker de donnée sensible sur les utilisateurs
- Avoir le concentement de l'utilistateur pour la newsletter
>Solution
Concernant la fonction Upsell IA, il ne faut pas stocker d'informations sensibles sur les utilisateurs, seulement sur leurs achats. Au sujet de la fonction newsletter IA, il faut recueillir le consentement explicite des utilisateurs avant de collecter leurs emails, et anonymiser leurs données le plus souvent possible.
Enfin, il est important de documenter l'utilisation de l'intelligence artificielle pour chaque fonctionnalité.

8. Quelle organisation de dossiers et de fichiers adopter pour implémenter correctement les endpoints Upsell et Newsletter dans le projet FastAPI ?

>Solution
* api/main.py contient les endpoints FastAPI. 
* api/schemas.py définit les schémas Pydantic.
* core/services contient les fonctions. 
* core/prompts stocke les prompts versionnés. 
* core/prompt_manager.py centralise les prompts 
* et enfin, models contient les modèles IA.