# FORMATOS.md — formatos e limites técnicos

## Formatos da POC

9 carrosséis + 3 reels em 4 semanas (PLANO-POC.md). Story fica fora da POC.

## Limites duros da API de publicação (Meta) — teto técnico, não opinião

| Regra | Valor |
|---|---|
| Volume | 100 posts/24h (carrossel conta como 1) |
| Imagem | JPEG only, ≤8MB, aspect 4:5 a 1.91:1 |
| Carrossel | 2–10 imagens |
| Reel | ≤300MB / ≤15min; só 5–90s é elegível para a aba Reels |
| Story | ≤100MB / ≤60s |
| Alt text | só em IMAGEM (reel e story não têm) |
| Música | só áudio original |
| Stickers | link/enquete/localização NÃO publicáveis via API |
| Branded content tags | não suportadas |
| Filtros | não suportados |

## Regras editoriais por formato

- Carrossel: slide 1 é o hook; um argumento por slide; alt text obrigatório por imagem (acessibilidade — e é o único lugar onde a API aceita alt text).
- Reel: 5–90s para valer a aba Reels; roteiro fechado antes de gravar; nunca depender de sticker (a API não publica).

## Identidade visual

Identidade provisória da POC: tecnológica, sóbria e humana. Deve parecer um caderno de raciocínio contemporâneo, não uma apresentação corporativa nem um perfil de “guru de IA”.

### Paleta

| Função | Cor | HEX |
|---|---|---|
| Fundo principal | Azul-noite quase preto | `#08111F` |
| Fundo claro alternativo | Branco azulado | `#F4F7FB` |
| Destaque principal | Azul elétrico | `#2F80FF` |
| Destaque secundário | Ciano | `#42D9C8` |
| Texto sobre fundo escuro | Branco suave | `#F7F9FC` |
| Texto sobre fundo claro | Grafite | `#172033` |
| Texto secundário | Cinza azulado | `#8B98AD` |

Regras: usar no máximo uma cor de destaque por slide; reservar o ciano para hipóteses, perguntas e elementos de exploração; evitar gradientes chamativos e fundos excessivamente decorados.

### Tipografia

- **Títulos:** Sora SemiBold ou Bold.
- **Texto e legendas:** Inter Regular ou Medium.
- **Números, critérios e pequenos rótulos:** IBM Plex Mono Medium.
- Usar caixa alta apenas em rótulos curtos. Nunca em parágrafos.

### Template de carrossel

- Formato padrão: `1080 × 1350 px` (4:5), margens mínimas de `96 px`.
- Slide 1: hook de até 12 palavras, muito contraste e um único elemento visual.
- Slides internos: título curto + um argumento; preferir 25–45 palavras e nunca ultrapassar 65.
- Componentes recorrentes: número discreto do slide, linha fina de progresso, rótulo do pilar e `@vidavesso` no rodapé.
- Slide final: síntese prática ou pergunta real; CTA só quando nascer naturalmente do conteúdo.
- Fotografias, quando usadas, devem ser reais e pouco tratadas. Diagramas devem ser simples e funcionais.

### Template de reel

- Cenário limpo, luz natural ou azul suave, enquadramento do peito para cima e legendas grandes.
- Primeira frase entrega a tensão ou conclusão; sem vinheta.
- B-roll apenas quando explica algo: tela, diagrama, processo ou resultado real.
- Capa segue o carrossel: fundo azul-noite, título curto em Sora e um detalhe azul elétrico.

### Critério de consistência da POC

Uma peça é visualmente consistente quando respeita paleta, família tipográfica, margens, hierarquia, rodapé e regra de um argumento por tela. Variações são permitidas, desde que pelo menos cinco desses seis elementos permaneçam estáveis.
