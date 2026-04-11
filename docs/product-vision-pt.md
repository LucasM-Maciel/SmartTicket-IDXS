# Visão de Produto — SmartTicket
## Plataforma de Inteligência Operacional para Atendimento ao Cliente

> Documento criado em: 2026-04-07  
> Autor: Lucas Marques Maciel  
> Propósito: definir a visão completa do produto para alinhamento do time e referência para desenvolvimento

---

## O que é o SmartTicket

O SmartTicket é uma **plataforma de inteligência operacional para atendimento ao cliente**, que combina Machine Learning, LLMs e automação para classificar, priorizar e resolver tickets de suporte — reduzindo a carga da equipe humana e gerando inteligência de negócio a partir de cada interação.

Não é um chatbot simples. É um sistema híbrido onde a IA resolve o que consegue sozinha e encaminha para humanos o que exige julgamento — com prioridade, contexto e histórico completo disponíveis para o atendente.

---

## O problema que resolve

Empresas que recebem volume médio-alto de mensagens de clientes enfrentam:

- Tempo de resposta lento por falta de triagem automática
- Atendentes sobrecarregados com perguntas repetitivas e simples
- Falta de visibilidade sobre o que os clientes mais precisam
- Dificuldade em priorizar tickets urgentes dos menos urgentes
- Perda de oportunidades de conversão por demora no atendimento
- Nenhuma inteligência extraída das interações históricas

O SmartTicket resolve todos esses pontos em uma única plataforma.

---

## Para quem é

**Perfil de cliente ideal:**
- Empresas de pequeno e médio porte
- Com equipe de atendimento de 1 a 10 pessoas
- Que recebem entre 300 e 5.000 tickets por mês
- Que usam WhatsApp como canal principal de atendimento
- Que não têm recursos para soluções enterprise (Zendesk, Salesforce)

**Exemplos de segmentos:**
- E-commerce
- Clínicas e consultórios
- Empresas de serviços
- SaaS pequenos
- Imobiliárias
- Escolas e cursos online

---

## Como o sistema funciona — visão geral

```
Cliente manda mensagem no WhatsApp
              ↓
WhatsApp Business API recebe e envia para o webhook
              ↓
FastAPI recebe, valida e salva o contato/ticket no banco
              ↓
Pipeline de preprocessing (limpeza + normalização)
              ↓
Modelo ML classifica (categoria + score de confiança)
              ↓
Prioridade é definida (modelo ou regra)
              ↓
         Score alto?
        /            \
      Sim             Não
       ↓               ↓
   LLM tenta       Entra na fila
   resolver        humana direto
       ↓
  Cliente confirmou resolução?
        /            \
      Sim             Não
       ↓               ↓
  Fecha ticket    Escalado para
  como resolvido  fila humana
       ↓
Atendente vê na interface
              ↓
Atendente responde pela interface do SmartTicket
              ↓
Sistema envia a resposta via WhatsApp API
              ↓
Cliente recebe no WhatsApp normalmente
              ↓
Tudo registrado no banco para analytics
```

---

## Fluxo detalhado — cada etapa

### 1. Entrada da mensagem

O cliente manda uma mensagem pelo WhatsApp normalmente. Ele não sabe que está interagindo com um sistema — para ele é uma conversa comum.

A **WhatsApp Business API** (via Z-API ou Twilio) recebe a mensagem e a encaminha via webhook para o servidor FastAPI de vocês.

O sistema identifica o remetente pelo número de WhatsApp:
- Se o número já existe no banco → recupera o histórico do contato
- Se não existe → cria novo registro em CONTATOS com `is_customer = false`

---

### 2. Pipeline de preprocessing

O texto bruto passa por:
1. `clean_text` — lowercase, remoção de pontuação, símbolos e ruído
2. `normalize_text` — remoção de stopwords, normalização de tokens
3. Texto limpo pronto para vetorização

---

### 3. Classificação pelo modelo ML

O texto limpo é vetorizado com TF-IDF e classificado pelo modelo de Logistic Regression.

**Saída:**
```json
{
  "category": "billing_inquiry",
  "score": 0.94
}
```

**Categorias do MVP (simplificadas para desenvolvimento):**
- `technical_issue` — problemas técnicos com produto/serviço
- `billing_inquiry` — dúvidas ou problemas de cobrança
- `refund_request` — solicitações de reembolso
- `cancellation_request` — solicitações de cancelamento
- `product_inquiry` — dúvidas sobre produto ou serviço

> **No produto real:** as categorias são definidas por cliente. O processo é:
> 1. Cliente lista todas as categorias que acredita precisar
> 2. Time analisa os tickets históricos e valida quais são realmente necessárias
> 3. Categorias muito similares são consolidadas
> 4. Categorias com volume muito baixo podem ser agrupadas em "outros"
> 5. Resultado final pode facilmente passar de 10 categorias dependendo do negócio
>
> O modelo é retreinado para cada configuração de categorias por cliente.

**Threshold de confiança:**
- Score ≥ 0.75 → classificação confiável, LLM pode tentar resolver
- Score < 0.75 → vai direto para fila humana com flag de "baixa confiança"

---

### 3.1 Quando classificar — primeira mensagem vs conversa acumulada

Na prática, nem sempre a primeira mensagem do cliente descreve o problema com clareza. É comum receber:

```
Cliente: "Oi, tudo bem?"
Cliente: "Preciso de ajuda"
Cliente: "É sobre minha cobrança do mês passado"
```

Nesse caso, classificar apenas na primeira mensagem geraria ruído ou baixo score de confiança.

**Estratégia do MVP (Abordagem A):**
O sistema classifica na primeira mensagem. Se o score for baixo (< 0.75), aguarda a próxima mensagem, concatena e reclassifica. Repete até atingir threshold ou até N mensagens (limite configurável, ex: 3).

```
Msg 1: "Oi tudo bem"              → score: 0.31 → aguarda
Msg 2: "preciso de ajuda"         → score: 0.44 → aguarda
Msg 3: "é sobre minha cobrança"   → score: 0.89 → classifica como billing_inquiry
```

**Estratégia do produto final (Abordagem B):**
O modelo recebe as mensagens acumuladas da conversa como contexto único, separadas por um delimitador. Mais preciso para conversas que começam vagamente.

```
Input: "oi tudo bem | preciso de ajuda | é sobre minha cobrança"
→ billing_inquiry · score: 0.91
```

Essa abordagem exige que o modelo seja treinado com conversas acumuladas, não apenas mensagens isoladas. Os dados coletados durante o cliente piloto devem preservar o histórico completo de cada conversa exatamente para viabilizar esse retreino.

**Decisão:** Abordagem A no MVP, Abordagem B após 3 meses de dados reais do cliente piloto.

**Impacto no dataset de treino:**
Durante a coleta manual (antes do sistema estar pronto), o atendente deve registrar a **mensagem principal que descreveu o problema** — que pode ser a segunda, terceira ou quarta mensagem da conversa. Não necessariamente a primeira.

---

### 4. Definição de prioridade

A prioridade inicial é definida com base na categoria e palavras-chave do texto:

| Prioridade | Critério |
|---|---|
| CRITICAL | Palavras como "urgente", "cobrado indevido", "fraude", "cancelar agora" |
| HIGH | Refund requests, billing issues com valor alto |
| MEDIUM | Cancellation requests, technical issues |
| LOW | Product inquiries, dúvidas gerais |

A prioridade é **dinâmica** — aumenta automaticamente com o tempo de espera (**priority aging**):

```
prioridade_final = prioridade_inicial + (horas_esperando × fator_escalada)
```

Um ticket LOW que está esperando há 6 horas pode ter prioridade equivalente a um MEDIUM recente. Um job agendado recalcula as posições da fila a cada 15 minutos.

---

### 5. Tentativa de resolução pelo LLM

Se o score for alto o suficiente, o LLM tenta resolver automaticamente.

O LLM **não** recebe só o texto bruto. Ele recebe contexto estruturado:

```
Categoria: billing_inquiry
Score de confiança: 0.94
Histórico do contato: cliente desde 2024, 3 tickets anteriores
Mensagem: "Fui cobrado duas vezes esse mês"
```

Essa abordagem híbrida (ML + LLM) reduz alucinações e gera respostas mais precisas e alinhadas com o negócio do cliente.

**Como o sistema detecta se o LLM resolveu ou não:**

O sistema usa três sinais combinados — nenhum é perfeito sozinho:

**Sinal 1 — Cliente confirma ou nega explicitamente**

Após a resposta do LLM, a próxima mensagem do cliente é analisada por um classificador de intenção de resolução (pode ser o próprio LLM com um prompt simples: *"o problema foi resolvido? responda apenas sim ou não"*):

```
"não resolveu"          → escalate = true  → fila humana imediato
"continua o problema"   → escalate = true
"quero falar com alguém"→ escalate = true
"obrigado"              → escalate = false → fecha como resolvido
"tá bom"                → escalate = false
```

**Sinal 2 — Timeout sem resposta do cliente**

Após a resposta do LLM, se o cliente não responder em X minutos (configurável, ex: 30 min), o sistema considera o ticket resolvido por timeout. Se o cliente voltar depois, abre novo ticket.

```
LLM responde → cliente some por 30 min → fecha como resolved_by: llm (timeout)
```

**Sinal 3 — Número máximo de trocas sem confirmação**

Se o LLM tentou N vezes (ex: 3 respostas) e o cliente continua mandando mensagens sem confirmar resolução, o sistema escala automaticamente — independente do conteúdo das mensagens.

```
LLM resposta 1 → cliente responde → LLM resposta 2 → cliente responde → LLM resposta 3
→ após 3 tentativas sem confirmação → escala para fila humana
```

**Fluxo de decisão completo:**

```
LLM envia resposta
       ↓
Cliente respondeu?
   Não → timeout de X minutos → fecha como resolvido
   Sim → analisar intenção
            ↓ escalate = true  → fila humana imediato
            ↓ escalate = false → fecha como resolvido
       ↓
Excedeu N trocas sem confirmação?
   Sim → fila humana (independente da intenção)
```

Se escalado → atendente humano recebe o ticket com **histórico completo** da tentativa do LLM visível na interface.

> Valores de timeout e N máximo de trocas são configuráveis por cliente. Valores padrão a definir com o time (ver `reuniao-regras-negocio.md`).

---

### 6. Fila de atendimento humano

Tickets que o LLM não resolveu ou que foram diretamente para humanos ficam na fila, ordenados por prioridade dinâmica.

A fila é visível na interface do SmartTicket para todos os atendentes do cliente.

---

### 7. Atendimento humano — 100% pela interface do SmartTicket

**Decisão de produto: o atendente responde exclusivamente pela interface do SmartTicket, nunca diretamente pelo WhatsApp.**

**Por quê essa decisão:**
- Tudo fica registrado no banco para analytics
- O feedback do atendente alimenta o retreino do modelo
- Histórico completo disponível para qualquer atendente pegar o ticket
- Controle total de qualidade e tempo de resposta
- Sem risco de mensagens fora do sistema que não são rastreadas

**Como funciona na prática:**
- O atendente digita a resposta na interface
- Clica em "Enviar"
- O sistema chama a WhatsApp API e entrega a mensagem
- O cliente recebe no WhatsApp normalmente, sem notar diferença

---

### 8. Tempo real — WebSockets

Para evitar que o atendente precise atualizar a página para ver novas mensagens do cliente:

- Cada conversa aberta tem um canal WebSocket dedicado
- O atendente está inscrito apenas nos canais dos tickets que ele pegou
- Quando o cliente responde, a mensagem aparece instantaneamente na tela
- Sem polling, sem refresh, sem travamento

**Para a demo (MVP):** polling simples a cada 5 segundos é suficiente.  
**Para produção:** WebSockets completos via FastAPI.

---

## A interface do atendente

### Tela 1 — Fila de atendimento

```
┌─────────────────────────────────────────────────┐
│  Fila de Tickets              12 pendentes       │
│                                                  │
│  🔴 CRÍTICO                                      │
│  ┌──────────────────────────────────────────┐   │
│  │ "Fui cobrado duas vezes no cartão"       │   │
│  │ billing · Score: 0.94 · Esperando: 2h30 │   │
│  │ ↑↑ Escalado por tempo de espera          │   │
│  │                        [Pegar ticket]    │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  🟡 MÉDIO                                        │
│  ┌──────────────────────────────────────────┐   │
│  │ "Quero cancelar meu plano"               │   │
│  │ cancellation · Score: 0.87 · 45min       │   │
│  │                        [Pegar ticket]    │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Tela 2 — Ticket aberto

```
┌─────────────────────────────────────────────────┐
│  Ticket #1042 — João Silva                       │
│  billing_inquiry · Score: 0.94 · HIGH            │
│  ─────────────────────────────────────────────  │
│  🤖 Sistema: "Identificamos sua solicitação..."  │
│  👤 João: "Mas o problema continua"              │
│  👤 João: "Já tentei 3 vezes" 🟢 agora           │
│                                                  │
│  💡 Sugestão do LLM:                             │
│  "Verificamos e identificamos a cobrança..."     │
│                              [Usar] [Editar]     │
│                                                  │
│  [Digite sua resposta...            ] [Enviar]   │
│                                                  │
│  ─────────────────────────────────────────────  │
│  Feedback:                                       │
│  ✅ Categoria correta                            │
│  ❌ Categoria errada → [Qual era? ___________]   │
│                                                  │
│  [Resolvido] [Aguardando cliente] [Escalar]      │
└─────────────────────────────────────────────────┘
```

### Tela 3 — Dashboard do gestor

```
┌─────────────────────────────────────────────────┐
│  Visão geral — Abril 2026                        │
│                                                  │
│  Total de tickets:        312                    │
│  Resolvidos pelo LLM:     187 (60%)              │
│  Resolvidos por humano:   125 (40%)              │
│  Tempo médio de resposta: 4min                   │
│  Acurácia do modelo:      89% ↑3%                │
│                                                  │
│  Por categoria:                                  │
│  product_inquiry    ████████░░  31%              │
│  billing_inquiry    ██████░░░░  24%              │
│  technical_issue    ███████░░░  28%              │
│  cancellation       █████░░░░░  17%              │
│                                                  │
│  Conversões este mês: 34 novos clientes          │
└─────────────────────────────────────────────────┘
```

---

## Estrutura do banco de dados

### CONTATOS
```
id                    → identificador interno
whatsapp_number       → identificador único (número do WhatsApp)
name                  → nome do contato
is_customer           → true/false
became_customer_at    → timestamp (null se ainda não converteu)
first_contact_at      → timestamp do primeiro ticket
customer_id_external  → ID no CRM do cliente (se houver integração)
```

### TICKETS
```
id
contact_id            → FK para CONTATOS
text                  → texto original
text_processed        → texto após pipeline
category              → classificação do modelo
score                 → confiança da classificação
priority              → LOW / MEDIUM / HIGH / CRITICAL
priority_score        → valor numérico para ordenação da fila (dinâmico)
status                → open / in_progress / resolved / escalated
assigned_to           → ID do atendente (null se ainda na fila)
resolved_by           → "llm" / "human" / null
created_at
resolved_at
response_sent         → texto da resposta enviada ao cliente
```

### MESSAGES
```
id
ticket_id             → FK para TICKETS
direction             → "inbound" (cliente) / "outbound" (sistema/humano)
text
sent_by               → "llm" / "human" / "system"
sent_at
```

### FEEDBACK
```
id
ticket_id             → FK para TICKETS
correct_category      → categoria correta segundo o atendente
was_classification_correct → true/false
agent_id
created_at
```

### CONVERSIONS
```
id
contact_id            → FK para CONTATOS
ticket_id             → qual ticket gerou a conversão
converted_at
```

---

## Como o modelo aprende com o tempo — Feedback Loop

```
Atendente corrige classificação errada
              ↓
Feedback salvo no banco (ticket_id + categoria_correta)
              ↓
Acumula N feedbacks (ex: 500 correções)
              ↓
Job de retreino roda automaticamente
              ↓
Novo modelo treinado com dados originais + feedbacks
              ↓
Métricas comparadas com modelo anterior
              ↓
Se melhor → substitui o modelo em produção
Se pior   → mantém o anterior e alerta o time
```

Com o tempo, o modelo aprende o vocabulário específico daquele cliente — os produtos que ele vende, os problemas recorrentes, o jeito que os clientes dele escrevem. Isso gera **lock-in por valor**: o modelo fica tão específico que trocar de sistema significa voltar à estaca zero em acurácia.

---

## Relatório mensal de analytics

Todo mês o sistema gera (ou o time produz manualmente no início) um relatório com:

**Volume e eficiência:**
- Total de tickets recebidos
- % resolvidos automaticamente pelo LLM
- % resolvidos por humano
- Tempo médio de primeira resposta
- Tempo médio de resolução completa
- Comparativo com mês anterior

**Distribuição:**
- % por categoria
- Categorias com maior volume → oportunidades de FAQ ou automação
- Horários e dias de maior demanda → sugestão de escala de atendentes

**Qualidade do modelo:**
- Acurácia geral
- F1 por categoria
- Evolução mês a mês

**Conversão:**
- Contatos novos (primeiro ticket, `is_customer = false`)
- Convertidos em clientes (`is_customer` mudou para `true`)
- Taxa de conversão
- Qual categoria gerou mais conversões

**Valor gerado:**
- Estimativa de horas economizadas pela automação
- Custo evitado (baseado no salário médio do atendente)

---

## Modelo de negócio

### Precificação

| Volume mensal | Implantação | Mensalidade |
|---|---|---|
| até 600 tickets | R$3.000 | R$500 |
| 600–2.000 tickets | R$4.000 | R$900 |
| 2.000–5.000 tickets | R$5.000 | R$1.500 |
| 5.000+ tickets | sob consulta | sob consulta |

**Custos repassados ao cliente:**
- WhatsApp Business API (Z-API ou similar)
- OpenAI API (LLM)

**O que está incluído na implantação:**
- Configuração completa do sistema
- Treinamento do modelo com dados do cliente (se houver histórico)
- Integração com WhatsApp do cliente
- Treinamento da equipe de atendentes
- Suporte durante os primeiros 30 dias
- 1 rodada de ajuste do modelo após 30 dias de uso

### Custos internos estimados por cliente

| Item | Custo/mês |
|---|---|
| Banco de dados (Railway/Render) | R$10–50 |
| Servidor API | R$25–100 |
| LLM e WhatsApp API | repassado |
| **Margem estimada** | **~R$400–490/mês** |

### Escalabilidade da receita

| Clientes ativos | Receita mensal recorrente |
|---|---|
| 1 | R$500 |
| 5 | R$2.500 |
| 10 | R$5.000 |
| 20 | R$10.000 |

---

## Estratégia de implantação por cliente

### Cliente com dados históricos
- Fornece tickets antigos já categorizados
- Mínimo viável: 500 tickets por categoria
- Retreino com dados específicos
- Tempo até modelo bom: 2–4 semanas

### Cliente sem dados históricos
- Inicia com modelo genérico (acerta ~70%)
- Atendente corrige erros no dia a dia
- Retreino após 2–3 meses de uso real
- Tempo até modelo específico bom: 2–3 meses

### Rotulagem acelerada (sem histórico mas quer resultado rápido)
- Atendente sênior do cliente categoriza 200–300 tickets recentes manualmente
- Treino com esses dados + dados públicos
- Tempo até modelo razoável: 3–4 semanas

---

## Capacidade do time

Com 4 pessoas, o limite realista de clientes simultâneos no início é **2–3 clientes**. O primeiro cliente piloto ensina o que nenhum planejamento prevê — problemas de integração, vocabulário específico, comportamento dos atendentes.

**Sequência recomendada:**
```
1 cliente piloto → aprende → ajusta → 2-3 clientes → sistematiza → escala
```

À medida que o onboarding for padronizado e o retreino for automatizado, o time consegue suportar mais clientes sem crescer na mesma proporção.

---

## Stack tecnológica

| Componente | Tecnologia |
|---|---|
| Backend / API | Python + FastAPI |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| LLM | OpenAI API |
| Banco de dados | PostgreSQL (Supabase para MVP, Railway/RDS para produção) |
| WhatsApp | Z-API (Brasil) ou Twilio |
| Tempo real | WebSockets (FastAPI) — polling para demo |
| Interface atendente | Streamlit (demo) → React ou Next.js (produção) |
| Job agendado (priority aging + retreino) | APScheduler |
| Processamento de dados | Pandas |

---

## Timeline de desenvolvimento

| Fase | Período | Entrega |
|---|---|---|
| MVP técnico | Agora → Abril 2026 | Classificação + API funcionando |
| Demo | Maio–Junho 2026 | Sistema completo para mostrar ao cliente piloto |
| Refinamento | Julho–Setembro 2026 | Fila + interface + WhatsApp + banco completo |
| Implantação piloto | Outubro 2026 | Primeiro cliente real |
| Escala | 2027 | 5–10 clientes |

---

## O que ainda não está definido (para a reunião do time)

- Quem desenvolve o frontend (maior gap atual do time)
- Threshold exato de score para escalar para humano
- Tempo de timeout do LLM antes de escalar
- Fórmula exata do priority aging
- Integração com CRM externo (se necessário para o cliente piloto)
- SLA de tempo de resposta prometido ao cliente

---

## Diferenciais competitivos

1. **Modelo que aprende com o cliente** — não é genérico, fica mais preciso com o uso
2. **Lock-in por valor** — quanto mais usa, mais específico fica, mais difícil de trocar
3. **Analytics de negócio** — não é só ferramenta, é inteligência operacional
4. **Preço acessível** — faixa de preço ignorada pelas soluções enterprise
5. **Hybrid AI** — ML + LLM com contexto estruturado, menos alucinação que LLM puro
6. **Human-in-the-loop** — IA resolve o que pode, humano trata o que importa

---

> Este documento deve ser atualizado a cada decisão relevante tomada pelo time.  
> Qualquer IA que leia este documento deve entender: o SmartTicket é uma plataforma de atendimento inteligente onde ML classifica, LLM resolve automaticamente quando possível, humanos tratam o restante pela nossa interface, e tudo gera dados para analytics e melhoria contínua do modelo.
