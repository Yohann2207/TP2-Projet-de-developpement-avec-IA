from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from config import Settings


# Prompt d'extraction strict: sortie JSON uniquement, sans invention de donnees.
EXTRACTION_PROMPT = """
Tu extrais des informations de lead depuis un texte brut.
Contexte metier: entreprise de services informatiques (developpement logiciel, web, data/IA, cloud, maintenance, support IT).
Retourne UNIQUEMENT un JSON valide avec ces cles exactes:
name, company, need, budget, timing, source.
Si une information est absente, mets la valeur null.
N'invente aucune information.
""".strip()


# Prompt de generation d'email court et exploitable commercialement.
EMAIL_PROMPT = """
Tu rediges un email de premier contact professionnel en francais.
Contexte: nous sommes une entreprise de services informatiques.
Contraintes:
- Base-toi uniquement sur les donnees fournies.
- Si une info manque, ne l'invente pas.
- 120 mots max.
- Ton: clair, courtois, oriente action.
""".strip()


def _client(settings: Settings) -> OpenAI:
    """Construit un client OpenAI a partir de la configuration."""

    return OpenAI(api_key=settings.openai_api_key)


def extract_lead(settings: Settings, raw_text: str) -> dict[str, Any]:
    """Extrait les champs metier d'un lead.

    Sans cle API, on passe en mode fallback local pour garder l'application testable.
    """

    if not settings.openai_api_key:
        return {
            "name": None,
            "company": None,
            "need": raw_text[:200] if raw_text else None,
            "budget": None,
            "timing": None,
            "source": "texte",
        }

    client = _client(settings)
    resp = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        temperature=0,
    )
    content = resp.output_text.strip()
    data = json.loads(content)

    return {
        "name": data.get("name"),
        "company": data.get("company"),
        "need": data.get("need"),
        "budget": data.get("budget"),
        "timing": data.get("timing"),
        "source": data.get("source"),
    }


def generate_first_email(settings: Settings, extracted: dict[str, Any]) -> str:
    """Genere un email de premier contact.

    Sans cle API, utilise un template local.
    """

    if not settings.openai_api_key:
        company = extracted.get("company") or "votre entreprise"
        need = extracted.get("need") or "votre besoin"
        return (
            f"Bonjour,\n\n"
            f"Merci pour votre message concernant {need}. "
            f"Nous serions ravis d'echanger avec {company} pour vous proposer une approche adaptee. "
            f"Pouvez-vous partager vos disponibilites cette semaine ?\n\n"
            f"Cordialement"
        )

    client = _client(settings)
    resp = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": EMAIL_PROMPT},
            {"role": "user", "content": json.dumps(extracted, ensure_ascii=True)},
        ],
        temperature=0.2,
    )
    return resp.output_text.strip()
