#!/usr/bin/env python3
"""
Nettoyer les fichiers de traduction des clés obsolètes
(clés arrival_guide, access)
"""

import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, 'assets')

# Patterns des clés à supprimer
patterns_to_remove = [
    r'"arrival_guide\.',  # Toutes les clés arrival_guide
    r'"access\.',         # Toutes les clés access
]

lang_files = [
    'lang-fr.js',
    'lang-en.js',
    'lang-de.js',
    'lang-es.js'
]

print("🧹 Nettoyage des fichiers de traduction...")
print("="*60)

for lang_file in lang_files:
    filepath = os.path.join(assets_dir, lang_file)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {lang_file} non trouvé")
        continue
    
    print(f"\n📝 Traitement {lang_file}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Compter les lignes avant
    original_count = len(lines)
    
    # Filtrer les lignes à supprimer
    new_lines = []
    removed_count = 0
    
    for line in lines:
        # Vérifier si la ligne contient une clé à supprimer
        should_remove = False
        
        for pattern in patterns_to_remove:
            if re.search(pattern, line):
                should_remove = True
                removed_count += 1
                break
        
        if not should_remove:
            new_lines.append(line)
    
    # Sauvegarder le fichier nettoyé
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"   ✅ {removed_count} ligne(s) supprimée(s)")
    print(f"   📊 Avant: {original_count} lignes, Après: {len(new_lines)} lignes")

print("\n" + "="*60)
print("✅ Nettoyage terminé!")
print("\n📋 Résumé des clés supprimées:")
print("   - Toutes les clés 'arrival_guide.*'")
print("   - Toutes les clés 'access.*'")
print("\n💡 Les fichiers de traduction sont maintenant à jour.")
