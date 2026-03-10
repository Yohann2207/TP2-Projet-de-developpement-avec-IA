# Journal de developpement - TP2 Projet 2

## Session 1 - Initialisation

### Objectif
Mettre en place une base de projet propre et alignee avec le cadrage (PostgreSQL, livrables, scope MVP).

### Prompts significatifs notes
- "Aide-moi a transformer mon cadrage en structure de projet simple (src, docs, journal, readme)."
- "Quelles variables d'environnement minimales faut-il pour PostgreSQL + OpenAI ?"

### Ce que j'ai decide
- Garder une architecture courte et lisible.
- Imposer PostgreSQL des le debut pour rester coherent avec mon document de cadrage.

### Problemes rencontres -> solutions trouvees
- Probleme: risque de m'ecarter du cadrage pendant le dev.
- Solution: creation d'un fichier `docs/PROJECT_RULES.md` comme reference unique.

### Ce que j'ai appris
Poser les regles projet des le debut simplifie les decisions techniques et evite les ecarts de scope.

## Session 2 - Trame produit + User Story 1

### Objectif
Definir la trame (Spec, Architecture, User Stories) et verrouiller le filtrage metier des leads hors IT.

### Prompts significatifs notes
- "Aide-moi a structurer le backlog en user stories testables pour un MVP de 6h."
- "Comment appliquer un filtrage metier IT avant insertion en base ?"

### Ce que j'ai decide
- Prioriser la qualite metier avant la complexite technique.
- Filtrer hors IT avant persistance (et pas seulement via le score).

### Problemes rencontres -> solutions trouvees
- Probleme: des leads hors IT pouvaient encore entrer en base.
- Solution: ajout d'une validation dediee `evaluate_it_scope` avant `insert`.

### Ce que j'ai appris
Le filtrage metier doit se faire avant la persistance, sinon la base est polluee.

## Session 3 - User Story 2 (Import CSV robuste)

### Objectif
Rendre l'import CSV exploitable en conditions reelles (batch + reporting par ligne).

### Prompts significatifs notes
- "Aide-moi a fiabiliser l'import CSV sans bloquer tout le traitement sur une seule erreur."
- "Quel format de rapport d'import est le plus utile pour debug ?"

### Ce que j'ai decide
- Continuer le traitement ligne par ligne meme si une ligne echoue.
- Afficher trois etats clairs: `importe`, `ignore`, `erreur`.

### Problemes rencontres -> solutions trouvees
- Probleme: le total global ne permettait pas d'analyser les echecs.
- Solution: ajout d'un rapport detaille par ligne + compteur importes/ignores/erreurs.

### Ce que j'ai appris
Un import batch doit fournir un feedback precis, sinon il est difficile a maintenir.

## Session 4 - User Story 3 (Scoring explicite)

### Objectif
Rendre le scoring defendable: lisible, explicable, reproductible.

### Prompts significatifs notes
- "Aide-moi a rendre le score interpretable par un humain dans l'interface."
- "Comment verifier rapidement que le score est reproductible ?"

### Ce que j'ai decide
- Afficher la decomposition des raisons de score dans l'UI.
- Ajouter un recalcul de controle sur le lead selectionne.

### Problemes rencontres -> solutions trouvees
- Probleme: score present mais justification peu visible.
- Solution: section "Detail scoring" + verification coherence score stocke/recalcule.

### Ce que j'ai appris
Un score sans explication est difficile a justifier a l'evaluation.

## Session 5 - User Story 4 (Gestion des statuts)

### Objectif
Fiabiliser la mise a jour des statuts et eviter les actions ambiguës.

### Prompts significatifs notes
- "Aide-moi a securiser la mise a jour de statut dans l'UI."
- "Comment confirmer en base qu'une modification a vraiment eu lieu ?"

### Ce que j'ai decide
- Remplacer la saisie libre d'ID par une selection de leads existants.
- Retourner un booleen cote DB pour afficher succes/echec de facon fiable.

### Problemes rencontres -> solutions trouvees
- Probleme: saisie manuelle d'ID pas robuste.
- Solution: `selectbox` d'IDs existants + verification `rowcount` dans `update_status`.

### Ce que j'ai appris
Une operation CRUD doit toujours fournir un retour verifiable.

## Session 6 - User Story 5 (Email de premier contact)

### Objectif
Finaliser la fonctionnalite email avec une visualisation claire dans l'app.

### Prompts significatifs notes
- "Aide-moi a rendre la fonctionnalite email testable directement dans l'interface."
- "Quel comportement afficher si aucun email n'est disponible ?"

### Ce que j'ai decide
- Ajouter une section dediee "Email de premier contact".
- Prevoir un message explicite si l'email est absent.

### Problemes rencontres -> solutions trouvees
- Probleme: email stocke mais peu visible pour validation.
- Solution: previsualisation par lead dans l'UI.

### Ce que j'ai appris
Une fonctionnalite de generation doit etre observable facilement pour etre validable.

## Session 7 - Finalisation

### Objectif
Preparer un rendu lisible et executable (README, checks, coherence docs/code).

### Prompts significatifs notes
- "Aide-moi a transformer le README en guide d'execution pas-a-pas."
- "Peux-tu me proposer une checklist finale de verification avant rendu ?"

### Ce que j'ai decide
- Ajouter le scenario Docker PostgreSQL dans le README.
- Formaliser la checklist de tests limites dans un document dedie.

### Problemes rencontres -> solutions trouvees
- Probleme: README initial trop court pour une reprise autonome.
- Solution: enrichissement avec installation, lancement, parcours de demo et limites connues.

### Ce que j'ai appris
Un bon livrable combine code fonctionnel + documentation exploitable.
