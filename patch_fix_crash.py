#!/usr/bin/env python3
"""
Run from your blackbook/final folder:
  python3 patch_fix_crash.py
"""

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    c = f.read()

# The C-1013 array was inserted without trailing comma, causing crash
# Find the bad closing and fix it
old = "    { id:'G1013F', name:'Gold Chain Bracelet', category:'Jewellery', price:'€1,800', stock:5, sku:'JWL-W-BRC-GD06', img:'https://www.prada.com/content/dam/pradabkg_products/2/230/230745/1WQ8F0002/230745_1WQ8_F0002_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg', reason:`Neck: 42cm on file — bracelet avoids fit risk. Gold, no dark. Lorenzo-appropriate anniversary gift.` },\n  ]\n};"
new = "    { id:'G1013F', name:'Gold Chain Bracelet', category:'Jewellery', price:'€1,800', stock:5, sku:'JWL-W-BRC-GD06', img:'https://www.prada.com/content/dam/pradabkg_products/2/230/230745/1WQ8F0002/230745_1WQ8_F0002_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg', reason:`Neck: 42cm on file — bracelet avoids fit risk. Gold, no dark. Lorenzo-appropriate anniversary gift.` },\n  ],\n};"

if old in c:
    c = c.replace(old, new)
    print("Fixed: trailing comma added to C-1013 array")
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(c)
    print("\nNow push:")
    print("  git add index.html && git commit -m 'fix crash: trailing comma' && git push")
else:
    # Try alternate — maybe it's ]\n}; with different spacing
    import re
    match = re.search(r"(G1013F.*?`),\n  \]\n\};", c, re.DOTALL)
    if match:
        print("Found alternate pattern — already has comma, issue elsewhere")
        print(repr(c[match.end()-20:match.end()+5]))
    else:
        # Show what's around G1013F
        idx = c.find('G1013F')
        if idx > 0:
            print("G1013F context:")
            print(repr(c[idx+200:idx+280]))
        else:
            print("G1013F not found — catalogues may not have inserted")
