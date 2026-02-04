#!/usr/bin/env python3
"""
Script pour mettre à jour tous les fichiers HTML pour utiliser le nouveau système multilingue
"""

import os
import re

# Répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Trouver tous les fichiers HTML
html_files = []
for file in os.listdir(base_dir):
    if file.endswith('.html') and file not in ['test-multilang.html', 'index_multilangue.html']:
        html_files.append(os.path.join(base_dir, file))

print(f"📁 Fichiers HTML trouvés: {len(html_files)}")

for html_file in html_files:
    print(f"\n🔄 Traitement: {os.path.basename(html_file)}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si c'est déjà à jour
    if 'assets/lang-fr.js' in content:
        print("   ✅ Déjà à jour")
        continue
    
    # Remplacer l'ancien script par le nouveau système
    old_script = '<script src="assets/lang.js"></script>'
    new_scripts = '''<script src="assets/lang-fr.js"></script>
    <script src="assets/lang-en.js"></script>
    <script src="assets/lang-de.js"></script>
    <script src="assets/lang-es.js"></script>
    <script src="assets/init-translations.js"></script>'''
    
    if old_script in content:
        content = content.replace(old_script, new_scripts)
        
        # Sauvegarder le fichier
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Mise à jour effectuée")
    else:
        print("   ⚠️ Script non trouvé, vérification manuelle nécessaire")

print("\n✅ Toutes les pages ont été mises à jour!")
