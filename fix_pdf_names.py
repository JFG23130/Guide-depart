#!/usr/bin/env python3
"""
Script pour renommer tous les fichiers PDF en minuscules
et mettre à jour les références dans les fichiers HTML
"""

import os
import re
from pathlib import Path
import unicodedata
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

def fix_html_references(html_file, old_path, new_path):
    """Met à jour les références PDF dans un fichier HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer toutes les occurrences du chemin PDF
    old_escaped = re.escape(old_path)
    pattern = r'data-pdf="' + old_escaped + r'"'
    new_ref = f'data-pdf="{new_path}"'
    
    if re.search(pattern, content):
        content = re.sub(pattern, new_ref, content)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("Renommage des PDFs en minuscules...")
    print("")
    
    pdfs_dir = Path("pdfs")
    if not pdfs_dir.exists():
        print("Erreur: Le dossier 'pdfs' n'existe pas")
        return
    
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
    
    # Récupérer la liste des fichiers Git
    try:
        git_files = subprocess.check_output(
            ['git', 'ls-files', 'pdfs/'],
            cwd=Path.cwd(),
            text=True
        ).strip().split('\n')
        git_files = {f for f in git_files if f}
    except:
        git_files = set()
        print("Attention: Impossible de recuperer la liste Git")
    
    renamed_count = 0
    skipped_count = 0
    html_updates = {}
    
    # Traiter tous les fichiers PDF
    for pdf_file in sorted(pdfs_dir.iterdir()):
        if not pdf_file.is_file():
            continue
        
        if pdf_file.suffix.lower() != '.pdf':
            continue
        
        current_name = pdf_file.name
        target_name = slugify_filename(current_name)
        
        # Si le nom est déjà correct, on skip
        if current_name == target_name:
            skipped_count += 1
            continue
        
        target_path = pdfs_dir / target_name
        
        # Si le fichier cible existe déjà, on skip
        if target_path.exists() and target_path != pdf_file:
            print(f"SKIP: {current_name} -> {target_name} (deja existe)")
            skipped_count += 1
            continue
        
        old_path = f"pdfs/{current_name}"
        new_path = f"pdfs/{target_name}"
        
        # Renommer avec git mv si c'est un fichier Git, sinon renommer normalement
        git_path = f"pdfs/{current_name}"
        if git_path in git_files:
            try:
                subprocess.run(
                    ['git', 'mv', str(pdf_file), str(target_path)],
                    cwd=Path.cwd(),
                    check=True,
                    capture_output=True
                )
                print(f"RENOMME (git): {current_name} -> {target_name}")
                renamed_count += 1
                html_updates[old_path] = new_path
            except subprocess.CalledProcessError as e:
                print(f"ERREUR git mv: {current_name} -> {target_name}")
                # Essayer un renommage normal
                try:
                    pdf_file.rename(target_path)
                    print(f"RENOMME: {current_name} -> {target_name}")
                    renamed_count += 1
                    html_updates[old_path] = new_path
                except Exception as e2:
                    print(f"ERREUR: Impossible de renommer {current_name}")
        else:
            # Fichier non suivi par Git, renommer normalement
            try:
                pdf_file.rename(target_path)
                print(f"RENOMME: {current_name} -> {target_name}")
                renamed_count += 1
                html_updates[old_path] = new_path
            except Exception as e:
                print(f"ERREUR: Impossible de renommer {current_name}")
    
    print("")
    print(f"{renamed_count} PDF(s) renomme(s)")
    print(f"{skipped_count} PDF(s) deja correct(s)")
    
    # Mettre à jour les références dans les fichiers HTML
    if html_updates:
        print("")
        print("Mise a jour des references dans les fichiers HTML...")
        html_updated = 0
        for html_file in html_files:
            path = Path(html_file)
            if path.exists():
                for old_path, new_path in html_updates.items():
                    if fix_html_references(path, old_path, new_path):
                        print(f"  {html_file}: {old_path} -> {new_path}")
                        html_updated += 1
        
        if html_updated > 0:
            print(f"{html_updated} reference(s) mise(s) a jour dans les fichiers HTML")

if __name__ == "__main__":
    main()
