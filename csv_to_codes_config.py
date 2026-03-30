#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir le CSV des réservations en configuration JavaScript
Utilité: Gérer facilement les codes d'accès via Excel/Sheets
"""

import csv
from pathlib import Path
from datetime import datetime

def csv_to_codes_config(csv_file='reservations_codes.csv', output_file='assets/codes-config-generated.js'):
    """
    Convertir reservations_codes.csv en assets/codes-config.js
    
    Format CSV attendu:
    Code,Date Arrivée,Date Départ,Nom Réservation,Porte,Piscine,Portail,Notes
    """
    
    codes_config = {}
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                code = row['Code'].strip().upper()
                date_depart = row['Date Départ'].strip()  # Format: YYYY-MM-DD
                
                # Validation date
                try:
                    datetime.strptime(date_depart, '%Y-%m-%d')
                except ValueError:
                    print(f"⚠️  Format date invalide pour {code}: {date_depart}")
                    continue
                
                codes_config[code] = {
                    'expires': date_depart,
                    'guest': row['Nom Réservation'].strip(),
                    'door': row['Porte'].strip(),
                    'pool': row['Piscine'].strip(),
                    'gate': row['Portail'].strip(),
                    'notes': row['Notes'].strip()
                }
                print(f"✅ {code} - Expire: {date_depart}")
        
        # Générer le fichier JavaScript
        js_content = generate_javascript(codes_config)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"\n✅ Configuration générée: {output_file}")
        print(f"📊 Total: {len(codes_config)} codes")
        
        return codes_config
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {csv_file}")
        return None

def generate_javascript(codes_dict):
    """Générer le contenu JavaScript"""
    
    js_lines = [
        "/**",
        " * Configuration des codes d'accès",
        " * Générée automatiquement depuis reservations_codes.csv",
        f" * Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        " */",
        "",
        "const CODES_DATABASE = {",
    ]
    
    for code, data in codes_dict.items():
        js_lines.append(f"    '{code}': {{")
        js_lines.append(f"        expires: '{data['expires']}',")
        js_lines.append(f"        guest: '{data['guest']}',")
        js_lines.append(f"        door: '{data['door']}',")
        js_lines.append(f"        pool: '{data['pool']}',")
        js_lines.append(f"        gate: '{data['gate']}',")
        js_lines.append(f"        notes: '{data['notes']}'")
        js_lines.append("    },")
    
    # Retirer la dernière virgule
    if js_lines[-1].endswith(','):
        js_lines[-1] = js_lines[-1][:-1]
    
    js_lines.extend([
        "};",
        "",
        "// À intégrer dans codes-acces.html avant le script principal:",
        "// <script src=\"codes-config-generated.js\"></script>",
    ])
    
    return "\n".join(js_lines)

def show_active_codes(codes_dict):
    """Afficher les codes actifs aujourd'hui"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    active = []
    expired = []
    
    for code, data in codes_dict.items():
        if data['expires'] >= today:
            active.append((code, data['guest'], data['expires']))
        else:
            expired.append((code, data['guest'], data['expires']))
    
    print("\n📋 CODES ACTIFS AUJOURD'HUI:")
    print("=" * 50)
    if active:
        for code, guest, expires in sorted(active, key=lambda x: x[2]):
            print(f"✅ {code} | {guest} | Expires: {expires}")
    else:
        print("Aucun code actif")
    
    print("\n⏰ CODES EXPIRÉS:")
    print("=" * 50)
    if expired:
        for code, guest, expires in sorted(expired, key=lambda x: x[2], reverse=True):
            print(f"❌ {code} | {guest} | Expiré: {expires}")
    else:
        print("Aucun code expiré")

if __name__ == "__main__":
    print("=" * 60)
    print("📋 CSV TO CODES CONFIG CONVERTER")
    print("=" * 60)
    
    # Convertir CSV en JS
    codes = csv_to_codes_config()
    
    if codes:
        # Afficher les codes actifs/expirés
        show_active_codes(codes)
        
        print("\n" + "=" * 60)
        print("🔧 INSTRUCTIONS D'INTÉGRATION:")
        print("=" * 60)
        print("1. Le fichier 'assets/codes-config-generated.js' a été créé")
        print("2. Ajouter dans codes-acces.html avant </body>:")
        print("   <script src=\"assets/codes-config-generated.js\"></script>")
        print("3. Le script codes-acces.html utilisera CODES_DATABASE automatiquement")
        print("\n💡 Ou remplacer le contenu de CODES_DATABASE dans codes-acces.html")
        print("=" * 60 + "\n")
