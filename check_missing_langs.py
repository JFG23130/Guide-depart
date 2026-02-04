#!/usr/bin/env python3
"""Identifier les clés HTML sans traduction"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lire lang-fr.js
with open('assets/lang-fr.js', encoding='utf-8') as f:
    lang_content = f.read()

lang_keys = set(re.findall(r'^\s+"([\w\.]+)"', lang_content, re.MULTILINE))

# Lire html-usage.js
with open('assets/html-usage.js', encoding='utf-8') as f:
    html_content = f.read()

html_keys = set(re.findall(r'^\s+"([\w\.]+)"', html_content, re.MULTILINE))

missing_in_lang = sorted(html_keys - lang_keys)

print("Clés utilisées dans HTML mais MANQUANTES dans lang-fr.js:")
for key in missing_in_lang:
    print(f"  ⚠️ {key}")

print(f"\nTotal: {len(missing_in_lang)} clés manquantes")
print(f"Résumé: {len(lang_keys)} clés dans langue / {len(html_keys)} clés dans HTML")
