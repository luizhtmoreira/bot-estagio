import httpx

from bot_estagio.gupy import buscar_vagas_gupy, registrar_coleta_gupy, vaga_da_gupy


def _inserir_coleta(conn, fonte: str) -> int:
    cursor = conn.execute(
        "INSERT INTO coletas (fonte) VALUES (%s) RETURNING id", (fonte,)
    )
    return cursor.fetchone()[0]


def test_registrar_coleta_gupy_grava_vaga_nova_e_aparicao(conn):
    coleta_id = _inserir_coleta(conn, fonte="gupy")
    itens_brutos = [
        {
            "id": 999,
            "name": "Estágio em Dados",
            "careerPageName": "Empresa X",
            "jobUrl": "https://empresa-x.gupy.io/job/999",
        }
    ]

    registrar_coleta_gupy(conn, coleta_id, itens_brutos)

    vaga = conn.execute(
        "SELECT titulo, empresa, url, primeira_coleta_id FROM vagas WHERE fonte = %s AND id_da_fonte = %s",
        ("gupy", "999"),
    ).fetchone()
    assert vaga == ("Estágio em Dados", "Empresa X", "https://empresa-x.gupy.io/job/999", coleta_id)

    aparicao = conn.execute(
        "SELECT 1 FROM vaga_aparicoes WHERE coleta_id = %s AND fonte = %s AND id_da_fonte = %s",
        (coleta_id, "gupy", "999"),
    ).fetchone()
    assert aparicao is not None


def test_buscar_vagas_gupy_devolve_lista_de_vagas_brutas():
    resposta_fake = {
        "data": [
            {"id": 1, "name": "Estágio em TI"},
            {"id": 2, "name": "Desenvolvedor Júnior"},
        ],
        "pagination": {"total": 2, "limit": 100, "offset": 0},
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["type"] == "vacancy_type_internship"
        assert request.url.params["workplaceType"] == "remote"
        return httpx.Response(200, json=resposta_fake)

    client = httpx.Client(transport=httpx.MockTransport(handler))

    vagas = buscar_vagas_gupy(
        client, tipo="vacancy_type_internship", modalidade="remote"
    )

    assert vagas == resposta_fake["data"]


def test_vaga_da_gupy_extrai_campos_do_schema():
    item_gupy = {
        "id": 12024455,
        "name": "Estágio em desenvolvimento Web",
        "careerPageName": "Instituto de Pesquisas ELDORADO",
        "jobUrl": "https://institutoeldorado.gupy.io/job/abc123?jobBoardSource=gupy_portal",
        "type": "vacancy_type_internship",
        "publishedDate": "2026-08-14T17:45:12.862Z",
    }

    vaga = vaga_da_gupy(item_gupy)

    assert vaga == {
        "fonte": "gupy",
        "id_da_fonte": "12024455",
        "titulo": "Estágio em desenvolvimento Web",
        "empresa": "Instituto de Pesquisas ELDORADO",
        "url": "https://institutoeldorado.gupy.io/job/abc123?jobBoardSource=gupy_portal",
    }