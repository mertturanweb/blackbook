#!/usr/bin/env python3
HTML_FILE = "index.html"
with open(HTML_FILE, "r", encoding="utf-8") as f:
    c = f.read()

# Find the exact end of the last line of C-1010 array
i = c.find("KNI-M-DGN-IV06")
if i == -1:
    print("ERROR: anchor not found"); exit()

# Find the }; that closes giftCatalogue — it's within 200 chars after KNI line
line_end = c.find('\n', i)           # end of G1010F line
array_close = c.find('\n  ],', line_end)  # end of C-1010 array
obj_close = c.find('\n};', array_close)   # closing }; of giftCatalogue

cut_from = obj_close      # position of \n};
cut_to   = cut_from + 3  # length of \n};

print(f"Inserting at char {cut_from}")
print(f"Context before: {repr(c[cut_from-30:cut_from+5])}")

URLS = [
    "https://www.prada.com/content/dam/pradabkg_products/1/1BA/1BA863/2CYSF0009/1BA863_2CYS_F0009_V_YO0_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/3/396/39610/189PF065G/39610_189P_F065G_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/P/P3R/P3R43/187QF0005/P3R43_187Q_F0005_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/P/P24/P24B3E/19IMF0EJ5/P24B3E_19IM_F0EJ5_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/4/4E1/4E1165/3D8CF0F24/4E1165_3D8C_F0F24_F_G001_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/2/2VC/2VC034/2FKLF0Y30/2VC034_2FKL_F0Y30_V_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1GG/1GG034/24ZF0002/1GG034_24Z_F0002_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/2/230/230745/1WQ8F0002/230745_1WQ8_F0002_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/U/UJN/UJN979/11CDF0009/UJN979_11CD_F0009_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1U2/1U275O/V69F0003/1U275O_V69_F0003_F_040_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1IC/1IC310/2HF1F04AZ/1IC310_2HF1_F04AZ_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1I1/1I188O/070F0002/1I188O_070_F0002_F_D055_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
]

new_entries = f"""
  ],
  'C-1011': [
    {{ id:'G1011A', name:'Fuchsia Embellished Clutch', category:'Bag', price:'€2,800', stock:3, sku:'BAG-W-CLT-FCH01', img:'{URLS[0]}', reason:`Bold fuchsia — her signature colour. Embellished hardware aligns with her festive aesthetic.` }},
    {{ id:'G1011B', name:'Saffron Silk Scarf', category:'Accessory', price:'€920', stock:5, sku:'ACC-W-SCF-SF02', img:'{URLS[1]}', reason:`Saffron is her stated palette. Silk, lightweight — perfect for the Maldives trip.` }},
    {{ id:'G1011C', name:'Gold Statement Earrings', category:'Jewellery', price:'€3,200', stock:2, sku:'JWL-W-EAR-GD03', img:'{URLS[2]}', reason:`Ring size 54 on file. Gold tone, bold drop — complements her Diwali and gala wardrobe.` }},
    {{ id:'G1011D', name:'Printed Resort Kaftan', category:'RTW', price:'€4,100', stock:2, sku:'DRE-W-KAF-PR04', img:'{URLS[3]}', reason:`Size FR40. Resort wear is exactly what she asked for. Bold print, no black or beige.` }},
    {{ id:'G1011E', name:'Fuchsia Strappy Sandal', category:'Footwear', price:'€1,100', stock:4, sku:'SHO-W-SND-FCH05', img:'{URLS[4]}', reason:`Size 38. Fuchsia tone. Open sandal — ideal for Maldives. Arjun would approve.` }},
    {{ id:'G1011F', name:'Gold Embroidered Evening Bag', category:'Bag', price:'€5,800', stock:1, sku:'BAG-W-EMB-GD06', img:'{URLS[5]}', reason:`Only 1 remaining. Gold embroidery, no black. Occasion bag for upcoming gala season.` }},
  ],
  'C-1015': [
    {{ id:'G1015A', name:'Black Sculptural Tote', category:'Bag', price:'€4,200', stock:2, sku:'BAG-W-SCL-BK01', img:'{URLS[5]}', reason:`Architectural silhouette. Black — her core colour. No classic cuts.` }},
    {{ id:'G1015B', name:'Red Leather Gloves', category:'Accessory', price:'€780', stock:3, sku:'ACC-W-GLV-RD02', img:'{URLS[6]}', reason:`Red is her accent colour. Leather, avant-garde edge. Ring: 50 — gloves are size-safe.` }},
    {{ id:'G1015C', name:'Geometric Gold Cuff', category:'Jewellery', price:'€4,800', stock:2, sku:'JWL-W-CUF-GD03', img:'{URLS[7]}', reason:`Sculptural form. Gold, no florals. Pairs with her deconstructed silhouettes.` }},
    {{ id:'G1015D', name:'Asymmetric Black Cape', category:'RTW', price:'€9,200', stock:1, sku:'COA-W-CAP-BK04', img:'{URLS[8]}', reason:`Size FR34. Black, deconstructed. Front row energy. Only 1 left — priority piece.` }},
    {{ id:'G1015E', name:'Black Platform Heel', category:'Footwear', price:'€1,400', stock:3, sku:'SHO-W-HEL-BK05', img:'{URLS[9]}', reason:`Size 35.5. Black, architectural heel. Statement footwear, avoids classic cuts.` }},
    {{ id:'G1015F', name:'Structured Black Card Case', category:'Accessory', price:'€580', stock:6, sku:'ACC-W-CDH-BK06', img:'{URLS[10]}', reason:`Minimal, black, no florals. Practical gift that fits her aesthetic precisely.` }},
  ],
  'C-1013': [
    {{ id:'G1013A', name:'Turquoise Woven Tote', category:'Bag', price:'€3,800', stock:3, sku:'BAG-W-WOV-TQ01', img:'{URLS[0]}', reason:`Turquoise is her signature. Woven tote — she loved her last one. Anniversary escalation.` }},
    {{ id:'G1013B', name:'Gold Hoop Earrings', category:'Jewellery', price:'€2,800', stock:4, sku:'JWL-W-EAR-GD02', img:'{URLS[2]}', reason:`Lorenzo bought her earrings last anniversary — step up with a finer pair. No dark tones.` }},
    {{ id:'G1013C', name:'Coral Linen Shirt Dress', category:'RTW', price:'€2,800', stock:2, sku:'DRE-W-LIN-CR03', img:'{URLS[3]}', reason:`Size IT42. Coral — her primary colour. Perfect for Monaco summer and boat trips.` }},
    {{ id:'G1013D', name:'Ivory Silk Scarf', category:'Accessory', price:'€780', stock:7, sku:'ACC-W-SCF-IV04', img:'{URLS[1]}', reason:`Light tone, no dark. UV-protective silk layer. Nautical context — exactly what she needs.` }},
    {{ id:'G1013E', name:'Turquoise Strappy Sandal', category:'Footwear', price:'€980', stock:3, sku:'SHO-W-SND-TQ05', img:'{URLS[11]}', reason:`Size 39. Open toe, avoids dark tones. Boat trip and Monaco waterfront ready.` }},
    {{ id:'G1013F', name:'Gold Chain Bracelet', category:'Jewellery', price:'€1,800', stock:5, sku:'JWL-W-BRC-GD06', img:'{URLS[7]}', reason:`Neck: 42cm on file — bracelet avoids fit risk. Gold, no dark. Lorenzo-appropriate anniversary gift.` }},
  ],
}};"""

# Replace the \n}; at obj_close with the new entries (which end with };)
c = c[:cut_from] + new_entries + c[cut_to:]

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(c)

# Verify
count = c.count('G1011A')
print(f"G1011A appears {count} time(s) — should be 1")
print(f"G1013F appears {c.count('G1013F')} time(s) — should be 1")
if count == 1:
    print("\nDone. Push:")
    print("  git add index.html && git commit -m 'add gift catalogues' && git push")
else:
    print("\nWARNING: still duplicated — do not push")
