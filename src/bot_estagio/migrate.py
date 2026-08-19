import os
import sys
from pathlib import Path

import psycopg

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / "db" / "migrations"


def aplicar_migracoes(conn: psycopg.Connection) -> list[str]:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            nome TEXT PRIMARY KEY,
            aplicada_em TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    aplicadas = {linha[0] for linha in conn.execute("SELECT nome FROM schema_migrations")}

    executadas = []
    for arquivo in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if arquivo.name in aplicadas:
            continue
        conn.execute(arquivo.read_text())
        conn.execute("INSERT INTO schema_migrations (nome) VALUES (%s)", (arquivo.name,))
        executadas.append(arquivo.name)

    conn.commit()
    return executadas


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL não definida", file=sys.stderr)
        sys.exit(1)

    with psycopg.connect(database_url) as conn:
        executadas = aplicar_migracoes(conn)

    if executadas:
        print("Migrações aplicadas:", ", ".join(executadas))
    else:
        print("Nada a aplicar.")


if __name__ == "__main__":
    main()
