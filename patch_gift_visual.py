#!/usr/bin/env python3
"""
Run from your blackbook/final folder:
  python3 patch_gift_visual.py
"""

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    c = f.read()

old_css = """.gift-card-visual {
  width: 100%;
  aspect-ratio: 3/2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 18px 18px 14px;
  box-sizing: border-box;
  position: relative;
  background: #faf8f4;
  border-bottom: 1px solid var(--rule);
}
.gift-card-visual-category {
  font-family: 'DM Sans', sans-serif;
  font-size: 7px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: rgba(0,0,0,0.3);
}
.gift-card-visual-name {
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  font-style: italic;
  color: var(--ink);
  line-height: 1.3;
  max-width: 160px;
  margin-top: auto;
  padding-top: 12px;
}
.gift-card-visual-price {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: var(--ink-mid);
  margin-top: 6px;
}
.gift-card-visual-stock {
  position: absolute;
  top: 18px;
  right: 14px;
  font-family: 'DM Sans', sans-serif;
  font-size: 8px;
  letter-spacing: 0.5px;
  color: rgba(0,0,0,0.3);
}
.gift-card-visual-stock.low {
  color: #c47a5a;
}
.gift-card-visual-rule {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 28px;
  height: 1px;
  background: var(--gold);
  opacity: 0.6;
}"""

new_css = """.gift-card-visual {
  width: 100%;
  aspect-ratio: 1/1;
  position: relative;
  background: #f5f2ed;
  overflow: hidden;
  border-bottom: 1px solid var(--rule);
}
.gift-card-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.gift-card-visual-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px 10px;
  background: linear-gradient(to top, rgba(245,242,237,0.95) 60%, transparent);
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}
.gift-card-visual-price {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: var(--ink);
}
.gift-card-visual-stock {
  font-family: 'DM Sans', sans-serif;
  font-size: 8px;
  letter-spacing: 0.5px;
  color: var(--ink-faint);
}
.gift-card-visual-stock.low { color: #c47a5a; }
.gift-card-visual-category { display: none; }
.gift-card-visual-name { display: none; }
.gift-card-visual-rule { display: none; }"""

old_fn = """function renderGiftVisual(g, clientColors) {
  const isLow = parseInt(g.stock) <= 2;
  return `
    <div class="gift-card-visual">
      <div class="gift-card-visual-category">${g.category}</div>
      <div class="gift-card-visual-stock ${isLow ? 'low' : ''}">${isLow ? '⚠ ' : ''}${g.stock} in stock</div>
      <div class="gift-card-visual-name">${g.name}</div>
      <div class="gift-card-visual-price">${g.price}</div>
      <div class="gift-card-visual-rule"></div>
    </div>`;
}"""

new_fn = """function renderGiftVisual(g, clientColors) {
  const isLow = parseInt(g.stock) <= 2;
  const imgSrc = g.img || getCategoryImg(g.category);
  return `
    <div class="gift-card-visual">
      <img src="${imgSrc}" alt="${g.name}">
      <div class="gift-card-visual-overlay">
        <span class="gift-card-visual-price">${g.price}</span>
        <span class="gift-card-visual-stock ${isLow ? 'low' : ''}">${isLow ? '⚠ ' : ''}${g.stock} in stock</span>
      </div>
    </div>`;
}"""

ok = True
if old_css in c:
    c = c.replace(old_css, new_css)
    print("CSS: OK")
else:
    print("CSS: NOT FOUND — file may already be patched")
    ok = False

if old_fn in c:
    c = c.replace(old_fn, new_fn)
    print("JS: OK")
else:
    print("JS: NOT FOUND — file may already be patched")
    ok = False

if ok:
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(c)
    print("\nDone — now push to GitHub:")
    print("  git add index.html && git commit -m 'fix gift images' && git push")
else:
    print("\nNothing changed.")
