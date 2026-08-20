import httpx

GUPY_JOBS_URL = "https://employability-portal.gupy.io/api/v1/jobs"


def buscar_vagas_gupy(client: httpx.Client, tipo: str, modalidade: str) -> list[dict]:
    resposta = client.get(
        GUPY_JOBS_URL,
        params={"type": tipo, "workplaceType": modalidade, "limit": 100, "offset": 0},
    )
    resposta.raise_for_status()
    return resposta.json()["data"]


def vaga_da_gupy(item: dict) -> dict:
    return {
        "fonte": "gupy",
        "id_da_fonte": str(item["id"]),
        "titulo": item["name"],
        "empresa": item["careerPageName"],
        "url": item["jobUrl"],
    }


def registrar_coleta_gupy(conn, coleta_id: int, itens_brutos: list[dict]) -> None:
    for item in itens_brutos:
        vaga = vaga_da_gupy(item)

        ja_existe = conn.execute(
            "SELECT 1 FROM vagas WHERE fonte = %s AND id_da_fonte = %s",
            (vaga["fonte"], vaga["id_da_fonte"]),
        ).fetchone()

        if not ja_existe:
            conn.execute(
                """
                INSERT INTO vagas (fonte, id_da_fonte, titulo, empresa, url, primeira_coleta_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    vaga["fonte"],
                    vaga["id_da_fonte"],
                    vaga["titulo"],
                    vaga["empresa"],
                    vaga["url"],
                    coleta_id,
                ),
            )

        conn.execute(
            """
            INSERT INTO vaga_aparicoes (coleta_id, fonte, id_da_fonte)
            VALUES (%s, %s, %s)
            """,
            (coleta_id, vaga["fonte"], vaga["id_da_fonte"]),
        )
