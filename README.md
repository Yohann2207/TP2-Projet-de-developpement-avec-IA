# TP2 - Projet 2 : Pipeline de qualification de leads (MVP)

## Objectif
MVP qui importe des leads, extrait les informations cles avec IA, calcule un score, gere les statuts de suivi et propose un email de premier contact personnalise.

## Stack
- Python
- Streamlit
- PostgreSQL
- Mistral API, Gemini API ou OpenAI API

## Fonctionnalites MVP
- Import CSV et texte brut
- Extraction structuree: `name`, `company`, `need`, `budget`, `timing`, `source`
- Scoring explicite et reproductible
- Statuts: `nouveau`, `contacte`, `qualifie`, `perdu`
- Generation d'email de premier contact
- Persistance PostgreSQL
- Filtrage metier: seuls les leads IT sont qualifies (les autres sont ignores avec raison)
- Rapport CSV detaille (importe / ignore / erreur par ligne)

## Installation
1. Creer un environnement virtuel Python.
2. Installer les dependances:
   - `pip install -r requirements.txt`
3. Copier `.env.example` vers `.env` puis completer les variables.
4. Verifier PostgreSQL (base `leads_db` accessible).

### Option recommandee (PostgreSQL avec Docker)
Exemple si ton conteneur mappe `5430:5432`:
- `PGHOST=localhost`
- `PGPORT=5430`
- `PGDATABASE=leads_db`
- `PGUSER=postgres`
- `PGPASSWORD=postgres`

## Lancement
Depuis le dossier projet:
- `streamlit run src/app.py`

## Parcours utilisateur (demo)
1. Importer un lead texte ou un CSV.
2. Verifier le resultat d'import (importes/ignores/erreurs).
3. Ouvrir la section **Detail scoring** pour voir la justification et le controle de reproductibilite.
4. Ouvrir la section **Email de premier contact** pour visualiser le message genere.
5. Modifier le statut d'un lead depuis la section **Mise a jour statut**.

## Variables d'environnement
- `MISTRAL_API_KEY`
- `MISTRAL_MODEL`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

## Priorite des providers IA
1. `MISTRAL_API_KEY` (si renseignee)
2. `GEMINI_API_KEY` (si Mistral absente)
3. `OPENAI_API_KEY` (si Gemini absente)
4. Fallback local (si aucune cle)

## Documentation projet
- Regles: `docs/PROJECT_RULES.md`
- Spec: `docs/SPEC.md`
- Architecture: `docs/ARCHITECTURE.md`
- Choix techniques: `docs/CHOIX_TECHNIQUES.md`
- User stories: `docs/USER_STORIES.md`
- Tests cas limites: `docs/TESTS_CAS_LIMITES.md`
- Journal: `JOURNAL.md`

## Limitations connues (MVP)
- Pas d'integration CRM.
- Pas d'envoi automatique d'email.
- Pas de relance multi-etapes.
- Pas de gestion multi-utilisateur.
