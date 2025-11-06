#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traduire TOUT le contenu de toutes les pages HTML
Extrait les textes, crée les traductions et ajoute les data-lang-key
"""

import re
from pathlib import Path
from collections import OrderedDict

# Dictionnaire pour stocker toutes les traductions
all_translations = {
    'fr': OrderedDict(),
    'en': OrderedDict(),
    'de': OrderedDict(),
    'es': OrderedDict()
}

# Compteur pour générer des clés uniques
key_counter = {}

def generate_key(category, text):
    """Génère une clé unique pour un texte"""
    # Créer un slug basé sur le texte (premiers mots)
    words = text.strip()[:50].lower().split()
    slug = '_'.join(words[:4]) if words else 'text'
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    slug = slug[:30]
    
    # Ajouter un compteur si la clé existe déjà
    base_key = f"{category}.{slug}"
    if base_key in key_counter:
        key_counter[base_key] += 1
        key = f"{base_key}_{key_counter[base_key]}"
    else:
        key_counter[base_key] = 0
        key = base_key
    
    return key

def translate_text(text, target_lang):
    """Traduction automatique simple (à remplacer par vraie traduction si nécessaire)"""
    # Pour l'instant, retourne le texte tel quel
    # Dans une vraie implémentation, on utiliserait une API de traduction
    # Ici, on va créer des traductions de base manuellement pour les textes les plus importants
    
    # Traductions manuelles pour les textes courants
    translations_dict = {
        'fr': text,
        'en': text,  # Sera remplacé par vraie traduction
        'de': text,
        'es': text
    }
    
    return translations_dict.get(target_lang, text)

def extract_texts_from_html(html_content, filename):
    """Extrait tous les textes traduisibles d'un fichier HTML"""
    texts = []
    
    # Extraire les titres h2, h3
    for match in re.finditer(r'<h2[^>]*>(.*?)</h2>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text and not text.startswith('📖') and 'data-lang-key' not in match.group(0):
            texts.append(('h2', text, match.group(0)))
    
    for match in re.finditer(r'<h3[^>]*>(.*?)</h3>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text and not text.startswith('📚') and 'data-lang-key' not in match.group(0):
            texts.append(('h3', text, match.group(0)))
    
    # Extraire les paragraphes
    for match in re.finditer(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        # Ignorer les paragraphes vides ou avec seulement des emojis
        if text and len(text) > 10 and 'data-lang-key' not in match.group(0):
            # Ignorer si c'est un lien ou contient des balises spéciales
            if '<a' not in match.group(1) and '<img' not in match.group(1):
                texts.append(('p', text, match.group(0)))
    
    # Extraire les list items
    for match in re.finditer(r'<li[^>]*>(.*?)</li>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text and len(text) > 3 and 'data-lang-key' not in match.group(0):
            texts.append(('li', text, match.group(0)))
    
    # Extraire les strong
    for match in re.finditer(r'<strong[^>]*>(.*?)</strong>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text and len(text) > 2 and 'data-lang-key' not in match.group(0):
            texts.append(('strong', text, match.group(0)))
    
    return texts

def add_translations_for_file(filename, texts):
    """Ajoute les traductions pour un fichier"""
    category = Path(filename).stem
    
    for tag_type, text, original_html in texts:
        # Générer une clé unique
        key = generate_key(category, text)
        
        # Stocker les traductions (pour l'instant en français seulement)
        all_translations['fr'][key] = text
        
        # Ici, on devrait appeler une vraie API de traduction
        # Pour l'instant, on garde le texte français comme placeholder
        all_translations['en'][key] = text  # TODO: vraie traduction
        all_translations['de'][key] = text  # TODO: vraie traduction
        all_translations['es'][key] = text  # TODO: vraie traduction

def main():
    """Fonction principale"""
    print("Extraction des textes de toutes les pages...")
    
    html_files = list(Path('.').glob('*.html'))
    html_files = [f for f in html_files if f.name != 'index_multilangue.html']
    
    for html_file in sorted(html_files):
        print(f"Traitement de {html_file.name}...")
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        texts = extract_texts_from_html(content, html_file.name)
        add_translations_for_file(html_file.name, texts)
        print(f"  {len(texts)} textes extraits")
    
    print(f"\nTotal: {len(all_translations['fr'])} textes extraits")
    print("\nPremieres cles:")
    for i, key in enumerate(list(all_translations['fr'].keys())[:10]):
        print(f"  {key}: {all_translations['fr'][key][:50]}...")

if __name__ == "__main__":
    main()


