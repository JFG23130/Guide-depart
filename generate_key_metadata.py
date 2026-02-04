#!/usr/bin/env python3
"""
Générer une liste des clés avec leurs numéros de ligne et fichiers sources
"""

import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, 'assets')

# Dictionnaire pour stocker les métadonnées
key_metadata = {}

# Fichiers de langue à analyser
lang_files = {
    'assets/lang-fr.js': 'FR',
    'assets/lang-en.js': 'EN',
    'assets/lang-de.js': 'DE',
    'assets/lang-es.js': 'ES'
}

print("📊 Analyse des fichiers de langue...")

for filepath, lang in lang_files.items():
    full_path = os.path.join(base_dir, filepath)
    
    if not os.path.exists(full_path):
        print(f"⚠️ {filepath} non trouvé")
        continue
    
    print(f"\n🔍 Analyse {filepath}...")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Chercher les définitions de clés
    # Pattern: "clé": "valeur"
    pattern = r'"([^"]+)"\s*:\s*'
    
    for line_num, line in enumerate(lines, 1):
        match = re.search(pattern, line)
        if match:
            key = match.group(1)
            
            # Ignorer les commentaires et les non-clés
            if key and not line.strip().startswith('//'):
                if key not in key_metadata:
                    key_metadata[key] = []
                
                key_metadata[key].append({
                    'file': filepath,
                    'lang': lang,
                    'line': line_num
                })

print(f"\n✅ {len(key_metadata)} clés trouvées")

# Générer le fichier JavaScript
output_content = '''// Métadonnées des clés de traduction (auto-généré)
// Mappe chaque clé à son fichier source et numéro de ligne

const keyMetadata = {
'''

for key in sorted(key_metadata.keys()):
    sources = key_metadata[key]
    # Prendre la première source (généralement FR)
    source = sources[0]
    
    output_content += f'    "{key}": {{\n'
    output_content += f'        file: "{source["file"]}",\n'
    output_content += f'        lang: "{source["lang"]}",\n'
    output_content += f'        line: {source["line"]}\n'
    output_content += f'    }},\n'

output_content += '};\n'

output_file = os.path.join(base_dir, 'assets', 'key-metadata.js')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

print(f"✅ Fichier généré: {output_file}")
