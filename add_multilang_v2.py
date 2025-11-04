#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter automatiquement le système multilingue à tous les fichiers HTML
Version corrigée pour éviter les duplications
"""

import os
import re
from pathlib import Path

# CSS pour le sélecteur de langue
LANG_CSS = """        .lang-selector {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .lang-selector select {
            padding: 8px 12px;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            background: white;
            color: #333;
        }
        .lang-selector select:focus {
            outline: none;
            border-color: #764ba2;
        }
        @media (max-width: 480px) {
            .lang-selector {
                top: 10px;
                right: 10px;
                padding: 8px;
            }
        }
"""

# HTML pour le sélecteur de langue
LANG_SELECTOR_HTML = """    <div class="lang-selector">
        <select id="langSelector" onchange="changeLanguage(this.value)">
            <option value="fr">🇫🇷 Français</option>
            <option value="en">🇬🇧 English</option>
            <option value="de">🇩🇪 Deutsch</option>
            <option value="es">🇪🇸 Español</option>
        </select>
    </div>
"""

# Script lang.js à inclure
LANG_SCRIPT = """    <script src="assets/lang.js"></script>
"""

def add_lang_css(content):
    """Ajoute le CSS du sélecteur de langue dans le style"""
    if '.lang-selector' in content:
        return content
    # Chercher la balise </style>
    if '</style>' in content:
        # Insérer avant </style>
        content = content.replace('</style>', LANG_CSS + '\n    </style>', 1)
    return content

def add_lang_selector(content):
    """Ajoute le sélecteur de langue dans le body"""
    if 'langSelector' in content:
        return content
    # Chercher <body> ou <body avec attributs>
    pattern = r'(<body[^>]*>)'
    match = re.search(pattern, content)
    if match:
        # Insérer après la balise <body>
        pos = match.end()
        content = content[:pos] + '\n' + LANG_SELECTOR_HTML + content[pos:]
    return content

def add_lang_script(content):
    """Ajoute le script lang.js avant </body>"""
    if 'assets/lang.js' in content:
        return content
    # Chercher </body>
    if '</body>' in content:
        # Insérer avant </body>
        content = content.replace('</body>', LANG_SCRIPT + '</body>', 1)
    return content

def add_data_lang_key_safe(content, pattern, replacement):
    """Ajoute un attribut data-lang-key de manière sûre"""
    # Vérifier si déjà présent
    if 'data-lang-key=' in replacement and 'data-lang-key=' in content:
        # Vérifier si cette clé spécifique existe déjà
        lang_key_match = re.search(r'data-lang-key="([^"]+)"', replacement)
        if lang_key_match:
            lang_key = lang_key_match.group(1)
            if f'data-lang-key="{lang_key}"' in content:
                return content
    
    # Faire le remplacement
    if pattern in content:
        # Si le pattern contient déjà data-lang-key, ne pas modifier
        if 'data-lang-key' in pattern:
            return content
        content = content.replace(pattern, replacement, 1)
    return content

def add_data_lang_keys(content, filepath):
    """Ajoute les attributs data-lang-key selon le fichier"""
    filename = Path(filepath).stem
    
    # Mappings spécifiques par fichier (patterns complets à remplacer)
    mappings = {
        'index': [
            ('<h1>🏡 Katikias 33</h1>', '<h1 data-lang-key="index.title">🏡 Katikias 33</h1>'),
            ('<p>Votre guide digital complet</p>', '<p data-lang-key="index.subtitle">Votre guide digital complet</p>'),
            ('<h3>Bienvenue à la maison !</h3>', '<h3 data-lang-key="index.welcome.title">Bienvenue à la maison !</h3>'),
            ('<h3>Les Equipements</h3>', '<h3 data-lang-key="index.equipements.title">Les Equipements</h3>'),
            ('<h3>La Résidence</h3>', '<h3 data-lang-key="index.residence.title">La Résidence</h3>'),
            ('<h3>À Proximité</h3>', '<h3 data-lang-key="index.proximity.title">À Proximité</h3>'),
            ('<h3>Votre Départ</h3>', '<h3 data-lang-key="index.departure.title">Votre Départ</h3>'),
            ('<h3>🔑 Accès Rapide</h3>', '<h3 data-lang-key="index.quick.title">🔑 Accès Rapide</h3>'),
            ('Merci de votre confiance ! Bon séjour à Katikias 33 🌟', '<p data-lang-key="index.footer">Merci de votre confiance ! Bon séjour à Katikias 33 🌟</p>'),
        ],
        'apartment_guide': [
            ('<h1>Plan de l\'appartement</h1>', '<h1 data-lang-key="apartment.title">Plan de l\'appartement</h1>'),
        ],
        'tips_and_tricks': [
            ('<h1>Les Essentiels à l\'arrivée</h1>', '<h1 data-lang-key="tips.title">Les Essentiels à l\'arrivée</h1>'),
        ],
        'residence': [
            ('<h1>La Résidence</h1>', '<h1 data-lang-key="residence.title">La Résidence</h1>'),
        ],
        'proximity': [
            ('<h1>📍 À Proximité</h1>', '<h1 data-lang-key="proximity.title">📍 À Proximité</h1>'),
        ],
        'departure_procedure': [
            ('<h1>Votre Départ</h1>', '<h1 data-lang-key="departure.title">Votre Départ</h1>'),
        ],
        'emergencies': [
            ('<h1>Urgences</h1>', '<h1 data-lang-key="emergencies.title">Urgences</h1>'),
        ],
    }
    
    # Mappings pour les pages de pièces
    room_mappings = {
        'salon': 'salon.title',
        'chambre': 'chambre.title',
        'cuisine': 'cuisine.title',
        'terrasse': 'terrasse.title',
        'salle_manger': 'salle_manger.title',
        'salle_deau': 'salle_deau.title',
        'wc': 'wc.title',
        'placard_bleu': 'placard.title',
    }
    
    # Appliquer les mappings spécifiques
    if filename in mappings:
        for pattern, replacement in mappings[filename]:
            if pattern in content and replacement not in content:
                content = content.replace(pattern, replacement, 1)
    
    # Appliquer les mappings pour les pages de pièces
    if filename in room_mappings:
        lang_key = room_mappings[filename]
        # Trouver le premier h1 qui n'a pas déjà data-lang-key
        pattern = r'<h1([^>]*)>([^<]+)</h1>'
        def replacer(match):
            attrs = match.group(1)
            text = match.group(2)
            if 'data-lang-key' not in attrs:
                return f'<h1 data-lang-key="{lang_key}">{text}</h1>'
            return match.group(0)
        content = re.sub(pattern, replacer, content, count=1)
    
    # Ajouter data-lang-key pour les boutons "Retour"
    if '← Retour' in content and 'data-lang-key="nav.back"' not in content:
        # Trouver les liens avec "← Retour"
        pattern = r'(<a[^>]*href="[^"]*"[^>]*>)\s*←\s*Retour(\s*</a>)'
        def replacer(match):
            return f'{match.group(1)}<span data-lang-key="nav.back">← Retour</span>{match.group(2)}'
        content = re.sub(pattern, replacer, content)
    
    return content

def process_html_file(filepath):
    """Traite un fichier HTML pour ajouter le multilingue"""
    print(f"Traitement de {filepath.name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Ajouter le CSS
    content = add_lang_css(content)
    
    # Ajouter le sélecteur HTML
    content = add_lang_selector(content)
    
    # Ajouter les data-lang-key
    content = add_data_lang_keys(content, filepath)
    
    # Ajouter le script lang.js
    content = add_lang_script(content)
    
    # Sauvegarder seulement si changements
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK - Modifie: {filepath.name}")
        return True
    else:
        print(f"  - Deja a jour: {filepath.name}")
        return False

def main():
    """Fonction principale"""
    print("Ajout du systeme multilingue aux fichiers HTML...")
    print("")
    
    # Lister tous les fichiers HTML
    html_files = list(Path('.').glob('*.html'))
    
    # Exclure index_multilangue.html (prototype)
    html_files = [f for f in html_files if f.name != 'index_multilangue.html']
    
    modified_count = 0
    
    for html_file in sorted(html_files):
        if process_html_file(html_file):
            modified_count += 1
    
    print("")
    print(f"{modified_count} fichier(s) modifie(s) sur {len(html_files)}")
    print("")
    print("OK - Systeme multilingue installe !")
    print("")
    print("Verifiez que le fichier assets/lang.js existe")

if __name__ == "__main__":
    main()
