# Architecture MVP

## Vue d'ensemble
- UI: Streamlit (`src/app.py`)
- Logique metier:
  - Extraction + generation email (`src/llm_service.py`)
  - Scoring + filtrage IT (`src/scoring.py`)
- Persistance PostgreSQL (`src/db.py`)
- Configuration (`src/config.py`)

## Flux principal
1. L'utilisateur soumet un lead texte ou un CSV.
2. Le service IA extrait les champs.
3. Le moteur metier valide la pertinence IT.
4. Le lead est score et (si pertinent) enregistre en base.
5. L'UI affiche la liste et permet la mise a jour de statut.

## Base PostgreSQL
Table `leads`:
- identifiants et metadonnees (`id`, `created_at`, `updated_at`)
- donnees lead (`name`, `company`, `need`, `budget`, `timing`, `source`)
- qualification (`score`, `score_reason`, `status`)
- sortie IA (`first_contact_email`)

## Decisions architecturales
- Structure simple monorepo pour faciliter la comprehension.
- SQL direct avec `psycopg` pour limiter la complexite.
