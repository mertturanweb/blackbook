#!/usr/bin/env python3
"""
BlackBook — Image Embedder v2
Run from the same folder as index.html:
  python3 embed_images.py
"""

import requests, base64, re, sys, time
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "requests"], check=True)
    from PIL import Image

HTML_FILE = "index.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://www.prada.com/",
}

# 18 confirmed live Prada URLs — assigned by category and client
URLS = [
    "https://www.prada.com/content/dam/pradabkg_products/S/SC8/SC813M/172XF0YRX/SC813M_172X_F0YRX_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.1680.1680.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/S/SC7/SC781/1480F0L76/SC781_1480_F0L76_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1BA/1BA863/2CYSF0009/1BA863_2CYS_F0009_V_YO0_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/P/P3R/P3R43/187QF0005/P3R43_187Q_F0005_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/2/230/230745/1WQ8F0002/230745_1WQ8_F0002_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1U2/1U275O/V69F0003/1U275O_V69_F0003_F_040_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/4/4E1/4E1165/3D8CF0F24/4E1165_3D8C_F0F24_F_G001_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/S/SPS/SPSB01/E591FE753/SPSB01_E591_FE753_C_040_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1IC/1IC310/2HF1F04AZ/1IC310_2HF1_F04AZ_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/2/2VC/2VC034/2FKLF0Y30/2VC034_2FKL_F0Y30_V_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/3/396/39610/189PF065G/39610_189P_F065G_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/P/P24/P24B3E/19IMF0EJ5/P24B3E_19IM_F0EJ5_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1I1/1I188O/070F0002/1I188O_070_F0002_F_D055_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/2/2FF/2FF041/2HFNF05A4/2FF041_2HFN_F05A4_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/S/SGC/SGC922/11C9F0SVF/SGC922_11C9_F0SVF_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/U/UJN/UJN979/11CDF0009/UJN979_11CD_F0009_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/1/1GG/1GG034/24ZF0002/1GG034_24Z_F0002_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
    "https://www.prada.com/content/dam/pradabkg_products/2/21H/21H025/18UUF0334/21H025_18UU_F0334_S_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2000.2000.jpg",
]

# Assign URLs to gift IDs — cycling through the 18 images across all 36 slots
# Bags → urls 0,1,2   Jewellery → 3,4,5   RTW → 6,7,8   Accessories → 9,10,11   Footwear → 12,13   Sunglasses/other → 14,15,16,17
GIFT_ASSIGNMENTS = {
    # Eleanor C-1001
    'G1001A': URLS[0],   # bag
    'G1001B': URLS[9],   # accessory / card holder
    'G1001C': URLS[3],   # jewellery
    'G1001D': URLS[6],   # RTW cashmere
    'G1001E': URLS[10],  # scarf
    'G1001F': URLS[14],  # small leather
    # Matteo C-1002
    'G1002A': URLS[11],  # scarf
    'G1002B': URLS[15],  # accessory
    'G1002C': URLS[9],   # card case
    'G1002D': URLS[7],   # RTW knitwear
    'G1002E': URLS[16],  # tie / accessory
    'G1002F': URLS[12],  # footwear
    # Sofia C-1003
    'G1003A': URLS[13],  # flat shoe
    'G1003B': URLS[4],   # jewellery cuff
    'G1003C': URLS[1],   # mini bag
    'G1003D': URLS[8],   # RTW knitwear
    'G1003E': URLS[17],  # belt / accessory
    'G1003F': URLS[16],  # gloves
    # Amira C-1007
    'G1007A': URLS[3],   # earrings
    'G1007B': URLS[2],   # clutch / bag
    'G1007C': URLS[5],   # bangle
    'G1007D': URLS[4],   # necklace
    'G1007E': URLS[6],   # evening RTW
    'G1007F': URLS[0],   # minaudière
    # David C-1010
    'G1010A': URLS[8],   # navy blazer RTW
    'G1010B': URLS[2],   # weekend bag
    'G1010C': URLS[7],   # vest knitwear
    'G1010D': URLS[17],  # belt
    'G1010E': URLS[11],  # scarf
    'G1010F': URLS[6],   # dressing gown RTW
    # Defaults
    'GD001':  URLS[10],
    'GD002':  URLS[9],
    'GD003':  URLS[14],
    'GD004':  URLS[5],
    'GD005':  URLS[15],
    'GD006':  URLS[8],
}


def download_and_encode(url, gift_id):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))
        img = img.resize((500, 500), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=75, optimize=True)
        size_kb = len(buf.getvalue()) / 1024
        encoded = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/jpeg;base64,{encoded}", size_kb
    except Exception as e:
        print(f"\n    ✗ {gift_id}: {e}")
        return None, 0


def main():
    print(f"\n{'='*55}")
    print("  BlackBook — Prada Image Embedder v2")
    print(f"{'='*55}\n")

    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"✗ Could not find {HTML_FILE}")
        print("  Make sure this script is in the same folder as index.html")
        sys.exit(1)

    # Cache downloads — same URL used for multiple gift IDs
    url_cache = {}
    total_kb = 0
    success = 0
    failed = []

    for gift_id, url in GIFT_ASSIGNMENTS.items():
        print(f"  {gift_id}...", end=" ", flush=True)

        if url not in url_cache:
            data_uri, size_kb = download_and_encode(url, gift_id)
            url_cache[url] = (data_uri, size_kb)
            time.sleep(0.2)
        else:
            data_uri, size_kb = url_cache[url]
            print("(cached)", end=" ", flush=True)

        if data_uri:
            pattern = rf"({{[^}}]*id:'{re.escape(gift_id)}'[^}}]*img:')([^'`]+)(['`])"
            new_html = re.sub(pattern, lambda m: m.group(1) + data_uri + m.group(3), html, flags=re.DOTALL)
            if new_html != html:
                html = new_html
                print(f"✓  ({size_kb:.0f} KB)")
                total_kb += size_kb
                success += 1
            else:
                print(f"⚠  (pattern not matched — skipping)")
                failed.append(gift_id)
        else:
            failed.append(gift_id)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n{'='*55}")
    print(f"  Done — {success}/{len(GIFT_ASSIGNMENTS)} images embedded")
    print(f"  Added: {total_kb:.0f} KB ({total_kb/1024:.1f} MB) to file size")
    if failed:
        print(f"  ⚠ Failed: {', '.join(failed)}")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
