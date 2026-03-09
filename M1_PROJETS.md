# TP2 — Projet de développement avec IA

## Informations générales

**Modalité** : Individuel
**Évaluation** : Sur livrables, sans soutenance orale  
**Outils autorisés** : Claude, ChatGPT, Cursor, Claude Code, Copilot... tous les outils IA

---

## Ce que ce TP évalue

En 2026, générer du code avec l'IA est trivial. Ce n'est plus une compétence.

**Ce qu'on évalue :**

| On évalue | On n'évalue plus |
|-----------|------------------|
| Ta capacité à formuler un besoin clair | Le volume de code |
| Ta compréhension de ce que l'IA génère | Le fait que ça compile |
| Tes choix d'architecture et leur justification | La vitesse d'exécution |
| Ta gestion des cas limites | Le nombre de features |
| Ton processus d'itération documenté | Les commentaires décoratifs |

**Question centrale** : As-tu construit quelque chose que tu comprends et pourrais maintenir ?

---

## Déroulement

###vCadrage

Choix du projet, analyse du problème, décisions techniques.

**Livrable** : Document de cadrage (1 page)
- Le problème que tu résous (avec tes mots)
- Tes choix techniques justifiés
- Ce que tu ne feras PAS (scope négatif)
- Les difficultés anticipées

### Développement 

Tu développes avec l'IA. Tu documentes dans ton journal.

**À chaque session** :
- Objectif clair
- Prompts significatifs notés
- Problèmes rencontrés → solutions trouvées
- Ce que tu as appris

### Finalisation 

Tests des cas limites, documentation, polish.

**Livrables finaux** :
- Code fonctionnel
- README (installation + utilisation)
- Journal de développement
- Documentation des choix

---

## Évaluation (100 points)

### Fonctionnalité — 25 points

| Critère | Points |
|---------|--------|
| Le projet démarre sans erreur | 5 |
| Les fonctionnalités principales marchent | 10 |
| Les cas limites sont gérés | 5 |
| C'est utilisable (pas juste "ça tourne") | 5 |

### Journal de développement — 25 points

| Critère | Points |
|---------|--------|
| Prompts documentés avec contexte | 8 |
| Itérations et corrections expliquées | 7 |
| Réflexion sur ce qui a marché/échoué | 5 |
| Évolution visible de la compréhension | 5 |

**Bonne entrée de journal :**
```
Session 2 — Objectif : implémenter la recherche sémantique

Prompt : "Ajoute une recherche par embeddings sur mes chunks. 
Utilise l'API OpenAI text-embedding-3-small."

Problème : le code généré stockait les embeddings en mémoire.
Avec 500 chunks, ça crashait au redémarrage (tout perdu).

Solution : j'ai demandé de persister dans un fichier JSON.
Pas optimal mais suffisant pour le MVP.

Apprentissage : toujours penser à la persistance dès le début.
```

**Mauvaise entrée :**
```
J'ai demandé à Claude de faire la recherche. Ça marche.
```

### Compréhension technique — 25 points

Questionnaire écrit de 15/30 minutes (sans IA, sans ordinateur).

Questions type :
- "Explique ce que fait cette fonction de ton code"
- "Si on voulait ajouter X, que faudrait-il modifier ?"
- "Que se passe-t-il si l'utilisateur fait Y ?"

### Documentation — 15 points

| Critère | Points |
|---------|--------|
| README clair et utilisable | 5 |
| Architecture expliquée | 5 |
| Choix techniques justifiés | 5 |

### Qualité — 10 points

| Critère | Points |
|---------|--------|
| Gestion des erreurs | 3 |
| Pas de crash sur inputs invalides | 4 |
| Code maintenable | 3 |

---

## Les pièges classiques

### Piège 1 : Accepter du code sans comprendre

Tu copies le code de l'IA, ça marche, tu passes à la suite. Au questionnaire, tu ne sais pas expliquer.

**Solution** : Pour chaque bloc généré, demande-toi "est-ce que je pourrais l'expliquer à quelqu'un ?"

### Piège 2 : Le projet trop ambitieux

Tu veux tout faire. À la fin, rien ne marche vraiment.

**Solution** : Un MVP (Minimum Viable Product) qui marche vaut mieux qu'un projet complet qui crashe.

### Piège 3 : Pas de gestion d'erreurs

L'IA génère le "happy path". Dès qu'on sort du cas normal, ça explose.

**Solution** : Teste avec des inputs vides, trop longs, mal formatés.

### Piège 4 : Le journal vide

Tu codes, tu oublies de documenter. À la fin, tu ne te souviens plus.

**Solution** : Note en temps réel, même juste 3 lignes par session.

---

## Structure des livrables

```
mon-projet/
├── README.md              # Description, installation, utilisation
├── JOURNAL.md             # Journal de développement
├── src/                   # Code source
└── .env.example           # Variables d'environnement (sans secrets)
```

---

# LES 15 PROJETS

Chaque projet a un **MVP** (objectif minimal) et une **version avancée** (pour ceux qui vont plus vite).

---

## Projet 1 : Système de suivi de réunions avec actions

### Le vrai problème

Tu sors de réunion, tu notes les actions dans un fichier, et... ça meurt là. Personne ne sait ce qui a été fait, les deadlines passent, les mêmes sujets reviennent à la réunion suivante.

### Ce que tu construis

Un système où tu importes tes notes/transcriptions de réunion. Le système extrait les actions, les assigne, track leur statut, et fait le lien entre les réunions (une action créée en réunion 1 peut être marquée "done" en réunion 3).

### Techniques IA utilisées

- **Extraction structurée** : actions, responsables, deadlines, décisions
- **Classification** : distinguer discussion/décision/action
- **RAG** : retrouver les actions liées dans les réunions précédentes

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Import réunion  │────▶│ Extraction IA    │────▶│ Base actions    │
│                 │     │ (LLM)            │     │ (SQLite/JSON)   │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│ Dashboard       │◀────│ Recherche/Liens  │◀─────────────┘
│ (actions, états)│     │ (embeddings)     │
└─────────────────┘     └──────────────────┘
```

### MVP (6h)

- Import d'une réunion (texte ou audio)
- Extraction des actions avec responsable et deadline si mentionnés
- Stockage persistant (fichier JSON ou SQLite)
- Liste des actions avec statut (todo/done)
- Modification manuelle du statut
- Vue "actions en retard"

### Version avancée

- Lien automatique entre réunions (détection de suivi d'action)
- Recherche sémantique dans l'historique ("qu'est-ce qu'on avait dit sur le budget ?")
- Détection d'actions récurrentes ("on en reparle à chaque réunion")
- Export rapport hebdo des actions par personne

### Critères spécifiques

- Les actions extraites sont vraiment des actions (pas des discussions)
- La persistance fonctionne (redémarrage = données conservées)
- Le lien entre réunions est pertinent

---

## Projet 2 : Pipeline de qualification de leads

### Le vrai problème

Tu reçois des leads (formulaires, emails, LinkedIn). Certains sont qualifiés, d'autres pas. Tu passes du temps à lire, qualifier manuellement, et souvent tu oublies de relancer.

### Ce que tu construis

Un pipeline où tu importes des leads (texte structuré ou non). Le système extrait les infos clés, score selon tes critères, et génère un plan de relance personnalisé.

### Techniques IA utilisées

- **Extraction structurée** : nom, entreprise, besoin, budget, timing
- **Scoring** : correspondance avec profil idéal
- **Génération personnalisée** : email de relance adapté au contexte

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Import leads    │────▶│ Extraction IA    │────▶│ Base leads      │
│ (CSV/texte)     │     │ + Scoring        │     │ + historique    │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│ Emails générés  │◀────│ Génération       │◀─────────────┘
│ personnalisés   │     │ contextualisée   │
└─────────────────┘     └──────────────────┘
```

### MVP (6h)

- Définition des critères de scoring (config)
- Import de leads (CSV avec colonnes libres ou texte brut)
- Extraction des infos clés + scoring
- Stockage avec statut (nouveau/contacté/qualifié/perdu)
- Génération d'un email de premier contact personnalisé
- Vue triée par score

### Version avancée

- Séquence de relance multi-étapes (J+3, J+7, J+14)
- Historique des interactions par lead
- Détection de signaux dans les réponses ("pas maintenant" → relancer dans 3 mois)
- Stats de conversion par source

### Critères spécifiques

- Le scoring est cohérent (mêmes infos = même score)
- Les emails générés sont personnalisés (pas de template générique visible)
- L'historique persiste

---

## Projet 3 : Comparateur de contrats avec alertes

### Le vrai problème

Tu reçois la V2 d'un contrat. "On a fait quelques ajustements mineurs." Tu dois comparer 40 pages pour trouver ce qui a changé. Et tu dois vérifier qu'il n'y a pas de clauses problématiques.

### Ce que tu construis

Un système où tu uploades deux versions d'un contrat. Le système identifie les changements, évalue leur importance, et alerte sur les clauses potentiellement dangereuses.

### Techniques IA utilisées

- **Extraction structurée** : clauses, conditions, montants, dates
- **Comparaison sémantique** : pas juste diff textuel, mais sens
- **Classification de risque** : clauses à surveiller

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Contrat V1      │────▶│ Extraction       │────▶│ Structure V1    │
└─────────────────┘     │ clauses          │     └────────┬────────┘
                        └──────────────────┘              │
┌─────────────────┐     ┌──────────────────┐              │
│ Contrat V2      │────▶│ Extraction       │────▶│ Structure V2    │
└─────────────────┘     │ clauses          │     └────────┬────────┘
                        └──────────────────┘              │
                        ┌──────────────────┐              │
                        │ Comparaison +    │◀─────────────┘
                        │ Alertes risques  │
                        └──────────────────┘
```

### MVP (6h)

- Upload de 2 documents texte (V1 et V2)
- Extraction des clauses principales (structurée)
- Comparaison : ajouts, suppressions, modifications
- Classification de chaque changement (mineur/important/critique)
- Liste d'alertes sur clauses à risque (délais courts, pénalités, exclusivité...)

### Version avancée

- Base de "clauses à surveiller" personnalisable
- Historique multi-versions (V1 → V2 → V3)
- Benchmark : comparer avec tes autres contrats similaires
- Export rapport de négociation ("points à discuter")

### Critères spécifiques

- Les changements détectés sont réels (vérifiables)
- Les alertes sont pertinentes (pas trop de faux positifs)
- Les changements "mineurs" sont vraiment mineurs

---

## Projet 4 : Chatbot support avec mémoire et escalade

### Le vrai problème

Tu as une doc produit. Les utilisateurs posent des questions. Un chatbot basique répond, mais il oublie tout à chaque message, ne détecte pas quand l'utilisateur est frustré, et ne sait pas escalader vers un humain.

### Ce que tu construis

Un chatbot qui répond sur ta documentation, se souvient du contexte de conversation, détecte l'insatisfaction, et escalade proprement quand il ne peut pas aider.

### Techniques IA utilisées

- **RAG** : recherche dans la documentation
- **Mémoire conversationnelle** : contexte des échanges précédents
- **Classification** : détection de sentiment/frustration
- **Décision** : quand escalader

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Documentation   │────▶│ Chunking +       │────▶│ Index           │
│ (md/txt)        │     │ Embeddings       │     │ (recherche)     │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│ Message user    │────▶│ Contexte + RAG   │◀─────────────┘
└─────────────────┘     │ + Mémoire        │
                        └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Réponse OU       │
                        │ Escalade         │
                        └──────────────────┘
```

### MVP (6h)

- Ingestion d'une documentation (chunking, stockage)
- Chat avec recherche RAG
- Mémoire de la conversation courante (le bot sait ce qu'on vient de dire)
- Détection basique d'escalade ("je veux parler à un humain", 3 questions sans réponse satisfaisante)
- Log des conversations pour analyse

### Version avancée

- Mémoire cross-sessions (le bot se souvient des conversations passées)
- Détection de frustration par analyse de sentiment
- Suggestions proactives ("Voulez-vous que je crée un ticket ?")
- Dashboard analytics (questions fréquentes, taux d'escalade)

### Critères spécifiques

- La mémoire fonctionne (référence à un message précédent = compris)
- L'escalade se déclenche au bon moment
- Les réponses citent la documentation

---

## Projet 5 : Agent de recherche multi-sources

### Le vrai problème

Tu dois répondre à une question complexe qui nécessite de croiser plusieurs sources : ta documentation interne, le web, des fichiers locaux. Tu fais ça manuellement, onglet par onglet.

### Ce que tu construis

Un agent qui prend une question, décide quelles sources interroger, exécute les recherches, et synthétise une réponse avec sources citées.

### Techniques IA utilisées

- **ReAct** : boucle Thought/Action/Observation
- **Tool calling** : recherche doc, recherche web (simulée), calcul
- **Synthèse** : combiner les résultats de plusieurs sources

### Architecture requise

```
┌─────────────────┐
│ Question        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Agent ReAct     │────▶│ Tool: Doc locale │
│ (boucle)        │────▶│ Tool: "Web"      │
│                 │────▶│ Tool: Calcul     │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│ Synthèse avec   │
│ sources citées  │
└─────────────────┘
```

### MVP (6h)

- 3 tools fonctionnels :
  - Recherche dans docs locales (RAG)
  - "Recherche web" (peut être simulée avec fichiers)
  - Calculatrice
- Boucle ReAct visible (on voit Thought/Action/Observation)
- Limite d'itérations (max 7)
- Réponse finale avec sources

### Version avancée

- Vraie recherche web (API ou scraping)
- Détection de sources contradictoires
- Mémoire des recherches précédentes
- Parallélisation des recherches indépendantes

### Critères spécifiques

- L'agent utilise les bons outils (pas recherche web pour une question sur doc locale)
- La trace ReAct est lisible
- L'agent s'arrête au bon moment (ni trop tôt ni boucle infinie)

---

## Projet 6 : Système de tri de CVs avec apprentissage

### Le vrai problème

Tu tries des CVs. Tu définis des critères, mais au fil du tri tu affines : "en fait les profils startup m'intéressent plus que prévu". Le système devrait apprendre de tes décisions.

### Ce que tu construis

Un système de tri de CVs qui extrait, score, et surtout apprend de tes validations/rejets pour affiner ses critères.

### Techniques IA utilisées

- **Extraction structurée** : compétences, expérience, formation
- **Scoring** : correspondance avec critères
- **Few-shot learning** : améliorer le scoring avec tes décisions

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ CVs (texte)     │────▶│ Extraction IA    │────▶│ Profils extraits│
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│ Critères +      │────▶│ Scoring          │◀─────────────┘
│ Exemples validés│     │ (avec feedback)  │
└─────────────────┘     └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Classement +     │
                        │ Explication      │
                        └──────────────────┘
```

### MVP (6h)

- Définition du profil recherché (critères obligatoires/souhaitables)
- Upload et extraction de CVs (5-10)
- Scoring avec explication pour chaque CV
- Interface de validation/rejet
- Le score se recalcule en intégrant les exemples validés (few-shot dans le prompt)

### Version avancée

- Détection de biais potentiel ("vous avez rejeté tous les profils de X")
- Suggestions de critères ("les profils validés ont souvent Y")
- Comparaison entre candidats sur critères spécifiques
- Export shortlist avec justifications

### Critères spécifiques

- L'apprentissage fonctionne (après feedback, le scoring change)
- Les explications sont vérifiables dans le CV
- Les critères obligatoires sont vraiment éliminatoires

---

## Projet 7 : Dashboard d'analyse de feedback client

### Le vrai problème

Tu as des centaines d'avis/feedbacks. Tu veux des insights : qu'est-ce qui plaît, qu'est-ce qui pose problème, est-ce que ça évolue dans le temps ? Pas juste un sentiment moyen.

### Ce que tu construis

Un dashboard qui analyse les feedbacks, identifie les thèmes, track l'évolution, et alerte sur les problèmes émergents.

### Techniques IA utilisées

- **Extraction thématique** : identifier les sujets abordés
- **Sentiment par aspect** : "livraison" négatif, "produit" positif
- **Agrégation** : patterns, tendances
- **Détection d'anomalie** : pic de plaintes sur un sujet

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Feedbacks       │────▶│ Analyse IA       │────▶│ Base analysée   │
│ (CSV/texte)     │     │ (thèmes, sent.)  │     │ (avec date)     │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│ Dashboard       │◀────│ Agrégation +     │◀─────────────┘
│ (vues, alertes) │     │ Tendances        │
└─────────────────┘     └──────────────────┘
```

### MVP (6h)

- Import de feedbacks avec date (CSV ou texte)
- Analyse : sentiment + 2-3 thèmes par feedback
- Stockage persistant
- Vue agrégée : répartition des thèmes, sentiment moyen par thème
- Top 3 positifs, top 3 négatifs avec exemples représentatifs

### Version avancée

- Évolution temporelle (graphique sentiment par semaine)
- Alertes : détection de pic négatif sur un thème
- Comparaison de périodes ("ce mois vs mois dernier")
- Clustering automatique des thèmes émergents

### Critères spécifiques

- Les thèmes identifiés sont cohérents
- L'agrégation est correcte (vérifiable manuellement sur un échantillon)
- La persistance fonctionne (ajout de nouveaux feedbacks)

---

## Projet 8 : Traducteur technique avec mémoire de traduction

### Le vrai problème

Tu traduis de la doc technique. À chaque nouveau document, tu retraduis les mêmes phrases. "Click on the button" tu l'as déjà traduit 50 fois. Et tu dois maintenir un glossaire.

### Ce que tu construis

Un traducteur qui maintient un glossaire, une mémoire de traduction (phrases déjà traduites), et assure la cohérence sur un projet.

### Techniques IA utilisées

- **RAG** : retrouver les traductions similaires passées
- **Few-shot** : utiliser le glossaire et les exemples
- **Structured output** : préserver le formatage (code, markdown)

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐
│ Glossaire       │────▶│                  │
└─────────────────┘     │                  │
                        │ Traduction IA    │────▶ Texte traduit
┌─────────────────┐     │ (contextualisée) │
│ Mémoire (TM)    │────▶│                  │
│ (phrases passées│     │                  │
└─────────────────┘     └──────────────────┘
         ▲                       │
         └───────────────────────┘
         (nouvelles traductions ajoutées)
```

### MVP (6h)

- Glossaire éditable (terme source → terme cible ou "ne pas traduire")
- Traduction d'un texte avec respect du glossaire
- Mémoire de traduction : stockage des segments traduits
- Réutilisation automatique des traductions similaires (>90% match)
- Le code et le formatage Markdown sont préservés

### Version avancée

- Fuzzy matching sur la mémoire (80-90% → suggestion avec diff)
- Détection d'incohérence ("tu as traduit X par Y avant, maintenant par Z")
- Import/export standard (TMX pour la mémoire)
- Stats de réutilisation (% de la mémoire utilisé)

### Critères spécifiques

- Le glossaire est toujours respecté
- La mémoire est effectivement réutilisée
- Le code n'est jamais traduit

---

## Projet 9 : Générateur de contenu avec workflow éditorial

### Le vrai problème

Tu génères du contenu (posts, articles). Mais c'est un processus : idée → premier jet → review → corrections → publication. Pas juste un prompt one-shot.

### Ce que tu construis

Un système de génération avec workflow : brouillon, review avec suggestions, itérations, et cohérence de style sur plusieurs contenus.

### Techniques IA utilisées

- **Few-shot** : exemples de ton style/format
- **Génération itérative** : amélioration par feedback
- **Review automatique** : checklist de qualité

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Brief + Style   │────▶│ Génération V1    │────▶│ Draft           │
│ (exemples)      │     └──────────────────┘     │ (statut: draft) │
└─────────────────┘                              └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│ Feedback user   │────▶│ Review IA +      │◀─────────────┘
│ ou IA           │     │ Régénération     │
└─────────────────┘     └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Version finale   │
                        │ (statut: ready)  │
                        └──────────────────┘
```

### MVP (6h)

- Définition d'un style (3-5 exemples de contenus validés)
- Génération d'un brouillon à partir d'un brief
- Review automatique (checklist : longueur, structure, ton)
- Stockage avec versions (V1, V2, V3...)
- Workflow simple (draft → review → ready)

### Version avancée

- Review croisée avec critique constructive
- Suggestions d'amélioration spécifiques
- A/B : générer 2 versions et comparer
- Bibliothèque de contenus publiés (pour cohérence)

### Critères spécifiques

- Le style des exemples est respecté (reconnaissable)
- La review identifie de vrais problèmes
- Les versions sont traçables

---

## Projet 10 : Simulateur d'entretien adaptatif

### Le vrai problème

Tu veux t'entraîner pour un entretien. Les listes de "100 questions d'entretien" sont génériques. Tu veux des questions adaptées à TON profil, qui s'adaptent à tes réponses.

### Ce que tu construis

Un simulateur qui pose des questions adaptées, évalue tes réponses, ajuste la difficulté, et donne du feedback actionnable.

### Techniques IA utilisées

- **Personnalisation** : questions basées sur CV + poste
- **Évaluation** : scoring de réponses avec critères
- **Adaptation** : ajuster la difficulté selon la performance
- **Few-shot** : exemples de bonnes réponses pour le feedback

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐
│ CV + Poste      │────▶│ Générateur de    │
└─────────────────┘     │ questions        │
                        └────────┬─────────┘
                                 │
┌─────────────────┐     ┌────────▼─────────┐
│ Réponse user    │────▶│ Évaluation +     │
└─────────────────┘     │ Score + Feedback │
                        └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Question suivante│
                        │ (adaptée)        │
                        └──────────────────┘
```

### MVP (6h)

- Input : description de poste + CV
- Génération de 5-7 questions spécifiques au contexte
- Pour chaque réponse : évaluation + feedback + pistes d'amélioration
- Adaptation basique (réponse faible → question de relance, réponse forte → question plus dure)
- Bilan de fin d'entretien

### Version avancée

- Suivi de progression sur plusieurs sessions
- Banque de questions par compétence avec maîtrise trackée
- Mode "stress" avec timer
- Exemples de bonnes réponses générées

### Critères spécifiques

- Les questions sont spécifiques (pas génériques)
- L'adaptation est perceptible
- Le feedback est actionnable

---

## Projet 11 : Assistant de code review multi-critères

### Le vrai problème

Tu review du code. Tu dois checker plusieurs choses : bugs, sécurité, performance, style, maintenabilité. C'est facile d'en oublier. Et les commentaires sont souvent vagues ("à améliorer").

### Ce que tu construis

Un assistant qui analyse le code sur plusieurs axes, priorise les problèmes, et propose des corrections concrètes.

### Techniques IA utilisées

- **Analyse multi-critères** : plusieurs prompts spécialisés
- **Priorisation** : scoring de sévérité
- **Génération de fix** : pas juste critiquer, proposer

### Architecture requise

```
┌─────────────────┐
│ Code à review   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Analyse Bugs    │  │ Analyse Sécu    │  │ Analyse Style   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                     ┌────────▼────────┐
                     │ Agrégation +    │
                     │ Priorisation    │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │ Rapport avec    │
                     │ suggestions     │
                     └─────────────────┘
```

### MVP (6h)

- Input : fichier de code (Python ou JS)
- 3 analyses séparées : bugs potentiels, sécurité, lisibilité
- Chaque problème a : localisation, sévérité, explication, suggestion de fix
- Rapport consolidé trié par sévérité
- Les suggestions de fix sont du code fonctionnel

### Version avancée

- Analyse de diff (juste les changements)
- Apprentissage des conventions d'équipe (exemples de code validé)
- Intégration Git (commenter sur les lignes)
- Tracking des problèmes récurrents par auteur

### Critères spécifiques

- Les problèmes identifiés sont réels (testables)
- La priorisation est pertinente
- Les fix proposés fonctionnent

---

## Projet 12 : FAQ auto-améliorante

### Le vrai problème

Tu as une FAQ. Les gens posent des questions qui ne sont pas dedans. Tu devrais enrichir ta FAQ avec les vraies questions, mais tu n'as pas le temps d'analyser les logs.

### Ce que tu construis

Un système de FAQ qui répond aux questions, identifie les questions fréquentes non couvertes, et suggère des ajouts.

### Techniques IA utilisées

- **RAG** : recherche dans la FAQ existante
- **Clustering** : regrouper les questions similaires
- **Génération** : proposer de nouvelles entrées FAQ

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ FAQ existante   │────▶│ Index            │◀────│ Questions       │
│ (Q/R)           │     │ (recherche)      │     │ utilisateurs    │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Réponse OU       │
                        │ "Je ne sais pas" │
                        └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Analytics :      │
                        │ questions sans   │
                        │ réponse → cluster│
                        └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Suggestions      │
                        │ nouvelles Q/R    │
                        └─────────────────┘
```

### MVP (6h)

- Import d'une FAQ existante (JSON ou Markdown)
- Réponse aux questions (RAG)
- Log de toutes les questions posées
- Détection des questions sans bonne réponse
- Clustering des questions similaires non couvertes
- Suggestion d'ajout à la FAQ (question + réponse proposée)

### Version avancée

- Validation des suggestions (approve/reject)
- Analytics : questions les plus fréquentes, taux de réponse
- Détection de FAQ obsolètes (jamais consultées)
- Génération de FAQ à partir de documentation existante

### Critères spécifiques

- Les clusters sont cohérents (questions vraiment similaires)
- Les suggestions de nouvelles Q/R sont pertinentes
- Le système s'améliore avec le temps

---

## Projet 13 : Extracteur de données de formulaires

### Le vrai problème

Tu reçois des formulaires remplis (PDF, images, emails mal formatés). Tu dois extraire les données et les mettre dans ton système. Copier-coller manuel, c'est des heures.

### Ce que tu construis

Un extracteur qui prend des formulaires variés, extrait les champs selon un schéma défini, valide, et signale les problèmes.

### Techniques IA utilisées

- **Extraction structurée** : mapping vers un schéma
- **Validation** : règles métier, cohérence
- **Gestion d'erreur** : champs manquants, illisibles

### Architecture requise

```
┌─────────────────┐     ┌──────────────────┐
│ Schéma attendu  │────▶│                  │
│ (champs, types) │     │                  │
└─────────────────┘     │ Extraction IA    │────▶ JSON structuré
                        │                  │
┌─────────────────┐     │                  │
│ Document input  │────▶│                  │
│ (texte/pdf)     │     └────────┬─────────┘
└─────────────────┘              │
                        ┌────────▼─────────┐
                        │ Validation +     │
                        │ Signalement      │
                        └──────────────────┘
```

### MVP (6h)

- Définition d'un schéma (JSON Schema simple)
- Extraction de documents texte vers le schéma
- Validation des types et des contraintes basiques
- Chaque champ a un niveau de confiance
- Les champs non trouvés ou douteux sont signalés
- Export JSON valide

### Version avancée

- Règles de validation métier (ex: IBAN valide, date cohérente)
- Traitement batch (plusieurs documents)
- Interface de correction manuelle
- Apprentissage des corrections (amélioration continue)

### Critères spécifiques

- Le JSON produit est valide contre le schéma
- Les champs "confiance basse" sont vraiment douteux
- Pas d'invention (champ absent = null, pas de valeur inventée)

---

## Projet 14 : Assistant de spécification technique

### Le vrai problème

Tu dois rédiger une spec technique à partir d'un besoin vague. "On veut un système de notification." OK mais quoi précisément ? Tu oublies toujours des cas, les specs sont incomplètes.

### Ce que tu construis

Un assistant qui t'interroge sur le besoin, génère une spec structurée, et identifie les zones floues ou les cas non couverts.

### Techniques IA utilisées

- **Dialogue structuré** : questions de clarification
- **Génération structurée** : format de spec standard
- **Chain-of-Thought** : raisonnement sur les cas limites

### Architecture requise

```
┌─────────────────┐
│ Besoin initial  │
│ (vague)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Questions de    │◀───▶│ Réponses user    │
│ clarification   │     │                  │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│ Génération spec │
│ structurée      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyse :       │
│ zones floues,   │
│ cas non couverts│
└─────────────────┘
```

### MVP (6h)

- Input : description informelle d'un besoin
- Génération de questions de clarification
- Dialogue jusqu'à suffisamment d'infos
- Génération de spec structurée (contexte, exigences fonctionnelles, non-fonctionnelles, cas d'usage)
- Identification des ambiguïtés restantes

### Version avancée

- Templates de spec par type de projet
- Génération de user stories à partir de la spec
- Estimation de complexité
- Checklist de complétude

### Critères spécifiques

- Les questions sont pertinentes (pas génériques)
- La spec générée est utilisable
- Les zones floues identifiées sont réelles

---

## Projet 15 : Debugger pédagogique

### Le vrai problème

Tu as un bug. L'IA te donne la solution. Tu n'as rien appris. La prochaine fois, même bug, même question. Tu veux comprendre, pas juste fix.

### Ce que tu construis

Un assistant de debugging qui t'accompagne dans la résolution au lieu de donner la réponse : hypothèses, tests à faire, explication de ce qui se passe.

### Techniques IA utilisées

- **Chain-of-Thought** : raisonnement visible
- **Dialogue socratique** : guider sans donner la réponse
- **Structured outputs** : hypothèses, tests, diagnostic

### Architecture requise

```
┌─────────────────┐
│ Code + Erreur   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyse : que   │
│ se passe-t-il ? │
│ (sans solution) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Hypothèses      │────▶│ Tests suggérés   │
│ possibles       │     │ pour vérifier    │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────┐
│ User fait les   │────▶│ Guidage vers     │
│ tests           │     │ la compréhension │
└─────────────────┘     └──────────────────┘
```

### MVP (6h)

- Input : code + message d'erreur
- Explication de ce que l'erreur signifie (pédagogique)
- 2-3 hypothèses de cause possible
- Pour chaque hypothèse : un test à faire pour vérifier
- L'utilisateur fait le test, reporte le résultat
- Guidage vers la solution avec explication du "pourquoi"

### Version avancée

- Mode "révèle la solution" si vraiment bloqué
- Base de bugs courants avec patterns
- Suivi des bugs résolus (historique d'apprentissage)
- Quiz sur le concept sous-jacent après résolution

### Critères spécifiques

- L'assistant ne donne PAS la solution directement
- Les hypothèses sont pertinentes
- L'explication finale est compréhensible
