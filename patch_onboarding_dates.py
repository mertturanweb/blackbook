#!/usr/bin/env python3
"""
Run from your blackbook/final folder:
  python3 patch_onboarding_dates.py
"""

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    c = f.read()

patches = [
    (
        '  filtered = [...clients];\n\n  // Show success then close',
        '  filtered = [...clients];\n  renderDashboard();\n\n  // Show success then close',
        'renderDashboard after client add'
    ),
    (
        '<input class="onboarding-input" id="ob-birthday" placeholder="12 April 1982">',
        '<input class="onboarding-input" id="ob-birthday" type="date" style="color-scheme:light;">',
        'Birthday date picker'
    ),
    (
        '<input class="onboarding-input" id="ob-anniversary" placeholder="5 September 2010">',
        '<input class="onboarding-input" id="ob-anniversary" type="date" style="color-scheme:light;">',
        'Anniversary date picker'
    ),
    (
        "    birthday: g('ob-birthday') || '—',",
        """    birthday: (() => {
      const raw = g('ob-birthday');
      if (!raw) return '—';
      const d = new Date(raw + 'T00:00:00');
      if (isNaN(d)) return raw;
      return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
    })(),""",
        'Birthday format conversion'
    ),
    (
        "    anniversary: g('ob-anniversary') || 'N/A',",
        """    anniversary: (() => {
      const raw = g('ob-anniversary');
      if (!raw) return 'N/A';
      const d = new Date(raw + 'T00:00:00');
      if (isNaN(d)) return raw;
      return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
    })(),""",
        'Anniversary format conversion'
    ),
]

changed = False
for old, new, label in patches:
    if old in c:
        c = c.replace(old, new)
        print(f'{label}: OK')
        changed = True
    else:
        print(f'{label}: NOT FOUND (may already be patched)')

if changed:
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(c)
    print("\nDone — now push to GitHub:")
    print("  git add index.html && git commit -m 'fix onboarding: date pickers + dashboard refresh' && git push")
else:
    print("\nNothing changed.")
