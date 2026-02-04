#!/usr/bin/env python3
"""Ajouter les clés manquantes aux fichiers de traduction en extrayant du HTML"""

import re
import os
import glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Clés manquantes
missing_keys = [
    "chambre.li.climatisation",
    "departure_procedure.h2.heure_de_départ",
    "emergencies.strong.112",
    "placard_bleu.li.service_à_raclette",
    "proximity.strong.aqualand_saintcyr",
    "proximity.strong.autoroute_a50_sortie_12_bandol",
    "proximity.strong.circuit_paul_ricard_du_castellet",
    "proximity.strong.domaines_viticoles_de_bandol",
    "proximity.strong.gare_sncf",
    "proximity.strong.golf_de_frégate",
    "proximity.strong.intermarché_carrefour_et_super_u",
    "proximity.strong.marchés_de_bandol",
    "proximity.strong.marchés_de_sanarysurmer",
    "proximity.strong.que_faire_à_bandol",
    "proximity.strong.toulon",
    "proximity.strong.villages_typiques",
    "proximity.strong.zoo_parc_de_sanarysurmer",
    "residence.p.les_gardiens_connaissent_bien_les_katiki",
    "residence.strong.7h_à_20h_7_jours_sur_7",
    "residence.strong.boulevard_du_bois_maurin",
    "residence.strong.bracelets_rouges",
    "residence.strong.local_poubelles_toujours_ouvert",
    "residence.strong.obligatoire",
    "tips_and_tricks.strong.chambre",
    "tips_and_tricks.strong.disney_21",
    "tips_and_tricks.strong.eau_calcaire",
    "tips_and_tricks.strong.en_cas_de_mise_en_sécurité",
    "tips_and_tricks.strong.important",
    "tips_and_tricks.strong.important_sécurité",
    "tips_and_tricks.strong.netflix_22",
    "tips_and_tricks.strong.règlement",
    "tips_and_tricks.strong.salon",
    "tips_and_tricks.strong.solidarité",
    "tips_and_tricks.strong.symbole_neige",
    "tips_and_tricks.strong.symbole_soleil",
]

# Trouver les valeurs FR en scannant les HTML
key_values = {}

for html_file in glob.glob("*.html"):
    if html_file == "test-multilang.html":
        continue
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher les patterns data-lang-key="..." suivis du contenu
        # Cela va chercher le texte immédiatement après l'attribut data-lang-key
        for key in missing_keys:
            # Pattern pour trouver le texte après data-lang-key
            pattern = f'data-lang-key="?{re.escape(key)}"?[^>]*>([^<]+)<'
            matches = re.findall(pattern, content)
            
            if matches:
                value = matches[0].strip()
                # Nettoyer les emojis et garder la traduction
                value = re.sub(r'^[^\w]+', '', value).strip()  # Supprimer emojis au début
                if value and key not in key_values:
                    key_values[key] = value
                    print(f"✅ {key} = {value[:60]}")
    
    except Exception as e:
        print(f"⚠️ Erreur {html_file}: {e}")

print(f"\n📊 Trouvé {len(key_values)} valeurs sur {len(missing_keys)} clés manquantes")

# Ajouter manuellement les clés non trouvées (fallback)
fallback_values = {
    "chambre.li.climatisation": "Climatisation Chambre",
    "departure_procedure.h2.heure_de_départ": "Heure de départ",
    "emergencies.strong.112": "112",
    "placard_bleu.li.service_à_raclette": "Service à raclette",
    "proximity.strong.aqualand_saintcyr": "Aqualand Saint-Cyr",
    "proximity.strong.autoroute_a50_sortie_12_bandol": "Autoroute A50 sortie 12 Bandol",
    "proximity.strong.circuit_paul_ricard_du_castellet": "Circuit Paul Ricard du Castellet",
    "proximity.strong.domaines_viticoles_de_bandol": "Domaines viticoles de Bandol",
    "proximity.strong.gare_sncf": "Gare SNCF",
    "proximity.strong.golf_de_frégate": "Golf de Frégate",
    "proximity.strong.intermarché_carrefour_et_super_u": "Intermarché, Carrefour et Super U",
    "proximity.strong.marchés_de_bandol": "Marchés de Bandol",
    "proximity.strong.marchés_de_sanarysurmer": "Marchés de Sanary-sur-Mer",
    "proximity.strong.que_faire_à_bandol": "Que faire à Bandol ?",
    "proximity.strong.toulon": "Toulon",
    "proximity.strong.villages_typiques": "Villages typiques",
    "proximity.strong.zoo_parc_de_sanarysurmer": "Zoo Parc de Sanary-sur-Mer",
    "residence.p.les_gardiens_connaissent_bien_les_katiki": "Les gardiens connaissent bien les Katikias",
    "residence.strong.7h_à_20h_7_jours_sur_7": "7h à 20h, 7 jours sur 7",
    "residence.strong.boulevard_du_bois_maurin": "Boulevard du Bois Maurin",
    "residence.strong.bracelets_rouges": "Bracelets rouges",
    "residence.strong.local_poubelles_toujours_ouvert": "Local poubelles toujours ouvert",
    "residence.strong.obligatoire": "Obligatoire",
    "tips_and_tricks.strong.chambre": "Chambre",
    "tips_and_tricks.strong.disney_21": "Disney+, 21",
    "tips_and_tricks.strong.eau_calcaire": "Eau calcaire",
    "tips_and_tricks.strong.en_cas_de_mise_en_sécurité": "En cas de mise en sécurité",
    "tips_and_tricks.strong.important": "Important",
    "tips_and_tricks.strong.important_sécurité": "Important - Sécurité",
    "tips_and_tricks.strong.netflix_22": "Netflix, 22",
    "tips_and_tricks.strong.règlement": "Règlement",
    "tips_and_tricks.strong.salon": "Salon",
    "tips_and_tricks.strong.solidarité": "Solidarité",
    "tips_and_tricks.strong.symbole_neige": "Symbole neige",
    "tips_and_tricks.strong.symbole_soleil": "Symbole soleil",
}

# Fusionner avec les fallbacks
for key, value in fallback_values.items():
    if key not in key_values:
        key_values[key] = value

print(f"📊 Total final: {len(key_values)} traductions prêtes")
