#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traduire automatiquement TOUS les textes avec data-lang-key
Utilise deep-translator pour les traductions automatiques
"""

import re
from pathlib import Path
import sys
import json

# Force UTF-8 encoding pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False
    print("AVERTISSEMENT: deep-translator non installe.")
    print("Installer avec: pip install deep-translator")
    print("Le script va generer les cles sans traductions.")

def extract_translations_from_html(html_content, filename):
    """Extrait tous les textes avec data-lang-key"""
    translations = {}
    
    # Chercher tous les attributs data-lang-key
    pattern = r'data-lang-key="([^"]+)"[^>]*>(.*?)</'
    
    for match in re.finditer(pattern, html_content, re.DOTALL):
        key = match.group(1)
        # Extraire le texte (enlever les balises HTML)
        text_with_html = match.group(2)
        text = re.sub(r'<[^>]+>', '', text_with_html).strip()
        
        if text and key not in translations:
            translations[key] = text
    
    return translations

def translate_text(text, source_lang='fr', target_lang='en'):
    """Traduit un texte"""
    if not HAS_TRANSLATOR or not text:
        return text
    
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        # Petit délai pour éviter les rate limits
        import time
        time.sleep(0.1)
        return translated
    except Exception as e:
        print(f"  Erreur traduction ({target_lang}): {e}")
        return text

def update_lang_js(all_translations):
    """Met à jour le fichier lang.js avec toutes les traductions"""
    lang_js_path = Path('assets/lang.js')
    
    if not lang_js_path.exists():
        print("ERREUR: assets/lang.js n'existe pas!")
        return
    
    with open(lang_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la position du dictionnaire translations
    # Chercher "const translations = {"
    pattern_start = r'(const\s+translations\s*=\s*\{)'
    match_start = re.search(pattern_start, content)
    
    if not match_start:
        print("ERREUR: Structure de lang.js non reconnue")
        return
    
    # Extraire les traductions existantes
    existing_translations = {}
    for lang in ['fr', 'en', 'de', 'es']:
        existing_translations[lang] = {}
        # Chercher chaque langue
        lang_pattern = rf'({lang}:\s*{{[^}}]*}})'
        lang_match = re.search(lang_pattern, content, re.DOTALL)
        if lang_match:
            # Extraire les clés existantes
            lang_content = lang_match.group(1)
            key_pattern = r'"([^"]+)":\s*"([^"]*)"'
            for key_match in re.finditer(key_pattern, lang_content):
                existing_translations[lang][key_match.group(1)] = key_match.group(2)
    
    # Fusionner avec les nouvelles traductions
    for lang in ['fr', 'en', 'de', 'es']:
        for key, text in all_translations.get(lang, {}).items():
            existing_translations[lang][key] = text
    
    # Générer le nouveau contenu de lang.js
    new_lang_js = generate_lang_js_content(existing_translations)
    
    # Sauvegarder
    with open(lang_js_path, 'w', encoding='utf-8') as f:
        f.write(new_lang_js)
    
    print(f"Fichier assets/lang.js mis a jour!")

def generate_lang_js_content(translations):
    """Génère le contenu complet du fichier lang.js"""
    output = []
    output.append("// Système multilingue pour Guide Katikias 33")
    output.append("// Langues supportées: Français, English, Deutsch, Español")
    output.append("")
    output.append("const translations = {")
    
    for lang_code, lang_name in [('fr', 'Français'), ('en', 'English'), ('de', 'Deutsch'), ('es', 'Español')]:
        output.append(f"    {lang_code}: {{  // {lang_name}")
        output.append("        // Navigation commune")
        
        # Organiser par catégories
        categories = {}
        for key in sorted(translations[lang_code].keys()):
            parts = key.split('.')
            if len(parts) >= 2:
                category = parts[0]
                if category not in categories:
                    categories[category] = []
                categories[category].append(key)
            else:
                if 'general' not in categories:
                    categories['general'] = []
                categories['general'].append(key)
        
        # Ajouter un commentaire de section pour la navigation
        if 'nav' in categories:
            output.append("        // Navigation")
            for key in categories['nav']:
                text = translations[lang_code][key]
                text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                output.append(f'        "{key}": "{text_escaped}",')
            del categories['nav']
            output.append("")
        
        # Parcourir les autres catégories
        for category in sorted(categories.keys()):
            if category == 'general':
                continue
            output.append(f"        // {category}")
            for key in categories[category]:
                text = translations[lang_code][key]
                text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                output.append(f'        "{key}": "{text_escaped}",')
            output.append("")
        
        # Général en dernier
        if 'general' in categories:
            output.append("        // General")
            for key in categories['general']:
                text = translations[lang_code][key]
                text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                output.append(f'        "{key}": "{text_escaped}",')
        
        output.append("    },")
    
    output.append("};")
    output.append("")
    output.append("// Fonction pour changer la langue")
    output.append("function changeLanguage(lang) {")
    output.append("    // Sauvegarder la préférence")
    output.append("    if (typeof Storage !== 'undefined') {")
    output.append("        localStorage.setItem('preferredLanguage', lang);")
    output.append("    }")
    output.append("    ")
    output.append("    // Mettre à jour l'attribut lang du HTML")
    output.append("    document.documentElement.lang = lang;")
    output.append("    ")
    output.append("    // Mettre à jour le sélecteur de langue s'il existe")
    output.append("    const langSelector = document.getElementById('langSelector');")
    output.append("    if (langSelector) {")
    output.append("        langSelector.value = lang;")
    output.append("    }")
    output.append("    ")
    output.append("    // Traduire tous les éléments avec data-lang-key")
    output.append("    document.querySelectorAll('[data-lang-key]').forEach(element => {")
    output.append("        const key = element.getAttribute('data-lang-key');")
    output.append("        if (translations[lang] && translations[lang][key]) {")
    output.append("            // Préserver le HTML interne si nécessaire")
    output.append("            if (element.innerHTML && element.innerHTML !== element.textContent) {")
    output.append("                // Si c'est du HTML, on le remplace complètement")
    output.append("                element.textContent = translations[lang][key];")
    output.append("            } else {")
    output.append("                element.textContent = translations[lang][key];")
    output.append("            }")
    output.append("        }")
    output.append("    });")
    output.append("    ")
    output.append("    // Traduire les attributs alt et title des images")
    output.append("    document.querySelectorAll('img[data-lang-alt], img[data-lang-title]').forEach(img => {")
    output.append("        const altKey = img.getAttribute('data-lang-alt');")
    output.append("        const titleKey = img.getAttribute('data-lang-title');")
    output.append("        if (altKey && translations[lang] && translations[lang][altKey]) {")
    output.append("            img.alt = translations[lang][altKey];")
    output.append("        }")
    output.append("        if (titleKey && translations[lang] && translations[lang][titleKey]) {")
    output.append("            img.title = translations[lang][titleKey];")
    output.append("        }")
    output.append("    });")
    output.append("}")
    output.append("")
    output.append("// Fonction d'initialisation de la langue")
    output.append("function initLanguage() {")
    output.append("    // Récupérer la langue sauvegardée ou détecter")
    output.append("    let initialLang = 'fr'; // Par défaut français")
    output.append("    ")
    output.append("    if (typeof Storage !== 'undefined') {")
    output.append("        const savedLang = localStorage.getItem('preferredLanguage');")
    output.append("        if (savedLang && translations[savedLang]) {")
    output.append("            initialLang = savedLang;")
    output.append("        } else {")
    output.append("            // Détection automatique basée sur le navigateur")
    output.append("            const browserLang = navigator.language || navigator.userLanguage;")
    output.append("            const langCode = browserLang.split('-')[0].toLowerCase();")
    output.append("            if (translations[langCode]) {")
    output.append("                initialLang = langCode;")
    output.append("            }")
    output.append("        }")
    output.append("    }")
    output.append("    ")
    output.append("    // Appliquer la langue")
    output.append("    changeLanguage(initialLang);")
    output.append("}")
    output.append("")
    output.append("// Initialiser au chargement du DOM")
    output.append("if (document.readyState === 'loading') {")
    output.append("    document.addEventListener('DOMContentLoaded', initLanguage);")
    output.append("} else {")
    output.append("    initLanguage();")
    output.append("}")
    
    return '\n'.join(output)

def main():
    """Fonction principale"""
    print("=" * 60)
    print("TRADUCTION AUTOMATIQUE DU CONTENU")
    print("=" * 60)
    
    if not HAS_TRANSLATOR:
        print("\nERREUR: deep-translator n'est pas installe.")
        print("Installer avec: pip install deep-translator")
        return
    
    # Extraire toutes les traductions de tous les fichiers HTML
    all_translations = {
        'fr': {},
        'en': {},
        'de': {},
        'es': {}
    }
    
    html_files = list(Path('.').glob('*.html'))
    html_files = [f for f in html_files if f.name not in ['index_multilangue.html']]
    
    print("\n1. Extraction des textes...")
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            translations = extract_translations_from_html(content, html_file.name)
            print(f"  {html_file.name}: {len(translations)} textes trouves")
            
            # Ajouter au dictionnaire global
            for key, text in translations.items():
                if key not in all_translations['fr']:
                    all_translations['fr'][key] = text
        
        except Exception as e:
            print(f"  ERREUR {html_file.name}: {e}")
            continue
    
    print(f"\nTotal: {len(all_translations['fr'])} textes uniques")
    
    # Traduire en EN, DE, ES
    print("\n2. Traduction automatique...")
    print("  (Cela peut prendre plusieurs minutes...)")
    
    total = len(all_translations['fr'])
    current = 0
    
    for key, fr_text in all_translations['fr'].items():
        current += 1
        if current % 10 == 0:
            print(f"  Progress: {current}/{total} ({current*100//total}%)")
        
        all_translations['en'][key] = translate_text(fr_text, 'fr', 'en')
        all_translations['de'][key] = translate_text(fr_text, 'fr', 'de')
        all_translations['es'][key] = translate_text(fr_text, 'fr', 'es')
    
    print(f"\n  Termine: {total} textes traduits")
    
    # Mettre à jour lang.js
    print("\n3. Mise a jour de assets/lang.js...")
    update_lang_js(all_translations)
    
    print("\n" + "=" * 60)
    print("TERMINE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
