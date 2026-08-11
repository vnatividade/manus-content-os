# CHECK-DIA-0 — antes de qualquer conteúdo

## 0. O conector existe? (decide a arquitetura inteira)

Abra o Manus → aba **Connectors** → confirme que **Instagram aparece** na lista.
O rollout é escalonado: pode não estar disponível na sua conta.

> **STATUS 09/08/2026:** conector presente e já conectado à conta `@vidavesso` (feito pelo Vitor). A checagem abaixo permanece como referência para reexecução futura.

- **Aparece** → siga o checklist abaixo. (Ainda NÃO autorize o OAuth — só na hora de rodar o Gate 0.)
- **NÃO aparece** → a arquitetura A2 cai. Pare aqui e migre para arquitetura própria (critério STOP do `PLANO-POC.md`). Nada abaixo se aplica.

## 1. Pré-requisitos da conta

- [x] Conta definida e conectada: `@vidavesso`.
- [x] A conta é profissional: **creator** (confirmado pelo Vitor em 09/08/2026) — atende a exigência da Meta (business OU creator).
- [ ] A conta tem ≥100 seguidores (abaixo disso a API não devolve nem o dado de follower, que é de conta).
- [ ] Conector **Google Sheets** disponível no Manus (é onde o ledger vive).

## 2. Montar o Project

- [ ] Criar o Manus Project e colar `project/PROJECT-INSTRUCTION.md` como instrução mestra.
- [ ] Subir na knowledge base: `VOZ.md`, `PILARES.md`, `FORMATOS.md`, `REGRAS-DURAS.md`, `PADROES.md` (lembrando: atualização de arquivo só vale em task NOVA — não há write-back).
- [ ] Importar as 5 skills de `skills/` — repo: `https://github.com/vnatividade/manus-content-os` (privado; se o import do Manus exigir acesso, autorize você mesmo — OAuth é gate) — ou colando o conteúdo manualmente.
- [ ] Criar a planilha do ledger com as 6 abas de `ledger/SCHEMA.md` (cabeçalhos exatos de `ledger/csv/`).

## 3. Gate 0 em camadas — funcionamento em horas, qualidade em 72h

Combinado de 10/08/2026: **validação de funcionamento nunca espera janela de dado.**
Defeito de fluxo (formato errado, conector mudo, métrica inventada) tem que aparecer no
mesmo dia; a janela de 72h só responde se o NÚMERO é estável — não se o sistema funciona.

### Teste A — funcionamento (mesmo dia, em horas)

1. **Smoke do pipeline no Manus (~1h, sem publicar):** rode 1 task de cada skill em
   sequência com um insumo real — score-editorial → brief manual → gerar-carrossel →
   anti-generico → fact-check. Confira se cada saída vem no formato exato da skill.
   Saída fora do formato = defeito de fluxo, corrigir antes de seguir.
2. Publique **3 peças manualmente** (você, no app — sem Manus).
3. **H+3 (mesmo dia):** peça ao Manus as métricas das 3 peças, exporte para `manus.csv`
   (`id_peca,metrica,valor`), leia as mesmas no app para `app.csv` e rode:

   python3 scripts/gate0_diff.py --manus manus.csv --app app.csv

   Números pequenos não importam aqui. O que o Teste A prova: conector lê a conta certa,
   devolve SÓ as seis métricas, o formato exporta, e o script fecha ponta a ponta.
   **Métrica fora das seis já reprova aqui** — não precisa esperar 72h para saber isso.

### Teste B — qualidade do dado (D+3, teto do combinado)

4. Em 72h, repita a coleta dupla (`manus.csv` × `app.csv`, janela `72h`) e rode o
   `gate0_diff.py` de novo. ESTE resultado decide se o ledger confia no conector.

## 4. Leitura do resultado (Teste B)

- **APROVADO (batem)** → o ledger pode confiar no conector. Siga o `PLANO-POC.md`.
- **REPROVADO por divergência** → coleta manual durante TODA a POC; o conector vira só publicador.
- **REPROVADO por métrica fora das seis** → o Manus está inventando dado (pior cenário, §3.6 do handoff). Reforce a trava anti-fabricação na instrução mestra e reteste antes de seguir.
