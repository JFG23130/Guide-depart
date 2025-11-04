#!/usr/bin/env python3
"""
Script pour mettre à jour toutes les références PDF dans les HTML
en convertissant les chemins en minuscules
"""

import re
from pathlib import Path
import unicodedata

def slugify_path(path):
    """Convertit un chemin PDF en slug (minuscules, underscores)"""
    # Extraire le nom de fichier
    parts = path.split('/')
    if len(parts) != 2:
        return path
    
    folder, filename = parts
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    # Convertir en minuscules
    name = name.lower()
    
    # Normaliser les accents
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    
    # Remplacer espaces et caractères spéciaux par underscores
    name = re.sub(r'[^a-z0-9_]+', '_', name)
    
    # Supprimer les underscores en début/fin et multiples
    name = re.sub(r'^_+|_+$', '', name)
    name = re.sub(r'_{2,}', '_', name)
    
    # Extension en minuscules
    ext = ext.lower()
    
    result = f"{folder}/{name}.{ext}" if ext else f"{folder}/{name}"
    return result

def fix_html_file(html_file):
    """Met à jour toutes les références PDF dans un fichier HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Trouver toutes les références data-pdf
    pattern = r'data-pdf="(pdfs/[^"]+)"'
    
    def replace_path(match):
        old_path = match.group(1)
        new_path = slugify_path(old_path)
        if old_path != new_path:
            return f'data-pdf="{new_path}"'
        return match.group(0)
    
    content = re.sub(pattern, replace_path, content)
    
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("Mise a jour des references PDF dans les fichiers HTML...")
    print("")
    
    html_files = [
        'salon.html',
        'cuisine.html',
        'chambre.html',
        'terrasse.html',
        'salle_deau.html',
        'wc.html',
        'placard_bleu.html',
        'salle_manger.html'
    ]
    
    updated_count = 0
    
    for html_file in html_files:
        path = Path(html_file)
        if path.exists():
            if fix_html_file(path):
                print(f"  {html_file}: OK")
                updated_count += 1
            else:
                print(f"  {html_file}: deja correct")
        else:
            print(f"  {html_file}: fichier non trouve")
    
    print("")
    print(f"{updated_count} fichier(s) HTML mis(e) a jour")

if __name__ == "__main__":
    main()
