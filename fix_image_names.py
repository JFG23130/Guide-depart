#!/usr/bin/env python3
"""
Script pour renommer tous les fichiers images en minuscules
pour correspondre aux slugs générés par le script JavaScript
"""

import os
from pathlib import Path
import unicodedata
import re
import subprocess

def slugify_filename(filename):
    """Convertit un nom de fichier en slug (minuscules, underscores)"""
    # Enlever l'extension
    name, ext = os.path.splitext(filename)
    
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
    
    return name + ext

def main():
    print("Analyse et correction des noms de fichiers images...")
    print("")
    
    images_dir = Path("images")
    if not images_dir.exists():
        print("Erreur: Le dossier 'images' n'existe pas")
        return
    
    # Extensions d'images supportées
    image_exts = {'.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP'}
    
    renamed_count = 0
    skipped_count = 0
    
    # Récupérer la liste des fichiers Git
    try:
        git_files = subprocess.check_output(
            ['git', 'ls-files', 'images/'],
            cwd=Path.cwd(),
            text=True
        ).strip().split('\n')
        git_files = {f for f in git_files if f}
    except:
        git_files = set()
        print("Attention: Impossible de récupérer la liste Git (peut-etre pas dans un depot Git)")
    
    # Traiter tous les fichiers images
    for img_file in sorted(images_dir.iterdir()):
        if not img_file.is_file():
            continue
        
        if img_file.suffix not in image_exts:
            continue
        
        current_name = img_file.name
        target_name = slugify_filename(current_name)
        
        # Si le nom est déjà correct, on skip
        if current_name == target_name:
            skipped_count += 1
            continue
        
        target_path = images_dir / target_name
        
        # Si le fichier cible existe déjà, on skip
        if target_path.exists() and target_path != img_file:
            print(f"SKIP: {current_name} -> {target_name} (deja existe)")
            skipped_count += 1
            continue
        
        # Renommer avec git mv si c'est un fichier Git, sinon renommer normalement
        git_path = f"images/{current_name}"
        if git_path in git_files:
            try:
                subprocess.run(
                    ['git', 'mv', str(img_file), str(target_path)],
                    cwd=Path.cwd(),
                    check=True,
                    capture_output=True
                )
                print(f"RENOMME (git): {current_name} -> {target_name}")
                renamed_count += 1
            except subprocess.CalledProcessError as e:
                print(f"ERREUR git mv: {current_name} -> {target_name}")
                print(f"  {e.stderr.decode() if e.stderr else ''}")
                # Essayer un renommage normal
                try:
                    img_file.rename(target_path)
                    print(f"RENOMME: {current_name} -> {target_name}")
                    renamed_count += 1
                except Exception as e2:
                    print(f"ERREUR: Impossible de renommer {current_name}")
        else:
            # Fichier non suivi par Git, renommer normalement
            try:
                img_file.rename(target_path)
                print(f"RENOMME: {current_name} -> {target_name}")
                renamed_count += 1
            except Exception as e:
                print(f"ERREUR: Impossible de renommer {current_name}")
                print(f"  {e}")
    
    print("")
    print(f"{renamed_count} fichier(s) renomme(s)")
    print(f"{skipped_count} fichier(s) deja correct(s)")

if __name__ == "__main__":
    main()
