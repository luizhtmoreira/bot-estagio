import psycopg

from bot_estagio.migrate import aplicar_migracoes


def _inserir_coleta(conn, fonte: str) -> int:
    cursor = conn.execute(
        "INSERT INTO coletas (fonte) VALUES (%s) RETURNING id", (fonte,)
    )
    return cursor.fetchone()[0]


def _inserir_vaga(conn, coleta_id: int, fonte: str, id_da_fonte: str) -> None:
    conn.execute(
        """
        INSERT INTO vagas (fonte, id_da_fonte, titulo, primeira_coleta_id)
        VALUES (%s, %s, %s, %s)
        """,
        (fonte, id_da_fonte, f"vaga {id_da_fonte}", coleta_id),
    )


def _inserir_aparicao(conn, coleta_id: int, fonte: str, id_da_fonte: str) -> None:
    conn.execute(
        """
        INSERT INTO vaga_aparicoes (coleta_id, fonte, id_da_fonte)
        VALUES (%s, %s, %s)
        """,
        (coleta_id, fonte, id_da_fonte),
    )


def _ids_da_coleta(conn, coleta_id: int) -> set[str]:
    cursor = conn.execute(
        "SELECT id_da_fonte FROM vaga_aparicoes WHERE coleta_id = %s", (coleta_id,)
    )
    return {linha[0] for linha in cursor.fetchall()}


def test_aplicar_migracoes_e_idempotente(conn):
    conn.commit()
    executadas = aplicar_migracoes(conn)
    conn.commit()
    assert executadas == []


def test_vaga_tem_identidade_fonte_mais_id_da_fonte(conn):
    coleta_id = _inserir_coleta(conn, fonte="gupy")
    _inserir_vaga(conn, coleta_id, fonte="gupy", id_da_fonte="123")

    try:
        _inserir_vaga(conn, coleta_id, fonte="gupy", id_da_fonte="123")
        assert False, "deveria ter rejeitado (fonte, id_da_fonte) duplicado"
    except psycopg.errors.UniqueViolation:
        pass


def test_mesma_vaga_em_fontes_diferentes_nao_colide(conn):
    coleta_gupy = _inserir_coleta(conn, fonte="gupy")
    coleta_solides = _inserir_coleta(conn, fonte="solides")

    _inserir_vaga(conn, coleta_gupy, fonte="gupy", id_da_fonte="123")
    _inserir_vaga(conn, coleta_solides, fonte="solides", id_da_fonte="123")


def test_aparicao_exige_vaga_ja_registrada(conn):
    coleta_id = _inserir_coleta(conn, fonte="gupy")

    try:
        _inserir_aparicao(conn, coleta_id, "gupy", "inexistente")
        assert False, "deveria ter rejeitado aparição sem vaga correspondente"
    except psycopg.errors.ForeignKeyViolation:
        pass


def test_diff_entre_coletas_identifica_novidade_e_sumico(conn):
    coleta_1 = _inserir_coleta(conn, fonte="gupy")
    _inserir_vaga(conn, coleta_1, fonte="gupy", id_da_fonte="1")
    _inserir_vaga(conn, coleta_1, fonte="gupy", id_da_fonte="2")
    _inserir_aparicao(conn, coleta_1, "gupy", "1")
    _inserir_aparicao(conn, coleta_1, "gupy", "2")

    coleta_2 = _inserir_coleta(conn, fonte="gupy")
    _inserir_vaga(conn, coleta_2, fonte="gupy", id_da_fonte="3")
    _inserir_aparicao(conn, coleta_2, "gupy", "1")
    _inserir_aparicao(conn, coleta_2, "gupy", "3")

    ids_coleta_1 = _ids_da_coleta(conn, coleta_1)
    ids_coleta_2 = _ids_da_coleta(conn, coleta_2)

    assert ids_coleta_2 - ids_coleta_1 == {"3"}
    assert ids_coleta_1 - ids_coleta_2 == {"2"}
