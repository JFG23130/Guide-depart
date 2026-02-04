#!/usr/bin/env python3
"""Regénérer key-metadata.js"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Générer key-metadata.js à partir de lang-fr.js
with open('assets/lang-fr.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire les clés avec leurs numéros de ligne
lines = content.split('\n')
key_metadata = {}

for i, line in enumerate(lines, 1):
    if '":' in line and not line.strip().startswith('//'):
        match = re.match(r'\s*"([^"]+)"', line)
        if match:
            key = match.group(1)
            key_metadata[key] = {
                'file': 'lang-fr.js',
                'line': i
            }

# Écrire le fichier
output = '''// Métadonnées source des clés de traduction
// Auto-généré - mappe chaque clé à son fichier source et numéro de ligne

const keyMetadata = {
'''

for key in sorted(key_metadata.keys()):
    meta = key_metadata[key]
    output += f'    "{key}": {{ file: "{meta["file"]}", line: {meta["line"]} }},\n'

output += '};\n'

with open('assets/key-metadata.js', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'✅ key-metadata.js: {len(key_metadata)} clés')
print(f'✅ Total: {len(key_metadata)} clés avec métadonnées complètes')
