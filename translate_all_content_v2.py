#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traduire TOUT le contenu de toutes les pages HTML
1. Extrait tous les textes traduisibles
2. Ajoute les attributs data-lang-key dans les HTML
3. Génère les traductions pour lang.js
"""

import re
from pathlib import Path
from collections import OrderedDict
import sys

# Force UTF-8 encoding pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Dictionnaire pour stocker toutes les traductions
all_translations = {
    'fr': OrderedDict(),
    'en': OrderedDict(),
    'de': OrderedDict(),
    'es': OrderedDict()
}

# Compteur pour générer des clés uniques
key_counter = {}

def slugify_key(text):
    """Crée un slug pour une clé de traduction"""
    # Nettoyer le texte
    text = text.strip()[:60]
    # Garder seulement les lettres, chiffres et espaces
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    # Convertir en minuscules
    text = text.lower()
    # Remplacer les espaces par des underscores
    text = re.sub(r'\s+', '_', text)
    # Limiter la longueur
    text = text[:40]
    # Supprimer les underscores multiples
    text = re.sub(r'_+', '_', text).strip('_')
    return text if text else 'text'

def generate_key(category, text, tag_type='text'):
    """Génère une clé unique pour un texte"""
    slug = slugify_key(text)
    base_key = f"{category}.{tag_type}.{slug}"
    
    # Ajouter un compteur si la clé existe déjà
    if base_key in key_counter:
        key_counter[base_key] += 1
        key = f"{base_key}_{key_counter[base_key]}"
    else:
        key_counter[base_key] = 0
        key = base_key
    
    return key

def extract_and_replace_texts(html_content, filename):
    """Extrait les textes et les remplace par des versions avec data-lang-key"""
    category = Path(filename).stem
    new_content = html_content
    translations_added = []
    
    def process_match(tag_type, match, pattern):
        """Traite un match et ajoute data-lang-key"""
        full_tag = match.group(0)
        
        # Vérifier si data-lang-key existe déjà
        if 'data-lang-key' in full_tag:
            return full_tag
        
        # Extraire le contenu
        content_match = re.search(pattern, full_tag, re.DOTALL)
        if not content_match:
            return full_tag
        
        inner_html = content_match.group(1)
        # Extraire le texte brut (sans HTML)
        text = re.sub(r'<[^>]+>', '', inner_html).strip()
        
        # Ignorer si texte vide ou trop court
        if not text or len(text) < 3:
            return full_tag
        
        # Ignorer les emojis seuls
        if len(text) < 5 and re.match(r'^[\U0001F300-\U0001F9FF\s]+$', text):
            return full_tag
        
        # Générer la clé
        key = generate_key(category, text, tag_type)
        
        # Stocker la traduction
        if key not in all_translations['fr']:
            all_translations['fr'][key] = text
            all_translations['en'][key] = text  # Placeholder
            all_translations['de'][key] = text  # Placeholder
            all_translations['es'][key] = text  # Placeholder
            translations_added.append((key, text))
        
        # Ajouter data-lang-key à la balise
        if f'<{tag_type}' in full_tag and f'</{tag_type}>' in full_tag:
            # Cas simple: balise sans attributs
            if re.match(rf'^<{tag_type}>\s*', full_tag):
                replacement = re.sub(rf'(<{tag_type}>)', rf'<{tag_type} data-lang-key="{key}">', full_tag, count=1)
            else:
                # Cas avec attributs: insérer avant >
                replacement = re.sub(rf'(<{tag_type}[^>]*?)(>)', rf'\1 data-lang-key="{key}"\2', full_tag, count=1)
            
            return replacement
        
        return full_tag
    
    # Traiter les h2
    def replace_h2(match):
        return process_match('h2', match, r'<h2[^>]*>(.*?)</h2>')
    
    new_content = re.sub(r'<h2[^>]*>.*?</h2>', replace_h2, new_content, flags=re.DOTALL)
    
    # Traiter les h3
    def replace_h3(match):
        return process_match('h3', match, r'<h3[^>]*>(.*?)</h3>')
    
    new_content = re.sub(r'<h3[^>]*>.*?</h3>', replace_h3, new_content, flags=re.DOTALL)
    
    # Traiter les p (mais pas ceux dans les scripts ou avec liens/images)
    def replace_p(match):
        full_tag = match.group(0)
        # Ignorer si contient <script, <a, <img, ou data-lang-key
        if '<script' in full_tag or '<a' in full_tag or '<img' in full_tag or 'data-lang-key' in full_tag:
            return full_tag
        return process_match('p', match, r'<p[^>]*>(.*?)</p>')
    
    new_content = re.sub(r'<p[^>]*>.*?</p>', replace_p, new_content, flags=re.DOTALL)
    
    # Traiter les li
    def replace_li(match):
        full_tag = match.group(0)
        if 'data-lang-key' in full_tag:
            return full_tag
        # Extraire le texte brut
        inner = re.search(r'<li[^>]*>(.*?)</li>', full_tag, re.DOTALL)
        if inner:
            text = re.sub(r'<[^>]+>', '', inner.group(1)).strip()
            if text and len(text) >= 3:
                return process_match('li', match, r'<li[^>]*>(.*?)</li>')
        return full_tag
    
    new_content = re.sub(r'<li[^>]*>.*?</li>', replace_li, new_content, flags=re.DOTALL)
    
    # Traiter les strong (mais seulement ceux qui sont seuls dans leur parent)
    def replace_strong(match):
        full_tag = match.group(0)
        if 'data-lang-key' in full_tag:
            return full_tag
        return process_match('strong', match, r'<strong[^>]*>(.*?)</strong>')
    
    new_content = re.sub(r'<strong[^>]*>.*?</strong>', replace_strong, new_content, flags=re.DOTALL)
    
    return new_content, translations_added

def main():
    """Fonction principale"""
    print("=" * 60)
    print("EXTRACTION ET AJOUT DES TRADUCTIONS")
    print("=" * 60)
    
    html_files = list(Path('.').glob('*.html'))
    html_files = [f for f in html_files if f.name not in ['index_multilangue.html']]
    
    total_added = 0
    
    for html_file in sorted(html_files):
        print(f"\nTraitement de {html_file.name}...")
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content, translations_added = extract_and_replace_texts(content, html_file.name)
            
            # Sauvegarder le fichier modifié
            if new_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  OK: {len(translations_added)} nouveaux textes ajoutes")
                total_added += len(translations_added)
            else:
                print(f"  Aucun changement")
        
        except Exception as e:
            print(f"  ERREUR: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {len(all_translations['fr'])} textes extraits")
    print(f"NOUVEAUX: {total_added} attributs data-lang-key ajoutes")
    print("=" * 60)
    
    # Générer le fichier de traductions
    print("\nGeneration du fichier de traductions...")
    generate_translations_file()
    print("Termine!")

def generate_translations_file():
    """Génère un fichier de traductions à intégrer dans lang.js"""
    output = []
    output.append("// Traductions automatiquement generees")
    output.append("// A COMPLETER avec les vraies traductions EN, DE, ES")
    output.append("")
    
    current_category = None
    for key in all_translations['fr'].keys():
        parts = key.split('.', 2)
        if len(parts) >= 3:
            category = parts[0]
            tag_type = parts[1]
            slug = '.'.join(parts[2:])
            
            if category != current_category:
                if current_category is not None:
                    output.append("")
                output.append(f"            // {category}")
                current_category = category
            
            fr_text = all_translations['fr'][key]
            en_text = all_translations['en'][key]
            
            # Échapper les guillemets et sauts de ligne
            fr_text_escaped = fr_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            
            output.append(f'            "{key}": "{fr_text_escaped}",  // TODO: traduire en EN/DE/ES')
    
    # Sauvegarder dans un fichier
    with open('translations_generated.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Fichier 'translations_generated.txt' genere avec {len(all_translations['fr'])} cles")

if __name__ == "__main__":
    main()


