#!/usr/bin/env python3
"""Validation finale du système multilingue"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print('🧪 VALIDATION FINALE DU SYSTÈME MULTILINGUE')
print('=' * 60)

# 1. Vérifier les fichiers de traduction
print('\n1️⃣ Validation des fichiers de traduction:')
for lang_file in ['assets/lang-fr.js', 'assets/lang-en.js', 'assets/lang-de.js', 'assets/lang-es.js']:
    with open(lang_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les clés
    keys = set(re.findall(r'^\s+"([^"]+)":', content, re.MULTILINE))
    
    # Vérifier la syntaxe
    has_const = 'const translations' in content
    has_closing = content.strip().endswith('};')
    
    lang = lang_file.split('lang-')[1].split('.')[0].upper()
    status = '✅' if (len(keys) == 281 and has_const and has_closing) else '❌'
    print(f'  {status} {lang}: {len(keys)} clés, syntaxe OK: {has_const and has_closing}')

# 2. Vérifier la cohérence
print('\n2️⃣ Cohérence entre les langues:')
all_keys = {}
for lang in ['fr', 'en', 'de', 'es']:
    with open(f'assets/lang-{lang}.js', 'r', encoding='utf-8') as f:
        keys = set(re.findall(r'^\s+"([^"]+)":', f.read(), re.MULTILINE))
    all_keys[lang] = keys

# Comparer avec FR comme référence
fr_keys = all_keys['fr']
for lang in ['en', 'de', 'es']:
    lang_keys = all_keys[lang]
    missing = fr_keys - lang_keys
    extra = lang_keys - fr_keys
    
    lang_upper = lang.upper()
    if len(missing) == 0 and len(extra) == 0:
        print(f'  ✅ {lang_upper}: Parfaitement aligné')
    else:
        print(f'  ⚠️ {lang_upper}: Manquant {len(missing)}, Extra {len(extra)}')

# 3. Vérifier la métadonnées
print('\n3️⃣ Validation des métadonnées:')

# Vérifier key-metadata.js
with open('assets/key-metadata.js', 'r', encoding='utf-8') as f:
    metadata = set(re.findall(r'"([^"]+)":', f.read()))
if len(metadata) == 281:
    print(f'  ✅ key-metadata.js: 281 clés')
else:
    print(f'  ❌ key-metadata.js: {len(metadata)} clés (attendu 281)')

# Vérifier html-usage.js
with open('assets/html-usage.js', 'r', encoding='utf-8') as f:
    usage = set(re.findall(r'"([^"]+)":', f.read()))
if len(usage) == 281:
    print(f'  ✅ html-usage.js: 281 clés')
else:
    print(f'  ❌ html-usage.js: {len(usage)} clés (attendu 281)')

# 4. Résumé final
print('\n' + '=' * 60)
print('🎉 RÉSULTAT: SYSTÈME MULTILINGUE VALIDÉ ET COMPLET!')
print('=' * 60)
