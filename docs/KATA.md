# KATA: Agent Trust & Intent Verification

> **KATA is a proposed open framework for verifying AI agents, the authority behind them, the intent they were granted, and the actions they actually perform.**

**Status:** Concept / Open Design  
**Author:** Kaan Uluer  
**Repository:** https://github.com/kaanuluer/agent-verification-framework

---

## 1. The Problem

AI agents are moving from answering questions to **taking actions**.

An agent can search, select, purchase, transfer money, modify records, call APIs, create accounts, or execute multi-step workflows on behalf of a human or organization.

Traditional fraud controls were designed around a human-operated session:

```
User → Device → Session → Transaction → Risk Decision
```

Agentic systems introduce a different trust problem:

```
Human / Organization
        ↓
   Delegation
        ↓
      Agent
        ↓
   Tool / API Calls
        ↓
     Actions
        ↓
   Transaction
```

The critical question is no longer only:

> **"Is this transaction risky?"**

It becomes:

> **"Is this agent legitimate, was it authorized by the right party, is this action within the granted intent, and is the agent behaving consistently with that intent?"**

KATA is a proposal for answering that question continuously.

---

## 2. What KATA Means

**KATA — Know And Trust Agents**

KATA is not intended to replace existing identity, fraud, authorization, or transaction-risk systems.

It adds an **agent trust and intent layer** between identity/delegation and action execution.

The core decision can be expressed as four questions:

1. **WHO** is the agent?
2. **WHO AUTHORIZED** the agent?
3. **WHAT INTENT** was the agent authorized to execute?
4. **IS THE AGENT'S BEHAVIOR CONSISTENT WITH THAT INTENT?**

---

## 3. The KATA Trust Model

KATA proposes five connected intelligence layers:

```
┌──────────────────────────────────────────────────────────────┐
│                         KATA                                 │
│              Agent Trust & Intent Intelligence                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. AGENT IDENTITY                                           │
│     Who is the agent?                                        │
│                                                              │
│  2. DELEGATION / AUTHORITY                                   │
│     Who authorized it?                                       │
│                                                              │
│  3. INTENT                                                   │
│     What was it allowed to do?                               │
│                                                              │
│  4. BEHAVIOR                                                 │
│     Is it behaving consistently with the authorization?      │
│                                                              │
│  5. ACTION / TRANSACTION                                     │
│     What is it actually trying to execute?                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

These layers should not be evaluated independently.

KATA treats them as a **trust graph**.

---

## 4. From Transaction Risk to Intent Risk

Traditional fraud engines often focus on transaction-level signals:

| Traditional Signal | Agentic Equivalent |
|---|---|
| IP reputation | Agent / infrastructure reputation |
| Device reputation | Agent identity |
| Cookie/session history | Agent history |
| Behavioral biometrics | Agent behavioral patterns |
| Account linkage | Human ↔ agent ↔ organization graph |
| Transaction velocity | Agent action velocity |
| Transaction risk | Intent + action risk |
| Authentication | Delegation verification |
| Authorization | Scope and intent verification |

This does not mean traditional signals disappear.

They become **one part of a larger graph**.

---

## 5. Agent Identity

KATA should establish a verifiable identity for the agent before trusting its actions.

Potential identity attributes include:

- Agent identifier
- Agent provider
- Agent software / model identity
- Agent deployment identity
- Cryptographic credentials
- Credential issuer
- Credential status
- Credential expiration
- Human or organization owner
- Delegating party
- Previous reputation
- Previous security events
- Known infrastructure
- Agent capability profile

### Key principle

**An agent should not be trusted simply because it can authenticate.**

Authentication answers:

> "Can you prove who you are?"

KATA additionally asks:

> "Can you prove who authorized you and what you are authorized to do?"

---

## 6. Delegation Intelligence

The delegation layer establishes the relationship between the principal and the agent.

Example:

```
Alice
  │
  │ delegates
  ▼
Shopping Agent A
  │
  ├── Maximum spend: $500
  ├── Categories: Electronics
  ├── Merchants: Approved merchants
  ├── Currency: CAD
  ├── Expiration: 24 hours
  └── Approval required: > $500
```

KATA should evaluate:

- Who issued the delegation?
- Is the delegation authentic?
- Is it still valid?
- What is its scope?
- What limits apply?
- Can the delegation itself be delegated?
- Has the delegation been revoked?
- Does the current action fall inside the delegation?

---

## 7. Intent Intelligence

Intent is the core differentiator.

KATA should represent intent as structured, machine-evaluable policy rather than relying only on natural-language instructions.

Example:

```json
{
  "principal": "user:12345",
  "agent": "agent:shopping-001",
  "intent": {
    "purpose": "purchase",
    "categories": ["electronics"],
    "max_amount": 500,
    "currency": "CAD",
    "allowed_merchants": ["approved"],
    "expires_at": "2026-10-05T12:00:00Z"
  }
}
```

An agent action can then be evaluated against the granted intent.

### Intent mismatch examples

**Granted:**
> Buy headphones up to $300.

**Agent action:**
> Purchase a $1,200 laptop.

Result:

**Intent mismatch → high risk**

---

**Granted:**
> Purchase from approved merchants.

**Agent action:**
> Create a new merchant relationship and purchase.

Result:

**Delegation boundary violation → high risk**

---

**Granted:**
> Transfer up to $1,000 to an existing beneficiary.

**Agent action:**
> Add a new beneficiary and transfer $4,000.

Result:

**Intent + behavioral anomaly → critical risk**

---

## 8. Behavioral Intelligence

Intent alone is not enough.

A compromised or manipulated agent may possess valid credentials while behaving abnormally.

KATA therefore observes **agent behavior**, not just human behavior.

Potential signals:

- Tool-call sequence
- Tool-call frequency
- Retry patterns
- Navigation path
- Action velocity
- Scope expansion
- Unexpected API usage
- Permission escalation attempts
- New beneficiary creation
- New merchant interaction
- Unusual transaction amount
- Unusual geography or infrastructure
- Unexpected data access
- Prompt / instruction changes
- Repeated failed authorization
- Agent-to-agent interaction
- Deviation from historical behavior

The important distinction is:

> **A valid agent can still perform an invalid action.**

---

## 9. The KATA Decision Model

KATA should not produce a single opaque score without explanation.

A proposed decision object:

```text
Agent Trust
    +
Delegation Trust
    +
Intent Alignment
    +
Behavioral Consistency
    +
Action / Transaction Risk
    ↓
KATA Decision
```

Possible decisions:

- **ALLOW**
- **ALLOW_WITH_MONITORING**
- **STEP_UP**
- **HUMAN_APPROVAL**
- **BLOCK**
- **REVOKE / QUARANTINE**

Every decision should be explainable.

Example:

```
Decision: HUMAN_APPROVAL

Agent Trust: 94/100
Delegation Trust: 98/100
Intent Alignment: 42/100
Behavior Consistency: 31/100
Transaction Risk: 76/100

Primary reasons:
- Amount exceeds delegated limit
- New beneficiary detected
- Action sequence deviates from baseline
- Agent attempted privilege escalation
```

---

## 10. KATA Risk Graph

The central architectural idea is a connected graph rather than a collection of isolated signals.

```
                    ┌─────────────┐
                    │   Human     │
                    └──────┬──────┘
                           │
                       authorizes
                           │
                           ▼
                    ┌─────────────┐
                    │    Agent    │
                    └──────┬──────┘
                           │
                    has credential
                           │
                           ▼
                    ┌─────────────┐
                    │ Delegation  │
                    └──────┬──────┘
                           │
                    defines intent
                           │
                           ▼
                    ┌─────────────┐
                    │   Intent    │
                    └──────┬──────┘
                           │
                    constrains
                           │
                           ▼
                    ┌─────────────┐
                    │   Action    │
                    └──────┬──────┘
                           │
                    produces
                           │
                           ▼
                    ┌─────────────┐
                    │ Transaction │
                    └─────────────┘

        Behavior continuously observes the entire chain.
```

This allows risk engines to correlate signals rather than simply collect more signals.

---

## 11. KATA Verification Flow

```
Agent Request
     │
     ▼
┌───────────────┐
│ Agent Identity│
│ Verification  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Delegation    │
│ Verification  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Intent        │
│ Evaluation    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Behavioral    │
│ Analysis      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Action /      │
│ Transaction   │
│ Risk          │
└───────┬───────┘
        │
        ▼
┌──────────────────────────┐
│ KATA Decision Engine     │
├──────────────────────────┤
│ Allow                    │
│ Monitor                  │
│ Step-up                  │
│ Human approval           │
│ Block                    │
│ Revoke / quarantine      │
└──────────────────────────┘
```

Verification should be **continuous**, not a one-time event.

---

## 12. Example: Agentic Payment

Imagine a user tells an AI shopping agent:

> "Find me a new laptop under CAD 2,000 from a reputable retailer."

The agent finds a laptop and attempts to purchase it.

KATA evaluates:

### Identity

Is the agent a known and trusted agent?

### Delegation

Did the user actually authorize this agent?

### Intent

Does the purchase match:

- Product category?
- Price limit?
- Merchant constraints?
- Currency?
- Time validity?

### Behavior

Did the agent behave normally?

For example:

```
Search
 ↓
Compare
 ↓
Select
 ↓
Checkout
```

is expected.

But:

```
Search
 ↓
Create new payment method
 ↓
Add beneficiary
 ↓
Modify permissions
 ↓
Retry payment 14 times
 ↓
Attempt $7,800 transaction
```

is not.

The transaction may be technically valid.

**The agent behavior is not.**

That distinction is central to KATA.

---

## 13. Relationship to Existing Standards

KATA is not proposed as a replacement for emerging agentic-commerce protocols.

Instead, it can operate as a **risk and trust layer around them**.

Relevant industry directions include:

- Google Agent2Agent Protocol (A2A)
- Google Agent Payments Protocol (AP2)
- Visa Trusted Agent Protocol
- Mastercard Agent Pay
- W3C Verifiable Credentials
- OpenID-based identity and authorization mechanisms
- Existing fraud, authentication and transaction-risk engines

KATA's role is to correlate identity, delegation, intent, behavior and action into a continuous trust decision.

---

## 14. Design Principles

### 1. Verify the agent, not just the transaction

Transaction verification happens too late if the agent itself is compromised.

### 2. Verify delegation

An authenticated agent is not automatically an authorized agent.

### 3. Make intent machine-readable

Natural-language intent should be translated into explicit constraints wherever possible.

### 4. Monitor continuously

Trust should be dynamic.

### 5. Correlate signals

The strongest signal may be the relationship between multiple weak signals.

### 6. Explain decisions

Every block, step-up or approval request should have an explainable reason.

### 7. Preserve human control

High-impact actions should support configurable human approval policies.

### 8. Fail safely

When identity, authorization or intent cannot be established, the system should fail according to the configured risk policy rather than silently trusting the agent.

---

## 15. Proposed KATA Object Model

A minimal conceptual model:

```text
Principal
  └── Delegation
        └── Agent
              ├── Credential
              ├── Capabilities
              ├── Reputation
              ├── Behavior
              └── Actions
                    └── Transactions
```

Each object should be independently verifiable and linked through signed or auditable relationships where appropriate.

---

## 16. Proposed API Concept

A future KATA API could expose:

```http
POST /v1/agents/verify
POST /v1/delegations/verify
POST /v1/intents/evaluate
POST /v1/actions/evaluate
POST /v1/decisions
GET  /v1/agents/{agent_id}/trust
GET  /v1/delegations/{delegation_id}
GET  /v1/audit/{decision_id}
POST /v1/agents/{agent_id}/revoke
```

Example decision request:

```json
{
  "agent_id": "agent:shopping-001",
  "principal_id": "user:12345",
  "delegation_id": "delegation:789",
  "intent_id": "intent:456",
  "action": {
    "type": "purchase",
    "amount": 1250,
    "currency": "CAD",
    "merchant": "example-retailer"
  }
}
```

Example response:

```json
{
  "decision": "ALLOW_WITH_MONITORING",
  "agent_trust": 94,
  "delegation_trust": 98,
  "intent_alignment": 91,
  "behavior_consistency": 87,
  "transaction_risk": 34,
  "reasons": [
    "Agent identity verified",
    "Delegation valid",
    "Purchase within authorized amount",
    "Merchant matches policy",
    "Behavior consistent with baseline"
  ]
}
```

---

## 17. What KATA Is Not

KATA is not:

- A replacement for IAM
- A replacement for authentication
- A replacement for fraud engines
- A replacement for payment authorization
- A generic AI safety framework
- A claim that every agent needs the same verification level

KATA is a **trust and risk intelligence layer for agentic actions**.

---

## 18. Open Questions

KATA is intentionally an open design.

The community should help answer:

1. What should constitute an agent identity?
2. How should agent ownership be proven?
3. How should delegation be represented?
4. How should intent be expressed across different agent ecosystems?
5. How should intent changes be detected?
6. How should agent reputation be shared?
7. How should agent-to-agent delegation work?
8. Who is legally responsible when an agent exceeds its delegation?
9. What should happen when a valid agent is compromised?
10. How should privacy-preserving reputation work?
11. Which signals should be standardized?
12. Can KATA decisions become interoperable across financial institutions and platforms?

---

## 19. Proposed Roadmap

### Phase 1 — Concept

- Define terminology
- Define trust model
- Define agent/delegation/intent objects
- Define decision taxonomy

### Phase 2 — Reference Model

- JSON schemas
- Reference decision engine
- Example risk graph
- Threat model
- Test scenarios

### Phase 3 — Prototype

- KATA API
- Agent verification service
- Delegation registry
- Intent evaluator
- Behavioral analyzer
- Explainable risk decisioning

### Phase 4 — Interoperability

- Integrate with existing identity and authorization standards
- Map to emerging agentic-commerce protocols
- Build adapters for payment and fraud systems

### Phase 5 — Community

- Open governance
- Threat intelligence sharing
- Industry feedback
- Reference implementations
- Security review

---

## 20. The Core Proposal

The internet built identity systems for people.

Payments built authorization systems for transactions.

AI agents create a new layer:

**machines acting with delegated authority on behalf of people and organizations.**

KATA proposes that this layer needs its own continuous trust model.

The future fraud question may not be:

> **"Is this transaction legitimate?"**

It may be:

> **"Is this agent trusted, was it authorized, does this action match the user's intent, and is the agent behaving as expected?"**

**KATA is a proposal to make that decision explicit, explainable and interoperable.**

---

## References

- Fraud Risk Intelligence and Signals: https://priyacali.github.io/fraud-risk-signals-article/
- Google Agent Payments Protocol (AP2): https://ap2-protocol.org/
- W3C Verifiable Credentials: https://www.w3.org/TR/vc-data-model/
- Visa Trusted Agent Protocol: https://developer.visa.com/
- Mastercard Agent Pay: https://www.mastercard.com/

## Disclaimer

KATA is an independent open concept and is not affiliated with or endorsed by Google, Visa, Mastercard, W3C, or any other organization referenced above.

---

## Contributing

This repository is currently a concept and discussion space.

Ideas, critiques, threat models, schemas, examples and reference implementations are welcome.

Open an issue to discuss a proposal before implementing a major architectural change.
