#!/usr/bin/env python3
"""Ajouter les clés manquantes aux fichiers de traduction"""

import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Dictionnaire avec les traductions dans les 4 langues
missing_translations = {
    "chambre.li.climatisation": {
        "fr": "Climatisation Chambre",
        "en": "Bedroom Air Conditioning",
        "de": "Klimaanlage Schlafzimmer",
        "es": "Aire Acondicionado Dormitorio",
    },
    "departure_procedure.h2.heure_de_départ": {
        "fr": "Heure de départ",
        "en": "Departure Time",
        "de": "Abfahrtszeit",
        "es": "Hora de Salida",
    },
    "emergencies.strong.112": {
        "fr": "112",
        "en": "112",
        "de": "112",
        "es": "112",
    },
    "placard_bleu.li.service_à_raclette": {
        "fr": "Service à raclette",
        "en": "Raclette Set",
        "de": "Raclette-Set",
        "es": "Juego de Raclette",
    },
    "proximity.strong.aqualand_saintcyr": {
        "fr": "Aqualand Saint-Cyr",
        "en": "Aqualand Saint-Cyr",
        "de": "Aqualand Saint-Cyr",
        "es": "Aqualand Saint-Cyr",
    },
    "proximity.strong.autoroute_a50_sortie_12_bandol": {
        "fr": "Autoroute A50 (Sortie 12 Bandol)",
        "en": "Highway A50 (Exit 12 Bandol)",
        "de": "Autobahn A50 (Ausfahrt 12 Bandol)",
        "es": "Autopista A50 (Salida 12 Bandol)",
    },
    "proximity.strong.circuit_paul_ricard_du_castellet": {
        "fr": "Circuit Paul Ricard du Castellet",
        "en": "Paul Ricard Circuit Castellet",
        "de": "Paul Ricard Schaltung Castellet",
        "es": "Circuito Paul Ricard Castellet",
    },
    "proximity.strong.domaines_viticoles_de_bandol": {
        "fr": "Domaines viticoles de Bandol",
        "en": "Bandol Wine Estates",
        "de": "Weingüter in Bandol",
        "es": "Dominios Vinícolas de Bandol",
    },
    "proximity.strong.gare_sncf": {
        "fr": "Gare SNCF",
        "en": "SNCF Train Station",
        "de": "SNCF Bahnhof",
        "es": "Estación SNCF",
    },
    "proximity.strong.golf_de_frégate": {
        "fr": "Golf de Frégate",
        "en": "Frégate Golf Course",
        "de": "Golfplatz Frégate",
        "es": "Campo de Golf Frégate",
    },
    "proximity.strong.intermarché_carrefour_et_super_u": {
        "fr": "Intermarché, Carrefour et Super U",
        "en": "Intermarché, Carrefour and Super U",
        "de": "Intermarché, Carrefour und Super U",
        "es": "Intermarché, Carrefour y Super U",
    },
    "proximity.strong.marchés_de_bandol": {
        "fr": "Marchés de Bandol",
        "en": "Bandol Markets",
        "de": "Märkte in Bandol",
        "es": "Mercados de Bandol",
    },
    "proximity.strong.marchés_de_sanarysurmer": {
        "fr": "Marchés de Sanary-sur-Mer",
        "en": "Sanary-sur-Mer Markets",
        "de": "Märkte in Sanary-sur-Mer",
        "es": "Mercados de Sanary-sur-Mer",
    },
    "proximity.strong.que_faire_à_bandol": {
        "fr": "Que faire à Bandol ?",
        "en": "What to do in Bandol?",
        "de": "Was man in Bandol unternehmen kann",
        "es": "¿Qué hacer en Bandol?",
    },
    "proximity.strong.toulon": {
        "fr": "Toulon",
        "en": "Toulon",
        "de": "Toulon",
        "es": "Toulon",
    },
    "proximity.strong.villages_typiques": {
        "fr": "Villages typiques",
        "en": "Typical Villages",
        "de": "Typische Dörfer",
        "es": "Pueblos Típicos",
    },
    "proximity.strong.zoo_parc_de_sanarysurmer": {
        "fr": "Zoo Parc de Sanary-sur-Mer",
        "en": "Zoo Park Sanary-sur-Mer",
        "de": "Zoo Park Sanary-sur-Mer",
        "es": "Parque Zoo Sanary-sur-Mer",
    },
    "residence.p.les_gardiens_connaissent_bien_les_katiki": {
        "fr": "Les gardiens connaissent bien les Katikias et la région",
        "en": "The caretakers know Katikias and the region well",
        "de": "Die Hausmeister kennen Katikias und die Region gut",
        "es": "Los cuidadores conocen bien Katikias y la región",
    },
    "residence.strong.7h_à_20h_7_jours_sur_7": {
        "fr": "7h à 20h, 7 jours sur 7",
        "en": "7am to 8pm, 7 days a week",
        "de": "7 Uhr bis 20 Uhr, 7 Tage die Woche",
        "es": "7am a 20pm, 7 días a la semana",
    },
    "residence.strong.boulevard_du_bois_maurin": {
        "fr": "Boulevard du Bois Maurin",
        "en": "Boulevard du Bois Maurin",
        "de": "Boulevard du Bois Maurin",
        "es": "Boulevard du Bois Maurin",
    },
    "residence.strong.bracelets_rouges": {
        "fr": "Bracelets rouges",
        "en": "Red Bracelets",
        "de": "Rote Armbänder",
        "es": "Pulseras Rojas",
    },
    "residence.strong.local_poubelles_toujours_ouvert": {
        "fr": "Local Poubelles toujours ouvert",
        "en": "Trash Area Always Open",
        "de": "Müllraum immer offen",
        "es": "Área de Basura Siempre Abierta",
    },
    "residence.strong.obligatoire": {
        "fr": "Obligatoire",
        "en": "Mandatory",
        "de": "Erforderlich",
        "es": "Obligatorio",
    },
    "tips_and_tricks.strong.chambre": {
        "fr": "Chambre",
        "en": "Bedroom",
        "de": "Schlafzimmer",
        "es": "Dormitorio",
    },
    "tips_and_tricks.strong.disney_21": {
        "fr": "Disney+ (21)",
        "en": "Disney+ (21)",
        "de": "Disney+ (21)",
        "es": "Disney+ (21)",
    },
    "tips_and_tricks.strong.eau_calcaire": {
        "fr": "Eau calcaire",
        "en": "Hard Water",
        "de": "Hartes Wasser",
        "es": "Agua Dura",
    },
    "tips_and_tricks.strong.en_cas_de_mise_en_sécurité": {
        "fr": "En cas de mise en sécurité",
        "en": "In case of security lockdown",
        "de": "Im Falle einer Sicherheitsblockade",
        "es": "En caso de bloqueo de seguridad",
    },
    "tips_and_tricks.strong.important": {
        "fr": "Important - Sécurité",
        "en": "Important - Security",
        "de": "Wichtig - Sicherheit",
        "es": "Importante - Seguridad",
    },
    "tips_and_tricks.strong.important_sécurité": {
        "fr": "Important - Sécurité",
        "en": "Important - Security",
        "de": "Wichtig - Sicherheit",
        "es": "Importante - Seguridad",
    },
    "tips_and_tricks.strong.netflix_22": {
        "fr": "Netflix (22)",
        "en": "Netflix (22)",
        "de": "Netflix (22)",
        "es": "Netflix (22)",
    },
    "tips_and_tricks.strong.règlement": {
        "fr": "Règlement",
        "en": "Rules",
        "de": "Regeln",
        "es": "Reglas",
    },
    "tips_and_tricks.strong.salon": {
        "fr": "Salon",
        "en": "Living Room",
        "de": "Wohnzimmer",
        "es": "Sala de estar",
    },
    "tips_and_tricks.strong.solidarité": {
        "fr": "Solidarité",
        "en": "Solidarity",
        "de": "Solidarität",
        "es": "Solidaridad",
    },
    "tips_and_tricks.strong.symbole_neige": {
        "fr": "Symbole neige ❄️",
        "en": "Snow symbol ❄️",
        "de": "Schnee-Symbol ❄️",
        "es": "Símbolo de nieve ❄️",
    },
    "tips_and_tricks.strong.symbole_soleil": {
        "fr": "Symbole soleil ☀️",
        "en": "Sun symbol ☀️",
        "de": "Sonnensymbol ☀️",
        "es": "Símbolo de sol ☀️",
    },
}

# Fichiers de traduction
lang_files = {
    'fr': ('assets/lang-fr.js', 'translationsFR'),
    'en': ('assets/lang-en.js', 'translationsEN'),
    'de': ('assets/lang-de.js', 'translationsDE'),
    'es': ('assets/lang-es.js', 'translationsES'),
}

for lang_code, (filepath, var_name) in lang_files.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la fin de l'objet
    lines = content.split('\n')
    
    # Insérer les nouvelles traductions avant la fermeture
    new_lines = []
    added_count = 0
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Chercher la ligne avant la fermeture };
        if line.strip() == '};':
            # Insérer les traductions juste avant
            new_lines.pop()  # Enlever le };
            
            # Ajouter les nouvelles clés
            for key, translations in sorted(missing_translations.items()):
                translation = translations[lang_code]
                # Échapper les guillemets et apostrophes
                translation = translation.replace('"', '\\"').replace("'", "\\'")
                new_lines.append(f'    "{key}": "{translation}",')
                added_count += 1
            
            new_lines.append('};')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ {filepath}: ajouté {added_count} clés")

print(f"\n✅ Toutes les traductions ajoutées!")
