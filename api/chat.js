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

  const { type, client: c, mood, tone, replyContext } = req.body;

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

  // ── ROUTE ────────────────────────────────────────────────────────────────────

  let prompt, max_tokens;

  if (type === 'briefing') {
    prompt = buildBriefingPrompt();
    max_tokens = 1000;
  } else if (type === 'message') {
    prompt = buildMessagePrompt();
    max_tokens = 250;
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
