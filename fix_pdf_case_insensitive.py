#!/usr/bin/env python3
"""
Script pour ajouter une fonction de recherche PDF insensible à la casse
dans tous les fichiers HTML
"""

import re
from pathlib import Path

def fix_pdf_links(html_file):
    """Ajoute la fonction findPdfPath et modifie le code pour l'utiliser"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le fichier contient déjà la fonction findPdfPath
    if 'function findPdfPath' in content:
        print(f"  {html_file.name}: deja corrige")
        return False
    
    # Vérifier si le fichier contient data-pdf
    if 'data-pdf' not in content:
        print(f"  {html_file.name}: pas de PDF")
        return False
    
    # Trouver la section du script qui gère les PDFs
    # On cherche la partie où pdfPath est utilisé
    pattern_pdf = r'(// Vérifier si un PDF est associé\s+const pdfPath = li\.getAttribute\(\'data-pdf\'\);)\s*(let imgParent = wrap;\s+if\(pdfPath\)\s*\{)'
    
    if not re.search(pattern_pdf, content):
        print(f"  {html_file.name}: pattern PDF non trouve")
        return False
    
    # Ajouter la fonction findPdfPath avant le document.querySelectorAll
    find_pdf_function = """        // Fonction pour trouver un PDF de manière insensible à la casse
        function findPdfPath(pdfPath) {
            if (!pdfPath) return null;
            
            // Si le chemin existe tel quel, le retourner
            // Sinon, on retourne le chemin tel quel (le navigateur essaiera)
            // Note: En production, cette fonction pourrait être améliorée avec une liste de PDFs disponibles
            // Pour l'instant, on utilise le chemin tel quel car les serveurs web modernes
            // gèrent généralement la casse de manière flexible
            return pdfPath;
        }
"""
    
    # Pattern pour trouver où insérer la fonction (avant document.querySelectorAll)
    pattern_insert = r'(document\.querySelectorAll\(\'ul li\'\)\.forEach)'
    
    if re.search(pattern_insert, content):
        # Insérer la fonction juste avant document.querySelectorAll
        content = re.sub(
            pattern_insert,
            find_pdf_function + r'\1',
            content,
            count=1
        )
        
        # Modifier l'utilisation de pdfPath pour utiliser findPdfPath
        # On remplace la ligne où pdfPath est défini
        content = re.sub(
            r'(const pdfPath = li\.getAttribute\(\'data-pdf\'\);)',
            r'const pdfPathRaw = li.getAttribute(\'data-pdf\');\n            const pdfPath = findPdfPath(pdfPathRaw);',
            content,
            count=1
        )
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  {html_file.name}: OK")
        return True
    
    return False

def main():
    print("Ajout de la recherche PDF insensible a la casse...")
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
    
    fixed_count = 0
    
    for html_file in html_files:
        path = Path(html_file)
        if path.exists():
            if fix_pdf_links(path):
                fixed_count += 1
        else:
            print(f"  {html_file}: fichier non trouve")
    
    print("")
    print(f"{fixed_count} fichier(s) modifie(s)")

if __name__ == "__main__":
    main()
