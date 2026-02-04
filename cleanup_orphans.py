#!/usr/bin/env python3
"""Nettoyer les clés orphelines des fichiers de traduction"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lire html-usage.js pour obtenir les clés utilisées
with open('assets/html-usage.js', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_keys = set(re.findall(r'^\s+"([\w\.]+)"', html_content, re.MULTILINE))

print(f"🔍 Clés utilisées: {len(html_keys)}")

# Clés à supprimer
orphans = [
    "apartment.guide.link",
    "apartment.guide.title",
    "apartment.subtitle",
    "apartment.title",
    "apartment_guide.li.essentiels_à_larrivée",
    "apartment_guide.li.la_résidence",
    "apartment_guide.li.mon_départ",
    "apartment_guide.li.à_proximité",
    "departure.subtitle",
    "departure.title",
    "emergencies.subtitle",
    "emergencies.title",
    "index.departure.desc",
    "index.equipements.desc",
    "index.essentiels.desc",
    "index.proximity.desc",
    "index.quick.piscine",
    "index.quick.piscine.bracelet",
    "index.quick.portail.car",
    "index.quick.portail.ped",
    "index.quick.urgences",
    "index.quick.wifi",
    "index.residence.desc",
    "index.welcome.text1",
    "index.welcome.text2",
    "index.welcome.text3",
    "index.welcome.text4",
    "index.welcome.text5",
    "proximity.subtitle",
    "residence.li.lundi_au_vendredi_9h12h_et_18h19h",
    "residence.li.samedi_9h12h",
    "residence.p.ajoutez_imagesplan_accesjpg",
    "residence.subtitle",
    "residence.title",
    "room.back",
    "room.equipments",
    "room.no_image",
    "tips.subtitle",
    "tips.title",
    "tips_and_tricks.h3.wifi",
    "tips_and_tricks.p.mot_de_passe_cmxplqydfcu7qcyl3n",
    "tips_and_tricks.p.nom_du_réseau_livebox6a50",
]

# Fichiers de traduction
lang_files = ['assets/lang-fr.js', 'assets/lang-en.js', 'assets/lang-de.js', 'assets/lang-es.js']

for lang_file in lang_files:
    with open(lang_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_length = len(content.split('\n'))
    
    # Supprimer chaque clé orpheline
    for orphan in orphans:
        # Pattern pour trouver et supprimer la ligne de clé-valeur
        pattern = f'\\s*["\']?{re.escape(orphan)}["\']?\\s*:\\s*["\'][^"\']*["\'],?\\n'
        content = re.sub(pattern, '', content)
    
    with open(lang_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_length = len(content.split('\n'))
    removed = original_length - new_length
    print(f"✅ {lang_file}: supprimé ~{removed} lignes")

print(f"\n✅ Nettoyage complété!")
