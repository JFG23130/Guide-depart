#!/usr/bin/env python3
"""Ajouter les 2 clés manquantes"""

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

translations = {
    "residence.strong.lundi_au_vendredi": {
        "fr": "Lundi au vendredi 9h-12h et 18h-19h",
        "en": "Monday to Friday 9am-12pm and 6pm-7pm",
        "de": "Montag bis Freitag 9-12 Uhr und 18-19 Uhr",
        "es": "Lunes a viernes 9-12 y 18-19 horas",
    },
    "residence.strong.samedi": {
        "fr": "Samedi 9h-12h",
        "en": "Saturday 9am-12pm",
        "de": "Samstag 9-12 Uhr",
        "es": "Sábado 9-12 horas",
    },
}

for lang in ['fr', 'en', 'de', 'es']:
    var_name = f'translations{lang.upper()}'
    filepath = f'assets/lang-{lang}.js'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Ajouter avant };
    new_lines = []
    for line in lines:
        if line.strip() == '};':
            # Ajouter les clés manquantes
            for key, trans in sorted(translations.items()):
                value = trans[lang].replace('"', '\\"')
                new_lines.append(f'    "{key}": "{value}",\n')
        new_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'✅ {filepath}: ajouté 2 clés')

print('✅ Complètement synchronisé!')
