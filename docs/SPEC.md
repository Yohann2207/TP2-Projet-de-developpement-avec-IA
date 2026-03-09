# Spec - TP2 Projet 2 (Pipeline de qualification de leads)

## 1. Contexte
Le projet cible la qualification de leads pour une boite informatique (services numeriques/IT). Le but est de reduire le tri manuel des demandes entrantes et de prioriser les leads les plus pertinents.

## 2. Probleme
Les leads arrivent sous des formats heterogenes (texte, CSV). Sans pipeline commun:
- la qualification est lente;
- les priorites sont incoherentes;
- certains leads ne sont pas traites.

## 3. Objectif MVP
Construire une application qui:
- importe des leads (texte/CSV);
- extrait des informations structurees;
- score les leads avec des regles explicites;
- gere un statut de suivi;
- genere un email de premier contact;
- persiste en PostgreSQL.

## 4. Contraintes
- Base de donnees imposée: PostgreSQL.
- Contexte metier impose: leads IT uniquement.
- MVP d'abord (pas de version avancee).
- Application comprehensible et defendable a l'oral.

## 5. Donnees traitees
Champs principaux:
- `name`
- `company`
- `need`
- `budget`
- `timing`
- `source`
- `score`
- `score_reason`
- `status`
- `first_contact_email`

## 6. Hors scope
- Integrations CRM externes.
- Envoi automatique d'emails.
- Workflow de relance multi-etapes.
- Multi-utilisateur et gestion des roles.

## 7. Critères d'acceptation MVP
- Import texte et CSV sans crash.
- Donnees conservees apres redemarrage.
- Score reproductible pour un meme lead.
- Statut modifiable manuellement.
- Email genere sans invention d'informations.
- Leads hors IT detectes et signales.

## 8. Plan d'implementation
1. Spec et regles.
2. Architecture.
3. User stories priorisees.
4. Implementation story par story avec journalisation.
