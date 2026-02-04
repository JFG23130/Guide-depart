#!/usr/bin/env python3
"""
Générer les métadonnées d'utilisation des clés dans les fichiers HTML
Améloré pour détecter les clés même avec des caractères échappés et dans les attributs complexes
"""

import os
import re
from collections import defaultdict
import html

base_dir = os.path.dirname(os.path.abspath(__file__))

# Dictionnaire pour stocker où chaque clé est utilisée
key_usage = defaultdict(list)

print("🔍 Scan des fichiers HTML pour trouver l'utilisation des clés...")

# Chercher dans tous les fichiers HTML (sauf ceux archivés et test)
for file in os.listdir(base_dir):
    if not file.endswith('.html'):
        continue
    if file in ['test-multilang.html']:
        continue
    
    filepath = os.path.join(base_dir, file)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Chercher les attributs data-lang-key dans différents formats
        for line_num, line in enumerate(lines, 1):
            # Décoder les entités HTML d'abord
            decoded_line = html.unescape(line)
            
            # Pattern 1: data-lang-key="clé" ou data-lang-key='clé'
            matches = re.findall(r'data-lang-key=["\']([^"\']+)["\']', decoded_line)
            
            # Pattern 2: Gérer aussi les cas où &quot; n'a pas été décodé
            matches += re.findall(r'data-lang-key=&quot;([^&]+?)&quot;', line)
            
            for key in matches:
                # Nettoy les clés
                key = key.strip()
                if key and not key_usage[key]:  # Première occurrence
                    key_usage[key].append({
                        'file': file,
                        'line': line_num
                    })
    
    except Exception as e:
        print(f"⚠️ Erreur lecture {file}: {e}")

print(f"✅ {len(key_usage)} clés utilisées trouvées\n")

# Générer le fichier JavaScript
output_content = '''// Métadonnées d'utilisation des clés de traduction dans les fichiers HTML
// Auto-généré - mappe chaque clé à son utilisation dans le HTML

const htmlUsage = {
'''

for key in sorted(key_usage.keys()):
    usages = key_usage[key]
    # Prendre la première utilisation
    usage = usages[0]
    
    output_content += f'    "{key}": {{\n'
    output_content += f'        file: "{usage["file"]}",\n'
    output_content += f'        line: {usage["line"]},\n'
    output_content += f'        count: {len(usages)}\n'
    output_content += f'    }},\n'

output_content += '};\n'

output_file = os.path.join(base_dir, 'assets', 'html-usage.js')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

print(f"✅ Fichier généré: assets/html-usage.js")
print(f"📊 Total: {len(key_usage)} clés avec localisation HTML")
