from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Charge automatiquement les variables du fichier .env
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Configuration centralisee de l'application (API + PostgreSQL)."""

    mistral_api_key: str
    mistral_model: str
    gemini_api_key: str
    gemini_model: str
    openai_api_key: str
    openai_model: str
    pg_host: str
    pg_port: int
    pg_database: str
    pg_user: str
    pg_password: str


def load_settings() -> Settings:
    """Lit les variables d'environnement et retourne un objet Settings."""

    # Les cles API sont optionnelles: si elles sont vides, l'app passe en fallback local.
    return Settings(
        mistral_api_key=os.getenv("MISTRAL_API_KEY", ""),
        mistral_model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        pg_host=os.getenv("PGHOST", "localhost"),
        pg_port=int(os.getenv("PGPORT", "5432")),
        pg_database=os.getenv("PGDATABASE", "leads_db"),
        pg_user=os.getenv("PGUSER", "postgres"),
        pg_password=os.getenv("PGPASSWORD", "postgres"),
    )
