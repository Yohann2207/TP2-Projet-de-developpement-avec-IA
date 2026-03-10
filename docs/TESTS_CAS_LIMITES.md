# Tests des cas limites (MVP)

## Campagne de verification
- Verification syntaxe Python (`py_compile`) sur `app`, `db`, `scoring`, `llm_service`, `config`: OK.
- Verification fonctionnelle runtime Streamlit + PostgreSQL: a executer localement (environnement utilisateur).

## Import texte
- Texte vide -> message d'avertissement, pas d'insertion.
- Texte tres court -> insertion possible avec champs manquants a null.
- Texte ambigu -> score calculable sans crash.

## Import CSV
- Fichier non CSV -> erreur explicite.
- CSV vide -> erreur explicite.
- CSV avec colonnes variables -> ingestion ligne par ligne.
- Rapport d'import detaille par ligne (importe/ignore/erreur).
- Lignes vides -> comptees en erreur, pas d'insertion.
- Le total importes + ignores + erreurs correspond au nombre de lignes du CSV.

## Extraction/Generation
- Sans `OPENAI_API_KEY` -> mode fallback local (pas de crash).
- Champs absents -> valeurs null, aucune invention.
- Email de premier contact visible dans l'UI pour un lead importe.
- Si email absent en base -> avertissement explicite dans l'UI.

## Base PostgreSQL
- Base indisponible -> erreur claire dans l'UI.
- Redemarrage app -> donnees conservees.
- Mise a jour statut -> valeur en base modifiee.
- Mise a jour statut sur ID valide -> message succes.
- Mise a jour statut sur ID invalide -> message d'erreur.

## Verification scoring
- Meme lead input -> meme score (reproductible).
- Champs budget/timing manquants -> score plus faible attendu.
- La justification (`score_reason`) est affichee et lisible dans l'UI.
- Recalcul du score depuis les champs du lead = score enregistre (controle de coherence).
