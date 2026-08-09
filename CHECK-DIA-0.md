# CHECK-DIA-0 — antes de qualquer conteúdo

## 0. O conector existe? (decide a arquitetura inteira)

Abra o Manus → aba **Connectors** → confirme que **Instagram aparece** na lista.
O rollout é escalonado: pode não estar disponível na sua conta.

> **STATUS 09/08/2026:** conector presente e já conectado à conta `@vidavesso` (feito pelo Vitor). A checagem abaixo permanece como referência para reexecução futura.

- **Aparece** → siga o checklist abaixo. (Ainda NÃO autorize o OAuth — só na hora de rodar o Gate 0.)
- **NÃO aparece** → a arquitetura A2 cai. Pare aqui e migre para arquitetura própria (critério STOP do `PLANO-POC.md`). Nada abaixo se aplica.

## 1. Pré-requisitos da conta

- [x] Conta definida e conectada: `@vidavesso`.
- [ ] A conta é profissional (**business OU creator**) — exigência confirmada pela Meta. <!-- TODO-VITOR: confirmar o tipo (business ou creator) da @vidavesso -->
- [ ] A conta tem ≥100 seguidores (abaixo disso a API não devolve nem o dado de follower, que é de conta).
- [ ] Conector **Google Sheets** disponível no Manus (é onde o ledger vive).

## 2. Montar o Project

- [ ] Criar o Manus Project e colar `project/PROJECT-INSTRUCTION.md` como instrução mestra.
- [ ] Subir na knowledge base: `VOZ.md`, `PILARES.md`, `FORMATOS.md`, `REGRAS-DURAS.md`, `PADROES.md` (lembrando: atualização de arquivo só vale em task NOVA — não há write-back).
- [ ] Importar as 5 skills de `skills/` — repo: `https://github.com/vnatividade/manus-content-os` (privado; se o import do Manus exigir acesso, autorize você mesmo — OAuth é gate) — ou colando o conteúdo manualmente.
- [ ] Criar a planilha do ledger com as 6 abas de `ledger/SCHEMA.md` (cabeçalhos exatos de `ledger/csv/`).

## 3. Gate 0 — o conector fala a verdade? (protocolo)

Antes de qualquer peça gerada pelo sistema:

1. Publique **3 peças manualmente** (você, no app — sem Manus).
2. Espere **72h**.
3. Peça ao Manus (via conector) as métricas das 3 peças e exporte para `manus.csv`, no formato `id_peca,metrica,valor`.
4. Leia as MESMAS métricas **no app do Instagram** e anote em `app.csv` (mesmo formato).
5. Rode:

   python3 scripts/gate0_diff.py --manus manus.csv --app app.csv

## 4. Leitura do resultado

- **APROVADO (batem)** → o ledger pode confiar no conector. Siga o `PLANO-POC.md`.
- **REPROVADO por divergência** → coleta manual durante TODA a POC; o conector vira só publicador.
- **REPROVADO por métrica fora das seis** → o Manus está inventando dado (pior cenário, §3.6 do handoff). Reforce a trava anti-fabricação na instrução mestra e reteste antes de seguir.
