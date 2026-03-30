#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 CONVERTISSEUR CSV → JAVASCRIPT OPTIMISÉ
Transforme reservations_codes.csv en assets/codes-config-generated.js
Uniquement WiFi + Portail (plus de porte/piscine)
"""

import csv
from datetime import datetime
from pathlib import Path

def convert_csv_to_js():
    """Convertit CSV → JavaScript"""
    
    csv_path = Path("reservations_codes.csv")
    js_path = Path("assets/codes-config-generated.js")
    
    if not csv_path.exists():
        print(f"❌ Fichier CSV non trouvé: {csv_path}")
        return False
    
    print("\n" + "="*60)
    print("📊 CONVERSION CSV → JAVASCRIPT")
    print("="*60)
    
    codes_database = {}
    active_codes = []
    expired_codes = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                code = row.get('Code', '').strip()
                check_in = row.get('Date Arrivée', '').strip()
                check_out = row.get('Date Départ', '').strip()
                guest = row.get('Nom Réservation', '').strip()
                wifi = row.get('WiFi', 'Katikias33').strip()
                portail = row.get('Portail', '9999').strip()
                notes = row.get('Notes', '').strip()
                
                if not code:
                    continue
                
                # Créer structure JavaScript
                codes_database[code] = {
                    'expires': check_out,
                    'guest': guest,
                    'wifi': wifi,
                    'portail': portail,
                    'notes': notes
                }
                
                # Vérifier si actif ou expiré
                now = datetime.now().date()
                try:
                    expiry_date = datetime.strptime(check_out, "%Y-%m-%d").date()
                    status = "✅" if now <= expiry_date else "❌"
                    
                    if now <= expiry_date:
                        active_codes.append((code, guest, check_out))
                    else:
                        expired_codes.append((code, guest, check_out))
                except:
                    status = "⚠️"
        
        # Générer fichier JavaScript
        js_content = generate_js_file(codes_database)
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"\n✅ Configuration générée: {js_path}")
        print(f"   Total codes: {len(codes_database)}")
        
        # Afficher statut
        print(f"\n📋 CODES ACTIFS ({len(active_codes)}):")
        for code, guest, expires in sorted(active_codes):
            print(f"   ✅ {code} | {guest} | Expire: {expires}")
        
        if expired_codes:
            print(f"\n⏰ CODES EXPIRÉS ({len(expired_codes)}):")
            for code, guest, expires in sorted(expired_codes):
                print(f"   ❌ {code} | {guest} | Expiré: {expires}")
        
        print("\n" + "="*60)
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def generate_js_file(codes_database):
    """Génère le contenu du fichier JavaScript"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    js = """/**
 * Configuration des codes d'accès
 * Générée automatiquement depuis reservations_codes.csv
 * Date: """ + timestamp + """
 * 
 * ✅ CODES INCLUS:
 *    - WiFi (SSID + mot de passe)
 *    - Portail (code d'accès)
 */

const CODES_DATABASE = {
"""
    
    # Ajouter chaque code
    for code, data in sorted(codes_database.items()):
        js += f"""    '{code}': {{
        expires: '{data['expires']}',
        guest: '{data['guest']}',
        wifi: '{data['wifi']}',
        portail: '{data['portail']}',
        notes: '{data['notes']}'
    }},
"""
    
    # Supprimer la dernière virgule
    js = js.rstrip(',\n') + '\n'
    
    js += """};\n"""
    
    return js

if __name__ == '__main__':
    convert_csv_to_js()
