export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  const { type, client: c, mood, tone, replyContext, occasion, catalog, rawNotes, history, appointmentContext, airtableId, newStock } = req.body;

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

  if (type === 'stock') {
    try {
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
    } catch(err) {
      console.error('Airtable stock update error:', err);
      return res.status(500).json({ error: 'Failed to update stock in Airtable' });
    }
  }

  if (!type || !c) {
    return res.status(400).json({ error: 'Missing required fields: type, client' });
  }

  // ── PROMPT BUILDERS ──────────────────────────────────────────────────────────

  function buildBriefingPrompt() {
    const partnerLine  = c.partner     !== 'None' ? ` | Partner: ${c.partner}` : '';
    const anniversLine = c.anniversary !== 'N/A'  ? ` | Anniversary: ${c.anniversary}` : '';
    const petLine      = c.pet         !== 'None' ? `Pet: ${c.pet}` : '';
    const jewelryLine  = c.jewelry && c.jewelry !== 'N/A' ? ` / Jewelry: ${c.jewelry}` : '';

    return `You are a discreet, highly intelligent luxury client intelligence system used internally by Client Advisors at a major luxury fashion house. Your tone is warm, precise, and human — never robotic or clinical. Help Client Advisors deliver extraordinary, personalised service.

Generate a pre-visit briefing. Three sections only. No filler.

CLIENT:
Name: ${c.name} | Tier: ${c.tier} | LTV: ${c.ltv}
Appointment: ${c.appointment} at ${c.location}
Birthday: ${c.birthday}${partnerLine}${anniversLine}
${petLine}
Sizes: Top ${c.sizeTop} / Bottom ${c.sizeBottom} / Shoe ${c.shoe}${jewelryLine}
Preferred colours: ${c.colors} | Never show: ${c.avoid}
Beverage: ${c.beverage}
Last contact: ${c.lastDate} (${c.lastType}) — "${c.lastNote}"
Last purchase: ${c.lastPurchase} (${c.sku}) on ${c.purchaseDate}
Alterations: ${c.alterations} | Aftercare due: ${c.aftercare}
Current CA action: ${c.caAction} | Urgency: ${c.urgency}

CA's read on the client today: ${mood || 'Relaxed'}. Let this shape tone and emphasis only — never reference the mood explicitly or narrate it. Relaxed: slightly more exploratory, surface one or two additional conversation threads. Busy: tighten everything, lead with the single most important action, cut anything optional. Celebrating: let warmth come through in word choice, lean into the occasion. Difficult: stay factual and measured, give the CA concrete tools to de-escalate, flag any known sensitivities upfront.

The briefing should read like a sharp, trusted colleague handing off before a meeting. Precise. Human. No performed warmth, no filler, no lines that narrate the client's personality back at the reader.
${appointmentContext && (appointmentContext.includes('TODAY') || appointmentContext.includes('TOMORROW')) ? `\nCRITICAL — IMMINENT APPOINTMENT: ${appointmentContext}\nThe "action" section must be completely rewritten as a pre-arrival checklist. Not general recommendations — specific things the CA must do or have ready before the client walks in. Reference the exact CA action on file (${c.caAction}), the urgency (${c.urgency}), and anything from the last contact note. Write it as if the client could arrive in the next hour.` : ''}

Respond ONLY with valid JSON, no markdown, no backticks:
{
  "opening": "2-3 sentences. Who this client is and what matters most to them right now. Reference specific personal context naturally — as if briefing a trusted colleague. If they have a pet, weave it in naturally as part of who they are.",
  "conversation": "2-3 sentences. Exact topics for the Client Advisor to raise and how to frame them. Specific, not generic. Reference real details from their file. If they have a pet and are likely to bring it, note any preparation (treats by the fitting room, etc.).",
  "action": "2-3 sentences. Precise commercial action to take in this appointment. What to show, confirm, or resolve. Reference the CA action and urgency.",
  "alerts": ["Any critical alert — dates, sensitivities, restrictions. Only if genuinely important. Max 2."],
  "tags": ["3-4 short descriptor tags for this client profile"]
}`;
  }

  function buildMessagePrompt() {
    const toneDesc = tone === 'Formal'
      ? 'Refined and professional. Complete sentences. No contractions.'
      : tone === 'Warm'
      ? 'Friendly but polished. Personal without being overly casual.'
      : 'Light and conversational. Brief sentences. Tasteful personality.';

    const partnerLine  = c.partner     !== 'None' ? `- Partner: ${c.partner}` : '';
    const anniversLine = c.anniversary !== 'N/A'  ? `- Anniversary: ${c.anniversary}` : '';
    const petLine      = c.pet         !== 'None' ? `- Pet: ${c.pet}` : '';

    return `You are a luxury Client Advisor at a high-end fashion house. Write a short, personalised ${c.contact} message to ${c.name} (${c.tier} client, lifetime value ${c.ltv}).

Tone: ${tone || 'Warm'}. ${toneDesc}

Context:
- ${replyContext || 'There is no recent inbound message. Write a proactive outreach message.'}
- Last CA note: "${c.lastNote}"
- Upcoming appointment: ${c.appointment} at ${c.location}
- Urgency: ${c.urgency}
- CA action: ${c.caAction}
${partnerLine}
${anniversLine}
${petLine}
- Beverage preference: ${c.beverage}

Rules:
- Max 4 sentences total
- No emojis unless WeChat or Instagram
- Do not mention prices
- Reference one specific personal detail naturally
- Output only the message text, nothing else`;
  }

  function buildGiftsPrompt() {
    const catalogJson = JSON.stringify(catalog, null, 2);

    const spendGuide = {
      'VVIC':     'Prioritise items above €3,000. Mix statement pieces (bags, coats, fine jewellery) with one or two refined accessories. No item below €500 unless exceptional personal match.',
      'VIC':      'Focus on €1,500–€6,000. One hero piece above €3,000 with complementary items at €1,000–€2,500.',
      'Platinum': 'Sweet spot is €800–€3,500. One elevated piece if occasion warrants.',
      'Gold':     '€500–€2,500 range. Aspirational but not overextended.',
      'Silver':   '€200–€1,500. Achievable and relevant to where this relationship currently is.'
    }[c.tier] || 'Mix price points thoughtfully based on occasion and relationship stage.';

    return `You are a luxury gift recommendation engine for a high-end fashion house. Select exactly 6 items from the catalog that are the best match for this client.

CLIENT PROFILE:
Name: ${c.name} | Tier: ${c.tier} | LTV: ${c.ltv} | Location: ${c.location}
Occasion: ${occasion || 'Important Date'}
Preferred colours: ${c.colors}
Avoid / never show: ${c.avoid}
Sizes: Top ${c.sizeTop} / Bottom ${c.sizeBottom} / Shoe ${c.shoe}
Jewellery sizing: ${c.jewelry || 'not specified'}
Last purchase: ${c.lastPurchase} — avoid recommending the same or near-identical item
Last CA note: "${c.lastNote}"
Partner: ${c.partner !== 'None' ? c.partner : 'none'}
Pet: ${c.pet !== 'None' ? c.pet : 'none'}

SPEND GUIDANCE FOR ${c.tier}:
${spendGuide}

SELECTION RULES:
- Exactly 6 items
- Follow the spend guidance — price alignment signals the maison's respect for this client's status
- Use PriceNum field for price logic, not any tier field
- Gender: W items for women, M items for men, U fine for either
- Colour: match preferred colours, strictly exclude anything in the avoid list
- Categories: vary across the 6 selections — no more than 2 from the same category
- Occasion calibration: anniversary → more elevated/romantic; birthday → personal/celebratory; evergreen → versatile
- Shoe size compatibility: only recommend footwear if shoe size is on file
- Jewellery compatibility: respect ring/neck sizing if noted
- Stock: avoid items with stock of 1 unless they are an exceptional match
- Last purchase: do not repeat the same category twice in a row if avoidable

REASON WRITING:
- Each reason must be 1–2 sentences
- Reference a specific profile detail (colour preference, location, occasion, partner, size, LTV tier)
- Never write generic copy like "a timeless piece" — be specific to this client
- Tone: warm, insider, like briefing a trusted colleague

CATALOG:
${catalogJson}

Respond ONLY with a valid JSON array — no markdown, no backticks, no explanation:
[
  { "id": "...", "reason": "..." },
  { "id": "...", "reason": "..." },
  { "id": "...", "reason": "..." },
  { "id": "...", "reason": "..." },
  { "id": "...", "reason": "..." },
  { "id": "...", "reason": "..." }
]`;
  }


  function buildDebriefPrompt() {
    const historyJson = JSON.stringify(history || {}, null, 2);
    return `You are a luxury clienteling intelligence system. A Client Advisor has just finished a visit with ${c.name} (${c.tier}, LTV ${c.ltv}) and left a raw voice/text brain dump. Your job is to extract EVERYTHING useful from those notes — nothing should be lost.

CLIENT:
Name: ${c.name} | Tier: ${c.tier} | LTV: ${c.ltv}
Preferred colours: ${c.colors} | Avoid: ${c.avoid}
Beverage on file: ${c.beverage}
Last purchase: ${c.lastPurchase} on ${c.purchaseDate}
Current CA action: ${c.caAction} | Urgency: ${c.urgency}
Preferred contact: ${c.contact}

EXISTING INTERACTION HISTORY (match this tone and length exactly):
${historyJson}

CA'S RAW NOTES FROM TODAY'S VISIT:
"${rawNotes}"

YOUR JOB — extract every single detail. Do not summarise loosely. Be specific:

1. LOG ENTRY: 2-3 sentences max. Past tense. Match the style of existing history entries exactly — short, factual, specific. Include items discussed, decisions made, anything notable that happened.

2. NEW PREFERENCES: Extract EVERY new preference, change, or update mentioned — including beverage changes, style preferences, things they rejected, size notes, occasions mentioned, people mentioned. If they changed their usual drink, note it. If they rejected something, note why. Be exhaustive.

3. OPEN TASKS: Any action items the CA mentioned needing to do — things to send, follow up on, arrange. Extract these exactly as stated.

4. FOLLOW-UP DATE: Based on urgency and what was discussed, suggest a specific date. Format: "15 April 2026".

5. FOLLOW-UP DRAFT: 2-3 sentence message via ${c.contact}. Warm, specific, references something concrete from today's visit.

Respond ONLY with valid JSON, no markdown, no backticks:
{
  "logEntry": "2-3 sentences matching existing history tone. Factual, specific, past tense.",
  "newPreferences": ["every new preference, change, rejection, or update — be exhaustive, not selective"],
  "openTasks": ["every action item the CA mentioned needing to do"],
  "followUpDate": "e.g. 15 April 2026",
  "followUpDraft": "Ready-to-send message via ${c.contact}."
}`;
  }

    // ── ROUTE ────────────────────────────────────────────────────────────────────

  let prompt, max_tokens;

  if (type === 'briefing') {
    prompt = buildBriefingPrompt();
    max_tokens = 1000;
  } else if (type === 'message') {
    prompt = buildMessagePrompt();
    max_tokens = 250;
  } else if (type === 'gifts') {
    if (!catalog || !Array.isArray(catalog)) {
      return res.status(400).json({ error: 'Missing catalog array for gifts request' });
    }
    prompt = buildGiftsPrompt();
    max_tokens = 800;
  } else if (type === 'debrief') {
    if (!rawNotes) return res.status(400).json({ error: 'Missing rawNotes for debrief request' });
    prompt = buildDebriefPrompt();
    max_tokens = 600;
  } else {
    return res.status(400).json({ error: `Unknown request type: ${type}` });
  }

  // ── CALL ANTHROPIC ────────────────────────────────────────────────────────────

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens,
        messages: [{ role: 'user', content: prompt }]
      })
    });

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (err) {
    console.error('BlackBook API error:', err);
    return res.status(500).json({ error: 'Request failed' });
  }
}
