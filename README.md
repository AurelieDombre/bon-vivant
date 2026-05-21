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

# Exercice : Partie 3 : Cas pratique EduFrance

Vous êtes développeur full-stack chez EduFrance, une entreprise française qui développe des logiciels pour les organismes de formation.

L'entreprise souhaite développer une application web qui aidera les formateurs et les apprenants à optimiser leur parcours grâce à l'IA.

L'application doit intégrer deux fonctionnalités principales :
1. Un chatbot multimodal (texte, voix, image) qui répond aux questions de l’apprenant sur un sujet donné.
2. Une fonctionnalité d’upsell : recommandation de cours complémentaires basées sur le panier de l’apprenant.

### Questions :

1. Rédigez les user stories puis l’analyse technique associée à chaque fonctionnalité :

Ce qui est attendu :
* Décrivez le cycle de vie de chaque fonctionnalité (de la collecte de données à la mise à jour continue),
* Évaluez les technologies d'IA les plus adaptées à chaque fonctionnalité,
* Justifiez vos choix en tenant compte des contraintes éthiques et de la conformité RGPD,
* Présentez une première version du projet ainsi qu’une V2 plus avancée,
* Intégrez les bonnes pratiques de développement.


- user stories : en tant qu’apprenant, je peux poser des questions au chatbot sous forme de texte, voix et image afin d’obtenir des recommandations basées sur le cours.

* Cycle de vie :

1. Collecte de données : le chatbot va s’appuyer sur une base de données de cours. Ce dataset servira de base pour répondre aux questions des apprenants.
2. Entrainement : aucun fine-tuning pour cette fonctionnalité. Nous utiliserons un modèle pré-entrainé (Mistral-7B).
3. Inférence : lors d’une requête, le chatbot interroge d’abord le dataset. Si aucune correspondance n’est trouvée, l’IA prend le relais.
4. Validation : nous testerons les deux cas : questions couvertes par le dataset. Et questions hors périmètre (fallback IA).
5. Réentrainement et mise à jour : pour la V2, possibilité d’intégrer une API externe comme par exemple OpenAI afin d’améliorer les performances du chatbot.

* Analyse technique :

1. Backend : FastAPI, modèle d’IA Mistral-7B pour la génération de texte car il s’agit d’un modèle opensource, local et léger,
2. Frontend : React + React Router + Vite +Tailwind.

* Considérations RGPD et éthiques :

1. Les informations échangées avec le chatbot ne devront pas être stockées sans l’accord au préalable de l’utilisateur.
2. Si les données sont stockées, il faudra anonymiser les données.
3. Il faudra documenter notre utilisation de l’IA de manière claire.

* Bonnes pratiques de développement :

1. Versionnage du code avec Git.
2. Utilisation de DVC pour versionner les modèles IA.
3. Le chatbot sera modulaire, avec un endpoint dédié pour chaque modalité.


* Fonctionnalité voix :

User story : en tant qu’apprenant je pose une question à l'oral au chatbot afin d’obtenir des recommandations basées sur le cours.

* Cycle de vie :

1. Collecte de données : la voix de l’apprenant est enregistrée temporairement puis transcrite en texte.
2. Entrainement : pas de fine tuning pour cette fonctionnalité. Nous allons utiliser un modèle pré entrainé (Vosk).
3. Inférence : le chatbot analyse la question transcrite et génère une réponse personnalisée en s’appuyant sur les connaissances du cours.
4. Validation : nous vérifions la réponse par rapport aux données disponibles dans le dataset et vérifions que les questions couvertes par le fallback IA sont fiables.
5. Réentrainement et mise à jour : pour une V2 nous pouvons utiliser une API pour accélérer le traitement des questions. Des enquêtes utilisateurs permettront de mesurer l’efficacité.

* Analyse technique :

1. Backend : modèle IA Vosk car il s’agit d’un modèle léger et opensource. Seule limite ici, nous commencerons par tester notre endpoint avec un modèle Vosk en anglais puis nous pourrons basculer vers un modèle IA français après avoir validé la fonctionnalité.
2. Frontend : React + React Router + Vite + Tailwind.

* Considérations RGPD et éthiques :

1. Ne pas stocker la voix de l’utilisateur sans son consentement explicite.
2. Si la voix est stockée, anonymiser les données.
3. Documenter l’usage de l’IA.

* Bonnes pratiques de développement :

1. Versionnage de code avec Git,
2. Utilisation de DVC pour versionner les modèles IA.

* Fonctionnalité Image :

User Story : en tant qu’apprenant je peux envoyer la photo d’un diagramme ou de tout autre élément visuel au chatbot afin d’obtenir une explication claire.

* Cycle de vie :

1. Collecte de données : les photos envoyées par les apprenants sont traitées comme données d’entrée.
2. Entrainement : pas de fine-tuning. Nous utiliserons un modèle pré-entrainé local et opensource (Llama-vision).
3. Inférence : le pipeline de vision Llama-vision analyse l’image et génère une explication adaptée.
4. Validation : les résultats sont testés avec différents visuels pour vérifier la pertinence et la clarté des réponses.
5. Réentrainement et mise à jour : recours à une API spécialisée en V2 pour améliorer les performances de la fonctionnalité.

* Analyse technique :

1. Backend : comme modèle IA nous allons utiliser llama-vision,
2. Frontend : React + React Router + Vite + Tailwind.

* Considérations RGPD et éthiques :

1. Ne pas stocker les images de l’utilisateur sans consentement explicite.
2. Si l’image est stockée, anonymiser les données.
3. Documenter l’utilisation de l’IA pour cette fonctionnalité.

* Bonnes pratiques de développement :

1. Versionning Git pour les fichiers légers et le code,
2. Utilisation de DVC pour versionner les modèles IA.

* Fonctionnalité 2 : Upsell

User story : en tant qu’apprenant, lorsque j’ajoute une formation à mon panier, le système me propose automatiquement une formation complémentaire.

* Cycle de vie :

1. Collecte de données : récupération de l’historique d’achats et des parcours de formation.
2. Entrainement : pas de fine tuning, utilisation de Mistral-7B avec prompts adaptés.
3. Inférence : lorsqu’une formation est ajoutée au panier, le modèle IA génère une suggestion contextuelle.
4. Validation : mesurer le taux de clic, d’ajouts au panier et taux de conversion pour mesurer la pertinence de la fonctionnalité.
5. Réentrainement et mise à jour : envisager l’utilisation d’une API (OpenAI par exemple) pour affiner la qualité des recommandations.

* Analyse technique :

1. Backend : modèle IA Mistral-7B, prompts versionnés,
2. Frontend : React + React Router + Vite + Tailwind. Ajout d’une route « Upsell ».

* Bonnes pratiques de développement :

1. Versionner le code avec Git,
2. Utilisation de DVC pour versionner les modèles IA.

### Question
Proposez une architecture technique backend intégrant les deux fonctionnalités.

Ce qui est attendu :
  * La stratégie modulaire employée
  * Le rôle de chaque dossier et fichiers par fonctionnalités

* Architecture technique :

  1. Mono répository avec un endpoint par fonctionnalité.
  2. Application modulaire organisée par dossiers/fichiers.

* Dossiers principaux :

  * backend/api
  * backend/api/main.py : il s’agit du point d’entrée de notre application. Il contiendra l’ensemble de nos endpoints.
  * backend/api/schemas.py : il contiendra l’ensemble de nos schémas Pydantic.
  * backend/core.
  * backend/core/services.py : logique métier des différentes fonctionnalités.
  * backend/core/voice_client.py : logique “voix” du chatbot
  * backend/core/vision_client.py : logique “image” du chatbot
  * backend/core/prompt_manager.py: centralisation des prompts
  * backend/core/prompts : contiendra nos différents prompts pour la
  * Fonctionnalité upsell. Ceux-ci seront versionnés sous la forme upsell_prompt_v.1.0.txt pour plus de lisibilité et faciliter le testing.
  * backend/models : contient les modèles IA
  * backend/requirements.txt : fige les dépendances et outils


* Proposez l'endpoint ainsi que la fonction “get_upsell”.

  - Étape 1 : créer l’endpoint /upsell dans backend/api/main.py  
  - Étape 2 : dans le fichier main.py : importer les modèles Pydantic UpsellResponse et UpsellRequest ([lien vers le fichier](/backend/api/schemas.py))
  - Étape 3 : dans le fichier main.py : importer la fonction get_upsell
  - Étape 4 : création de l’endpoint /upsell 
[(Lien vers le fichier)](/backend/api/main.py)

# Exercice : Partie 4 : Mises en situation spécifiques
## Scénario 1 : Intégration d'une nouvelle capacité IA et amélioration du chatbot multimodal

EduFrance souhaite ajouter une fonctionnalité de génération de cours personnalisé basé sur les intérêts de l'apprenant 
ainsi qu’un système d’analyse de sentiment pour le chatbot.


### Questions :

1. Sélectionnez la technologie la plus adaptée pour les deux fonctionnalités supplémentaires.

* Fonctionnalité génération de cours personnalisé :
  * LLM : Mistral-7B,
  * Pourquoi : modèle open-source, léger, exécution locale donc plus de confidentialité, coûts maîtrisés. V2 : basculer vers API si besoin d’amélioration des performances (qualité des réponses, latence, etc.).
  * Approche : prompts versionnés (pas de fine-tuning en V1).
  * Frontend : ajout d’une route /cours.
  
* Fonctionnalité amélioration du chatbot multimodal viaAnalyse de sentiment :
  * Analyse technique : transformers (HuggingFace) avec Pytorch en local.
  * Règle d’escalade : si label == NEGATIVE et score > 0.75, escalate_to_human = True

2. Créez le prompt de la fonctionnalité de génération de cours personnalisé.
Dans un fichier : backend/core/prompts/course_v1.0.txt
--- 
> Solution :
Tu es concepteur pédagogique.
À partir des intérêts {interests} et du niveau {level}, produis :
  * 3 à 5 objectifs d’apprentissage
  * Un plan par modules (titres + contenus)
  * 1 activité pratiques et exercices
  * 1 ressource complémentaire
Style clair, concis, en français.
---


3. Créez l’endpoint de la fonctionnalité de génération de cours.

Endpoint /course : backend/api/main.py

> Étape 1 : Importer les modèles Pydantic : CourseResponse et CourseRequest

> Étape 2 : Importer la fonction generate_course.

> Étape 3 : Création de l’endpoint
````python
@app.post("/course", response_model=CourseResponse)
async def course_endpoint(req: CourseRequest):
    text = generate_course(req.interests)
    return CourseResponse(newsletter=text)
````

## Scénario 2 : Optimisation de performances
Le système de génération automatique de cours présente des latences importantes lorsque plusieurs apprenants l'utilisent simultanément.

1. Vous devez proposer l’implémentation d’une API pour améliorer la latence et les performances globales de la fonctionnalité.

Plusieurs facteurs peuvent expliquer la latence observée. Toutefois, la cause principale reste l’utilisation d’un modèle local dont les ressources sont limitées lorsque plusieurs apprenants sollicitent le service en simultané.
Pour pallier ce problème, nous mettons en place un switch to API. Grâce à une fonction toggle et des variables d’environnement, le système pourra basculer automatiquement du modèle local vers une API externe. Ici, nous retenons l’API OpenAI 
car elle est performante et capable d’absorber une forte charge.
Cette intégration permettra de réduire de manière significative le temps de réponse et de limiter la latence.
