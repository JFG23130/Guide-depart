#!/usr/bin/env python3
"""Comparer les clés et identifier celles sans localisation HTML"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lire lang-fr.js
with open('assets/lang-fr.js', 'r', encoding='utf-8') as f:
    lang_content = f.read()

# Extraire les clés
lang_keys = set(re.findall(r'^\s+["\']+([\w\.]+)["\']', lang_content, re.MULTILINE))

# Lire html-usage.js
with open('assets/html-usage.js', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_keys = set(re.findall(r'^\s+"([\w\.]+)"', html_content, re.MULTILINE))

missing = sorted(lang_keys - html_keys)

print(f'📊 Statistiques:')
print(f'  Total clés dans lang-fr.js: {len(lang_keys)}')
print(f'  Total clés trouvées dans HTML: {len(html_keys)}')
print(f'  ❌ Clés sans localisation HTML: {len(missing)}')
print()

if missing:
    print('Clés orphelines (définies mais jamais utilisées):')
    for key in missing:
        print(f'  - {key}')
else:
    print('✅ Toutes les clés ont une localisation HTML!')
