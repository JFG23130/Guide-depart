#!/usr/bin/env python3
"""Identifier les clés manquantes dans les langues"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Récupérer les clés FR
with open('assets/lang-fr.js', 'r', encoding='utf-8') as f:
    fr_keys = set(re.findall(r'^\s+"([^"]+)":', f.read(), re.MULTILINE))

# Vérifier les autres langues
for lang in ['en', 'de', 'es']:
    with open(f'assets/lang-{lang}.js', 'r', encoding='utf-8') as f:
        lang_keys = set(re.findall(r'^\s+"([^"]+)":', f.read(), re.MULTILINE))
    
    missing = fr_keys - lang_keys
    
    if missing:
        print(f'🔴 {lang.upper()} manquant {len(missing)} clés:')
        for key in sorted(missing):
            print(f'  - {key}')
    else:
        print(f'✅ {lang.upper()} complet')
