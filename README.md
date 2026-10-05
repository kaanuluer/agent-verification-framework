# KATA: Agent Trust & Intent Verification

An open concept for continuously verifying **AI agents, delegated authority, intent, behavior, and actions**.

> **KATA — Know And Trust Agents**

## Why KATA?

AI agents are moving from generating information to taking actions on behalf of people and organizations.

Traditional fraud models often ask:

> Is this transaction risky?

KATA proposes a broader question:

> **Is this agent trusted, was it authorized, does the action match the granted intent, and is the agent behaving consistently with that intent?**

This repository explores that model as an open design.

## Core Model

```
Principal
   ↓
Delegation
   ↓
Agent Identity
   ↓
Intent
   ↓
Behavior
   ↓
Action
   ↓
Transaction
   ↓
KATA Decision
```

KATA evaluates five connected layers:

1. **Agent Identity** — Who is the agent?
2. **Delegation** — Who authorized it?
3. **Intent** — What was it authorized to do?
4. **Behavior** — Is it behaving consistently with that authorization?
5. **Action / Transaction** — What is it actually trying to execute?

The resulting decision may be:

**ALLOW · MONITOR · STEP-UP · HUMAN APPROVAL · BLOCK · REVOKE**

## Read the Concept

See the full proposal:

**[KATA Concept and Architecture](docs/KATA.md)**

The document covers:

- Agent identity and trust
- Delegation intelligence
- Machine-readable intent
- Agent behavioral intelligence
- Risk graphs
- Continuous verification
- Explainable decisions
- API concepts
- Existing standards and interoperability
- Threat and governance questions
- Proposed roadmap

## The Key Idea

An authenticated agent is not automatically an authorized agent.

An authorized agent is not automatically authorized for every action.

And a valid authorization does not guarantee that the agent is behaving as intended.

KATA therefore treats **identity + delegation + intent + behavior + action** as a connected trust graph rather than isolated fraud signals.

## Status

**Concept / Open Design**

This repository is intentionally positioned as an open framework for discussion, threat modeling, schemas, prototypes, and interoperability work.

## Contributing

Ideas, critiques, threat models, schemas, examples and reference implementations are welcome.

Open an issue to discuss a proposal before implementing a major architectural change.

## Author

**Kaan Uluer, CFE, MBA**

Fraud, Payment Systems & Product Management

GitHub: https://github.com/kaanuluer

---

### Disclaimer

KATA is an independent open concept and is not affiliated with or endorsed by Google, Visa, Mastercard, W3C, or any other organization referenced in the proposal.
