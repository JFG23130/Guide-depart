#!/usr/bin/env python3
"""Analyser les clés orphelines"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lire lang-fr.js et extraire les clés
with open('assets/lang-fr.js', 'r', encoding='utf-8') as f:
    lang_content = f.read()

lang_keys = set(re.findall(r'^\s+"([\w\.]+)"', lang_content, re.MULTILINE))

# Lire html-usage.js
with open('assets/html-usage.js', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_keys = set(re.findall(r'^\s+"([\w\.]+)"', html_content, re.MULTILINE))

# Trouver les clés orphelines
orphans = sorted(lang_keys - html_keys)

print(f'📊 Analyse des clés:')
print(f'  Clés dans lang-fr.js: {len(lang_keys)}')
print(f'  Clés trouvées dans HTML: {len(html_keys)}')
print(f'  Clés orphelines: {len(orphans)}')
print()

if orphans:
    print('Clés définies mais jamais utilisées (orphelines):')
    for key in orphans:
        print(f'  ❌ {key}')
else:
    print('✅ Toutes les clés sont utilisées!')
