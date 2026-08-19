import os

import psycopg
import pytest

from bot_estagio.migrate import aplicar_migracoes

TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]


@pytest.fixture(scope="session", autouse=True)
def _esquema_migrado():
    with psycopg.connect(TEST_DATABASE_URL) as conexao_setup:
        aplicar_migracoes(conexao_setup)


@pytest.fixture
def conn():
    conexao = psycopg.connect(TEST_DATABASE_URL)
    try:
        yield conexao
    finally:
        conexao.rollback()
        conexao.close()
