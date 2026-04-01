#!/usr/bin/env python3
"""
BlackBook Gift Pre-Generator
────────────────────────────
Calls Claude once per client, generates 6 personalised gift selections,
and bakes the results into index.html as a static prebuiltGiftSelections object.

Run from ~/Desktop/blackbook/final/:
  python3 generate_gifts.py

Requires:
  pip3 install anthropic
  export ANTHROPIC_API_KEY=sk-ant-...
"""

import json, os, re, sys, time
import anthropic

# ── CONFIG ────────────────────────────────────────────────────────────────────
INDEX_PATH   = os.path.join(os.path.dirname(__file__), 'index.html')
API_KEY      = os.environ.get('ANTHROPIC_API_KEY', '')
MODEL        = 'claude-sonnet-4-20250514'
MAX_TOKENS   = 800
DELAY_SECS   = 0.8   # polite delay between calls

if not API_KEY:
    print("✗ ANTHROPIC_API_KEY not set.\n  Run: export ANTHROPIC_API_KEY=sk-ant-...")
    sys.exit(1)

# ── LOAD DATA FROM index.html ─────────────────────────────────────────────────
print("Reading index.html…")
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract clients
clients_match = re.search(r'const clients = (\[.*?\]);', content, re.DOTALL)
clients = json.loads(clients_match.group(1))
print(f"  {len(clients)} clients loaded")

# Extract catalog
cat_start = content.find('const masterCatalog = [')
cat_end   = content.find('\nconst catalogById = {}', cat_start)
cat_block = content[cat_start:cat_end]
items = re.findall(
    r"\{ id:'(T\d-\d+)', tier:(\d+), name:'([^']+?)'.*?category:'([^']+)'.*?gender:'([^']+)'.*?price:'([^']+)'.*?priceNum:(\d+).*?stock:(\d+).*?colors:\[([^\]]+)\].*?img:'([^']*)' \}",
    cat_block
)
catalog = []
for m in items:
    id_, tier, name, cat, gender, price, priceNum, stock, colors_raw, img = m
    colors = [c.strip().strip("'") for c in colors_raw.split(',')]
    catalog.append({
        'id': id_, 'tier': int(tier), 'name': name.strip(), 'category': cat,
        'gender': gender, 'price': price, 'priceNum': int(priceNum),
        'stock': int(stock), 'colors': colors
    })
print(f"  {len(catalog)} catalog items loaded")

# ── TIER GUIDANCE ──────────────────────────────────────────────────────────────
TIER_GUIDE = {
    'VVIC':     'Prioritise Tier 5–6 (fine jewellery, bags, outerwear). Tier 1–2 only as a thoughtful accent alongside a hero piece.',
    'VIC':      'Focus on Tier 4–6. Mix one statement Tier 6 with complementary Tier 3–4 items.',
    'Platinum': 'Tier 3–5 is the sweet spot. One Tier 6 item if the occasion warrants.',
    'Gold':     'Tier 2–4 range. Avoid the very top of Tier 6 unless the occasion is exceptional.',
    'Silver':   'Tier 1–3. Aspirational but appropriate for this relationship stage.'
}

# ── PROMPT BUILDER ─────────────────────────────────────────────────────────────
def build_prompt(client, catalog, occasion='Important Date'):
    tier_advice = TIER_GUIDE.get(client['tier'], 'Mix tiers thoughtfully.')
    catalog_json = json.dumps(catalog, ensure_ascii=False)
    return f"""You are a luxury gift recommendation engine for a high-end fashion house. Select exactly 6 items from the catalog that best match this client.

CLIENT PROFILE:
Name: {client['name']} | Tier: {client['tier']} | LTV: {client['ltv']} | Location: {client['location']}
Occasion: {occasion}
Preferred colours: {client['colors']}
Avoid / never show: {client['avoid']}
Sizes: Top {client['sizeTop']} / Bottom {client['sizeBottom']} / Shoe {client['shoe']}
Jewellery sizing: {client.get('jewelry', 'not specified')}
Last purchase: {client['lastPurchase']} — avoid near-identical repeat
Last CA note: "{client['lastNote']}"
Partner: {client['partner']} | Pet: {client['pet']}

TIER SPEND GUIDANCE FOR {client['tier']}:
{tier_advice}

RULES:
- Exactly 6 items, all from the catalog
- Vary categories — no more than 2 from the same category
- Match preferred colours, strictly exclude avoid list
- Follow tier spend guidance
- For footwear: only recommend if shoe size is on file
- Stock ≤ 1: only if exceptional fit
- Occasion calibration: anniversary = elevated/romantic, birthday = personal/celebratory

REASON WRITING (critical):
- 1–2 sentences per item
- Reference a specific profile detail (colour, location, partner, size, occasion, last purchase)
- Never write generic copy — be specific to this client
- Tone: warm insider, briefing a trusted colleague

CATALOG:
{catalog_json}

Respond ONLY with a valid JSON array, no markdown, no backticks:
[
  {{"id": "T#-###", "reason": "..."}},
  {{"id": "T#-###", "reason": "..."}},
  {{"id": "T#-###", "reason": "..."}},
  {{"id": "T#-###", "reason": "..."}},
  {{"id": "T#-###", "reason": "..."}},
  {{"id": "T#-###", "reason": "..."}}
]"""

# ── GENERATE ──────────────────────────────────────────────────────────────────
client_api = anthropic.Anthropic(api_key=API_KEY)
results = {}

print(f"\nGenerating gift selections for {len(clients)} clients…\n")

for i, client in enumerate(clients, 1):
    cid  = client['id']
    name = client['name']

    # Determine occasion from upcoming important dates
    occasion = 'Important Date'
    if client.get('birthday') and client['birthday'] != 'N/A':
        occasion = 'Birthday'
    if client.get('anniversary') and client['anniversary'] not in ('N/A', 'None'):
        occasion = 'Anniversary'

    print(f"  [{i:02d}/{len(clients)}] {name} ({client['tier']}, {occasion})…", end=' ', flush=True)

    prompt = build_prompt(client, catalog, occasion)

    def try_generate(attempt=1):
        response = client_api.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{'role': 'user', 'content': prompt}]
        )
        text = response.content[0].text.strip()
        text = re.sub(r'```json|```', '', text).strip()
        # Sanitize smart quotes and apostrophes inside JSON string values
        # Replace curly apostrophes/quotes with straight equivalents
        text = text.replace('\u2019', "'").replace('\u2018', "'")
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        # Escape any bare apostrophes inside reason strings
        # Find reason values and escape unescaped single quotes within them
        def escape_reason(m):
            return m.group(0).replace("'", "\\'")
        return json.loads(text)

    try:
        selections = None
        for attempt in range(1, 4):  # up to 3 tries
            try:
                selections = try_generate(attempt)
                break
            except json.JSONDecodeError as e:
                if attempt < 3:
                    print(f"(retry {attempt}) ", end='', flush=True)
                    time.sleep(1)
                else:
                    raise e

        if not isinstance(selections, list) or len(selections) == 0:
            raise ValueError("Empty or non-list response")

        # Validate all IDs exist in catalog
        cat_ids = {item['id'] for item in catalog}
        valid = [s for s in selections if s.get('id') in cat_ids]
        if len(valid) < len(selections):
            print(f"(⚠ {len(selections)-len(valid)} invalid IDs filtered) ", end='')

        # Strip apostrophes from reasons to prevent JS string breakage
        for s in valid:
            if 'reason' in s:
                s['reason'] = s['reason'].replace("'", "\u2019")

        results[cid] = valid[:6]
        print(f"✓ {len(valid[:6])} items")

    except Exception as e:
        print(f"✗ FAILED: {e}")
        results[cid] = []

    time.sleep(DELAY_SECS)

# ── BAKE INTO index.html ──────────────────────────────────────────────────────
print(f"\nBaking results into {INDEX_PATH}…")

results_js = 'const prebuiltGiftSelections = ' + json.dumps(results, ensure_ascii=False, indent=2) + ';\n'

# Replace existing block if present, or inject before catalogById
anchor = '\nconst catalogById = {}'
if 'const prebuiltGiftSelections = ' in content:
    content = re.sub(
        r'const prebuiltGiftSelections = \{.*?\};\n',
        results_js,
        content, flags=re.DOTALL
    )
    print("  Replaced existing prebuiltGiftSelections block")
else:
    content = content.replace(anchor, '\n' + results_js + anchor)
    print("  Injected new prebuiltGiftSelections block")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

# Summary
success = sum(1 for v in results.values() if v)
print(f"\n✓ Done. {success}/{len(clients)} clients have gift selections baked in.")
print(f"  Push to deploy: git add index.html && git commit -m 'data: pre-generate gift selections' && git push")
