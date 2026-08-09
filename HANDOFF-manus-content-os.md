# HANDOFF — Content OS de Instagram sobre Manus (para o Claude Code no Mac)

**Data:** 08/08/2026 · **Para:** Claude Code (tem shell no Mac) · **Dono:** Vitor Natividade
**Postura:** construtor supervisionado. Faça o que é seguro e verificável; **PARE e peça aprovação humana** para OAuth, publicação, compra e mutação externa.

**Fonte de verdade:** este doc. Se `plano_pesquisa_manus_instagram_claude_opus_5_max.md` e `manus-content-os-instagram-decisao.md` estiverem no diretório, leia-os para contexto — mas **este handoff prevalece** em caso de divergência.

**Diretório de trabalho:** `~/Developer/pipe-ai-runtime/manus-content-os/`
Fora do repo de governança. **Não toque em `pipe-venture-builder`.**

---

## 1. Objetivo

Construir os artefatos de um **Content Operating System de Instagram** cujo motor de execução é o Manus AI, mas cuja **memória editorial e ledger de performance vivem fora dele**.

O objetivo NÃO é uma fábrica de posts. É um sistema que transforma ideias reais do Vitor em conteúdo de qualidade e usa performance real para melhorar a capacidade editorial. Automação é meio.

Sua entrega é o **scaffolding completo, testado e pronto para o Vitor plugar no Manus** — não a operação rodando (isso exige OAuth e aprovação dele).

---

## 2. Decisão já tomada (não reabrir)

**Arquitetura A2 — Manus como orquestrador, não Manus-first.** Vencedora em matriz ponderada (4,18 vs 3,95 do agente próprio, 3,50 do n8n, 3,25 do Manus-first).

Três coisas ficam **deliberadamente fora do Manus**:
1. **Captura** do insumo humano (Telegram/WhatsApp → thread do Manus)
2. **Ledger editorial** em Google Sheets (connector nativo, zero infra nova)
3. **Caminho B de publicação** (skills Publora, MIT, open-source)

Motivo estrutural: Manus Projects são **instrução mestra + knowledge base estática**. Atualização de arquivo só vale em tasks novas. **Não há write-back.** Sem ledger externo não existe loop de aprendizado — existe repetição.

---

## 3. Fatos confirmados que restringem o desenho

### 3.1 Conector de Instagram — o que ele faz
Publica **post, carrossel, story e reel com caption**. Exige conta profissional (**business OU creator** — confirmado pela Meta). Rollout **escalonado**: pode não estar disponível na conta do Vitor.

### 3.2 Métricas — teto confirmado por DUAS fontes de primeira parte
Manus e Meta listam, independentemente, **exatamente seis**:
`views · reach · likes · comments · shares · saves`

**NÃO EXISTEM** (deprecados, inexistentes por peça, ou fora do conector):
- `impressions`, `video_views`, `plays` — deprecados na v22.0
- `profile_views` / visitas ao perfil — deprecado na API
- **`follower conversion` / follows por peça — NÃO EXISTE.** Follower é dado **de conta**, exige ≥100 seguidores
- Curva de retenção por segundo
- Watch time / avg watch time / skip rate — existem na API para reels, **não confirmados no conector**
- Demografia de audiência
- Melhores horários de postagem baseados em engajamento da audiência

⚠️ **Retenção do Instagram Insights ≈ 90 dias.** Sem snapshot externo, o histórico morre. É a razão de existir o ledger.

### 3.3 Limites da API de publicação (Meta)
100 posts/24h (carrossel = 1) · alt text **só em imagem** (reel e story não) · música só com áudio original · stickers de link/enquete/localização **não publicáveis** · sem branded content tags · sem filtros · **JPEG only, ≤8MB** · aspect 4:5 a 1.91:1 · carrossel 2–10 imagens · reel ≤300MB/15min (só 5–90s elegível para a aba Reels) · story ≤100MB/60s.

### 3.4 Agendamento
**Não há fila de rascunhos nativa.** Agendamento é da **task**, não do post: você agenda uma Scheduled Task que publica no horário. Padrão confirmado em uso real.

### 3.5 Confiabilidade
Degradação consistente acima de **~5 passos dependentes**; lógica condicional descarrila; falhas silenciosas (pula fonte sem avisar); sem preview de custo. Custo medido: 89–148 créditos por task de pesquisa, 12 para agendar.

→ **Regra de desenho inegociável: 1 Scheduled Task = 1 etapa do pipeline.** Nunca encadeie ideação→publicação numa execução só.

### 3.6 O risco mais perigoso: analytics alucinada
Há indício de que o Manus reporta métricas que a API não expõe. Ele tem tendência documentada a entregar **faixas estimadas quando não tem a fonte**, apresentadas como dado. Se isso acontecer com métricas de Instagram, o loop de aprendizado se corrompe **em silêncio**.

→ Toda métrica no ledger carrega **origem declarada**. Toda instrução ao Manus carrega a **trava anti-fabricação**.

### 3.7 Contexto de plataforma (2026)
Sinais de ranking do Instagram: **watch time, sends/reach, likes/reach**. Conteúdo original recebe 40–60% mais distribuição. IA **não** é penalizada; *templated/unoriginal* é. Rótulo de IA custa confiança da audiência.
→ **Métrica-norte: `sends/reach`** (= shares/reach). Likes é o sinal mais fraco. Volume não é estratégia.

---

## 4. Regras invioláveis (gates)

**Sem aprovação humana explícita do Vitor, NÃO:**
- Autorizar OAuth de nada (Instagram, Google, Publora, Manus)
- Digitar ou colar credenciais, tokens, senhas ou dados de cartão
- Publicar, agendar publicação ou enviar qualquer conteúdo para o Instagram ou qualquer serviço externo
- Enviar e-mail, DM ou mensagem em nome dele
- Comprar, assinar ou fazer upgrade de plano
- `git push`, PR, merge, criar/editar tickets no Linear
- Tocar no repo `pipe-venture-builder`
- Instalar serviço 24/7, usar `sudo`, alterar configuração de sistema
- Deletar nada fora do diretório de trabalho

**E nunca:**
- Inventar a voz, as opiniões, as histórias ou os pilares do Vitor. Onde faltar insumo dele: escreva `<!-- TODO-VITOR: ... -->` e siga.
- Imprimir valores de secret (só nomes / "preenchido-vazio").

---

## 5. O que construir (em ordem)

### 5.1 Estrutura
```
~/Developer/pipe-ai-runtime/manus-content-os/
├── README.md                  # como operar, em 1 página
├── CHECK-DIA-0.md             # checagens do Vitor antes de começar
├── PLANO-POC.md               # 4 semanas, 12 peças, GO/ADJUST/STOP
├── project/
│   ├── PROJECT-INSTRUCTION.md # instrução mestra do Manus Project
│   ├── VOZ.md
│   ├── PILARES.md
│   ├── FORMATOS.md
│   ├── REGRAS-DURAS.md
│   └── PADROES.md             # vazio; preenchido pelos dados reais
├── skills/                    # importáveis no Manus via GitHub
│   ├── score-editorial/SKILL.md
│   ├── gerar-carrossel/SKILL.md
│   ├── anti-generico/SKILL.md
│   ├── fact-check/SKILL.md
│   └── analise-semanal/SKILL.md
├── ledger/
│   ├── SCHEMA.md
│   └── csv/{ideias,briefs,publicados,metricas,hipoteses,aprendizados}.csv
├── scripts/
│   ├── ledger_lint.py
│   ├── gate0_diff.py
│   └── fixtures/
└── FALLBACK-PUBLICACAO.md     # caminho B, documentado, não instalado
```

### 5.2 `PROJECT-INSTRUCTION.md` — precisa conter, literalmente
- Releia `VOZ.md` e `REGRAS-DURAS.md` **a cada geração**; nunca use versão em cache.
- **Trava anti-fabricação:** *"Só reporte métricas que o conector retornar. Se um dado não estiver disponível, escreva INDISPONIVEL. NUNCA estime, infira ou complete. É proibido reportar: impressions, profile visits, follower conversion, follows por peça, watch time, demografia, melhores horários — esses dados não existem nesta integração."*
- **Trava anti-alucinação factual:** nenhum número, citação ou dado sem link verificável.
- **Trava de escopo:** entregue exatamente o pedido. Não gere dashboards, PDFs, gráficos ou artefatos não solicitados (isso queima créditos).
- **Trava de atomicidade:** uma task = uma etapa. Se a tarefa exigir mais de 5 passos dependentes, pare e reporte.
- Toda peça precisa rastrear ao `id_ideia` de um insumo real do Vitor no ledger. Sem insumo, não há peça.

### 5.3 `skills/anti-generico/SKILL.md` — critérios de REJEIÇÃO
Rejeitar e devolver (não "melhorar") se: poderia ter sido publicado por qualquer perfil · soa a texto padrão de IA · não contém ideia relevante · exagera uma afirmação · **inventa experiência pessoal** · usa clichê · é didático sem insight · não preserva a voz · transforma tudo em "lições" · força CTA sem necessidade. Saída: `APROVADO` ou `REJEITADO: <critério> — <trecho>`.

### 5.4 `skills/analise-semanal/SKILL.md`
Estrutura que força saída acionável: analisar peças dos últimos 30 dias com as **seis métricas permitidas**; quebrar por hook, formato, tema e nº de slides; **terminar com 5 ângulos para dobrar a aposta e 3 coisas para parar de postar**. Comparar apenas dentro do mesmo formato e faixa de reach (evita conclusão causal falsa). Incluir a trava anti-fabricação.

### 5.5 `ledger/SCHEMA.md` + CSVs (cabeçalho, sem dados)
- **ideias:** `id, data_captura, insumo_bruto, origem, pilar, score_so_eu, score_evidencia, score_tensao, score_utilidade, score_total, status`
- **briefs:** `id_brief, id_ideia, pilar, formato, angulo, hook, n_slides, cta, estrutura, data`
- **publicados:** `id_peca, id_brief, data, hora, formato, n_slides, hook_tipo, cta, primeira_pessoa, historia_pessoal, framework, permalink, creditos, reescrita, n_intervencoes, tempo_humano_min`
- **metricas:** `id_peca, janela, data_coleta, origem_dado, views, reach, saves, shares, comments, sends_por_reach`
- **hipoteses:** `id_hip, data, variavel_editorial, hipotese, previsao, pecas_teste, status, evidencia`
- **aprendizados:** `data, aprendizado, evidencia_ids, acao_no_sistema`

`origem_dado` ∈ {`conector`, `app`, `indisponivel`}. `janela` ∈ {`72h`, `7d`}.

### 5.6 `scripts/ledger_lint.py`
Valida `metricas.csv`: `origem_dado` no domínio permitido; colunas de métrica proibida ausentes; valores numéricos ou literal `INDISPONIVEL`. Exit 0 se válido, **exit 1** com relatório se inválido.

### 5.7 `scripts/gate0_diff.py`
Recebe dois CSVs (`--manus` e `--app`), compara por `id_peca` × métrica, imprime divergências e **exit 1** se houver divergência acima da tolerância **ou** se o arquivo do Manus contiver métrica fora das seis permitidas. É o executor do Gate 0.

### 5.8 Fixtures obrigatórias
`scripts/fixtures/` com casos **bom** e **ruim** para cada script — o ruim precisa incluir uma linha com `follower_conversion`. Os scripts têm que ser demonstrados rodando em ambos.

---

## 6. Gate 0 — o primeiro teste do Vitor, antes de qualquer conteúdo

Documente em `CHECK-DIA-0.md`:
1. Abrir aba **Connectors** no Manus e confirmar que **Instagram aparece** (rollout escalonado). Se não aparecer → A2 cai, migrar para arquitetura própria.
2. Publicar 3 peças **manualmente**, esperar 72h, pedir as métricas ao Manus, exportar para `manus.csv`, ler no app do Instagram para `app.csv`, rodar `gate0_diff.py`.
   - **Batem** → o ledger pode confiar no conector.
   - **Divergem** → coleta manual durante toda a POC; conector vira só publicador.
   - **Manus reporta métrica fora das seis** → está inventando. Pior cenário. Trava anti-fabricação na instrução mestra e reteste.

---

## 7. Métricas e critérios da POC (para `PLANO-POC.md`)

**Escopo:** 4 semanas · 12 peças (9 carrosséis + 3 reels) · 1 conta · 2 pilares.

**Operacionais:** aprovação sem reescrita ≥60% · intervenções ≤2/peça · tempo humano ≤5 min/peça · publicação bem-sucedida ≥90% · créditos ≤600/peça · erro factual publicado = 0 · consistência visual ≥90% · ≥1 insight acionável/semana a partir da semana 2.

**Editoriais (só as seis permitidas):** atenção = views, reach · valor percebido = saves, shares · conversa = comments · **norte = sends/reach**.

**GO:** todos os alvos operacionais + ≥1 hipótese validada ou refutada com dados + custo ≤US$40/mês.
**ADJUST:** aprovação 35–59% ou tempo humano 5–15 min → iterar `VOZ.md` e a skill de crítica, repetir 2 semanas.
**STOP → arquitetura própria:** aprovação <35% após 2 iterações do brand file · ou falha de publicação >20% · ou conector indisponível/instável · ou custo >US$100/mês.

---

## 8. Gates humanos permanentes da operação

- **Gate 1 — seleção de ideias** (~5 min/semana): aprova 3 de 8.
- **Gate 2 — aprovação da cópia** (alvo 90s/peça): voz, argumento, posicionamento.
- **Gate 3 — publicação:** manual nas 4 primeiras peças; se erro = 0, pode virar automático na semana 3.

Gates 1 e 2 **permanecem para sempre** — é onde o leverage humano é desproporcional.

---

## 9. Handoff final que você devolve

Tabela: **feito / pendente / bloqueado-aguardando-humano**, com a evidência (comando + saída) de cada item e o próximo passo. Sem expor secrets. Liste separadamente todos os `TODO-VITOR` que você deixou nos arquivos.
