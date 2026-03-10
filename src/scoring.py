import re
from typing import Any


# Liste de mots-cles utilises pour verifier l'alignement avec le perimetre IT.
IT_KEYWORDS = [
    "site web",
    "application web",
    "application mobile",
    "logiciel",
    "saas",
    "api",
    "crm",
    "erp",
    "cloud",
    "devops",
    "data",
    "ia",
    "ai",
    "cyber",
    "infrastructure",
    "support informatique",
    "maintenance informatique",
]

NON_IT_KEYWORDS = [
    "traiteur",
    "mariage",
    "restauration",
    "menu",
    "photographe",
    "fleuriste",
    "coiffure",
    "esthetique",
    "voyage",
    "hotel",
    "immobilier",
]


def _contains_keyword(text: str, keyword: str) -> bool:
    """Detecte un mot-cle dans un texte avec une logique robuste.

    - Mot court (<=3): borne de mot pour eviter les faux positifs.
    - Mot long / expression: recherche simple en sous-chaine.
    """

    if len(keyword) <= 3:
        pattern = rf"\b{re.escape(keyword)}\b"
        return re.search(pattern, text) is not None
    return keyword in text


def evaluate_it_scope(extracted: dict[str, Any], raw_text: str = "") -> tuple[bool, str]:
    """Valide si le besoin du lead est dans le perimetre metier IT.

    Important: on combine les infos extraites + le texte brut pour reduire
    les faux positifs quand le modele reformule mal le besoin.
    """

    need = (extracted.get("need") or "").strip().lower()
    raw = (raw_text or "").strip().lower()

    raw_has_it = any(_contains_keyword(raw, keyword) for keyword in IT_KEYWORDS)
    raw_has_non_it = any(_contains_keyword(raw, keyword) for keyword in NON_IT_KEYWORDS)

    # Regle anti faux-positif: si le texte brut contient des indices non IT
    # et aucun signal IT, on bloque directement.
    if raw_has_non_it and not raw_has_it:
        return False, "Lead ignore: besoin hors perimetre IT (detecte dans le texte brut)."

    if not need:
        return False, "Lead ignore: besoin absent (impossible de verifier le perimetre IT)."
    if any(_contains_keyword(need, keyword) for keyword in IT_KEYWORDS):
        return True, "Lead IT detecte."
    return False, "Lead ignore: besoin hors perimetre IT."


def score_lead(extracted: dict[str, Any]) -> tuple[int, str]:
    """Calcule un score de priorite (0-100) avec justification textuelle."""

    score = 0
    reasons: list[str] = []

    budget = (extracted.get("budget") or "").lower()
    timing = (extracted.get("timing") or "").lower()
    need = (extracted.get("need") or "").strip()
    need_lower = need.lower()

    # 1) Qualite de formulation du besoin.
    if need:
        score += 25
        reasons.append("besoin explicite (+25)")
    else:
        reasons.append("besoin non precise (+0)")

    # 2) Adequation metier (IT).
    if need and any(_contains_keyword(need_lower, keyword) for keyword in IT_KEYWORDS):
        score += 15
        reasons.append("besoin aligne services IT (+15)")
    elif need:
        score -= 10
        reasons.append("besoin hors cible IT (-10)")
    else:
        reasons.append("alignement IT non evaluable (+0)")

    # 3) Maturite budget.
    if any(x in budget for x in ["k", "euro", "$", "budget", "1000", "5000", "10000"]):
        score += 35
        reasons.append("budget identifie (+35)")
    elif budget:
        score += 15
        reasons.append("budget partiel (+15)")
    else:
        reasons.append("budget absent (+0)")

    # 4) Urgence / fenetre de decision.
    if any(x in timing for x in ["urgent", "semaine", "mois", "q1", "q2", "q3", "q4"]):
        score += 25
        reasons.append("timing defini (+25)")
    elif timing:
        score += 10
        reasons.append("timing partiel (+10)")
    else:
        reasons.append("timing absent (+0)")

    # 5) Identification de l'entreprise.
    if extracted.get("company"):
        score += 15
        reasons.append("entreprise identifiee (+15)")
    else:
        reasons.append("entreprise absente (+0)")

    # Borne de securite pour rester dans l'intervalle attendu.
    score = max(0, min(score, 100))
    return score, " | ".join(reasons)
