# PONTE-AURASITE — mapa de convergência pós-POC

**Status: mapa, não plano aprovado.** A decisão é do Vitor e só se abre ao fim da POC,
condicionada ao GO/ADJUST/STOP do `PLANO-POC.md`. Regra standing: **não tocar no motor de
geração do AuraSite sem pesquisa/alinhamento prévios** — este arquivo é só documentação.
Referências abaixo apontam para o código real em `~/Developer/aurasite` (verificadas em
09/08/2026).

## O que o motor v3 do AuraSite realmente tem (resumo verificado)

Pipeline de 7 estágios + gates, orquestrado em `server/engineV3/pipeline.ts` (definição
canônica em `docs/site-engine-v3/architecture/02-target-pipeline.md`):

| Estágio | Arquivo | O que faz |
|---|---|---|
| S0 Intake | `server/shadowGeneration.ts:48` | monta briefing (corpus + entrevista + fotos) |
| S1 Classificação | `server/engineV3/classify.ts` | o que o projeto É (+ `confidence`, `openQuestions`) |
| S2 Estratégia | `server/engineV3/strategy.ts` | o que dizer/provar (plano de seções, narrativa) |
| S3 Direção criativa + gate de conceito | `server/engineV3/direction.ts`, `conceptGate.ts` | 2–3 direções de bancos nomeados; gate determinístico + juiz LLM |
| S4 Composição | `server/engineV3/compose.ts` | materializa; valida schema→auditoria→regras |
| S5 Render | `worker-local/render_harness.ts:129` | Playwright: screenshots + probe de DOM |
| S6 Crítica visual | `server/engineV3/critique.ts` | LLM com visão, 8 dimensões 0–5 |
| S7 Refino | `server/engineV3/refine.ts` | 1 rodada nos 3 maiores achados |

Infra ao redor: fila em MySQL (`atelier_shadow_jobs`, `drizzle/schema.ts:459-510`) com
worker local via claim/result (`server/shadowRoutes.ts:65,140`); **decision log** por
estágio (`shared/engineV3/decisionLog.ts`); **memória anti-repetição** por Jaccard sobre
os últimos 10 runs (`server/engineV3/memory.ts`, ADR-004); gates em 3 camadas
(`shared/engineV3/rules/artifactRules.ts`, DOM probes, crítica visual); retomada por
estágio com custo zero (`pipeline.ts:46-52`); orçamento e modelo por estágio via env
(`server/engineV3/config.ts:51-64`); LLM via `claude -p` headless
(`server/atelierHeadless.ts`).

## Cenário C — captura (vale JÁ, independente de GO/STOP)

É o pedido explícito do Vitor: "usar parte do motor do Aura para conseguir capturar isso".
O AuraSite já tem exatamente o mecanismo de captura que o Content OS não tem:

- **Ingestão de Instagram** (`server/ingestion.ts:10-15`): descrição visual por vision +
  **transcrição de áudio dos vídeos** (Whisper, `server/transcriptionFallback.ts:199`,
  fila `awaiting_transcriptions`).
- **Corpus curado com seleção gulosa** (`server/corpus.ts:58-109`): transcript de fala
  real pesa +0,35 no score ("fala real do profissional = sinal forte") — o mesmo
  princípio do nosso `insumo_bruto` real.
- **Entrevista sob medida gerada do corpus** (`server/interview.ts:87-107`): perguntas
  específicas em vez de formulário genérico.

Ponte concreta: um adaptador que rode essa ingestão sobre `@vidavesso` (ou sobre áudios
soltos do Vitor) e emita linhas de `ideias.csv` (`insumo_bruto` = transcript,
`origem=nota`), alimentando a skill score-editorial. Isso NÃO mexe no motor do AuraSite —
consome os módulos de ingestão como biblioteca ou processo separado. Exige alinhamento
antes (regra standing) e chaves próprias (Whisper/vision custam dinheiro).

## Cenário A — POC dá GO (Manus continua motor de execução)

O Content OS continua no Manus; importamos do AuraSite os PADRÕES que o Manus não dá:

| Dor do Content OS | Peça do AuraSite a copiar (padrão, não código acoplado) |
|---|---|
| Ledger é planilha passiva | `decisionLog` por etapa (choice + rationale + alternativas) anexado a cada peça |
| Repetição editorial | memória anti-repetição por similaridade sobre os últimos N briefs (ADR-004) |
| anti-generico é 1 crítico LLM | gates em camadas: regras determinísticas PRIMEIRO (ex.: palavras banidas de `REGRAS-DURAS.md` viram código), LLM só nos sobreviventes (`conceptGate.ts` faz assim) |
| Task do Manus que falha no meio | padrão `precomputed`/retomada por estágio: cada etapa persiste artefato e é retomável sem repagar |

## Cenário B — POC dá STOP (arquitetura própria)

O critério STOP do `PLANO-POC.md` manda "migrar para arquitetura própria". A fundação NÃO
se constrói do zero: o motor v3 já é um pipeline conteúdo-agnóstico nos pontos certos.
Mapa estágio-a-estágio:

| Content OS | Engine v3 equivalente | Adaptação |
|---|---|---|
| captura de insumo | S0 Intake + ingestão/corpus | trocar "site" por "peça"; corpus = insumos do Vitor |
| score-editorial | S1 Classificação | `ProjectClassification` → pilar + 4 eixos de score |
| brief | S2 Estratégia | `sectionPlan` → estrutura de slides/roteiro |
| ângulo/hook | S3 Direção + gate de conceito | bancos nomeados de hooks; anti-repetição já embutida |
| gerar-carrossel | S4 Composição | novo contrato Zod (`CarrosselContentV1` em vez de `SiteContentV3`) |
| arte final | S5 Render | template 1080×1350 de `FORMATOS.md` renderizado + screenshot |
| anti-generico + consistência visual | camada 1 (regras) + S6 crítica visual | os 10 critérios viram regras/dimensões |
| ledger | `atelier_shadow_jobs` + decision log | fila MySQL substitui Scheduled Tasks do Manus |

Pontos de costura já injetáveis (por desenho, não por sorte): `StageInvoker`
(`stageRunner.ts:29`) troca o LLM; `options.render` e `onStage`/`precomputed`
(`pipeline.ts:41-52`) injetam render e persistência de fora; contrato claim/result do
worker (`shadowRoutes.ts`) já é a fila. A publicação (conector Instagram/Publora) entraria
como um S8 novo — o motor não publica nada hoje.

## Avisos honestos (medidos, não opinião)

1. O v3 roda **somente em shadow** — nunca escreveu em produção (`drizzle/schema.ts:452-455`).
2. Custo real do 1º run: **US$4,10** vs teto alvo de US$0,50
   (`docs/site-engine-v3/implementation/07-known-limitations.md:9`). Uma peça de carrossel
   é mais simples que um site, mas o número manda dimensionar ANTES de migrar.
3. Crítica visual depende do CLI `claude` do worker ler imagens e degrada sem Playwright
   (limitação 7 do mesmo doc).
4. A realimentação `openQuestions`→entrevista está desenhada mas NÃO implementada no
   AuraSite (run falha com `confidence < 0.6`) — não contar com ela na ponte.

## Gatilho de decisão

Fim da semana 4 da POC → aplicar GO/ADJUST/STOP do `PLANO-POC.md` → Vitor escolhe o
cenário (A, B, C ou combinação). Pré-requisito de qualquer cenário: a pesquisa/alinhamento
do motor AuraSite que já é regra standing da venture.
