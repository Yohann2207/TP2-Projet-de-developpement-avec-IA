from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import psycopg

from config import Settings


@dataclass(frozen=True)
class Lead:
    """Modele de donnees d'un lead tel qu'il est persiste en base."""

    raw_input: str
    source: str | None
    name: str | None
    company: str | None
    need: str | None
    budget: str | None
    timing: str | None
    score: int
    score_reason: str
    status: str
    first_contact_email: str | None


def get_conn(settings: Settings) -> psycopg.Connection:
    """Ouvre une connexion PostgreSQL en autocommit pour les operations courantes."""

    return psycopg.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        dbname=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
        autocommit=True,
    )


def init_db(settings: Settings) -> None:
    """Cree la table et les index si absents.

    Point important: cette fonction permet de demarrer l'app sans migration manuelle.
    """

    ddl = """
    CREATE TABLE IF NOT EXISTS leads (
        id BIGSERIAL PRIMARY KEY,
        raw_input TEXT NOT NULL,
        source TEXT,
        name TEXT,
        company TEXT,
        need TEXT,
        budget TEXT,
        timing TEXT,
        score INTEGER NOT NULL DEFAULT 0,
        score_reason TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'nouveau',
        first_contact_email TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
    CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score DESC);
    """
    with get_conn(settings) as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)


def insert_lead(settings: Settings, lead: Lead) -> int:
    """Insere un lead et retourne son identifiant technique."""

    sql = """
    INSERT INTO leads (
        raw_input, source, name, company, need, budget, timing,
        score, score_reason, status, first_contact_email
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    values = (
        lead.raw_input,
        lead.source,
        lead.name,
        lead.company,
        lead.need,
        lead.budget,
        lead.timing,
        lead.score,
        lead.score_reason,
        lead.status,
        lead.first_contact_email,
    )
    with get_conn(settings) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            row = cur.fetchone()
            return int(row[0])


def list_leads(settings: Settings) -> list[dict[str, Any]]:
    """Retourne les leads tries par priorite (score puis date)."""

    sql = """
    SELECT id, name, company, source, need, budget, timing, score, score_reason, status,
           first_contact_email, created_at
    FROM leads
    ORDER BY score DESC, created_at DESC;
    """
    with get_conn(settings) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(sql)
            return list(cur.fetchall())


def update_status(settings: Settings, lead_id: int, status: str) -> bool:
    """Met a jour le statut d'un lead.

    Retourne True si une ligne a ete modifiee, False sinon.
    """

    sql = """
    UPDATE leads
    SET status = %s, updated_at = NOW()
    WHERE id = %s;
    """
    with get_conn(settings) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (status, lead_id))
            return cur.rowcount > 0
