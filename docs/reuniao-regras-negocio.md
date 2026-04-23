# Reunião — Regras de Negócio
## SmartTicket-IDXS

> Criado em: 2026-04-07  
> Última atualização: 2026-04-07  
> Legenda: ✅ Decidido · [ ] Pendente de alinhamento com o time

---

## Bloco 1 — Decide agora (trava o MVP se não responder)

### Sobre o usuário final
- ✅ Quem usa o sistema: **atendente humano** pela interface do SmartTicket + **LLM** para casos simples automáticos
- ✅  O sistema responde automaticamente via LLM quando possível; casos não resolvidos vão para fila humana
- ✅ Humano no loop: sim — o atendente pega o ticket na interface e responde; o LLM nunca age sem supervisão indireta

### Sobre classificação
- ✅ Score baixo (< 0.75): sistema aguarda próximas mensagens (até 3), concatena e reclassifica. Após N mensagens sem score alto, vai direto para fila humana com flag "baixa confiança"
- ✅ Classificação na primeira mensagem que atingir threshold — não necessariamente a primeira mensagem da conversa
- [ ] Tem uma categoria "outros" para tickets que não se encaixam nas 5 categorias? → **decidir com o time**

### Sobre falhas do LLM
- ✅ Se o LLM falhar (timeout, rate limit), o sistema retorna a categoria sem resposta ou retorna erro ao cliente? → **decidir com o time**

---

## Bloco 2 — Decide antes do Sprint 5 (LLM)

### Sobre resposta automática
- [ ] O LLM responde em qual idioma? Só português ou também inglês? → **definir com Rafael**
- [ ] Qual o tom da resposta — formal, informal, empático? → **definir com Rafael**
- [ ] Tem limite de tamanho da resposta? → **definir com Rafael**
- [ ] Timeout do LLM: após quantos minutos sem resposta do cliente o ticket é considerado resolvido? → **sugestão: 30 min, confirmar com o time**
- [ ] Número máximo de trocas LLM ↔ cliente sem confirmação antes de escalar para humano? → **sugestão: 3 tentativas, confirmar com o time**
- [ ] Classificador de intenção de resolução: usar o próprio LLM (prompt simples) ou lista de palavras-chave? → **decidir com o time**

### Sobre prioridade
- ✅ O sistema classifica prioridade: LOW / MEDIUM / HIGH / CRITICAL
- ✅ Prioridade definida por regra baseada em palavras-chave ("urgente", "fraude", "cobrado indevido") + categoria
- ✅ Priority aging: prioridade aumenta automaticamente com o tempo de espera (job a cada 15 minutos)
- ✅ Prioridade alta muda a posição na fila — ticket CRITICAL sempre no topo
- [ ] Fórmula exata do priority aging: `prioridade_final = prioridade_inicial + (horas × fator)` → **definir o fator de escalada com o time**

### Sobre persistência
- ✅ O que é salvo: texto original, texto processado, categoria, score, prioridade, todas as mensagens da conversa, feedback do atendente, status de resolução, timestamps
- ✅ Estrutura do banco: CONTATOS, TICKETS, MESSAGES, FEEDBACK, CONVERSIONS (ver `product-vision-pt.md`)
- ✅ Contato identificado pelo número de WhatsApp — campo `is_customer` indica se já é cliente ou prospect
- [ ] Dados sensíveis (nome, email, CPF): o sistema salva só o que o cliente fornecer na conversa — definir política de privacidade mínima para o piloto
- [ ] Por quanto tempo os tickets ficam armazenados? → **definir com o time**

---

## Bloco 3 — Pode resolver depois

### Sobre canal
- ✅ Canal principal: WhatsApp via WhatsApp Business API (Z-API para Brasil)
- ✅ Atendente responde 100% pela interface do SmartTicket — nunca diretamente pelo WhatsApp
- ✅ O sistema envia a resposta via WhatsApp API nos bastidores; o cliente não percebe diferença
- [ ] Tem limite de tamanho de mensagem para o WhatsApp? → verificar limite da Z-API

### Sobre tempo real
- ✅ Demo/MVP: polling simples a cada 5 segundos para atualizar a interface
- ✅ Produção: WebSockets — cada conversa tem canal dedicado, atendente inscrito só nos seus tickets

### Sobre métricas de sucesso
- [ ] O que define que o MVP funcionou para o cliente de validação? → **definir critério de sucesso com o time**
- [ ] Meta de accuracy mínima aceitável para ir para produção? → sugestão: 75% geral, F1 ≥ 0.60 por categoria
- [ ] SLA de tempo de resposta prometido ao cliente? → **definir antes da proposta comercial**

### Sobre o modelo ao longo do tempo
- ✅ Retreino automático: job roda quando acumular N feedbacks (ex: 500 correções)
- ✅ Feedback do atendente: marca correto/incorreto na interface + qual categoria estava certa
- ✅ Modelo novo só substitui o anterior se métricas forem melhores
- [ ] Gatilho alternativo de retreino: ex. accuracy cai abaixo de X% → **definir threshold**

### Sobre erros e edge cases
- [ ] O que o sistema faz se receber um ticket em outro idioma? → **definir comportamento**
- [ ] E se o texto for ofensivo ou inadequado? → **definir moderação mínima**
- [ ] Tem log de erros? Quem monitora? → responsabilidade do Salim definir

---

## Bloco 4 — Perguntas novas (surgiram no planejamento de produto)

### Sobre o frontend
- [ ] **Quem desenvolve a interface do atendente?** → maior gap atual do time, ninguém tem isso como responsabilidade principal
- [ ] Para a demo: usar Streamlit (rápido) ou já começar em React/Next.js? → **decidir com o time**

### Sobre o cliente de validação confirmado
- [ ] Qual o segmento do cliente piloto? (e-commerce, clínica, serviços...) → impacta as categorias do modelo
- [ ] As 5 categorias atuais se aplicam ao negócio dele ou precisam ser redefinidas?
- [ ] Ele tem histórico de tickets antigos para treinar o modelo?
- [ ] Quantos tickets por mês ele recebe atualmente?

### Sobre coleta de dados do cliente piloto (agora, antes do sistema ficar pronto)
- [ ] Definir formato de coleta: Google Forms preenchido pelo atendente após cada ticket
- [ ] Combinar com o cliente que o atendente vai preencher diariamente
- [ ] Pedir export do histórico do WhatsApp para ter dados retroativos
- [ ] Campos mínimos: data · canal · mensagem principal · categoria · resolvido (sim/não) · como foi resolvido

### Sobre o modelo de negócio
- ✅ Precificação definida: R$3.000 implantação + R$500/mês para até 600 tickets
- ✅ Custos de LLM e WhatsApp API repassados ao cliente
- [ ] O que está incluído no contrato de implantação? → formalizar escopo antes da proposta

---

