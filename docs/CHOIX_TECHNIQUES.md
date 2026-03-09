# Documentation des choix techniques

## Choix principaux
- Langage: Python (lisible et rapide pour MVP).
- Interface: Streamlit (developpement rapide).
- Base de donnees: PostgreSQL.
- IA: En réflexion

## Pourquoi PostgreSQL
- Contrainte explicite du document de cadrage.
- Persistance fiable et requetes SQL simples pour tri/statuts.

## Architecture MVP
- `src/app.py`: interface et orchestration.
- `src/db.py`: schema + CRUD leads PostgreSQL.
- `src/llm_service.py`: extraction et email.
- `src/scoring.py`: regles de scoring explicites.
- `src/config.py`: chargement des variables d'environnement.

## Scope assume
- MVP uniquement.
- Pas d'integration CRM.
- Pas d'envoi automatique d'email.
- Pas de workflow avance multi-relances.
