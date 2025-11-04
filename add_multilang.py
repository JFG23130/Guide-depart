#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter automatiquement le système multilingue à tous les fichiers HTML
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
    # Chercher la balise </style>
    if '</style>' in content:
        # Insérer avant </style>
        content = content.replace('</style>', LANG_CSS + '\n    </style>')
    return content

def add_lang_selector(content):
    """Ajoute le sélecteur de langue dans le body"""
    # Chercher <body>
    if '<body>' in content:
        # Insérer après <body>
        content = content.replace('<body>', '<body>\n' + LANG_SELECTOR_HTML)
    elif '<body ' in content:
        # Si <body> a des attributs, trouver la fin de la balise
        pattern = r'(<body[^>]*>)'
        def replacer(match):
            return match.group(0) + '\n' + LANG_SELECTOR_HTML
        content = re.sub(pattern, replacer, content, count=1)
    return content

def add_lang_script(content):
    """Ajoute le script lang.js avant </body>"""
    # Chercher </body>
    if '</body>' in content:
        # Vérifier si assets/lang.js n'est pas déjà inclus
        if 'assets/lang.js' not in content:
            # Insérer avant </body>
            content = content.replace('</body>', LANG_SCRIPT + '</body>')
    return content

def add_data_lang_keys(content, filepath):
    """Ajoute les attributs data-lang-key selon le fichier"""
    filename = Path(filepath).stem
    
    # Mappings spécifiques par fichier
    mappings = {
        'index': [
            (r'<h1>🏡 Katikias 33</h1>', '<h1 data-lang-key="index.title">🏡 Katikias 33</h1>'),
            (r'<p>Votre guide digital complet</p>', '<p data-lang-key="index.subtitle">Votre guide digital complet</p>'),
            (r'<h3>Bienvenue à la maison !</h3>', '<h3 data-lang-key="index.welcome.title">Bienvenue à la maison !</h3>'),
            (r'💌 Mot d\'accueil', '<span data-lang-key="index.welcome.greeting">💌 Mot d\'accueil</span>'),
            (r'<h3>Les Equipements</h3>', '<h3 data-lang-key="index.equipements.title">Les Equipements</h3>'),
            (r'<h3>La Résidence</h3>', '<h3 data-lang-key="index.residence.title">La Résidence</h3>'),
            (r'<h3>À Proximité</h3>', '<h3 data-lang-key="index.proximity.title">À Proximité</h3>'),
            (r'<h3>Votre Départ</h3>', '<h3 data-lang-key="index.departure.title">Votre Départ</h3>'),
            (r'<h3>🔑 Accès Rapide</h3>', '<h3 data-lang-key="index.quick.title">🔑 Accès Rapide</h3>'),
            (r'Merci de votre confiance ! Bon séjour à Katikias 33', 'data-lang-key="index.footer"'),
        ],
        'apartment_guide': [
            (r'<h1>Plan de l\'appartement</h1>', '<h1 data-lang-key="apartment.title">Plan de l\'appartement</h1>'),
            (r'<p>Cliquez sur une pièce pour voir ses équipements</p>', '<p data-lang-key="apartment.subtitle">Cliquez sur une pièce pour voir ses équipements</p>'),
        ],
        'tips_and_tricks': [
            (r'<h1>Les Essentiels à l\'arrivée</h1>', '<h1 data-lang-key="tips.title">Les Essentiels à l\'arrivée</h1>'),
        ],
        'residence': [
            (r'<h1>La Résidence</h1>', '<h1 data-lang-key="residence.title">La Résidence</h1>'),
        ],
        'proximity': [
            (r'<h1>📍 À Proximité</h1>', '<h1 data-lang-key="proximity.title">📍 À Proximité</h1>'),
        ],
        'departure_procedure': [
            (r'<h1>Votre Départ</h1>', '<h1 data-lang-key="departure.title">Votre Départ</h1>'),
        ],
        'emergencies': [
            (r'<h1>Urgences</h1>', '<h1 data-lang-key="emergencies.title">Urgences</h1>'),
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
            if 'data-lang-key=' in replacement:
                # Ajouter l'attribut à la balise
                content = re.sub(pattern, lambda m: m.group(0).replace('>', ' ' + replacement + '>'), content, count=1)
            else:
                content = re.sub(pattern, replacement, content, count=1)
    
    # Appliquer les mappings pour les pages de pièces
    for room_name, lang_key in room_mappings.items():
        if filename == room_name:
            # Trouver le h1 principal
            pattern = r'(<h1[^>]*>)([^<]+)(</h1>)'
            def replacer(match):
                if 'data-lang-key' not in match.group(0):
                    return f'<h1 data-lang-key="{lang_key}">{match.group(2)}</h1>'
                return match.group(0)
            content = re.sub(pattern, replacer, content, count=1)
            break
    
    # Ajouter data-lang-key pour les boutons "Retour"
    content = re.sub(r'(<a[^>]*href="[^"]*"[^>]*>)\s*←\s*Retour', 
                     r'\1<span data-lang-key="nav.back">← Retour</span>', 
                     content)
    
    return content

def process_html_file(filepath):
    """Traite un fichier HTML pour ajouter le multilingue"""
    print(f"Traitement de {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Ajouter le CSS
    if '.lang-selector' not in content:
        content = add_lang_css(content)
    
    # Ajouter le sélecteur HTML
    if 'langSelector' not in content:
        content = add_lang_selector(content)
    
    # Ajouter les data-lang-key
    content = add_data_lang_keys(content, filepath)
    
    # Ajouter le script lang.js
    if 'assets/lang.js' not in content:
        content = add_lang_script(content)
    
    # Sauvegarder seulement si changements
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK - Modifie: {filepath}")
        return True
    else:
        print(f"  - Déjà à jour: {filepath}")
        return False

def main():
    """Fonction principale"""
    print("Ajout du système multilingue aux fichiers HTML...")
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
    print(f"{modified_count} fichier(s) modifié(s) sur {len(html_files)}")
    print("")
    print("OK - Systeme multilingue installe !")
    print("")
    print("N'oubliez pas de vérifier que le fichier assets/lang.js existe")

if __name__ == "__main__":
    main()
