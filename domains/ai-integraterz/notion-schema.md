# Notion Database Schema — Complete Reference

**Operations Hub:** `3493fa00-4c9d-8105-8a4e-ccdb8f4700c9`
**Total Databases:** 25
**Generated:** 2026-05-02

---

## Clients

**ID:** `f57e30ec-a7da-4246-95e0-313d4e3fbe1c`

| Property | Type | Details |
|---|---|---|
| Category | select | Offer Delivery, Client Campaign, JV Deal, Internal |
| Client ID | unique_id |  |
| Company / Name | title |  |
| Contact Email | email |  |
| Contact Name | rich_text |  |
| Content | relation | → 9fabc332-d7a... |
| Deal Value | number | dollar |
| Drive Folder | url |  |
| Health Score | number | number |
| Industry | select | AI/Tech, Consulting, Marketing, Education, SaaS, Speaking, Sales, Other |
| Invoices | relation | → 5b824640-fb4... |
| MRR | number | dollar |
| Meetings | relation | → b33f9993-526... |
| NPS Score | number | number |
| Notes | rich_text |  |
| Offer | select | 30 Day AI Chief Officer, Sovereign Audience Method, Zion AI Academy, N/A |
| Onboarded Date | date |  |
| Projects | relation | → 9dc3586b-84b... |
| Slack Channel | url |  |
| Status | status |  |
| Upsell Ready | checkbox |  |

---

## Team Members

**ID:** `e596c0ba-e2c6-45a1-830b-e978ff547a00`

| Property | Type | Details |
|---|---|---|
| Assigned Tasks | relation | → f52411c6-2cc... |
| Authored Content | relation | → 9fabc332-d7a... |
| Email | email |  |
| Hourly Rate | number | dollar |
| Name | title |  |
| Notes | rich_text |  |
| Performance Score | number | number |
| Role | select | Founder, Operations, VA, Contractor, AI Specialist |
| Skills | multi_select | AI Automation, Content, Sales, Operations, Development, Design, Research |
| Start Date | date |  |
| Status | status |  |
| Team ID | unique_id |  |
| Time Entries | relation | → 253abb88-637... |
| Utilization Target | number | number |

---

## Projects

**ID:** `9dc3586b-84b5-44dc-a2e8-9bbfcaffae47`

| Property | Type | Details |
|---|---|---|
| Budget | number | dollar |
| Category | select | Offer Delivery, Client Campaign, JV Deal, Internal |
| Client | relation | → f57e30ec-a7d... |
| Description | rich_text |  |
| End Date | date |  |
| Health | formula | formula |
| Hours Budget | number | number |
| Hours Estimated | rollup | rollup |
| Hours Logged | rollup | rollup |
| Hours Used | number | number |
| Invoices | relation | → 5b824640-fb4... |
| Meetings | relation | → b33f9993-526... |
| Next Task Due | rollup | rollup |
| Offer | select | 30 Day AI Chief Officer, Sovereign Audience Method, Zion AI Academy, N/A |
| Overdue Tasks | rollup | rollup |
| PM | people |  |
| Priority | select | Critical, High, Medium, Low |
| Progress | formula | formula |
| Project ID | unique_id |  |
| Project Name | title |  |
| Start Date | date |  |
| Status | select | Planning, Active, On Hold, Completed, Cancelled |
| Tasks | relation | → f52411c6-2cc... |
| Tasks Done | rollup | rollup |
| Time Entries | relation | → 253abb88-637... |
| Total Tasks | rollup | rollup |

---

## Meetings

**ID:** `b33f9993-5266-43d4-ae0b-8dbf538438d9`

| Property | Type | Details |
|---|---|---|
| Action Items Created | checkbox |  |
| Attendees | people |  |
| Client | relation | → f57e30ec-a7d... |
| Date | date |  |
| External Attendees | rich_text |  |
| Meeting ID | unique_id |  |
| Meeting Title | title |  |
| Project | relation | → 9dc3586b-84b... |
| Recording URL | url |  |
| Sentiment | select | Positive, Neutral, Concerned, Negative |
| Source | select | Read.ai, Manual, Granola |
| Summary | rich_text |  |
| Tasks | relation | → f52411c6-2cc... |
| Type | select | Kickoff, Weekly Check-in, Strategy Session, Review, Internal, Sales Call, JV Partner, Ad Hoc |

---

## Tasks

**ID:** `f52411c6-2cc6-48e8-a6f8-2c3378dcc8ab`

| Property | Type | Details |
|---|---|---|
| Assignee | people |  |
| Content | relation | → 9fabc332-d7a... |
| Days Left | formula | formula |
| Due Date | date |  |
| Effort (hours) | number | number |
| Is Done | formula | formula |
| Is Overdue | formula | formula |
| Meetings | relation | → b33f9993-526... |
| PM (auto) | rollup | rollup |
| Parent Task | relation | → f52411c6-2cc... |
| Priority | select | Urgent, High, Medium, Low |
| Project | relation | → 9dc3586b-84b... |
| Source | select | Manual, Slack, Email, Agent, Meeting, Read.ai |
| Sprint | select | Backlog, Current Sprint, Next Sprint |
| Status | status |  |
| Sub-tasks | relation | → f52411c6-2cc... |
| Tags | multi_select | From Slack, From Email, Agent Created, Blocked, Quick Win, Client Facing, Internal |
| Task ID | unique_id |  |
| Task Name | title |  |
| Team Member | relation | → e596c0ba-e2c... |
| Time Entries | relation | → 253abb88-637... |
| Time Logged | number | number |
| Week | select | Week 0, Week 1, Week 2, Week 3, Week 4, Ongoing |

---

## Time Entries

**ID:** `253abb88-637e-44f7-a0aa-6c1093a3c90a`

| Property | Type | Details |
|---|---|---|
| Billable | checkbox |  |
| Date | date |  |
| Description | title |  |
| Entry ID | unique_id |  |
| Hours | number | number |
| Notes | rich_text |  |
| Person | people |  |
| Project | relation | → 9dc3586b-84b... |
| Rate | number | dollar |
| Task | relation | → f52411c6-2cc... |
| Team Member | relation | → e596c0ba-e2c... |

---

## Invoices

**ID:** `5b824640-fb43-4d32-b5ce-6f5010af75fc`

| Property | Type | Details |
|---|---|---|
| Amount | number | dollar |
| Category | select | Offer Delivery, Client Campaign, JV Deal, Retainer, One-Time |
| Client | relation | → f57e30ec-a7d... |
| Due Date | date |  |
| Invoice # | title |  |
| Invoice ID | unique_id |  |
| Notes | rich_text |  |
| Paid Date | date |  |
| Project | relation | → 9dc3586b-84b... |
| Sent Date | date |  |
| Status | select | Draft, Sent, Paid, Overdue, Payment Failed, Cancelled |
| Stripe ID | rich_text |  |

---

## Content Calendar

**ID:** `9fabc332-d7ad-438c-b096-e06947c8299f`

| Property | Type | Details |
|---|---|---|
| Author | people |  |
| Content ID | unique_id |  |
| Engagement | number | number |
| Linked Author | relation | → e596c0ba-e2c... |
| Linked Client | relation | → f57e30ec-a7d... |
| Notes | rich_text |  |
| Offer | select | 30 Day AI Chief Officer, Sovereign Audience Method, Zion AI Academy, AI Integraterz General, N/A |
| Platform | multi_select | LinkedIn, YouTube, Twitter/X, Blog, Newsletter, Instagram, TikTok |
| Publish Date | date |  |
| Related Tasks | relation | → f52411c6-2cc... |
| Repurposed From | rich_text |  |
| Status | status |  |
| Title | title |  |
| Type | select | YouTube Video, LinkedIn Post, Blog Post, Newsletter, Twitter Thread, Short-Form Video, Podcast, Case Study |
| URL | url |  |

---

## Competitors

**ID:** `6305ef90-e8f4-4362-a803-792c16c40dd8`

| Property | Type | Details |
|---|---|---|
| Competes With | multi_select | 30 Day AI Chief Officer, Sovereign Audience Method, Zion AI Academy, AI Integraterz General |
| Intel Briefings | relation | → 34a3fa00-4c9... |
| Last Checked | date |  |
| LinkedIn | url |  |
| Name | title |  |
| Notes | rich_text |  |
| Pricing Notes | rich_text |  |
| Strengths | rich_text |  |
| Threat Level | select | High, Medium, Low, Watch |
| Weaknesses | rich_text |  |
| Website | url |  |

---

## Agent Logs

**ID:** `4ea81396-ab21-465d-8038-4e4167da1ed2`

| Property | Type | Details |
|---|---|---|
| Action | title |  |
| Agent | select | Onboarding, PM, Finance, Content, Client Success, Market Intel, HR, Reporting (+2 more) |
| Duration (sec) | number | number |
| Error Details | rich_text |  |
| Log ID | unique_id |  |
| Status | select | Success, Failed, Partial, Manual Override |
| Timestamp | date |  |
| Trigger | rich_text |  |

---

## Community Members

**ID:** `34a3fa00-4c9d-815a-b2bb-c9f98f57b9f9`

| Property | Type | Details |
|---|---|---|
| Capstone Client | relation | → f57e30ec-a7d... |
| Capstone Project | rich_text |  |
| Cert Level | select | Entry, Cert 1, Cert 2, Cert 3, Certified |
| Client Landed | checkbox |  |
| Cold Email Active | checkbox |  |
| DMs Sent This Week | number | number |
| Email | email |  |
| Emails Sent This Week | number | number |
| Enrolled Date | date |  |
| Flywheel Posts This Week | number | number |
| Graduation Date | date |  |
| Job Leads Received | number | number |
| Jobs Applied This Week | number | number |
| Member ID | unique_id |  |
| Name | title |  |
| Notes | rich_text |  |
| SKOOL Profile | url |  |
| Status | status |  |

---

## Intel Briefings

**ID:** `34a3fa00-4c9d-813b-8065-fbb432413761`

| Property | Type | Details |
|---|---|---|
| Alert Level | select | Red, Yellow, Green |
| Briefing ID | unique_id |  |
| Competitors | relation | → 6305ef90-e8f... |
| Competitors Mentioned | multi_select |  |
| Date | date |  |
| Opportunities | rich_text |  |
| Summary | rich_text |  |
| Title | title |  |
| Type | select | Daily, Weekly, Ad Hoc |

---

## Newsletter Archive

**ID:** `e793052f-99f9-4b6f-b7f2-6902d5ca7979`

| Property | Type | Details |
|---|---|---|
| Body Summary | rich_text |  |
| Date | date |  |
| Read | checkbox |  |
| Sender | rich_text |  |
| Sender Email | email |  |
| Source Thread ID | rich_text |  |
| Subject | title |  |
| Type | select | AI, Crypto, Marketing, Community, Other |
| URL | url |  |

---

## AI Updates

**ID:** `8bdf2f43-022c-4393-81f6-3aa318121a34`

| Property | Type | Details |
|---|---|---|
| Category | select | Tool, Feature, Model, Workflow, Trend |
| Date | date |  |
| Link | url |  |
| Sentiment | select | Bullish, Neutral, Cautious |
| Source Newsletter IDs | rich_text |  |
| Summary | rich_text |  |
| Title | title |  |

---

## Content Ideas

**ID:** `675aedac-0553-4466-b716-12deb53a714a`

| Property | Type | Details |
|---|---|---|
| Brief | rich_text |  |
| Date | date |  |
| Idea Type | select | Tutorial, Hot Take, Case Study, Demo |
| Source Newsletter IDs | rich_text |  |
| Status | status |  |
| Title | title |  |

---

## Updates Log

**ID:** `930e7b97-876a-4903-8868-ec0e64cd8e8c`

| Property | Type | Details |
|---|---|---|
| Date | date |  |
| Resolved | checkbox |  |
| Severity | select | Info, Warn, Action |
| Summary | rich_text |  |
| System | select | GitHub, Google Alerts, Bank, Vercel, Security, Other |
| Title | title |  |
| URL | url |  |

---

## Calendar Daily Brief

**ID:** `7ef02657-a5b5-4edb-8bca-38281975bd2c`

| Property | Type | Details |
|---|---|---|
| Date | title |  |
| Future Meeting Count | number | number |
| Past Meeting Count | number | number |
| Today Plan | rich_text |  |
| Week Ahead | rich_text |  |
| Yesterday Summary | rich_text |  |

---

## EOD Reports

**ID:** `70537fb6-ada9-452c-be56-1c1a70ba03f9`

| Property | Type | Details |
|---|---|---|
| Author | rich_text |  |
| Blockers | rich_text |  |
| Channel | rich_text |  |
| Checklist Pct | number | number |
| Date | date |  |
| Source URL | url |  |
| Title | title |  |
| Tomorrow Priorities | rich_text |  |
| Wins | rich_text |  |

---

## Tutor Curriculum

**ID:** `7cac710c-b03f-4e14-b92d-6ef991b8b1a2`

| Property | Type | Details |
|---|---|---|
| Bucket | select | Foundations, Data Modeling, Formulas, Automations, API, Operating Model |
| Concept | rich_text |  |
| Day | number | number |
| Exercise | rich_text |  |
| Status | status |  |
| Title | title |  |

---

## Tutor Lessons

**ID:** `968c34d7-8cac-4565-af1c-08824612fb14`

| Property | Type | Details |
|---|---|---|
| Anchor Operation | rich_text |  |
| Date | date |  |
| Day | number | number |
| Source | url |  |
| Title | title |  |

---

## Leads

**ID:** `3543fa00-4c9d-8115-a286-ee7aa2c5a924`

| Property | Type | Details |
|---|---|---|
| Campaign | rich_text |  |
| Company | rich_text |  |
| Deal Value | number | dollar |
| Email | email |  |
| Emails Opened | number | number |
| Emails Sent | number | number |
| Last Touch | date |  |
| LinkedIn URL | url |  |
| Name | title |  |
| Next Action | rich_text |  |
| Next Action Date | date |  |
| Niche | select | Recruiters, Agencies, SaaS, Consulting, E-commerce, Other |
| Notes | rich_text |  |
| Phone | phone_number |  |
| Replied | checkbox |  |
| Reply Sentiment | select | Positive, Objection, Question, Soft No, Not Interested, OOO |
| Signal Summary | rich_text |  |
| Signal Tier | select | S, A, B, C |
| SmartLead ID | rich_text |  |
| Source | select | Skool, LinkedIn, Inbound, SDR Call, Cold Email, Referral, SmartLead, Apify Scrape (+1 more) |
| Status | select | New, Researched, Contacted, Warm, Hot, Booked, Closed Won, Closed Lost (+2 more) |
| Title | rich_text |  |
| Verified | checkbox |  |

---

## Influencers

**ID:** `3543fa00-4c9d-8196-bd46-eb743053c9ac`

| Property | Type | Details |
|---|---|---|
| Avg Comments | number | number |
| Avg Likes | number | number |
| Collab Status | select | Identified, Reached Out, In Convo, Active Collab, Past Collab, Engagement Army, No Response |
| Collab Type | multi_select | Guest Post, Podcast Swap, Co-Stream, Engagement Pod, Cross-Promo, Affiliate, Shoutout |
| DM Handle | rich_text |  |
| Email | email |  |
| Engagement Rate | number | percent |
| Follower Count | number | number |
| Handle | rich_text |  |
| Last Contact | date |  |
| Name | title |  |
| Niche | select | AI/ML, Automation, No-Code, SaaS, Marketing, Recruiting, Entrepreneurship, Developer (+1 more) |
| Notes | rich_text |  |
| Platform | multi_select | LinkedIn, X/Twitter, YouTube, TikTok, Instagram, Substack, Skool, Podcast |
| Priority | select | High, Medium, Low |
| Profile URL | url |  |

---

## Growth Stats

**ID:** `3543fa00-4c9d-8199-b987-ee91f22b248b`

| Property | Type | Details |
|---|---|---|
| Call Connect Rate | number | percent |
| Calls Made | number | number |
| Date | date |  |
| Email Open Rate | number | percent |
| Email Reply Rate | number | percent |
| Emails Sent | number | number |
| Engagement Rate | number | percent |
| Followers | number | number |
| Followers Change | number | number |
| Impressions | number | number |
| Meetings Booked | number | number |
| New Leads | number | number |
| Notes | rich_text |  |
| Platform | select | LinkedIn, X/Twitter, YouTube, Substack, Skool, TikTok, Instagram, Cold Email (+2 more) |
| Posts Published | number | number |
| Revenue | number | dollar |
| Subscribers | number | number |
| Week | title |  |

---

## Cold Email Campaigns

**ID:** `3543fa00-4c9d-81de-a9a4-e15bb7c7a34d`

| Property | Type | Details |
|---|---|---|
| Bounce Rate | number | percent |
| Bounces | number | number |
| Brief | url |  |
| Campaign Name | title |  |
| Last Updated | date |  |
| Meetings Booked | number | number |
| Niche | select | Recruiters, Agencies, SaaS, Consulting, E-commerce |
| Notes | rich_text |  |
| Offer | select | Power Partner, Direct Value, Capstone |
| Open Rate | number | percent |
| Opens | number | number |
| Positive Replies | number | number |
| Replies | number | number |
| Reply Rate | number | percent |
| Sent | number | number |
| SmartLead ID | number | number |
| Start Date | date |  |
| Status | select | Drafted, Active, Paused, Stopped, Completed |
| Total Leads | number | number |
| Variant | select | A, B, C |

---

## Outreach Activities

**ID:** `3543fa00-4c9d-81f3-bd62-d0cd983d04e1`

| Property | Type | Details |
|---|---|---|
| Activity | title |  |
| Campaign Name | rich_text |  |
| Channel | select | SmartLead, Retell AI, LinkedIn, Email (Manual), Phone (Manual), Skool |
| Date | date |  |
| Lead Email | email |  |
| Notes | rich_text |  |
| Outcome | select | No Response, Opened, Replied, Meeting Set, Not Interested, Bounced, Unsubscribed |
| Type | select | Cold Email, Cold Call, LinkedIn DM, Follow-up, Meeting, Content Engagement, Referral Ask |

---

