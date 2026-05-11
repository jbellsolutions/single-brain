# Deliverability Audit — 2026-05-11

**Period:** May 4–11, 2026 | **Run:** Weekly Monday audit (cron)

---

## Campaign Status Overview

| Campaign | ID | Status | Leads | Sent (7d) | Replied | Reply Rate | Bounced | Bounce Rate | 1% Rule |
|---|---|---|---|---|---|---|---|---|---|
| recruiters-power-partner-A | 3249954 | PAUSED | 1,577 | 1,722 | 15 | 0.87% | 118 | 6.85% | 🔴 FAIL |
| recruiters-direct-value-A | 3249956 | PAUSED | 259 | 395 | 2 | 0.51% | 45 | 11.4% | 🔴 FAIL |
| ai-operator-10hr-broad | 3287517 | PAUSED | 1,986 | 594 | 1 | 0.17% | 25 | 4.21% | 🔴 FAIL |
| ai-operator-10hr-niche | 3287518 | **STOPPED** | 1,948 | 2,206 | 7 | 0.32% | 75 | 3.40% | 🔴 FAIL |
| home-services-hvac-florida | 3314165 | ACTIVE | 1,170 | — | — | — | — | — | 🟡 <200 |

**Overall (7d):** 4,617 sent | 19 replied (0.41%) | 241 bounced (5.22%)

---

## 1% Rule Check

🔴 **ALL campaigns above 200 sends fail the 1% rule.** Not a single campaign has ≥1% reply rate.

| Campaign | Sends | Replies | Rate | Verdict |
|---|---|---|---|---|
| recruiters-power-partner-A | 1,722 | 15 | 0.87% | Fails by 0.13pp |
| recruiters-direct-value-A | 395 | 2 | 0.51% | Fails by 0.49pp |
| ai-operator-10hr-broad | 594 | 1 | 0.17% | Fails by 0.83pp |
| ai-operator-10hr-niche | 2,206 | 7 | 0.32% | Fails by 0.68pp |

**Likely causes (in order):**
1. Domain auth gap — see below (SPF/DKIM missing → spam folder)
2. List quality — legacy campaigns had no verification step
3. Copy resonance — see triage recommendations

---

## Bounce Rate Assessment

| Campaign | Bounce Rate | Threshold | Status |
|---|---|---|---|
| recruiters-power-partner-A | 6.85% (118/1722) | 3% | 🔴 2.3x over |
| recruiters-direct-value-A | 11.4% (45/395) | 3% | 🔴 3.8x over |
| ai-operator-10hr-broad | 4.21% (25/594) | 3% | 🔴 1.4x over |
| ai-operator-10hr-niche | 3.40% (75/2206) | 3% | 🔴 borderline |

🔴 **All active/sending campaigns exceed the 3% bounce threshold.** Legacy campaigns (3249954, 3249956) were uploaded without email verification — this is the root cause. Niche campaign (3287518) also shows elevated bounces despite PipelineLabs "verified" status (known limitation — PipelineLabs verified ≠ deliverable, per May 8 evidence log).

---

## Domain Authentication 🔴 CRITICAL

**All 30 sending domains share the same auth gap:**

| Record | Status | Detail |
|---|---|---|
| **SPF** | 🔴 MISSING | All domains return only `google-site-verification` tokens — no `v=spf1` record exists. No mail servers are authorized to send. |
| **DKIM** | 🔴 MISSING | No `default._domainkey` records found on any domain. |
| **DMARC** | ⚠️ PRESENT BUT HARMFUL | `v=DMARC1; p=quarantine` with `aspf=s` (strict). Without SPF passing, DMARC quarantines ALL mail. |

**Impact:** Without SPF `include:_spf.google.com` or equivalent, receiving mail servers cannot authenticate these domains. Combined with DMARC `p=quarantine`, this means:

1. **SPF fails** → DMARC evaluation fails → email lands in **spam/quarantine** for any receiver enforcing DMARC
2. **Gmail-to-Gmail** may bypass some checks, but Microsoft 365, Yahoo, and corporate mail servers will quarantine
3. **This is the most likely root cause of low reply rates** — emails are being delivered but landing in spam folders

**Fix needed:** Add proper SPF records (`v=spf1 include:_spf.google.com ~all`) and DKIM keys to all sending domains.

---

## Domain Health (Sending Domains — last 7d)

| Domain | Sent | Bounced | Bounce Rate | Replies | Status |
|---|---|---|---|---|---|
| raxkoy.info | 161 | 0 | 0.0% | 2 | ✅ Best performer |
| talmuy.info | 162 | 3 | 1.9% | 0 | ✅ Good |
| ravlui.info | 192 | 13 | 6.8% | 1 | ⚠️ |
| nalkues.info | 195 | 14 | 7.2% | 0 | ⚠️ |
| zijmuq.info | 162 | 14 | 8.6% | 0 | 🔴 |
| zilmues.info | 192 | 27 | 14.1% | 2 | 🔴 |
| dalkus.info | 190 | 25 | 13.2% | 0 | 🔴 |
| mikxoy.info | 161 | 22 | 13.7% | 1 | 🔴 |
| tamrois.info | 194 | 28 | 14.4% | 0 | 🔴 |
| mirkup.info | 162 | 26 | 16.0% | 1 | 🔴 |
| valmuc.info | 192 | 49 | 25.5% | 1 | 🔴🔴 |
| timvoi.info | 190 | 52 | 27.4% | 0 | 🔴🔴 |
| mirvoes.info | 188 | 60 | 31.9% | 0 | 🔴🔴 |

🔴 **5 domains have bounce rates >20%** — valmuc.info, timvoi.info, and mirvoes.info are the worst offenders. These domains are damaging overall sender reputation.

---

## Inbox Health

| Metric | Value |
|---|---|
| Total mailboxes | 100 |
| Unique domains | 33 |
| SMTP healthy | 100/100 ✅ |
| IMAP healthy | 100/100 ✅ |
| Warmup issues | 0 |
| Daily sends (all) | 0 |

### 🔴 Critical: 100 New Mailboxes Not Connected

- **100 mailboxes** across **33 new domains** (elevateaxisca.info, progressdeskks.info, strategypointil.info, etc.) were created May 9-10
- **All show `campaign_count: 0`** — not attached to any campaign
- **All show `daily_sent_count: 0`** — zero sends from the entire batch
- These were presumably intended for the HVAC campaign (3314165) and future niche campaigns

**Action needed:** Connect these mailboxes to active campaigns. The HVAC campaign needs inboxes to send.

### Legacy Mailbox Issues (from mailbox-health API)

Several individual mailboxes on the old domains show extreme bounce rates:

- `b.hale@timvoi.info`: 23/63 (36.5%)
- `branson.h@timvoi.info`: 29/63 (46.0%)
- `branson.v@mirvoes.info`: 32/63 (50.8%)
- `b.voss@mirvoes.info`: 28/62 (45.2%)
- `c.ellwood@mikxoy.info`: 22/54 (40.7%)
- `soren@mirkup.info`: 26/54 (48.1%)
- `orin@valmuc.info`: 26/64 (40.6%)

🔴 **These mailboxes should be paused or retired** — individual bounce rates >40% will damage domain reputation.

---

## Action Items

### 🔴 P0 — Immediate (this week)

- [ ] **Add SPF records to all sending domains** — `v=spf1 include:_spf.google.com ~all` — this is the single biggest deliverability fix
- [ ] **Add DKIM keys to all sending domains** — generate via Google Workspace admin console
- [ ] **Connect 100 new mailboxes to HVAC campaign (3314165)** — campaign has 1,170 leads and 0 inboxes
- [ ] **Retire 7 high-bounce mailboxes** (>40% bounce rate) on mirvoes.info, timvoi.info, mikxoy.info, mirkup.info, valmuc.info
- [ ] **Pause domains with >25% bounce rate** — valmuc.info, timvoi.info, mirvoes.info

### 🟠 P1 — This week

- [ ] **Run spam placement test** on niche campaign copy — verify where emails land
- [ ] **Run spam-word-checker** on all active campaign copy (niche + HVAC)
- [ ] **Verify legacy lead lists** — recruiters campaigns were uploaded without verification
- [ ] **Re-verify niche campaign leads** — 3.4% bounce rate suggests PipelineLabs "verified" didn't catch everything

### 🟡 P2 — Monitor

- [ ] **HVAC campaign Day 1-3 metrics** — check lead status progression daily
- [ ] **DMARC reports** — review aggregate reports after SPF/DKIM fix to confirm auth passing
- [ ] **Domain warmup** — new 33 domains need warmup before full send volume

---

## Triage Decision Tree Applied

| Symptom | Finding | Action |
|---|---|---|
| 1% rule failed (all campaigns) | Domain auth gap primary cause | Fix SPF/DKIM → retest |
| Bounce >3% (all campaigns) | No pre-upload verification on legacy lists | Verify lists, retire bad mailboxes |
| Listed but low replies | Likely spam folder from auth gap | Run spam placement test after SPF/DKIM fix |
| 100 mailboxes idle | Not connected to any campaign | Connect to HVAC campaign |

---

## Next Steps

**Primary deliverable this week:** Fix SPF/DKIM across all domains + connect new mailboxes to HVAC campaign. Without authentication, all other optimizations are irrelevant — the emails aren't reaching inboxes.

**After auth fix:** Re-run this audit in 7 days to measure improvement. Reply rates should lift once emails pass DMARC.

---

*Generated by Hermes Agent — delverability audit cron job*
*Source: SmartLead campaign stats + domain health + mailbox health APIs, Cloudflare DoH DNS*
