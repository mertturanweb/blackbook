# BlackBook — Master Project Document
### Client Intelligence Layer for Luxury Retail

**Live demo:** https://blackbookai.vercel.app
**GitHub:** github.com/mertturanweb/blackbook (main branch)
**Built by:** Mert Turan
**Stack:** Single HTML file · Vercel Serverless · Anthropic API · Airtable · GitHub

---

## Table of Contents

1. [Product Overview](#1-product-overview)
2. [Current Feature Set](#2-current-feature-set)
3. [Security & Architecture Rules](#3-security--architecture-rules)
4. [Codebase Structure](#4-codebase-structure)
5. [API & Prompt Architecture](#5-api--prompt-architecture)
6. [CA Login & Session System](#6-ca-login--session-system)
7. [Airtable Integration — Current Status & Next Steps](#7-airtable-integration--current-status--next-steps)
8. [Future Roadmap](#8-future-roadmap)
9. [Environment Variables](#9-environment-variables)
10. [Deployment](#10-deployment)
11. [Positioning & Context](#11-positioning--context)

---

## 1. Product Overview

BlackBook is an AI-powered clienteling intelligence layer for luxury retail. It is not a CRM replacement. It is the connective tissue that sits on top of existing systems (Salesforce, ERP, product catalogs) and gives Client Advisors everything they need before, during, and after a high-value client interaction.

**The scenario it solves:** A VVIC client walks in unannounced. The CA serving them has never met them before. Their history, preferences, last purchase, and upcoming anniversary are scattered across a CRM nobody has time to read in the moment. Once the client leaves, the outreach is just as fragmented. The advisor has to juggle multiple platforms just to prepare for a visit and stay in touch. One awkward interaction can put a six-figure relationship at risk.

**The goal:** One interface. Everything before, during, and after. The final touch stays human.

**Operational philosophy:** The goal is not a conventional clienteling tool with AI bolted on. It is a layer where AI does the actual work — for the CA using it, and behind the scenes building it. What that frees up is judgment: thinking about what this layer should actually do, and making sure it is good enough to hold up in a real boutique.

---

## 2. Current Feature Set

### AI Pre-Visit Briefing
Generates a 3-section briefing from full client history and CRM data.

- **Section i — Client Intelligence:** Who this client is and what matters most right now. References specific personal context naturally — pet, partner, upcoming occasions, last purchase.
- **Section ii — Conversation Guide:** Exact topics for the CA to raise and how to frame them. Specific, not generic.
- **Section iii — Action Items:** Precise commercial action for this appointment. References current CA action and urgency.
- **Mood Selector:** Relaxed / Busy / Celebrating / Difficult. Shapes tone and priority subtly — never names the mood in output. Relaxed = exploratory. Busy = tightened, lead with single action. Celebrating = warmth in word choice. Difficult = factual, de-escalation tools.
- **Appointment-Aware Mode:** When appointment is TODAY or TOMORROW, action section becomes a pre-arrival checklist. References exact CA action on file, urgency, and last contact note.
- **Preparation Checklist:** Section iv with checkable items the CA must complete before arrival.
- **Alerts & Tags:** Critical flags (date proximity, sensitivities) and 3-4 descriptor tags.

### AI Post-Visit Debrief
CA types or dictates raw notes after a visit. System extracts everything — nothing is lost.

- **Log Entry:** 1-2 sentences in the tone and style of existing interaction history.
- **New Preferences:** Every update — beverage changes, rejections and why, size notes, occasions, people mentioned.
- **Open Tasks:** Action items the CA mentioned needing to do, extracted exactly as stated.
- **Follow-Up Date:** Realistic date based on urgency and what was discussed.
- **Follow-Up Draft:** Ready-to-send message via the client's preferred channel.
- **Review Panel:** Full output shown before accepting — log entry, preferences, tasks, follow-up date, draft message.
- **Accept & Save:** Writes to post-visit notes, logs preferences and tasks to activity log.

### Voice Notes (Mic Button)
- Web Speech API — runs entirely in browser, zero API cost.
- Chrome desktop only (Web Speech API limitation on mobile and other browsers).
- Tap to start, tap again to stop. Auto-restarts if Chrome cuts on silence.
- Transcript appends to post-visit textarea. CA then hits AI Debrief.

### Message Drafting
Drafts outreach messages per client's preferred channel.

- Channels: WhatsApp, WeChat, Email, SMS, Phone, Line App, Instagram
- Tone selector: Formal / Warm / Casual
- Reply context field: paste inbound message for contextual replies
- Max 4 sentences. No emojis unless WeChat/Instagram. No prices. References one specific personal detail.

### Gift Intelligence
6 AI-selected gift items per client based on profile, occasion, live inventory.

- **Occasion types:** Birthday, Anniversary, Evergreen
- **Spend guidance by tier:** VVIC prioritises €3,000+. VIC €1,500–6,000. Platinum €800–3,500. Gold €500–2,500. Silver €200–1,500.
- **Selection rules:** Colour match, avoid list enforced, category diversity (max 2 per category), gender match, stock awareness, size compatibility.
- **Each item includes:** Reason written in warm insider tone referencing specific profile detail.
- **Ship Now / Reserve:** CA can action items directly. Stock decrements in session.
- **Live catalog:** Being migrated from hardcoded array to live Airtable fetch (see Section 7).

### Important Dates
- Birthday and anniversary alerts with 30-day countdown.
- Urgent (≤7 days) = terracotta accent.
- Passed dates show follow-up nudge for 7 days after, then disappear.
- Click row → opens gift section for that client and occasion.

### Dashboard
- **Stats bar:** Total LTV, VVIC count, VIC count, urgent alerts today.
- **Upcoming Appointments:** Cards sorted by tier priority then date. Each card shows: tier pill, client name, LTV, last purchase, current CA action, appointment row (date + countdown chip), open action field.
- **Appointment card lifecycle:** Today = terracotta chip. Future = neutral chip. Past (1-2 days) = dimmed card, "Visit passed" / "Log visit →" nudge. Past (3+ days) = removed.
- **Important Dates:** Unified bordered list, urgent items with terracotta left accent.
- **Needs Attention:** Clients with critical/high urgency. Terracotta top border. Clicking opens client profile.

### Client Profiles
20 fictional clients with full CRM data.

**Data fields per client:**
- Identity: id, name, tier (VVIC/VIC/Platinum/Gold/Silver), ltv, ca, contact, location
- Personal: birthday, partner, anniversary, pet, beverage
- Sizing: sizeTop, sizeBottom, shoe, jewelry
- Style: colors (preferred), avoid (never show)
- CRM: lastDate, lastType, lastNote, lastPurchase, sku, purchaseDate, urgency, caAction, appointment, followUp, alterations, aftercare

**Profile cards:**
- **Client:** ID, tier badge, LTV, assigned CA, preferred contact
- **Personal:** Birthday, partner, anniversary, pet, beverage — lighter text weight (contextual layer)
- **Sizing & Style:** All sizes, preferred colours, Never Show (terracotta warning row)
- **Last Transaction:** Item, SKU, date, boutique, alterations, aftercare
- **Current Status:** Urgency, CA action (dominant), follow-up due, last interaction (dimmed)
- **Appointment:** Date, location, Google Calendar sync indicator, aftercare follow-up with + Add button

**Interaction history:** Last interaction note displayed prominently. Previous 3 interactions shown below. Full transaction log accessible.

**Relationship sparkline:** Visual trajectory of the relationship.

### CA Performance Tab
Per-advisor portfolio LTV, conversion rate, VVIC client count.

### Activity Log
Every CA action stamps the active CA's name. Events logged: note added/edited/deleted, AI debrief accepted, follow-up added to calendar, message sent, handover submitted/cancelled, Salesforce sync.

### Onboarding (New Client)
4-step intake form. Fields: name, tier, CA assignment, contact preference, location, beverage, sizes, colours, avoid, CA notes, appointment, LTV, current action, last purchase, follow-up. New clients added to filtered list immediately.

### Handover Notes
CA can submit a handover note for an incoming CA. Dispatches to floor Slack channel (simulated). Pending handovers shown on dashboard card.

### Demo Mode
~90 second scripted walkthrough triggered by DEMO button. Navigates through key features automatically.

### Export PDF
Generates printable client profile PDF from current briefing.

### Salesforce Sync (Simulated)
Profile sync indicator on every client profile. Post-visit notes have "SF Sync to Salesforce" button.

### Google Calendar (Simulated)
Appointment sync indicator. Aftercare follow-up "+ Add" button.

---

## 3. Security & Architecture Rules

These rules are non-negotiable.

**Rule 1 — All prompts stay server-side.**
Never move prompt text into `index.html` or any frontend file. Every AI call goes through `/api/chat.js`. The frontend sends structured JSON (`type`, `client`, `mood`, etc.) and receives structured JSON back. A user opening DevTools Network tab sees request bodies with data objects, never prompt strings.

**Rule 2 — API keys are environment variables only.**
`ANTHROPIC_API_KEY`, `AIRTABLE_API_KEY`, and `AIRTABLE_BASE_ID` live in Vercel environment variables. They never appear in any committed file.

**Rule 3 — No logic commentary in frontend.**
Avoid comments in `index.html` that explain how AI scoring, tier matching, or gift selection logic works. Comments should describe UI structure only.

**Rule 4 — Catalog fetch is server-side proxied.**
The Airtable API key must never be called directly from the frontend. All Airtable requests route through `/api/chat.js` as a `type: 'catalog'` request.

**Rule 5 — Maintain single-file frontend discipline.**
`index.html` is the entire frontend. Do not split into multiple JS or CSS files. Keeps deployment simple and reduces inspection surface area.

**Rule 6 — Response shapes are internal.**
The JSON field names used in AI responses (`opening`, `conversation`, `action`, `logEntry`, `newPreferences`, etc.) should not be exposed in UI labels in ways that reveal the underlying prompt architecture.

---

## 4. Codebase Structure

```
final/
├── index.html          ← Entire frontend (~7,700 lines, single file)
├── api/
│   └── chat.js         ← Vercel serverless backend (all AI prompts live here)
```

### index.html Architecture

**CSS Variables:**
```css
:root {
  --bg: #f2ede6;           /* page background */
  --bg2: #e8e2d8;          /* secondary background */
  --surface: #f8f5f0;      /* card surfaces */
  --ink: #181814;          /* primary text */
  --ink-mid: #42423c;      /* secondary text */
  --ink-light: #6e6c64;    /* tertiary text */
  --ink-faint: #a8a59c;    /* hints/labels */
  --rule: #d4cfc5;         /* borders */
  --rule-dark: #b8b4a8;    /* strong borders */
  --gold: #7a5e28;         /* primary accent */
  --gold-light: #a07c3e;   /* gold hover */
  --gold-pale: #ece0c4;    /* gold background tint */
}
```

**Typography:**
- `Playfair Display` — serif, client names, section headers, greeting
- `Libre Baskerville` — serif, data values in profile cards
- `DM Sans` — sans-serif, all UI labels, buttons, metadata

**Layout:** Fixed sidebar (260px) + scrollable content area. Mobile-responsive with collapsible sidebar.

**Key Data Structures (current stable — pre-Airtable):**
```javascript
const clients = [...]           // 20 client objects, ~line 3575
const histories = {...}         // interaction + transaction history, keyed by client ID
const masterCatalog = [...]     // 56 items T1-001 to T6-015 — TO BE REPLACED
const prebuiltGiftSelections = {...}  // per-client pre-generated gifts — TO BE REMOVED
const catalogById = {}          // lookup map built from masterCatalog
```

**CA System:**
```javascript
const caProfiles = [
  { id: 'CA-101', name: 'Sophie Marchand',  location: 'Milan Flagship' },
  { id: 'CA-102', name: 'James Reid',        location: 'Paris Flagship' },
  { id: 'CA-103', name: 'Giulia Ferretti',   location: 'Rome Boutique' },
  { id: 'CA-104', name: 'Kenji Park',        location: 'New York' },
  { id: 'CA-105', name: 'Nadia Al-Hassan',   location: 'Dubai' },
];
let activeCA = null;       // logged-in CA object
let selected = null;       // currently viewed client
let filtered = [...clients]; // CA-filtered client array
```

**Session State (resets on refresh — pending Supabase):**
```javascript
const postVisitNotes = {};   // clientId → [{id, text, date, time, aiGenerated}]
const handoverNotes = {};    // clientId → {text, date, time}
const activityLogs = {};     // clientId → [{type, title, detail, caName, time, date}]
const aiGiftCache = {};      // clientId → [{id, reason}]
const advisorNotes = {};     // clientId → [{id, text, date}]
const giftActions = {};      // giftId → 'shipped' | 'reserved'
const flaggedClients = new Set();
const arrivedClients = new Set();
```

**Key Functions:**
| Function | Description |
|---|---|
| `renderDashboard()` | Builds full dashboard with stats, appointment cards, important dates, needs attention |
| `renderProfile()` | Builds client profile with all data cards, history, briefing area, gift section |
| `renderList()` | Renders sidebar client list filtered to active CA |
| `generateBriefing()` | POST `/api/chat` type:briefing |
| `generateAIDebrief(id)` | POST `/api/chat` type:debrief |
| `generateCommDraft(clientId)` | POST `/api/chat` type:message |
| `loginCA()` | Handles CA selection, filters dashboard, personalises greeting |
| `toggleVoiceNote(id)` | Web Speech API mic toggle |
| `logActivity(clientId, type, title, detail)` | Stamps active CA name on every log entry |
| `fetchCatalogFromAirtable()` | Fetches live catalog — defined, needs wiring (see Section 7) |
| `apptCountdown(dateStr)` | Returns styled countdown chip HTML |
| `getBriefingAppointmentContext(c)` | Returns urgency string for briefing prompt |
| `buildLoginScreen()` | Populates CA selector on dark login screen |
| `selectCARow(id)` | Highlights selected CA row, enables Enter button |

---

## 5. API & Prompt Architecture

All AI calls route through `/api/chat.js` on Vercel. The frontend never builds prompts.

### Request Types

**`type: 'briefing'`**
```javascript
// Frontend sends:
{ type: 'briefing', client: c, mood: 'Relaxed', appointmentContext: '...' }

// Returns JSON:
{
  opening: "...",      // Client Intelligence section
  conversation: "...", // Conversation Guide section
  action: "...",       // Action Items section
  alerts: ["..."],     // Critical flags, max 2
  tags: ["...","..."]  // 3-4 descriptor tags
}
// max_tokens: 1000
```

**`type: 'message'`**
```javascript
// Frontend sends:
{ type: 'message', client: c, tone: 'Warm', replyContext: '...' }

// Returns: plain message text string
// max_tokens: 250
```

**`type: 'gifts'`**
```javascript
// Frontend sends:
{ type: 'gifts', client: c, occasion: 'Birthday', catalog: masterCatalog }

// Returns JSON array:
[{ id: "W-001", reason: "..." }, ...]  // exactly 6 items
// max_tokens: 800
```

**`type: 'debrief'`**
```javascript
// Frontend sends:
{ type: 'debrief', client: c, rawNotes: '...', history: histories[id] }

// Returns JSON:
{
  logEntry: "...",
  newPreferences: ["..."],
  openTasks: ["..."],
  followUpDate: "15 April 2026",
  followUpDraft: "..."
}
// max_tokens: 600
```

**`type: 'catalog'`** *(to be added — see Section 7)*
```javascript
// Frontend sends:
{ type: 'catalog' }

// Returns:
{ catalog: [...] }  // full Airtable catalog array
```

### Model
`claude-sonnet-4-20250514` — hardcoded server-side.

---

## 6. CA Login & Session System

**Login screen:** Dark full-screen overlay on load. CA selects name from list, clicks Enter. Screen fades out (500ms), dashboard loads filtered to their portfolio.

**After login:**
- `activeCA` set to selected CA profile object
- `filtered` set to `clients.filter(c => c.ca === selectedCAId)`
- Dashboard greeting: "Good afternoon, Sophie. Here is your client overview."
- All `logActivity()` calls stamp `activeCA.name`

**Current limitation:** CA selection is demo-grade — no real auth. Anyone can select any CA. Real auth via Supabase magic links is planned (see Section 8b).

**Client-CA mapping:** Each client has a `ca` field (CA-101 through CA-105). The `filtered` array uses this for dashboard and sidebar filtering.

---

## 7. Airtable Integration — Current Status & Next Steps

### Current Status
The Airtable base is live and populated. The connection code exists in `index.html` (`fetchCatalogFromAirtable()`) but the previous integration attempt was reverted because the gift generation trigger was not properly wired — the UI showed "No gift selections yet" with no way to generate them.

**The project is currently on the stable pre-Airtable backup.**

### Airtable Base
- **Base ID:** `applcdHUp1qAiquUl`
- **Table:** `Catalog`
- **Records:** 142 items — 80 womenswear (W-001 to W-080), 62 menswear (M-001 to M-062)

### Catalog Schema
| Field | Type | Notes |
|---|---|---|
| Name | Single line text | Product name, color variant in name if multiple colorways |
| ID | Single line text | W-001, M-001 format |
| SKU | Single line text | Auto-generated: WORD-WORD-GENDER-INDEX |
| Category | Multiple select | Bag, RTW, Footwear, Jewellery, Accessory, Outerwear, Leather Goods |
| Gender | Single select | W, M, U |
| Price | Single line text | e.g. €3,600 |
| PriceNum | Number | e.g. 3600, for AI price logic |
| Stock | Number | Integer |
| Colors | Single line text | Comma-separated |
| Image | URL | Prada CDN URLs — plan to migrate to Cloudinary |
| Description | Single line text | Short descriptor for AI context |

### Step-by-Step Integration Instructions

**Step 1 — Add catalog endpoint to chat.js**

Add this block before the `if (!type || !c)` guard so it runs without a client object:

```javascript
if (type === 'catalog') {
  try {
    const baseId = process.env.AIRTABLE_BASE_ID;
    const apiKey = process.env.AIRTABLE_API_KEY;
    let allRecords = [];
    let offset = null;

    do {
      const url = `https://api.airtable.com/v0/${baseId}/Catalog${offset ? `?offset=${offset}` : ''}`;
      const atRes = await fetch(url, {
        headers: { 'Authorization': `Bearer ${apiKey}` }
      });
      const atData = await atRes.json();
      if (atData.error) throw new Error(atData.error.message);
      allRecords = allRecords.concat(atData.records || []);
      offset = atData.offset || null;
    } while (offset);

    const catalog = allRecords.map(r => ({
      id:          r.fields.ID || r.id,
      airtableId:  r.id,
      name:        r.fields.Name || '',
      category:    Array.isArray(r.fields.Category) ? r.fields.Category : [r.fields.Category].filter(Boolean),
      gender:      r.fields.Gender || 'U',
      price:       r.fields.Price || '',
      priceNum:    r.fields.PriceNum || 0,
      stock:       r.fields.Stock || 0,
      sku:         r.fields.SKU || '',
      colors:      r.fields.Colors ? r.fields.Colors.split(',').map(c => c.trim()) : [],
      img:         r.fields.Image || '',
      description: r.fields.Description || ''
    }));

    return res.status(200).json({ catalog });
  } catch(err) {
    console.error('Airtable fetch error:', err);
    return res.status(500).json({ error: 'Failed to fetch catalog from Airtable' });
  }
}
```

**Step 2 — Update gifts prompt in chat.js**

Replace the old tier-based spend guide with price-based logic:

```javascript
const spendGuide = {
  'VVIC':     'Prioritise items above €3,000. Mix statement pieces (bags, coats, fine jewellery) with one or two refined accessories. No item below €500 unless exceptional personal match.',
  'VIC':      'Focus on €1,500–€6,000. One hero piece above €3,000 with complementary items at €1,000–€2,500.',
  'Platinum': 'Sweet spot is €800–€3,500. One elevated piece if occasion warrants.',
  'Gold':     '€500–€2,500 range. Aspirational but not overextended.',
  'Silver':   '€200–€1,500. Achievable and relevant to where this relationship currently is.'
}[c.tier] || 'Mix price points thoughtfully based on occasion and relationship stage.';
```

Also update the response format example from `"id": "T#-###"` to `"id": "..."` since IDs are now W-001/M-001 format.

Add `- Use PriceNum field for price logic, not any tier field` to selection rules.
Add `- Gender: W items for women, M items for men, U fine for either` to selection rules.

**Step 3 — Replace masterCatalog in index.html**

Replace the entire `const masterCatalog = [...]` block, the `const prebuiltGiftSelections = {...}` block, and the `masterCatalog.forEach(...)` line with:

```javascript
// ── CATALOG — loaded live from Airtable ──────────────────────────────────
let masterCatalog = [];
const catalogById = {};

async function fetchCatalogFromAirtable() {
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'catalog' })
    });
    const data = await res.json();
    if (data.catalog && Array.isArray(data.catalog)) {
      masterCatalog = data.catalog;
      masterCatalog.forEach(item => { catalogById[item.id] = item; });
      console.log(`Catalog loaded: ${masterCatalog.length} items from Airtable`);
    }
  } catch(err) {
    console.error('Failed to load catalog from Airtable:', err);
  }
}
```

**Step 4 — Wire catalog fetch on app init**

```javascript
buildLoginScreen();
fetchCatalogFromAirtable(); // async — catalog ready before first gift request
renderList();
renderDashboard();
```

**Step 5 — Fix renderGiftSection (critical — this was the failure point)**

Replace the existing `renderGiftSection` function entirely:

```javascript
function renderGiftSection(clientId, occasion) {
  const occasionLabel = occasion || 'Important Date';
  const selections = aiGiftCache[clientId] || [];

  if (selections.length === 0) {
    const grid = document.getElementById('giftGrid-' + clientId);
    if (grid) {
      grid.innerHTML = `
        <div style="grid-column:1/-1;padding:24px;text-align:center;">
          <div style="color:var(--ink-faint);font-size:12px;margin-bottom:16px;">
            No gift selections yet — generate a personalised selection from live inventory.
          </div>
          <button class="post-visit-save-btn" onclick="openGiftSection('${clientId}','${occasionLabel}')">
            Generate Gift Intelligence
          </button>
        </div>`;
    }
    return;
  }

  populateGiftGrid(clientId, selections, occasionLabel);
}
```

**Step 6 — Guard against empty catalog on gift generation**

In the gift generation function (where it calls `/api/chat` with `type: 'gifts'`), add:

```javascript
if (!masterCatalog.length) {
  showToast('!', 'Catalog loading', 'Please wait a moment and try again');
  return;
}
```

**Step 7 — Stock write-back on Ship Now**

Add `type: 'stock'` to chat.js:

```javascript
if (type === 'stock') {
  const { airtableId, newStock } = req.body;
  const url = `https://api.airtable.com/v0/${process.env.AIRTABLE_BASE_ID}/Catalog/${airtableId}`;
  await fetch(url, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${process.env.AIRTABLE_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ fields: { Stock: newStock } })
  });
  return res.status(200).json({ ok: true });
}
```

Update the Ship Now action in `index.html` to call this endpoint with the item's `airtableId` and decremented stock value.

### Verification After Deploy
Open browser console on Vercel URL. Should see:
```
Catalog loaded: 142 items from Airtable
```
Then test gift intelligence on any client. Selections should use W-001/M-001 IDs and reference real Prada items.

---

## 8. Future Roadmap

### 8a. Inventory / Shop Section

**Concept:** A visual catalog section where CAs browse live inventory for appointment preparation and inspiration. First feature that will look and feel like luxury retail rather than a data tool.

**UI Structure:**
- Compact catalog strip on the dashboard — 4-6 featured items as horizontal scroll
- "View All" expands to full catalog page
- Filter by Category, Gender, Price range
- Items: product image (full bleed), name, price, stock indicator, category tag
- Low stock (≤2) highlighted
- CA can pull any item into a client's gift section or flag it for an upcoming appointment

**Implementation notes:**
- Catalog is already fetched on load — shop section just renders it visually
- Filter state managed client-side, no additional API calls
- Lazy-load images to avoid blocking dashboard render
- Images currently Prada CDN URLs — plan to migrate to Cloudinary for permanence

### 8b. Supabase Integration

**Why Supabase:** PostgreSQL database + auth + real-time in one. Enables persistent memory, proper CA logins, multi-boutique isolation, and the audit trails enterprise buyers require.

**Auth Strategy:**
- Current CA selector stays for public demo — creates anonymous Supabase session
- Real boutiques: magic link auth (CA receives email, clicks link, authenticated — no password)
- "Continue as Guest" creates anonymous session with full functionality
- "Request Access" path for boutiques wanting real accounts
- Row-level security: CA-101 can only read rows where `ca_id = CA-101`

**Database Schema:**
```sql
clients         (id, name, tier, ltv, ca_id, contact, location, birthday, partner, 
                 anniversary, pet, beverage, size_top, size_bottom, shoe, jewelry,
                 colors, avoid, last_date, last_type, last_note, last_purchase, 
                 sku, urgency, ca_action, appointment, follow_up, alterations, aftercare)

interactions    (id, client_id, date, type, note, ca_id, created_at)
transactions    (id, client_id, date, item, sku, amount, location)
post_visit_notes (id, client_id, text, ca_id, ai_generated, created_at)
activity_logs   (id, client_id, type, title, detail, ca_id, created_at)
advisor_notes   (id, client_id, text, ca_id, created_at)
ca_profiles     (id, name, location, email)
```

**Memory (what Supabase unlocks):**
Currently all session data resets on page refresh. With Supabase: CA accepts a debrief → writes to `interactions` table → next CA opens same client, sees that debrief in the history. The relationship memory is real and shared across the team.

**Multi-Boutique Architecture:**
Each boutique gets their own Supabase schema (or separate project) and their own Airtable base:
- `maisonx.blackbook.ai` → Supabase schema `maison_x` + Airtable base `appXXX`
- `maisony.blackbook.ai` → Supabase schema `maison_y` + Airtable base `appYYY`

Per-boutique Vercel env vars control which database and catalog each deployment reads from. Boutique manager has editor access to their Airtable base only. CAs have read/write access to their Supabase schema only.

**Realistic Boutique Onboarding Flow:**
1. Create Airtable base for boutique, share editor access with their boutique manager
2. Boutique manager populates catalog (or migrate from existing source — CSV, brand website)
3. Connect their Salesforce via OAuth — initial client sync runs, populates Supabase `clients` table
4. CAs receive magic link invitations, first login creates their Supabase session
5. From that point: catalog updates in Airtable by boutique manager, client data syncs from Salesforce nightly, all CA activity persists in Supabase

### 8c. CRM Integration Strategy

**The problem in luxury retail today:** CAs toggle between Salesforce on desktop, a stock system on another screen, personal WhatsApp, and their own memory. The interaction history, preferences, and CA notes are scattered across systems — or live only in the advisor's head.

**Salesforce (primary target):**
- Most luxury maisons use Salesforce as system of record
- One-time OAuth connection — boutique IT authorises BlackBook to read their Salesforce data
- Nightly sync job pulls client profiles into Supabase
- The "Salesforce · Profile synced · [date]" indicator already in the UI becomes real
- Write-back: when CA accepts a debrief, post interaction log back to Salesforce

**Product catalog:**
- Airtable is the live catalog management layer
- Boutique manager self-serves — no developer needed for stock updates, new season additions, price changes
- Cloudinary for image hosting — permanent URLs, no dependency on brand CDNs

**CSV fallback:**
- For boutiques without proper CRM or API access
- Import client data once from CSV into Supabase
- Kills real-time stock sync — acceptable as a starting point, not a long-term solution

**Commercial positioning:**
The pitch to a buyer: "We don't replace your CRM. We sit on top of what you already have and give your CAs the intelligence layer they need in the moment." This is easier to sell than replacement, faster to onboard, and lower risk for the boutique's IT team.

### 8d. Slack / Teams Notifications

- When AI Debrief accepted: post summary to boutique's floor channel — "Sophie logged a visit with Eleanor Vance. Follow-up scheduled 1 April. New preference: sparkling water instead of champagne."
- 48 hours before client birthday/anniversary: ping assigned CA
- When briefing generated for same-day appointment: quiet notification to boutique manager
- When handover submitted: notify floor channel
- Implementation: Slack webhook URL stored as Vercel env var, triggered server-side from `chat.js`

### 8e. Outfit Recommendations

- **Hard dependency:** Real product images in catalog (Cloudinary migration)
- **Prompt logic:** Given client profile + live catalog, suggest 2-3 pieces that work together as a look for the upcoming appointment occasion
- **Placement:** Inside briefing as "Suggested Look" section (Section iv), or as separate tab on profile alongside Gift Intelligence
- **Requirement:** Sufficient catalog depth per gender category to make combinations feel intentional — 30+ well-photographed items minimum before this feature lands well

### 8f. Google Calendar Real Connection

- Currently simulated via sync indicator and animated dot
- Real implementation: OAuth connection, read actual CA calendar, display real appointments in profile
- Appointment data feeds into `getBriefingAppointmentContext()` automatically — no manual date entry

---

## 9. Environment Variables

All stored in Vercel → Project Settings → Environment Variables.

```
ANTHROPIC_API_KEY=sk-ant-...        # Claude API key
AIRTABLE_API_KEY=pat...              # Airtable personal access token
AIRTABLE_BASE_ID=applcdHUp1qAiquUl  # BlackBook Airtable base
```

Future additions:
```
SUPABASE_URL=https://...supabase.co
SUPABASE_ANON_KEY=eyJ...
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

---

## 10. Deployment

```bash
# Standard deploy
cd ~/Desktop/blackbook/final
git add index.html api/chat.js
git commit -m "description"
git push
# Vercel auto-deploys in ~30 seconds

# If remote is ahead
git pull --rebase origin main
git push
```

Vercel is connected to the `main` branch of `github.com/mertturanweb/blackbook`. Every push to main triggers an automatic redeploy.

---

## 11. Positioning & Context

**Product:** BlackBook — clienteling intelligence layer for luxury retail
**Creator:** Mert Turan — AI Operations Specialist for luxury consumer experiences
**Target buyers:** Boutique managers, heads of clienteling, retail innovation leads at luxury maisons
**Competitive context:** Zegna X (built with Microsoft, proprietary, closed). BlackBook is the outside-in version — built independently, deployable without enterprise procurement cycles.

**The edge:** The biggest luxury houses are currently spending millions building custom, closed-loop AI clienteling apps. BlackBook is a working prototype that demonstrates the same intelligence layer can be built from the outside in — and deployed for a fraction of the cost. The AI does the heavy lifting on implementation. What that frees up is judgment about what the layer should actually do in a real boutique.

**Build-in-public series:** LinkedIn posts documenting the build process. Post 1 published March 2026 (initial launch). Post 2 covers the post-visit debrief flow, appointment-aware briefings, and CA login screen.

**Key insight from industry research (McKinsey × Business of Fashion State of Fashion 2026):** Luxury's next edge is a unified client view, AI-empowered advisors, and perfectly timed outreach. BlackBook is built directly on that thesis.

---

*Document version: April 2026. Reflects stable pre-Airtable codebase state. Last updated by Mert Turan.*
