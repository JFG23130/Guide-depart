#!/usr/bin/env python3
"""Nettoyer les clés orphelines sans casser la syntaxe"""

import re
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Clés à supprimer
orphans = set([
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
    # Plus les clés arrival_guide qui sont archivées
    "arrival_guide.h2.codes_daccès",
    "arrival_guide.h2.liens_utiles",
    "arrival_guide.h2.plan_de_lappartement",
    "arrival_guide.h2.à_votre_arrivée",
    "arrival_guide.h3.balcon",
    "arrival_guide.h3.chambres",
    "arrival_guide.h3.cuisine",
    "arrival_guide.h3.en_cas_durgence",
    "arrival_guide.h3.parking",
    "arrival_guide.h3.piscine",
    "arrival_guide.h3.porte_dentrée",
    "arrival_guide.h3.salle_de_bain",
    "arrival_guide.h3.wifi",
    "arrival_guide.li.astuces_conseils_pratiques",
    "arrival_guide.li.configurer_le_wifi_sur_vos_appareils",
    "arrival_guide.li.consulter_le_guide_de_lappartement",
    "arrival_guide.li.guide_complet_de_lappartement",
    "arrival_guide.li.noter_les_numéros_durgence",
    "arrival_guide.li.procédure_de_départ",
    "arrival_guide.li.récupérer_les_clés_dans_la_boîte_à_clés",
    "arrival_guide.li.vérifier_le_fonctionnement_des_équipemen",
    "arrival_guide.p.2_chambres_avec_lits_doubles",
    "arrival_guide.p.code_1234",
    "arrival_guide.p.code_5678",
    "arrival_guide.p.douche_wc_séparés",
    "arrival_guide.p.gestionnaire_33_5_xx_xx_xx_xx",
    "arrival_guide.p.katikias33welcome2024",
    "arrival_guide.p.merci_de_votre_confiance_bon_séjour_à_ka",
    "arrival_guide.p.place_réservée",
    "arrival_guide.p.police_17",
    "arrival_guide.p.pompierssamu_112",
    "arrival_guide.p.propriétaire_33_6_xx_xx_xx_xx",
    "arrival_guide.p.votre_guide_darrivée_complet",
    "arrival_guide.p.vue_sur_la_piscine",
    "arrival_guide.p.équipée_complète",
])

# Fichiers de traduction
lang_files = [
    ('assets/lang-fr.js', 'translationsFR'),
    ('assets/lang-en.js', 'translationsEN'),
    ('assets/lang-de.js', 'translationsDE'),
    ('assets/lang-es.js', 'translationsES'),
]

for filepath, var_name in lang_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire l'objet JSON
    match = re.search(rf'const {var_name} = ' + r'{(.*?)};', content, re.DOTALL)
    if not match:
        print(f"❌ Impossible de parser {filepath}")
        continue
    
    # Charger comme dict
    json_str = '{' + match.group(1) + '}'
    try:
        data = json.loads(json_str)
    except:
        # Parser avec regex si JSON échoue
        lines = content.split('\n')
        data = {}
        for line in lines:
            if '":' in line and not line.strip().startswith('//'):
                m = re.match(r'\s*"([^"]+)"\s*:\s*"([^"]*)",?\s*$', line)
                if m:
                    data[m.group(1)] = m.group(2)
    
    # Filtrer les orphans
    original_count = len(data)
    for key in orphans:
        data.pop(key, None)
    
    # Reconstruire le fichier
    lines = [f'// Fichier de traductions {var_name.replace("translations", "").lower()}']
    lines.append('// Katikias 33 - Guide multilingue')
    lines.append('')
    lines.append(f'const {var_name} = ' + '{')
    
    for i, (key, value) in enumerate(sorted(data.items())):
        comma = ',' if i < len(data) - 1 else ''
        # Échapper les guillemets dans la valeur
        safe_value = value.replace('"', '\\"')
        lines.append(f'    "{key}": "{safe_value}"{comma}')
    
    lines.append('};')
    lines.append('')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ {filepath}: {original_count} → {len(data)} clés (supprimé {original_count - len(data)})")

print(f"\n✅ Nettoyage complété!")
