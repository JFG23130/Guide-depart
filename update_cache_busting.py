#!/usr/bin/env python3
"""
Script pour mettre à jour le cache busting dans tous les fichiers HTML
Ajoute les meta tags anti-cache et améliore le cache busting JavaScript
"""

import os
from pathlib import Path
import re

def update_html_file(file_path):
    """Met à jour un fichier HTML avec les meta tags et le cache busting amélioré"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Ajouter les meta tags anti-cache si elles n'existent pas
        if '<meta http-equiv="Cache-Control"' not in content:
            # Trouver la position après <meta name="viewport"
            viewport_pattern = r'(<meta name="viewport" content="[^"]*">)'
            replacement = r'\1\n    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n    <meta http-equiv="Pragma" content="no-cache">\n    <meta http-equiv="Expires" content="0">'
            content = re.sub(viewport_pattern, replacement, content, count=1)
        
        # 2. Mettre à jour le cache busting JavaScript - remplacer l'ancien timestamp
        # Remplacer simplement 'v=20251030T' par 'v=' (le + reste)
        content = content.replace("'v=20251030T'", "'v='")
        content = content.replace('"v=20251030T"', '"v="')
        content = content.replace("v=20251030T", "v=")
        
        # 4. Améliorer le code pour être plus robuste - remplacer forEach simple par version améliorée
        old_foreach = r"document\.querySelectorAll\('img\[src\]'\)\.forEach\(function\(img\)\{ img\.src = bust\(img\.getAttribute\('src'\)\); \}\);"
        new_foreach = """document.querySelectorAll('img[src]').forEach(function(img){ 
                var originalSrc = img.getAttribute('src');
                img.src = bust(originalSrc);
            });"""
        content = re.sub(old_foreach, new_foreach, content)
        
        # Écrire seulement si le contenu a changé
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Erreur lors du traitement de {file_path}: {e}")
        return False

def main():
    print("Mise à jour du cache busting pour tous les fichiers HTML...")
    print("")
    
    html_dir = Path(".")
    html_files = list(html_dir.glob("*.html"))
    
    updated_count = 0
    for html_file in html_files:
        if update_html_file(html_file):
            print(f"OK: {html_file.name}")
            updated_count += 1
        else:
            print(f"  {html_file.name} (deja a jour ou pas de cache busting)")
    
    print("")
    print(f"{updated_count} fichier(s) mis à jour")

if __name__ == "__main__":
    main()
