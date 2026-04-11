# Product Vision — SmartTicket
## Operational Intelligence Platform for Customer Support

> Document created: 2026-04-07  
> Author: Lucas Marques Maciel  
> Purpose: define the complete product vision for team alignment and development reference

---

## What is SmartTicket

SmartTicket is an **operational intelligence platform for customer support**, combining Machine Learning, LLMs, and automation to classify, prioritize, and resolve support tickets — reducing the human team's workload while generating business intelligence from every interaction.

It is not a simple chatbot. It is a hybrid system where AI resolves what it can on its own and escalates to humans what requires judgment — with priority, context, and full conversation history available to the agent.

---

## The problem it solves

Companies receiving medium-to-high volumes of customer messages face:

- Slow response times due to lack of automatic triage
- Support agents overwhelmed with repetitive and simple questions
- Lack of visibility into what customers need most
- Difficulty prioritizing urgent tickets over less urgent ones
- Lost conversion opportunities due to delayed responses
- No intelligence extracted from historical interactions

SmartTicket solves all of these in a single platform.

---

## Who it's for

**Ideal customer profile:**
- Small and medium-sized businesses
- With a support team of 1 to 10 people
- Receiving between 300 and 5,000 tickets per month
- Using WhatsApp as their main support channel
- Without budget for enterprise solutions (Zendesk, Salesforce)

**Example segments:**
- E-commerce
- Clinics and medical offices
- Service companies
- Small SaaS businesses
- Real estate agencies
- Schools and online courses

---

## How the system works — overview

```
Customer sends message on WhatsApp
              ↓
WhatsApp Business API receives and sends to webhook
              ↓
FastAPI receives, validates, and saves contact/ticket to database
              ↓
Preprocessing pipeline (cleaning + normalization)
              ↓
ML model classifies (category + confidence score)
              ↓
Priority is defined (model or rule-based)
              ↓
         High score?
        /            \
      Yes              No
       ↓               ↓
   LLM tries       Goes directly
   to resolve      to human queue
       ↓
  Customer confirmed resolution?
        /            \
      Yes              No
       ↓               ↓
  Closes ticket    Escalated to
  as resolved      human queue
       ↓
Agent sees in interface
              ↓
Agent responds through SmartTicket interface
              ↓
System sends response via WhatsApp API
              ↓
Customer receives on WhatsApp normally
              ↓
Everything recorded in database for analytics
```

---

## Detailed flow — each step

### 1. Message input

The customer sends a message on WhatsApp normally. They don't know they're interacting with a system — to them it's a regular conversation.

The **WhatsApp Business API** (via Z-API or Twilio) receives the message and forwards it via webhook to your FastAPI server.

The system identifies the sender by WhatsApp number:
- If the number already exists in the database → retrieves the contact's history
- If it doesn't exist → creates a new record in CONTACTS with `is_customer = false`

---

### 2. Preprocessing pipeline

The raw text goes through:
1. `clean_text` — lowercase, punctuation removal, symbols and noise
2. `normalize_text` — stopword removal, token normalization
3. Clean text ready for vectorization

---

### 3. ML model classification

The clean text is vectorized with TF-IDF and classified by the Logistic Regression model.

**Output:**
```json
{
  "category": "billing_inquiry",
  "score": 0.94
}
```

**MVP categories (simplified for development):**
- `technical_issue` — technical problems with product/service
- `billing_inquiry` — billing questions or issues
- `refund_request` — refund requests
- `cancellation_request` — cancellation requests
- `product_inquiry` — product or service questions

> **In the real product:** categories are defined per client. The process is:
> 1. Client lists all categories they believe they need
> 2. Team analyzes historical tickets and validates which are truly necessary
> 3. Very similar categories are consolidated
> 4. Very low-volume categories may be grouped into "other"
> 5. Final result can easily exceed 10 categories depending on the business
>
> The model is retrained for each client's category configuration.

**Confidence threshold:**
- Score ≥ 0.75 → reliable classification, LLM can attempt resolution
- Score < 0.75 → goes directly to human queue with "low confidence" flag

---

### 3.1 When to classify — first message vs accumulated conversation

In practice, the first customer message doesn't always clearly describe the problem. It's common to receive:

```
Customer: "Hi, how are you?"
Customer: "I need some help"
Customer: "It's about my last month's charge"
```

In this case, classifying only on the first message would generate noise or low confidence scores.

**MVP strategy (Approach A):**
The system classifies on the first message. If the score is low (< 0.75), it waits for the next message, concatenates, and reclassifies. Repeats until reaching the threshold or N messages (configurable limit, e.g.: 3).

```
Msg 1: "Hi how are you"               → score: 0.31 → waits
Msg 2: "I need some help"             → score: 0.44 → waits
Msg 3: "it's about my charge"         → score: 0.89 → classifies as billing_inquiry
```

**Final product strategy (Approach B):**
The model receives accumulated conversation messages as a single context, separated by a delimiter. More accurate for conversations that start vaguely.

```
Input: "hi how are you | I need some help | it's about my charge"
→ billing_inquiry · score: 0.91
```

This approach requires the model to be trained with accumulated conversations, not just isolated messages. Data collected during the pilot client must preserve the complete conversation history to enable this retraining.

**Decision:** Approach A for MVP, Approach B after 3 months of real pilot client data.

**Impact on training dataset:**
During manual collection (before the system is ready), the agent must record the **main message that described the problem** — which may be the second, third, or fourth message in the conversation. Not necessarily the first.

---

### 4. Priority definition

Initial priority is defined based on category and text keywords:

| Priority | Criterion |
|---|---|
| CRITICAL | Words like "urgent", "charged twice", "fraud", "cancel now" |
| HIGH | Refund requests, billing issues with high amounts |
| MEDIUM | Cancellation requests, technical issues |
| LOW | Product inquiries, general questions |

Priority is **dynamic** — increases automatically with waiting time (**priority aging**):

```
final_priority = initial_priority + (hours_waiting × escalation_factor)
```

A LOW ticket waiting 6 hours may have equivalent priority to a recent MEDIUM ticket. A scheduled job recalculates queue positions every 15 minutes.

---

### 5. LLM resolution attempt

If the score is high enough, the LLM attempts to resolve automatically.

The LLM does **not** receive just raw text. It receives structured context:

```
Category: billing_inquiry
Confidence score: 0.94
Contact history: customer since 2024, 3 previous tickets
Message: "I was charged twice this month"
```

This hybrid approach (ML + LLM) reduces hallucinations and generates more precise responses aligned with the client's business.

**How the system detects whether the LLM resolved or not:**

The system uses three combined signals — none is perfect on its own:

**Signal 1 — Customer explicitly confirms or denies**

After the LLM's response, the customer's next message is analyzed by a resolution intent classifier (can be the LLM itself with a simple prompt: *"was the problem resolved? answer only yes or no"*):

```
"didn't resolve"         → escalate = true  → human queue immediately
"problem continues"      → escalate = true
"I want to talk to someone" → escalate = true
"thank you"              → escalate = false → closes as resolved
"ok got it"              → escalate = false
```

**Signal 2 — Timeout without customer response**

After the LLM's response, if the customer doesn't reply within X minutes (configurable, e.g.: 30 min), the system considers the ticket resolved by timeout. If the customer comes back later, a new ticket is opened.

```
LLM responds → customer gone for 30 min → closes as resolved_by: llm (timeout)
```

**Signal 3 — Maximum number of exchanges without confirmation**

If the LLM tried N times (e.g.: 3 responses) and the customer keeps sending messages without confirming resolution, the system escalates automatically — regardless of message content.

```
LLM response 1 → customer replies → LLM response 2 → customer replies → LLM response 3
→ after 3 attempts without confirmation → escalates to human queue
```

**Complete decision flow:**

```
LLM sends response
       ↓
Did customer respond?
   No  → timeout after X minutes → closes as resolved
   Yes → analyze intent
            ↓ escalate = true  → human queue immediately
            ↓ escalate = false → closes as resolved
       ↓
Exceeded N exchanges without confirmation?
   Yes → human queue (regardless of intent)
```

If escalated → human agent receives the ticket with the **complete history** of the LLM's attempt visible in the interface.

> Timeout values and maximum N exchanges are configurable per client. Default values to be defined with the team (see `reuniao-regras-negocio.md`).

---

### 6. Human support queue

Tickets the LLM didn't resolve or that went directly to humans remain in the queue, ordered by dynamic priority.

The queue is visible in the SmartTicket interface to all of the client's agents.

---

### 7. Human support — 100% through the SmartTicket interface

**Product decision: agents respond exclusively through the SmartTicket interface, never directly through WhatsApp.**

**Why this decision:**
- Everything is recorded in the database for analytics
- Agent feedback feeds model retraining
- Full history available for any agent to pick up the ticket
- Complete quality and response time control
- No risk of untracked messages outside the system

**How it works in practice:**
- Agent types the response in the interface
- Clicks "Send"
- System calls the WhatsApp API and delivers the message
- Customer receives on WhatsApp normally, without noticing any difference

---

### 8. Real-time — WebSockets

To prevent agents from having to refresh the page to see new customer messages:

- Each open conversation has a dedicated WebSocket channel
- The agent is subscribed only to the channels of tickets they picked up
- When the customer replies, the message appears instantly on screen
- No polling, no refresh, no freezing

**For demo (MVP):** simple polling every 5 seconds is sufficient.  
**For production:** full WebSockets via FastAPI.

---

## The agent interface

### Screen 1 — Support queue

```
┌─────────────────────────────────────────────────┐
│  Ticket Queue                  12 pending        │
│                                                  │
│  🔴 CRITICAL                                     │
│  ┌──────────────────────────────────────────┐   │
│  │ "I was charged twice on my card"         │   │
│  │ billing · Score: 0.94 · Waiting: 2h30   │   │
│  │ ↑↑ Escalated due to wait time            │   │
│  │                        [Pick ticket]     │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  🟡 MEDIUM                                       │
│  ┌──────────────────────────────────────────┐   │
│  │ "I want to cancel my plan"               │   │
│  │ cancellation · Score: 0.87 · 45min       │   │
│  │                        [Pick ticket]     │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Screen 2 — Open ticket

```
┌─────────────────────────────────────────────────┐
│  Ticket #1042 — John Smith                       │
│  billing_inquiry · Score: 0.94 · HIGH            │
│  ─────────────────────────────────────────────  │
│  🤖 System: "We identified your request..."      │
│  👤 John: "But the problem continues"            │
│  👤 John: "I've tried 3 times" 🟢 just now       │
│                                                  │
│  💡 LLM suggestion:                              │
│  "We checked and identified the charge..."       │
│                              [Use] [Edit]        │
│                                                  │
│  [Type your response...             ] [Send]     │
│                                                  │
│  ─────────────────────────────────────────────  │
│  Feedback:                                       │
│  ✅ Category correct                             │
│  ❌ Category wrong → [What was it? ___________]  │
│                                                  │
│  [Resolved] [Waiting for customer] [Escalate]   │
└─────────────────────────────────────────────────┘
```

### Screen 3 — Manager dashboard

```
┌─────────────────────────────────────────────────┐
│  Overview — April 2026                           │
│                                                  │
│  Total tickets:           312                    │
│  Resolved by LLM:         187 (60%)              │
│  Resolved by human:       125 (40%)              │
│  Avg response time:       4min                   │
│  Model accuracy:          89% ↑3%                │
│                                                  │
│  By category:                                    │
│  product_inquiry    ████████░░  31%              │
│  billing_inquiry    ██████░░░░  24%              │
│  technical_issue    ███████░░░  28%              │
│  cancellation       █████░░░░░  17%              │
│                                                  │
│  Conversions this month: 34 new customers        │
└─────────────────────────────────────────────────┘
```

---

## Database structure

### CONTACTS
```
id                    → internal identifier
whatsapp_number       → unique identifier (WhatsApp number)
name                  → contact name
is_customer           → true/false
became_customer_at    → timestamp (null if not yet converted)
first_contact_at      → timestamp of first ticket
customer_id_external  → ID in client's CRM (if integration exists)
```

### TICKETS
```
id
contact_id            → FK to CONTACTS
text                  → original text
text_processed        → text after pipeline
category              → model classification
score                 → classification confidence
priority              → LOW / MEDIUM / HIGH / CRITICAL
priority_score        → numeric value for queue ordering (dynamic)
status                → open / in_progress / resolved / escalated
assigned_to           → agent ID (null if still in queue)
resolved_by           → "llm" / "human" / null
created_at
resolved_at
response_sent         → text of response sent to customer
```

### MESSAGES
```
id
ticket_id             → FK to TICKETS
direction             → "inbound" (customer) / "outbound" (system/human)
text
sent_by               → "llm" / "human" / "system"
sent_at
```

### FEEDBACK
```
id
ticket_id             → FK to TICKETS
correct_category      → correct category according to agent
was_classification_correct → true/false
agent_id
created_at
```

### CONVERSIONS
```
id
contact_id            → FK to CONTACTS
ticket_id             → which ticket generated the conversion
converted_at
```

---

## How the model learns over time — Feedback Loop

```
Agent corrects wrong classification
              ↓
Feedback saved to database (ticket_id + correct_category)
              ↓
Accumulates N feedbacks (e.g.: 500 corrections)
              ↓
Retraining job runs automatically
              ↓
New model trained with original data + feedbacks
              ↓
Metrics compared with previous model
              ↓
If better  → replaces model in production
If worse   → keeps previous and alerts team
```

Over time, the model learns the specific vocabulary of that client — the products they sell, recurring problems, the way their customers write. This generates **value-based lock-in**: the model becomes so specific that switching systems means starting over at zero accuracy.

---

## Monthly analytics report

Every month the system generates (or the team produces manually at first) a report with:

**Volume and efficiency:**
- Total tickets received
- % resolved automatically by LLM
- % resolved by human
- Average first response time
- Average total resolution time
- Comparison with previous month

**Distribution:**
- % by category
- Highest volume categories → FAQ or automation opportunities
- Peak demand hours and days → staffing suggestions

**Model quality:**
- Overall accuracy
- F1 by category
- Month-over-month evolution

**Conversion:**
- New contacts (first ticket, `is_customer = false`)
- Converted to customers (`is_customer` changed to `true`)
- Conversion rate
- Which category generated the most conversions

**Value generated:**
- Estimated hours saved by automation
- Avoided cost (based on average agent salary)

---

## Business model

### Pricing

| Monthly volume | Setup fee | Monthly fee |
|---|---|---|
| up to 600 tickets | R$3,000 | R$500 |
| 600–2,000 tickets | R$4,000 | R$900 |
| 2,000–5,000 tickets | R$5,000 | R$1,500 |
| 5,000+ tickets | custom | custom |

**Costs passed to client:**
- WhatsApp Business API (Z-API or similar)
- OpenAI API (LLM)

**What's included in setup:**
- Full system configuration
- Model training with client's data (if historical data exists)
- WhatsApp integration
- Support team training
- Support during the first 30 days
- 1 model adjustment round after 30 days of use

### Estimated internal costs per client

| Item | Cost/month |
|---|---|
| Database (Railway/Render) | R$10–50 |
| API server | R$25–100 |
| LLM and WhatsApp API | passed to client |
| **Estimated margin** | **~R$400–490/month** |

### Revenue scalability

| Active clients | Monthly recurring revenue |
|---|---|
| 1 | R$500 |
| 5 | R$2,500 |
| 10 | R$5,000 |
| 20 | R$10,000 |

---

## Deployment strategy per client

### Client with historical data
- Provides old categorized tickets
- Minimum viable: 500 tickets per category
- Retrain with specific data
- Time to good model: 2–4 weeks

### Client without historical data
- Starts with generic model (~70% accuracy)
- Agent corrects errors day to day
- Retrain after 2–3 months of real usage
- Time to specific good model: 2–3 months

### Accelerated labeling (no history but wants fast results)
- Client's senior agent manually categorizes 200–300 recent tickets
- Train with that data + public data
- Time to reasonable model: 3–4 weeks

---

## Team capacity

With 4 people, the realistic limit of simultaneous clients at the start is **2–3 clients**. The first pilot client teaches what no planning can predict — integration issues, specific vocabulary, agent behavior.

**Recommended sequence:**
```
1 pilot client → learn → adjust → 2-3 clients → systematize → scale
```

As onboarding becomes standardized and retraining automated, the team can support more clients without growing proportionally.

---

## Tech stack

| Component | Technology |
|---|---|
| Backend / API | Python + FastAPI |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| LLM | OpenAI API |
| Database | PostgreSQL (Supabase for MVP, Railway/RDS for production) |
| WhatsApp | Z-API (Brazil) or Twilio |
| Real-time | WebSockets (FastAPI) — polling for demo |
| Agent interface | Streamlit (demo) → React or Next.js (production) |
| Scheduled job (priority aging + retraining) | APScheduler |
| Data processing | Pandas |

---

## Development timeline

| Phase | Period | Delivery |
|---|---|---|
| Technical MVP | Now → April 2026 | Classification + API working |
| Demo | May–June 2026 | Full system to show pilot client |
| Refinement | July–September 2026 | Queue + interface + WhatsApp + full database |
| Pilot deployment | October 2026 | First real client |
| Scale | 2027 | 5–10 clients |

---

## What's still undefined (for team meeting)

- Who develops the frontend (biggest current gap in the team)
- Exact score threshold for escalating to human
- LLM timeout before escalating
- Exact priority aging formula
- External CRM integration (if needed for pilot client)
- Response time SLA promised to clients

---

## Competitive advantages

1. **Model that learns with the client** — not generic, gets more accurate with usage
2. **Value-based lock-in** — the more they use it, the more specific it gets, the harder to switch
3. **Business analytics** — not just a tool, it's operational intelligence
4. **Affordable pricing** — price range ignored by enterprise solutions
5. **Hybrid AI** — ML + LLM with structured context, less hallucination than pure LLM
6. **Human-in-the-loop** — AI resolves what it can, humans handle what matters

---

> This document must be updated with every relevant decision made by the team.  
> Any AI reading this document should understand: SmartTicket is an intelligent support platform where ML classifies, LLM resolves automatically when possible, humans handle the rest through our interface, and everything generates data for analytics and continuous model improvement.
