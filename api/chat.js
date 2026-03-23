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

  const { type, client: c, mood, tone, replyContext, occasion, catalog, rawNotes, history } = req.body;

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

Client mood/energy today (CA assessment): ${mood || 'Relaxed'} — adjust your briefing tone and what you prioritise accordingly. If Relaxed: warm and exploratory. If Busy: concise, direct, pre-select fewer options. If Celebrating: lean into the moment. If Difficult: flag sensitivities, give CA tools to de-escalate.

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

    const tierGuide = {
      'VVIC':     'Prioritise Tier 5–6 items (fine jewellery, bags, coats). Tier 1–2 only as a thoughtful accent alongside a hero piece.',
      'VIC':      'Focus on Tier 4–6. Mix one statement Tier 6 piece with complementary Tier 3–4 items.',
      'Platinum': 'Tier 3–5 is the sweet spot. One Tier 6 item if occasion warrants.',
      'Gold':     'Tier 2–4 range. Avoid the very top of Tier 6 unless the occasion is exceptional.',
      'Silver':   'Tier 1–3. Keep selections aspirational but not over-extended for this relationship stage.'
    };

    const spendGuide = tierGuide[c.tier] || 'Mix tiers thoughtfully based on the occasion.';

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

TIER SPEND GUIDANCE FOR ${c.tier}:
${spendGuide}

SELECTION RULES:
- Exactly 6 items
- Follow the tier spend guidance — tier alignment signals the maison's respect for this client's status
- Colour: match preferred colours, strictly exclude anything in the avoid list
- Categories: vary across the 6 selections — no more than 2 from the same category
- Occasion calibration: anniversary → more elevated/romantic; birthday → personal/celebratory; evergreen → versatile
- Shoe size compatibility: only recommend footwear if shoe size is on file
- Jewellery compatibility: respect ring/neck sizing if noted
- Stock: avoid items with stock of 1 unless they are an exceptional match
- Last purchase: do not repeat the same category twice in a row if avoidable
- Gender: infer appropriate gender targeting from the client's name and profile

REASON WRITING:
- Each reason must be 1–2 sentences
- Reference a specific profile detail (colour preference, location, occasion, partner, size, LTV tier)
- Never write generic copy like "a timeless piece" — be specific to this client
- Tone: warm, insider, like briefing a trusted colleague

CATALOG:
${catalogJson}

Respond ONLY with a valid JSON array — no markdown, no backticks, no explanation:
[
  { "id": "T#-###", "reason": "..." },
  { "id": "T#-###", "reason": "..." },
  { "id": "T#-###", "reason": "..." },
  { "id": "T#-###", "reason": "..." },
  { "id": "T#-###", "reason": "..." },
  { "id": "T#-###", "reason": "..." }
]`;
  }


  function buildDebriefPrompt() {
    const historyJson = JSON.stringify(history || {}, null, 2);
    return `You are a luxury clienteling intelligence system. A Client Advisor has just finished a visit with ${c.name} (${c.tier}, LTV ${c.ltv}) and left raw notes. Your job is to turn those raw notes into a polished interaction log entry — matching the tone and style of existing entries in this client's history.

CLIENT:
Name: ${c.name} | Tier: ${c.tier} | LTV: ${c.ltv}
Preferred colours: ${c.colors} | Avoid: ${c.avoid}
Last purchase: ${c.lastPurchase} on ${c.purchaseDate}
Current CA action: ${c.caAction} | Urgency: ${c.urgency}

EXISTING INTERACTION HISTORY (match this tone exactly):
${historyJson}

CA'S RAW NOTES FROM TODAY'S VISIT:
"${rawNotes}"

RULES:
- Log entry: 1–2 sentences max. Factual, warm, written in past tense. Match the style of existing interaction notes exactly — short, specific, no fluff.
- Extract any new preferences mentioned (colours, categories, fits, occasions, people). Only real ones from the notes, not inferred.
- Suggest a follow-up date: realistic based on urgency and what was discussed. Format as "15 April 2026".
- Draft a short follow-up message (2–3 sentences, via ${c.contact}) to send within the suggested timeframe. Warm, specific, references something from the visit.

Respond ONLY with valid JSON, no markdown, no backticks:
{
  "logEntry": "One or two sentences. What happened in the visit, written like the existing history entries.",
  "newPreferences": ["only if something genuinely new was mentioned — e.g. 'prefers wider lapels', 'interested in jewellery for first time'. Empty array if nothing new."],
  "followUpDate": "e.g. 15 April 2026",
  "followUpDraft": "Short follow-up message text, ready to send via ${c.contact}."
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
