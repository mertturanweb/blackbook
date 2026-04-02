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
7. [Airtable Integration — Live](#7-airtable-integration--live)
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

### Stylist Picks
3 AI-selected recommendations per client, generated on demand by the CA — not automatic.

- **Trigger:** CA selects an Outreach Context from a dropdown and clicks "Generate Recommendations." The button updates to "Refresh Picks" after the first generation. Clicking it again clears the cache and fires a new request.
- **Outreach contexts:** Just Because, New Arrivals, Birthday, Anniversary, Seasonal Update.
- **Spend guidance by tier:** VVIC prioritises €3,000+. VIC €1,500–6,000. Platinum €800–3,500. Gold €500–2,500. Silver €200–1,500. Guidance is injected into the prompt as hardcoded text per tier — `PriceNum` is stripped from the AI catalog and not sent to Claude. No legacy T1-T6 codes.
- **Additive preferences:** Colour and avoid data is a merge of the client's onboarding record (Airtable `colors`/`avoid` fields) AND any CA-entered values in the Style Intelligence section. Both sources are honoured simultaneously — neither overrides the other.
- **Conflict Resolution Hierarchy:** The avoid list is supreme. If a color is avoided, that item is hard-rejected regardless of any other match. No near-synonyms permitted (avoiding Black also blocks Dark Charcoal, Onyx, Jet). If strict filtering leaves 0 viable items, the AI returns `{ "gifts": [], "reasoning": "..." }` and the frontend displays the message elegantly in the Stylist Picks grid — no hallucination, no bad picks.
- **Selection rules:** Strict colour compliance (cross-referenced against catalog `colors` field), avoid list enforced item-by-item, category diversity (max 1 per category), gender match, size compatibility, context calibration per occasion.
- **Stylist Note:** Each recommendation includes a 1-sentence stylist note (max 15 words) that explicitly references how the pick aligns with the client's colour preferences — never generic.
- **Ship Now / Reserve:** CA can action items directly. Ship Now decrements stock in Airtable via a live PATCH write-back. Session stock updates immediately.
- **Placement:** Appears immediately after the Last Interaction summary, before the History Tables. CAs see it at the right moment — not buried at the bottom.
- **AI Cost Optimisation:** Gender pre-filter (W/U or M/U) reduces the catalog by ~44%. Field strip cuts it to `id`, `name`, `category`, `colors` only — no images, descriptions, or SKUs. Hard cap of 40 items. Payload is ~80% smaller than the full catalog. `max_tokens` set to 400.
- **Live catalog:** Fetched from Airtable on app init via server-side proxy. No hardcoded items in the frontend.

### Shop Dashboard
Full in-memory catalog view for browsing and curating — no additional API calls.

- Accessible via the "Catalog" button in the sidebar navigation.
- Displays all 142 items from `masterCatalog` in a responsive 4-column grid (3-col at 1200px, 2-col mobile).
- **Each card shows:** Product image, name, price (formatted in €), stock count. Low stock (≤2) shown in terracotta. Sold-out cards grayed out with a "Sold Out" badge.
- **Search bar:** Real-time filtering by item name or category.
- **Filter row:** Four dropdowns — Department (All / Womenswear / Menswear), Category (dynamically extracted from `masterCatalog`), Color (dynamically extracted), Sort (Default / Price: Low to High / Price: High to Low). All filter state is held in memory; the grid re-renders on every change without any API call.
- **Save to Client:** Each card has a "Save to Client ＋" button. Clicking opens a minimalist modal listing all clients by name and tier. Selecting a client pushes the item ID into that client's `lookbook` array and shows a toast confirmation.

### Client Curation — Lookbook
Per-client in-memory moodboard built from the live catalog.

- Every client object carries a `lookbook: []` array initialised on page load.
- Items saved via the Shop Dashboard appear as a "Curated Lookbook" section on the client's profile, rendered after the relationship sparkline and before the Communication section.
- Lookbook renders as a 4-column mini-grid of product cards (square image, name, price).
- Empty state: a subtle "No items curated yet" message.
- State is session-only until Supabase persistence is added (see Section 8b).

### Important Dates
- Birthday and anniversary alerts with 30-day countdown.
- Urgent (≤7 days) = terracotta accent.
- Passed dates show follow-up nudge for 7 days after, then disappear.
- Click row → opens client profile, scrolls to the Stylist Picks section, and pre-sets the Outreach Context dropdown to the matching occasion. Does not auto-generate picks — the CA clicks "Generate Recommendations" when ready.

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
- Gender: `gender` field (`W` or `M`) — used by `generateGiftIntelligence` for catalog pre-filtering; not displayed in UI
- Curation: lookbook (array of catalog item IDs)
- Intelligence: preferences `{ colors, avoid, notes }` — CA-editable, session-persisted

**Profile layout:** Single-column vertical. Data cards at the top, followed by Last Interaction, then Stylist Picks, then History Tables. The intelligence layer (Style Intelligence + Stylist Picks) is deliberately positioned where the CA needs it — not buried below history.

**Profile cards:**
- **Client:** ID, tier badge, LTV, assigned CA, preferred contact
- **Personal:** Birthday, partner, anniversary, pet, beverage — lighter text weight (contextual layer)
- **Sizing & Style:** All sizes, preferred colours, Never Show (terracotta warning row)
- **Last Transaction:** Item, SKU, date, boutique, alterations, aftercare
- **Current Status:** Urgency, CA action (dominant), follow-up due, last interaction (dimmed)
- **Appointment:** Date, location, Google Calendar sync indicator, aftercare follow-up with + Add button

**Style Intelligence section:** Editable panel that sits directly above Stylist Picks. Three fields:
- **Preferred Colors** — placeholder shows the client's onboarding value (`Onboarding: Ivory, Camel`). Any value entered here is merged additively with the onboarding data — both are sent to the AI.
- **Items / Colors to Avoid** — placeholder shows the onboarding avoid list. Entered values merge with onboarding avoid data. This combined list is the SUPREME hard-filter in the AI prompt — no item survives if it contains an avoided color.
- **CA Private Notes** — freeform context the AI receives as `finalNotes`; use for behavioural cues that don't belong in a CRM.

All three fields write to `c.preferences` in memory via `saveStylePref()` on every keystroke. No save button needed. Preference resolution in `buildGiftsPrompt`:
```javascript
finalColors = [c.colors, c.preferences.colors].filter(Boolean).join(', ')
finalAvoid  = [c.avoid,  c.preferences.avoid ].filter(Boolean).join(', ')
finalNotes  = [c.preferences.notes].filter(Boolean).join(' | ')
```

**Interaction history:** Last interaction note displayed prominently. Previous 3 interactions shown below. Full transaction log accessible.

**Relationship sparkline:** Visual trajectory of the relationship.

**Curated Lookbook:** Mini-grid of catalog items saved from the Shop Dashboard.

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
The Airtable API key must never be called directly from the frontend. All Airtable requests route through `/api/chat.js` as a `type: 'catalog'` request. The Shop Dashboard reads from `masterCatalog` in memory — it never makes its own Airtable call.

**Rule 5 — Maintain single-file frontend discipline.**
`index.html` is the entire frontend. Do not split into multiple JS or CSS files. Keeps deployment simple and reduces inspection surface area.

**Rule 6 — Response shapes are internal.**
The JSON field names used in AI responses (`opening`, `conversation`, `action`, `logEntry`, `newPreferences`, etc.) should not be exposed in UI labels in ways that reveal the underlying prompt architecture.

---

## 4. Codebase Structure

```
final/
├── index.html          ← Entire frontend (~7,905 lines, single file)
├── api/
│   └── chat.js         ← Vercel serverless backend (all AI prompts + Airtable proxy)
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
- `Libre Baskerville` — serif, data values in profile cards and product names
- `DM Sans` — sans-serif, all UI labels, buttons, metadata, filter controls

**Layout:** Fixed sidebar (260px) + scrollable content area. Mobile-responsive with collapsible sidebar.

**Key Data Structures:**
```javascript
const clients = [...]           // 20 client objects — each carries lookbook: [] and preferences: {}
const histories = {...}         // interaction + transaction history, keyed by client ID
let masterCatalog = []          // populated on init via fetchCatalogFromAirtable()
const catalogById = {}          // lookup map built from masterCatalog after fetch
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
const aiGiftReasoning = {};  // clientId → string (AI's expert feedback when 0 picks survive filtering)
const advisorNotes = {};     // clientId → [{id, text, date}]
const giftActions = {};      // giftId → 'shipped' | 'reserved'
const flaggedClients = new Set();
const arrivedClients = new Set();
```

**Shop Dashboard State:**
```javascript
window._shopQuery          = '';      // live search input value
window._shopFilterGender   = 'All';   // 'All' | 'Women' | 'Men'
window._shopFilterCategory = 'All';   // dynamic — any category string from masterCatalog
window._shopFilterColor    = 'All';   // dynamic — any color string from masterCatalog
window._shopSortPrice      = 'None';  // 'None' | 'asc' | 'desc'
```

**Key Functions:**
| Function | Description |
|---|---|
| `renderDashboard()` | Builds full dashboard with stats, appointment cards, important dates, needs attention |
| `renderProfile()` | Builds single-column client profile: data cards → Last Interaction → Style Intelligence → Stylist Picks → History → Lookbook → Communication |
| `renderList()` | Renders sidebar client list filtered to active CA |
| `generateBriefing()` | POST `/api/chat` type:briefing |
| `generateAIDebrief(id)` | POST `/api/chat` type:debrief |
| `generateCommDraft(clientId)` | POST `/api/chat` type:message |
| `triggerStyleRecommendations(clientId)` | Reads the Outreach Context dropdown, clears `aiGiftCache`, updates button state, calls `generateGiftIntelligence` |
| `generateGiftIntelligence(clientId, occasion)` | Gender pre-filter → field strip to `{id, name, category, colors}` → 40-item cap → POST `/api/chat` type:gifts. Caches result in `aiGiftCache` |
| `saveStylePref(clientId, key, value)` | Writes CA-entered preference directly to `clients[x].preferences[key]` in memory |
| `fetchCatalogFromAirtable()` | POST `/api/chat` type:catalog — populates `masterCatalog` and `catalogById` on init |
| `goShop()` | Clears selected client, updates nav state, calls `renderList()` + `renderShopDashboard()` |
| `renderShopDashboard()` | Applies all shop filter state to `masterCatalog`, renders product grid + filter controls |
| `renderShopCard(item)` | Returns HTML string for a single catalog card with sold-out logic |
| `openClientPicker(itemId)` | Appends client selection modal to body; dismisses on backdrop click |
| `saveToClient(itemId, clientId)` | Pushes item ID into `client.lookbook`, shows toast, refreshes profile if open |
| `renderLookbook(clientId)` | Returns "Curated Lookbook" section HTML — mini-grid or empty state |
| `loginCA()` | Handles CA selection, filters dashboard, personalises greeting |
| `toggleVoiceNote(id)` | Web Speech API mic toggle |
| `logActivity(clientId, type, title, detail)` | Stamps active CA name on every log entry |
| `apptCountdown(dateStr)` | Returns styled countdown chip HTML |
| `getBriefingAppointmentContext(c)` | Returns urgency string for briefing prompt |
| `buildLoginScreen()` | Populates CA selector on dark login screen |

---

## 5. API & Prompt Architecture

All AI and Airtable calls route through `/api/chat.js` on Vercel. The frontend never builds prompts or holds API keys.

### Request Types

**`type: 'catalog'`**
```javascript
// Frontend sends:
{ type: 'catalog' }

// chat.js paginates through Airtable with offset until all records fetched.
// Returns:
{ catalog: [{ id, airtableId, name, category, gender, price, priceNum, stock, sku, colors, img, description }, ...] }
// 142 items (80W + 62M) on first load
```

**`type: 'stock'`**
```javascript
// Frontend sends (fire-and-forget after Ship Now action):
{ type: 'stock', airtableId: 'recXXX', newStock: 2 }

// chat.js issues PATCH to Airtable Catalog table.
// Returns:
{ ok: true }
```

**`type: 'briefing'`**
```javascript
// Frontend sends:
{ type: 'briefing', client: c, mood: 'Relaxed', appointmentContext: '...' }

// Returns JSON:
{
  opening: "...",       // Client Intelligence section
  conversation: "...",  // Conversation Guide section
  action: "...",        // Action Items section
  alerts: ["..."],      // Critical flags, max 2
  tags: ["...","..."]   // 3-4 descriptor tags
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
// Frontend sends (after pre-filter):
{ type: 'gifts', client: c, occasion: 'Just Because', catalog: aiCatalog }
// aiCatalog is gender-filtered (W/U or M/U), field-stripped to {id, name, category, colors} only,
// and hard-capped at 40 items. img, sku, priceNum, description are stripped before the call.
// Payload is ~80% smaller than the full catalog.
// client object includes c.preferences {colors, avoid, notes} — used in the prompt to resolve
// preferred/avoid colours before falling back to the Airtable-sourced c.colors / c.avoid fields.

// Returns one of two JSON shapes:
// Success (3 picks):
[{ id: "W-001", reason: "..." }, ...]
// Zero picks (conflict resolution triggered):
{ "gifts": [], "reasoning": "My apologies. Based on your current strict restrictions (Avoid: ...), there are no items in the current collection that meet your standards." }
// max_tokens: 400
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

### Model
`claude-sonnet-4-20250514` — hardcoded server-side. Never exposed to the frontend.

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

## 7. Airtable Integration — Live

The Airtable integration is fully complete. All steps described in the previous version of this document as "next steps" have been implemented and are live.

### What is Live

| Feature | Status |
|---|---|
| `type: 'catalog'` endpoint in `chat.js` | Live — paginated fetch, all 142 records |
| `fetchCatalogFromAirtable()` called on app init | Live — runs before first gift request |
| Hardcoded `masterCatalog` and `prebuiltGiftSelections` | Removed entirely |
| Prompt uses `PriceNum` + spend guidance by tier (not legacy tier codes) | Live |
| Catalog guard (empty catalog check before generation) | Live |
| Stylist Picks: on-demand trigger with Outreach Context dropdown | Live — `triggerStyleRecommendations()` |
| Stylist Picks: "Generate Recommendations" → "Refresh Picks" after first run | Live |
| Stylist Picks: positioned after Last Interaction, before History Tables | Live |
| Style Intelligence section (Preferred Colors, Avoid, CA Notes) | Live — writes to `c.preferences` in memory |
| AI colour rules: cross-reference catalog `colors` field against avoid list | Live — mandatory COLOUR RULES block in prompt |
| Additive preference merge (onboarding + UI fields combined) | Live — `finalColors`/`finalAvoid`/`finalNotes` in `buildGiftsPrompt` |
| Conflict Resolution Protocol — avoid list supreme, no synonym compromises | Live — CONFLICT RESOLUTION PROTOCOL block in prompt |
| Expert Feedback — `{gifts:[], reasoning}` when 0 picks survive filtering | Live — displayed in Stylist Picks grid via `aiGiftReasoning` |
| `type: 'stock'` write-back on Ship Now | Live — PATCH to Airtable on every ship action |
| Pre-filter: gender + 40-item cap + strip to `{id, name, category, colors}` | Live — runs inside `generateGiftIntelligence` |

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
| PriceNum | Number | e.g. 3600 — used for Shop Dashboard price sort only; stripped from AI catalog payload |
| Stock | Number | Integer — decremented live on Ship Now |
| Colors | Single line text | Comma-separated |
| Image | URL | CDN URLs — plan to migrate to Cloudinary |
| Description | Single line text | Short descriptor for AI context |

### AI Payload Optimisation Detail

Before calling Claude for Stylist Picks, `generateGiftIntelligence` applies three filters client-side:

1. **Gender filter:** Reduces 142 items to ~70–80 relevant to the client's gender (W/U or M/U).
2. **Hard cap:** Slices the filtered array to a maximum of 40 items.
3. **Field strip:** Maps to `{ id, name, category, colors }` only. Removes `img`, `sku`, `priceNum`, and `description`. The `colors` field is now **retained** — the AI must cross-reference it against the client's avoid list before selecting any item.

Total reduction: ~80% smaller payload than the full catalog on average.

A `console.log` statement in the function reports the reduction:
```
[Gift Catalog] Full: 142 → Gender-filtered: 80 → AI payload: 40 items (id/name/category/colors only)
```

### Verification
Open browser console on the live Vercel URL. On page load you should see:
```
Catalog loaded: 142 items from Airtable
```
Then open any client profile, fill in a "Items / Colors to Avoid" value in the Style Intelligence section, and generate Stylist Picks. All 3 selections will reference real catalog items with W-001/M-001 IDs, and none will contain the avoided color. Ship Now will decrement stock in Airtable immediately.

---

## 8. Future Roadmap

### 8a. Supabase Integration

**Why Supabase:** PostgreSQL database + auth + real-time in one. Enables persistent memory, proper CA logins, multi-boutique isolation, and the audit trails enterprise buyers require.

**Auth Strategy:**
- Current CA selector stays for public demo — creates anonymous Supabase session
- Real boutiques: magic link auth (CA receives email, clicks link, authenticated — no password)
- "Continue as Guest" creates anonymous session with full functionality
- "Request Access" path for boutiques wanting real accounts
- Row-level security: CA-101 can only read rows where `ca_id = CA-101`

**Database Schema:**
```sql
clients          (id, name, tier, ltv, ca_id, contact, location, birthday, partner,
                  anniversary, pet, beverage, size_top, size_bottom, shoe, jewelry,
                  colors, avoid, last_date, last_type, last_note, last_purchase,
                  sku, urgency, ca_action, appointment, follow_up, alterations, aftercare)

interactions     (id, client_id, date, type, note, ca_id, created_at)
transactions     (id, client_id, date, item, sku, amount, location)
post_visit_notes (id, client_id, text, ca_id, ai_generated, created_at)
activity_logs    (id, client_id, type, title, detail, ca_id, created_at)
advisor_notes    (id, client_id, text, ca_id, created_at)
ca_profiles      (id, name, location, email)
lookbook_items   (id, client_id, catalog_item_id, ca_id, created_at)
```

**Memory (what Supabase unlocks):**
Currently all session data resets on page refresh. With Supabase: CA accepts a debrief → writes to `interactions` table → next CA opens same client, sees that debrief in the history. The `lookbook_items` table persists client curation across sessions. The relationship memory is real and shared across the team.

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

### 8b. CRM Integration Strategy

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

### 8c. Slack / Teams Notifications

- When AI Debrief accepted: post summary to boutique's floor channel — "Sophie logged a visit with Eleanor Vance. Follow-up scheduled 1 April. New preference: sparkling water instead of champagne."
- 48 hours before client birthday/anniversary: ping assigned CA
- When briefing generated for same-day appointment: quiet notification to boutique manager
- When handover submitted: notify floor channel
- Implementation: Slack webhook URL stored as Vercel env var, triggered server-side from `chat.js`

### 8d. Outfit Recommendations

- **Hard dependency:** Real product images in catalog (Cloudinary migration)
- **Prompt logic:** Given client profile + live catalog, suggest 2-3 pieces that work together as a look for the upcoming appointment occasion
- **Placement:** Inside briefing as "Suggested Look" section, or as separate tab alongside Stylist Picks
- **Requirement:** Sufficient catalog depth per gender category to make combinations feel intentional — 30+ well-photographed items minimum before this feature lands well

### 8e. Google Calendar Real Connection

- Currently simulated via sync indicator and animated dot
- Real implementation: OAuth connection, read actual CA calendar, display real appointments in profile
- Appointment data feeds into `getBriefingAppointmentContext()` automatically — no manual date entry

### 8f. Outfit Builder in Shop Dashboard

- Extend Shop Dashboard with a "Build a Look" mode
- CA selects 2-3 items from the catalog and assigns them as a curated outfit to a client
- Looks stored alongside the Lookbook on the client profile
- Requires Cloudinary image migration for stable image URLs

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

*Document version: April 2026. Reflects live production codebase with Airtable integration, Shop Dashboard, Client Lookbook, Style Intelligence section, on-demand Stylist Picks with Outreach Context, additive preference merging (onboarding + UI data), Conflict Resolution Protocol (avoid list is supreme), Expert Feedback on zero-pick scenarios, and aggressive AI cost optimisation (id/name/category/colors only, 40-item cap, ~80% payload reduction). Last updated by Mert Turan.*
