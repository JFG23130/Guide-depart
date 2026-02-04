#!/usr/bin/env python3
"""
Analyse des fichiers HTML utilisés et inutilisés dans le projet
"""

import os
import re
from collections import defaultdict

base_dir = os.path.dirname(os.path.abspath(__file__))

# Liste de tous les fichiers HTML
all_html_files = []
for file in os.listdir(base_dir):
    if file.endswith('.html'):
        all_html_files.append(file)

print(f"📁 {len(all_html_files)} fichiers HTML trouvés:")
for f in sorted(all_html_files):
    print(f"   - {f}")

# Dictionnaire pour stocker les références
references = defaultdict(set)

# Analyser tous les fichiers HTML pour trouver les liens
for html_file in all_html_files:
    filepath = os.path.join(base_dir, html_file)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trouver tous les liens href vers d'autres fichiers HTML
        # Pattern: href="fichier.html"
        pattern = r'href=["\']([^"\']+\.html)["\']'
        matches = re.findall(pattern, content)
        
        for match in matches:
            # Nettoyer le lien (enlever les paramètres, ancres, etc.)
            clean_link = match.split('?')[0].split('#')[0]
            # Ne garder que le nom de fichier si c'est un chemin relatif
            filename = os.path.basename(clean_link)
            
            if filename in all_html_files:
                references[html_file].add(filename)
    
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture de {html_file}: {e}")

print(f"\n📊 Analyse des références:\n")

# Trouver les fichiers référencés
referenced_files = set()
for source, targets in references.items():
    for target in targets:
        referenced_files.add(target)
    if targets:
        print(f"✓ {source}")
        for target in sorted(targets):
            print(f"    → {target}")

# Trouver les fichiers non référencés (sauf index.html qui est le point d'entrée)
unreferenced = []
for html_file in all_html_files:
    if html_file not in referenced_files and html_file != 'index.html':
        unreferenced.append(html_file)

print(f"\n" + "="*60)
print(f"📋 RÉSUMÉ")
print("="*60)

print(f"\n✅ Fichiers UTILISÉS ({len(referenced_files) + 1}):")
print(f"   - index.html (point d'entrée)")
for f in sorted(referenced_files):
    print(f"   - {f}")

print(f"\n❌ Fichiers NON RÉFÉRENCÉS ({len(unreferenced)}):")
if unreferenced:
    for f in sorted(unreferenced):
        print(f"   - {f}")
    
    print(f"\n💡 RECOMMANDATION:")
    print(f"   Ces fichiers peuvent être archivés car ils ne sont plus")
    print(f"   accessibles depuis la navigation du site:")
    print()
    for f in sorted(unreferenced):
        print(f"   📦 {f}")
else:
    print(f"   (Aucun - tous les fichiers sont référencés)")

# Vérification spéciale pour arrival_guide.html
if 'arrival_guide.html' in unreferenced:
    print(f"\n⚠️  ATTENTION: arrival_guide.html n'est plus utilisé!")
    print(f"   Ce fichier était probablement remplacé par tips_and_tricks.html")

print(f"\n" + "="*60)
