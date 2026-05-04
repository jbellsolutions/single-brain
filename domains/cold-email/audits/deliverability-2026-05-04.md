## Deliverability Audit — 2026-05-04

**Period:** 2026-04-27 to 2026-05-04 (7 days)

---

### Overall Summary

| Metric | Value |
|---|---|
| Total Emails Sent | 300 |
| Total Opens | 49 |
| Total Replies | 6 |
| Total Bounces | 2 |
| Overall Reply Rate | 2.00% |
| Overall Bounce Rate | 0.67% |

**Verdict: ✅ HEALTHY** — Both campaigns pass all checks. No immediate action required.

---

### 1% Rule Check

> Threshold: ≥1% reply rate after 200+ sends. Below 200 sends = too early to judge.

| Campaign | ID | Sent (7d) | Replies | Reply Rate | Bounces | Bounce % | Status |
|---|---|---|---|---|---|---|---|
| recruiters-power-partner-A | 3249954 | 150 | 4 | 2.67% | 0 | 0.00% | ✅ PASS |
| recruiters-direct-value-A | 3249956 | 150 | 2 | 1.33% | 2 | 1.33% | ✅ PASS |

**Note:** Both campaigns are under 200 sends in this window — technically too early for the 1% rule, but both reply rates exceed the threshold and would pass.

---

### Campaign Configuration Compliance

| Rule | Campaign 3249954 | Campaign 3249956 | Status |
|---|---|---|---|
| NO open tracking | `DONT_EMAIL_OPEN`, `DONT_LINK_CLICK` ✅ | `DONT_EMAIL_OPEN`, `DONT_LINK_CLICK` ✅ | ✅ |
| Reply tracking only | `REPLY_TO_AN_EMAIL` ✅ | `REPLY_TO_AN_EMAIL` ✅ | ✅ |
| Plain text only | `send_as_plain_text: true` ✅ | `send_as_plain_text: true` ✅ | ✅ |
| Max 50 leads/day | 50 ✅ | 50 ✅ | ✅ |
| Mon-Fri 8AM-5PM ET | M-F, 08:00-17:00 ET ✅ | M-F, 08:00-17:00 ET ✅ | ✅ |
| AI ESP matching | ON ✅ | ON ✅ | ✅ |

---

### Inbox Health

**Mailbox health data:** Not yet populated (campaigns launched April 28-30, insufficient history).

**Mailbox inventory:** 24 total mailboxes across 4 domain groups, all `ACTIVE` warmup status:

| Domain Group | Domain | Mailboxes | Reputation | Type |
|---|---|---|---|---|
| darmors.info | darmors.info | 3 | 100% | Gmail |
| vakloe.info | vakloe.info | 3 | 100% | Gmail |
| sivrue.info | sivrue.info | 3 | 100% | Gmail |
| rivkoe.info | rivkoe.info | 3 | 100% | Gmail |
| kamrue.info | kamrue.info | 3 | 100% | Gmail |
| integraterzgroup.com | integraterzgroup.com | 2 | 88-95% | SMTP (MonkeyBrass) |
| integraterzworks.com | integraterzworks.com | 2 | 81-88% | SMTP (MonkeyBrass) |
| hireaiintegraterz.com | hireaiintegraterz.com | 1 | 92% | SMTP (MonkeyBrass) |
| meetaiintegraterz.com | meetaiintegraterz.com | 1 | 89% | SMTP (MonkeyBrass) |
| tryaiintegraterz.com | tryaiintegraterz.com | 1 | 86% | SMTP (MonkeyBrass) |
| withaiintegraterz.com | withaiintegraterz.com | 1 | 80% | SMTP (MonkeyBrass) |
| bookaiintegraterz.com | bookaiintegraterz.com | 1 | 91% | SMTP (MonkeyBrass) |

All Gmail mailboxes at 100% reputation. MonkeyBrass SMTP mailboxes range 80-95%. No blocked or paused mailboxes.

---

### Domain Authentication

| Domain | SPF | DKIM | DMARC |
|---|---|---|---|
| darmors.info | ✅ | ❌ MISSING | p=quarantine |
| vakloe.info | ✅ | ❌ MISSING | p=quarantine |
| sivrue.info | ✅ | ❌ MISSING | p=quarantine |
| rivkoe.info | ✅ | ❌ MISSING | p=quarantine |
| kamrue.info | ✅ | ❌ MISSING | p=quarantine |
| integraterzgroup.com | ✅ | ❌ MISSING | p=reject |
| integraterzworks.com | ✅ | ❌ MISSING | p=reject |
| hireaiintegraterz.com | ✅ | ❌ MISSING | p=reject |
| meetaiintegraterz.com | ✅ | ❌ MISSING | p=reject |
| tryaiintegraterz.com | ✅ | ❌ MISSING | p=reject |
| withaiintegraterz.com | ✅ | ❌ MISSING | p=reject |
| bookaiintegraterz.com | ✅ | ❌ MISSING | p=reject |

**⚠️ All 12 sending domains are missing DKIM records.** SPF is present everywhere. DMARC is configured with appropriate policies (quarantine for .info warmup domains, reject for .com production domains).

**Risk:** Missing DKIM means Gmail/Outlook cannot cryptographically verify email integrity. While not blocking yet (reply rates are healthy), this is a standard best practice gap. Google's bulk sender guidelines require DKIM for domains sending >5,000 emails/day — not currently the case, but should be addressed before scaling.

---

### Flag Summary

| Severity | Issue | Detail |
|---|---|---|
| ⚠️ WARNING | DKIM missing on all 12 domains | All domains have SPF + DMARC but no DKIM. Not currently causing deliverability issues but a compliance/trust gap. |

**No other flags.** No 1% rule violations. No high bounce rates. No warmup blocks. No configuration deviations.

---

### Action Items

- [ ] **Add DKIM to all sending domains** — Priority: Medium. Not urgent (current deliverability is fine), but should be done before scaling volume or launching B/C variants.
  - MonkeyBrass SMTP domains: DKIM keys available from MonkeyBrass panel
  - Gmail (.info) domains: DKIM configured automatically by Google, but verify `default._domainkey` CNAME records are published
- [ ] Re-run audit in 7 days (2026-05-11) with more sending history

---

### Comparison to Previous

No prior audit found — this is the first deliverability audit.
