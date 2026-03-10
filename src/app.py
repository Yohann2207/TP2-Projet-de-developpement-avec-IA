from __future__ import annotations

import io
from typing import Any

import pandas as pd
import streamlit as st

from config import load_settings
from db import Lead, init_db, insert_lead, list_leads, update_status
from llm_service import extract_lead, generate_first_email
from scoring import evaluate_it_scope, score_lead

# Ensemble des statuts autorises dans le pipeline.
VALID_STATUSES = ["nouveau", "contacte", "qualifie", "perdu"]


def _ingest_text(settings, raw_text: str) -> tuple[int | None, str]:
    """Traite un lead texte de bout en bout.

    Etapes:
    1) extraction structuree;
    2) validation perimetre IT;
    3) scoring + email;
    4) insertion en base.
    """

    extracted = extract_lead(settings, raw_text)
    # Le filtre combine extraction + texte brut pour eviter les faux positifs LLM.
    is_it, scope_reason = evaluate_it_scope(extracted, raw_text)
    if not is_it:
        return None, scope_reason

    score, reason = score_lead(extracted)
    email = generate_first_email(settings, extracted)

    lead = Lead(
        raw_input=raw_text,
        source=extracted.get("source"),
        name=extracted.get("name"),
        company=extracted.get("company"),
        need=extracted.get("need"),
        budget=extracted.get("budget"),
        timing=extracted.get("timing"),
        score=score,
        score_reason=reason,
        status="nouveau",
        first_contact_email=email,
    )
    lead_id = insert_lead(settings, lead)
    return lead_id, scope_reason


def _row_to_raw_text(row: pd.Series, columns: list[str]) -> str:
    """Transforme une ligne CSV en texte brut interpretable par l'extracteur."""

    parts = []
    for col in columns:
        value = row.get(col)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            parts.append(f"{col}: {text}")
    return " | ".join(parts)


def _ingest_csv(settings, data: bytes) -> tuple[int, int, int, list[dict[str, Any]]]:
    """Importe un CSV et retourne un bilan complet.

    Retour:
    - nb importes
    - nb ignores (hors IT)
    - nb erreurs
    - rapport detaille par ligne
    """

    df = pd.read_csv(io.BytesIO(data), dtype=str, keep_default_na=False)
    if df.empty:
        raise ValueError("Le CSV est vide.")

    inserted = 0
    skipped = 0
    errors = 0
    report: list[dict[str, Any]] = []

    columns = list(df.columns)
    for idx, row in df.iterrows():
        # +2 car l'index commence a 0 et la ligne 1 est l'entete CSV.
        line_no = int(idx) + 2
        raw_text = _row_to_raw_text(row, columns)

        if not raw_text:
            errors += 1
            report.append(
                {
                    "ligne": line_no,
                    "resultat": "erreur",
                    "detail": "Ligne vide ou sans colonnes exploitables.",
                    "lead_id": None,
                }
            )
            continue

        try:
            lead_id, reason = _ingest_text(settings, raw_text)
        except Exception as exc:
            # Une ligne en erreur ne bloque pas le reste de l'import batch.
            errors += 1
            report.append(
                {
                    "ligne": line_no,
                    "resultat": "erreur",
                    "detail": str(exc),
                    "lead_id": None,
                }
            )
            continue

        if lead_id is None:
            skipped += 1
            report.append(
                {
                    "ligne": line_no,
                    "resultat": "ignore",
                    "detail": reason,
                    "lead_id": None,
                }
            )
        else:
            inserted += 1
            report.append(
                {
                    "ligne": line_no,
                    "resultat": "importe",
                    "detail": reason,
                    "lead_id": lead_id,
                }
            )

    return inserted, skipped, errors, report


def main() -> None:
    """Point d'entree Streamlit."""

    st.set_page_config(page_title="Lead Qualifier MVP", layout="wide")
    st.title("Pipeline de qualification de leads - MVP")

    settings = load_settings()

    # Verification immediate de la connectivite DB pour eviter les erreurs diffuses.
    try:
        init_db(settings)
    except Exception as exc:
        st.error(f"Erreur PostgreSQL: {exc}")
        st.stop()

    st.subheader("Import")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Texte brut**")
        raw_text = st.text_area("Lead texte", height=180)
        if st.button("Importer texte", use_container_width=True):
            if not raw_text.strip():
                st.warning("Le texte est vide.")
            else:
                lead_id, reason = _ingest_text(settings, raw_text)
                if lead_id is None:
                    st.warning(reason)
                else:
                    st.success(f"Lead importe (id={lead_id}). {reason}")

    with col2:
        st.markdown("**CSV**")
        csv_file = st.file_uploader("Fichier CSV", type=["csv"])
        if st.button("Importer CSV", use_container_width=True):
            if csv_file is None:
                st.warning("Aucun fichier CSV selectionne.")
            else:
                try:
                    inserted, skipped, errors, report = _ingest_csv(settings, csv_file.getvalue())
                    st.success(f"{inserted} leads importes.")
                    if skipped:
                        st.warning(f"{skipped} leads ignores (hors perimetre IT).")
                    if errors:
                        st.error(f"{errors} lignes en erreur.")
                    if report:
                        with st.expander("Rapport d'import CSV", expanded=False):
                            st.dataframe(pd.DataFrame(report), use_container_width=True)
                except Exception as exc:
                    st.error(f"Import CSV invalide: {exc}")

    st.subheader("Leads")
    rows = list_leads(settings)
    if not rows:
        st.info("Aucun lead pour le moment.")
        return

    df = pd.DataFrame(rows)
    st.dataframe(df[["id", "name", "company", "source", "score", "status", "created_at"]], use_container_width=True)

    st.subheader("Detail scoring")
    selected_id = st.selectbox("Selectionner un lead", df["id"].tolist())
    selected_row = df.loc[df["id"] == selected_id].iloc[0]
    details = [x.strip() for x in str(selected_row["score_reason"]).split("|") if x.strip()]

    st.markdown(f"**Score enregistre:** {int(selected_row['score'])}/100")
    st.markdown("**Justification:**")
    for detail in details:
        st.write(f"- {detail}")

    # Controle de coherence: le score recalcule doit rester identique au score stocke.
    recalculated_score, recalculated_reason = score_lead(
        {
            "need": selected_row.get("need"),
            "budget": selected_row.get("budget"),
            "timing": selected_row.get("timing"),
            "company": selected_row.get("company"),
        }
    )
    is_same = int(selected_row["score"]) == recalculated_score
    if is_same:
        st.success("Verification reproductibilite: OK (meme entree -> meme score).")
    else:
        st.error("Verification reproductibilite: ECHEC (score recalcule different).")
        st.caption(f"Details recalcules: {recalculated_reason}")

    st.subheader("Email de premier contact")
    email_lead_id = st.selectbox("Lead ID (email)", df["id"].tolist(), key="email_lead_id")
    email_row = df.loc[df["id"] == email_lead_id].iloc[0]
    email_text = (email_row.get("first_contact_email") or "").strip()
    if not email_text:
        st.warning("Aucun email disponible pour ce lead.")
    else:
        st.text_area(
            "Email genere",
            value=email_text,
            height=180,
            key=f"email_preview_{email_lead_id}",
        )

    st.subheader("Mise a jour statut")
    update_col1, update_col2 = st.columns(2)
    with update_col1:
        status_lead_id = st.selectbox("Lead ID", df["id"].tolist(), key="status_lead_id")
    with update_col2:
        new_status = st.selectbox("Nouveau statut", VALID_STATUSES)

    current_status = df.loc[df["id"] == status_lead_id, "status"].iloc[0]
    st.caption(f"Statut actuel du lead {status_lead_id}: {current_status}")

    if st.button("Mettre a jour le statut"):
        updated = update_status(settings, int(status_lead_id), new_status)
        if updated:
            st.success("Statut mis a jour.")
        else:
            st.error("Mise a jour impossible: lead introuvable.")


if __name__ == "__main__":
    main()
