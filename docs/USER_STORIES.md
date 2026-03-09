# User Stories MVP

## Avancement
- US-01: Validee (code implemente)
- US-02: Validee (code implemente)
- US-03: Validee (code implemente)
- US-04: En cours
- US-05: En attente

## Backlog

### US-01 - Import texte avec filtrage IT
En tant qu'utilisateur, je veux importer un lead texte pour qu'il soit qualifie seulement s'il est dans le perimetre IT.

Critères d'acceptation:
- Si le texte est vide, aucun insert.
- Si le besoin est hors IT, le lead est refuse avec un message explicite.
- Si le lead est IT, il est enregistre en base.

### US-02 - Import CSV en batch
En tant qu'utilisateur, je veux importer un CSV de leads pour traiter plusieurs leads en une action.

Critères d'acceptation:
- Le systeme traite chaque ligne.
- Le resultat affiche nombre importes et nombre ignores (hors IT).
- Le systeme ne crash pas sur colonnes variables.

### US-03 - Scoring explicite
En tant qu'utilisateur, je veux un score avec justification pour comprendre pourquoi un lead est prioritaire.

Critères d'acceptation:
- Score entre 0 et 100.
- Justification textuelle presente.
- Meme entree -> meme score.

### US-04 - Gestion des statuts
En tant qu'utilisateur, je veux changer le statut d'un lead (`nouveau`, `contacte`, `qualifie`, `perdu`).

Critères d'acceptation:
- Le statut est modifiable depuis l'UI.
- Le changement persiste en base.

### US-05 - Email de premier contact
En tant qu'utilisateur, je veux generer un premier email base sur les donnees extraites.

Critères d'acceptation:
- Email en francais, court et professionnel.
- Pas d'invention d'informations absentes.
