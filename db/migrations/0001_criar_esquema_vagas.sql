-- Coleta: uma execução do processo que busca vagas ativas numa fonte (CONTEXT.md).
CREATE TABLE coletas (
    id BIGSERIAL PRIMARY KEY,
    fonte TEXT NOT NULL,
    executada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Vaga: identidade é só (fonte, id_da_fonte) — CONTEXT.md. Guarda o estado mais
-- recente conhecido; primeira_coleta_id é a coleta em que a vaga apareceu pela
-- primeira vez, usada para decidir "novidade".
CREATE TABLE vagas (
    fonte TEXT NOT NULL,
    id_da_fonte TEXT NOT NULL,
    titulo TEXT NOT NULL,
    empresa TEXT,
    url TEXT,
    primeira_coleta_id BIGINT NOT NULL REFERENCES coletas (id),
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (fonte, id_da_fonte)
);

-- Aparição: a vaga estava presente no snapshot dessa coleta. Histórico
-- completo (não só "última vista"), necessário para detectar sumiço
-- (presente numa coleta, ausente na seguinte) — CONTEXT.md.
CREATE TABLE vaga_aparicoes (
    coleta_id BIGINT NOT NULL REFERENCES coletas (id),
    fonte TEXT NOT NULL,
    id_da_fonte TEXT NOT NULL,
    PRIMARY KEY (coleta_id, fonte, id_da_fonte),
    FOREIGN KEY (fonte, id_da_fonte) REFERENCES vagas (fonte, id_da_fonte)
);

CREATE INDEX idx_vaga_aparicoes_vaga ON vaga_aparicoes (fonte, id_da_fonte);
