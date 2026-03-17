from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from openai import OpenAI

from config import Settings


# Prompt d'extraction strict: sortie JSON uniquement, sans invention de donnees.
EXTRACTION_PROMPT = """
Tu extrais des informations de lead depuis un texte brut.
Le texte peut venir d'un message libre OU d'une ligne CSV transformee en paires "champ: valeur".
Contexte metier: entreprise de services informatiques (developpement logiciel, web, data/IA, cloud, maintenance, support IT).
Si le besoin n'est PAS informatique, ne le reformule pas en besoin IT.
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


def _call_mistral(settings: Settings, instruction: str, user_text: str, temperature: float) -> str:
    """Appelle l'API Mistral (REST chat completions) et retourne le texte genere."""

    endpoint = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": settings.mistral_model or "mistral-small-latest",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": user_text},
        ],
        "temperature": temperature,
    }
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.mistral_api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Mistral HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Mistral indisponible: {exc}") from exc

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("Mistral: aucune reponse choice.")

    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, list):
        # Compatibilite si le provider retourne des segments structures.
        text_parts = [x.get("text", "") for x in content if isinstance(x, dict)]
        content = "\n".join(x for x in text_parts if x)

    output = str(content).strip()
    if not output:
        raise RuntimeError("Mistral: reponse vide.")
    return output


def _call_gemini(settings: Settings, instruction: str, user_text: str, temperature: float) -> str:
    """Appelle l'API Gemini (REST) et retourne le texte genere."""

    model = settings.gemini_model or "gemini-2.0-flash"
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={urllib.parse.quote(settings.gemini_api_key)}"
    )

    # On fusionne instruction + input dans un seul prompt robuste.
    combined = f"{instruction}\n\nINPUT:\n{user_text}"
    payload = {
        "contents": [{"parts": [{"text": combined}]}],
        "generationConfig": {"temperature": temperature},
    }
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Gemini indisponible: {exc}") from exc

    candidates = data.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini: aucune reponse candidate.")

    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = [p.get("text", "") for p in parts if isinstance(p, dict)]
    output = "\n".join(x for x in text_parts if x).strip()
    if not output:
        raise RuntimeError("Gemini: reponse vide.")
    return output


def _normalize_extraction_payload(payload: Any) -> dict[str, Any]:
    """Normalise la sortie JSON du modele vers un dictionnaire.

    Certains modeles renvoient:
    - un objet JSON (cas attendu)
    - une liste contenant un objet (ex: [{...}])
    """

    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        return payload[0]
    raise ValueError(f"Format JSON non supporte pour extraction: {type(payload).__name__}")


def _parse_json_output(raw: str) -> dict[str, Any]:
    """Parse un JSON meme si le modele renvoie des fences markdown."""

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        parsed = json.loads(cleaned)
        return _normalize_extraction_payload(parsed)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            parsed = json.loads(cleaned[start : end + 1])
            return _normalize_extraction_payload(parsed)
        raise


def extract_lead(settings: Settings, raw_text: str) -> dict[str, Any]:
    """Extrait les champs metier d'un lead.

    Priorite provider:
    1) Mistral si MISTRAL_API_KEY est renseignee
    2) Gemini si GEMINI_API_KEY est renseignee
    3) OpenAI si OPENAI_API_KEY est renseignee
    4) Fallback local sinon
    """

    if not settings.mistral_api_key and not settings.gemini_api_key and not settings.openai_api_key:
        return {
            "name": None,
            "company": None,
            "need": raw_text[:200] if raw_text else None,
            "budget": None,
            "timing": None,
            "source": "texte",
        }

    # Priorite explicite: Mistral -> Gemini -> OpenAI.
    if settings.mistral_api_key:
        content = _call_mistral(settings, EXTRACTION_PROMPT, raw_text, temperature=0.0)
    elif settings.gemini_api_key:
        content = _call_gemini(settings, EXTRACTION_PROMPT, raw_text, temperature=0.0)
    else:
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

    data = _parse_json_output(content)

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

    if not settings.mistral_api_key and not settings.gemini_api_key and not settings.openai_api_key:
        company = extracted.get("company") or "votre entreprise"
        need = extracted.get("need") or "votre besoin"
        return (
            f"Bonjour,\n\n"
            f"Merci pour votre message concernant {need}. "
            f"Nous serions ravis d'echanger avec {company} pour vous proposer une approche adaptee. "
            f"Pouvez-vous partager vos disponibilites cette semaine ?\n\n"
            f"Cordialement"
        )

    payload = json.dumps(extracted, ensure_ascii=True)
    # Meme priorite provider pour garder un comportement coherent dans toute l'app.
    if settings.mistral_api_key:
        return _call_mistral(settings, EMAIL_PROMPT, payload, temperature=0.2)
    if settings.gemini_api_key:
        return _call_gemini(settings, EMAIL_PROMPT, payload, temperature=0.2)

    client = _client(settings)
    resp = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": EMAIL_PROMPT},
            {"role": "user", "content": payload},
        ],
        temperature=0.2,
    )
    return resp.output_text.strip()
