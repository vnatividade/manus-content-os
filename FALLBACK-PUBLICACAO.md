# FALLBACK-PUBLICACAO — Caminho B (documentado, NÃO instalado)

Este arquivo existe para o dia em que o conector nativo falhar. Nada daqui está
instalado ou conectado — instalar exige decisão explícita e OAuth do Vitor.

## Quando o Caminho B entra na conversa

O Caminho B resolve UMA coisa: falha do PUBLICADOR. Ele não anula os critérios de decisão
do `PLANO-POC.md` — ele é uma opção que o Vitor pode escolher no momento de decidi-los:

- **Falha de publicação >20% ou conector instável durante a POC** → isso atinge o critério
  STOP do `PLANO-POC.md`. Na decisão, o Vitor escolhe: migrar já para arquitetura própria
  OU tentar o Caminho B primeiro para salvar a arquitetura A2 (trocando só o publicador)
  e reavaliar em 2 semanas.
- **Conector nem aparece no dia 0** → vale o `CHECK-DIA-0.md` §0: a A2 cai e a migração é
  para arquitetura própria. Nesse cenário o Caminho B não salva a A2 (ele não traz
  métricas); só pode reaparecer depois, como peça de publicação DENTRO da arquitetura
  própria.

## O que é

Skills open-source (**MIT**) da **Publora** para o Manus: a publicação passa a sair pela
API da Publora em vez do conector nativo Manus↔Instagram.

## O que muda (e o que não muda)

- Publicação: Manus → skill Publora → Instagram.
- Métricas: o Caminho B NÃO traz métricas do conector — a coleta vira manual (app do
  Instagram), com `origem_dado=app` no ledger. A trava anti-fabricação continua valendo
  integralmente.
- Ledger, gates humanos e skills editoriais: intactos — o Caminho B troca só o publicador.

## Passos (TODOS aguardam aprovação humana do Vitor)

1. Vitor cria conta na Publora e conecta o Instagram lá (OAuth — dele, nunca do agente).
2. Importar as skills da Publora no Manus a partir do repositório oficial da Publora no GitHub.
3. Testar com 1 peça de baixo risco, com Gate 3 manual.
4. Registrar no ledger que o publicador mudou (nota em `publicados.csv`, campo `framework`).

## O que este agente NÃO fez (por regra do handoff)

Não instalou skill, não criou conta, não autorizou OAuth, não testou publicação.
