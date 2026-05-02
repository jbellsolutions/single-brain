# Decision Log

Append-only log of significant architectural and operational decisions.

## Format

```markdown
## YYYY-MM-DD — Decision Title

**Context**: What situation prompted this decision.
**Decision**: What was decided.
**Rationale**: Why this approach over alternatives.
**Outcome**: (filled in later) What happened.
```

---

## Example

## 2026-04-28 — Use OpenRouter instead of Anthropic direct

**Context**: Monthly LLM costs were projected at $500–700/mo using Claude Sonnet via Anthropic API.
**Decision**: Route all inference through OpenRouter using DeepSeek V4 Flash.
**Rationale**: 17–35× cheaper at equivalent capability for task execution. OpenRouter provides a single API compatible with OpenClaw's model config.
**Outcome**: Stack running at $5–20/mo for LLM costs.
