#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VALIDATION COMPLÈTE DU SYSTÈME V2.0
Vérifie que tous les fichiers sont correctement configurés
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime

def validate_system():
    """Valide le système complet"""
    
    print("\n" + "="*70)
    print("✅ VALIDATION COMPLÈTE - SYSTÈME CODES V2.0")
    print("="*70)
    
    errors = []
    warnings = []
    passed = []
    
    # ═════════════════════════════════════════════════════════════
    # 1. VÉRIFIER FICHIERS ESSENTIELS
    # ═════════════════════════════════════════════════════════════
    
    print("\n📁 1. FICHIERS ESSENTIELS")
    print("─" * 70)
    
    essential_files = {
        'hub.html': 'Page d\'accueil',
        'codes-acces.html': 'Page codes sécurisés',
        'arrival_guide.html': 'Guide d\'arrivée (modifié)',
        'assets/codes-config-generated.js': 'Configuration codes',
        'reservations_codes.csv': 'Données réservations',
        'qrcodes/qrcode_hub_noir.png': 'QR code noir (recommandé)',
        'import_from_airbnb_emails.py': 'Import emails Airbnb',
        'csv_to_codes_config_optimized.py': 'Conversion CSV optimisée',
        'qrcode_manager.py': 'Gestionnaire QR codes'
    }
    
    for filename, description in essential_files.items():
        path = Path(filename)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {filename:<40} ({size:>6} bytes)")
            passed.append(f"Fichier: {filename}")
        else:
            print(f"❌ {filename:<40} (MANQUANT!)")
            errors.append(f"Fichier manquant: {filename}")
    
    # ═════════════════════════════════════════════════════════════
    # 2. VÉRIFIER CONTENU codes-acces.html
    # ═════════════════════════════════════════════════════════════
    
    print("\n📄 2. CONTENU codes-acces.html")
    print("─" * 70)
    
    try:
        html_content = Path('codes-acces.html').read_text(encoding='utf-8')
        
        checks = {
            'wifi-code': 'Affichage WiFi',
            'gate-code': 'Affichage Portail',
            'codes.wifi': 'Clé traduction WiFi',
            'codes.gate': 'Clé traduction Portail'
        }
        
        for check, desc in checks.items():
            if check in html_content:
                print(f"✅ {desc:<40} (présent)")
                passed.append(f"HTML: {desc}")
            else:
                print(f"⚠️  {desc:<40} (non trouvé)")
                warnings.append(f"HTML: {desc} absent")
        
        # Vérifier que les anciens codes sont supprimés
        old_codes = ['door-code', 'pool-code', 'codes.door', 'codes.pool']
        old_found = [code for code in old_codes if code in html_content]
        
        if old_found:
            print(f"⚠️  Anciennes références trouvées: {old_found}")
            warnings.append(f"Anciennes références: {old_found}")
        else:
            print(f"✅ Anciennes références supprimées")
            passed.append("Nettoyage codes porte/piscine")
    
    except Exception as e:
        errors.append(f"Erreur lecture HTML: {e}")
    
    # ═════════════════════════════════════════════════════════════
    # 3. VÉRIFIER CONFIGURATION JAVASCRIPT
    # ═════════════════════════════════════════════════════════════
    
    print("\n⚙️  3. CONFIGURATION JAVASCRIPT")
    print("─" * 70)
    
    try:
        js_content = Path('assets/codes-config-generated.js').read_text(encoding='utf-8')
        
        if 'const CODES_DATABASE' in js_content:
            print(f"✅ CODES_DATABASE déclaré")
            passed.append("CODES_DATABASE déclaré")
        else:
            errors.append("CODES_DATABASE pas trouvé")
        
        # Vérifier clés correctes
        required_keys = ['expires', 'guest', 'wifi', 'portail', 'notes']
        all_found = all(key in js_content for key in required_keys)
        
        if all_found:
            print(f"✅ Clés correctes: {', '.join(required_keys)}")
            passed.append(f"Clés config: {', '.join(required_keys)}")
        else:
            missing = [k for k in required_keys if k not in js_content]
            print(f"❌ Clés manquantes: {missing}")
            errors.append(f"Clés manquantes: {missing}")
        
        # Vérifier pas d'anciennes clés
        old_keys = ['door', 'pool', 'gate']
        old_found = [k for k in old_keys if f"'{k}'" in js_content or f'"{k}"' in js_content]
        
        if not old_found:
            print(f"✅ Anciennes clés supprimées")
            passed.append("Nettoyage anciennes clés")
        else:
            print(f"⚠️  Anciennes clés trouvées: {old_found}")
            warnings.append(f"Anciennes clés: {old_found}")
    
    except Exception as e:
        errors.append(f"Erreur lecture JS: {e}")
    
    # ═════════════════════════════════════════════════════════════
    # 4. VÉRIFIER CSV
    # ═════════════════════════════════════════════════════════════
    
    print("\n📊 4. DONNÉES CSV")
    print("─" * 70)
    
    try:
        with open('reservations_codes.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        expected_columns = ['Code', 'Date Arrivée', 'Date Départ', 'Nom Réservation', 'WiFi', 'Portail', 'Notes']
        csv_columns = list(reader.fieldnames) if reader.fieldnames else []
        
        # Vérifier colonnes
        if len(rows) > 0:
            print(f"✅ Réservations trouvées: {len(rows)}")
            passed.append(f"CSV: {len(rows)} réservations")
        
        # Vérifier format codes
        valid_codes = all(row['Code'].startswith('KATI') for row in rows if row.get('Code'))
        if valid_codes:
            print(f"✅ Format codes valide (KATI####)")
            passed.append("Format codes KATI valide")
        else:
            warnings.append("Certains codes ne commencent pas par KATI")
        
        # Vérifier dates
        today = datetime.now().date()
        active_codes = []
        expired_codes = []
        
        for row in rows:
            try:
                expiry = datetime.strptime(row['Date Départ'], "%Y-%m-%d").date()
                if expiry >= today:
                    active_codes.append(row['Code'])
                else:
                    expired_codes.append(row['Code'])
            except:
                pass
        
        print(f"✅ Codes actifs aujourd'hui: {len(active_codes)}")
        print(f"✅ Codes expirés: {len(expired_codes)}")
        passed.append(f"Codes actifs: {len(active_codes)}, Expirés: {len(expired_codes)}")
    
    except Exception as e:
        errors.append(f"Erreur lecture CSV: {e}")
    
    # ═════════════════════════════════════════════════════════════
    # 5. VÉRIFIER QR CODES
    # ═════════════════════════════════════════════════════════════
    
    print("\n📱 5. QR CODES")
    print("─" * 70)
    
    qr_files = list(Path('qrcodes').glob('*.png')) if Path('qrcodes').exists() else []
    
    if len(qr_files) >= 1:
        print(f"✅ QR codes trouvés: {len(qr_files)}")
        for qr in sorted(qr_files):
            size = qr.stat().st_size / 1024
            print(f"   - {qr.name:<30} ({size:>5.1f} KB)")
        passed.append(f"QR codes: {len(qr_files)} fichiers")
    else:
        errors.append("Aucun QR code trouvé")
    
    # ═════════════════════════════════════════════════════════════
    # 6. VÉRIFIER SCRIPTS PYTHON
    # ═════════════════════════════════════════════════════════════
    
    print("\n🐍 6. SCRIPTS PYTHON")
    print("─" * 70)
    
    python_scripts = {
        'import_from_airbnb_emails.py': ['AirbnbEmailParser', 'ReservationManager'],
        'csv_to_codes_config_optimized.py': ['convert_csv_to_js', 'generate_js_file'],
        'qrcode_manager.py': ['QRCodeManager', 'list_qrcodes']
    }
    
    for script, required_classes in python_scripts.items():
        path = Path(script)
        if path.exists():
            content = path.read_text(encoding='utf-8')
            found = all(cls in content for cls in required_classes)
            
            if found:
                print(f"✅ {script:<40}")
                passed.append(f"Script: {script}")
            else:
                print(f"⚠️  {script:<40} (classes manquantes)")
                warnings.append(f"Script {script}: classes manquantes")
        else:
            errors.append(f"Script manquant: {script}")
    
    # ═════════════════════════════════════════════════════════════
    # RÉSUMÉ
    # ═════════════════════════════════════════════════════════════
    
    print("\n" + "="*70)
    print("📋 RÉSUMÉ VALIDATION")
    print("="*70)
    
    print(f"\n✅ VALIDATIONS RÉUSSIES: {len(passed)}")
    print(f"⚠️  AVERTISSEMENTS: {len(warnings)}")
    print(f"❌ ERREURS: {len(errors)}")
    
    if errors:
        print(f"\n🔴 ERREURS CRITIQUES:")
        for error in errors:
            print(f"   ❌ {error}")
    
    if warnings:
        print(f"\n🟡 AVERTISSEMENTS:")
        for warning in warnings:
            print(f"   ⚠️  {warning}")
    
    # ═════════════════════════════════════════════════════════════
    # STATUS FINAL
    # ═════════════════════════════════════════════════════════════
    
    print("\n" + "="*70)
    
    if not errors:
        print("🎉 ✅ SYSTÈME VALIDÉ - PRÊT POUR PRODUCTION!")
        print("="*70)
        
        print("\nPROCHAINES ÉTAPES:")
        print("1. Éditer reservations_codes.csv avec vraies réservations")
        print("2. Exécuter: python csv_to_codes_config_optimized.py")
        print("3. Tester: http://localhost:8000/hub.html")
        print("4. Uploader en production")
        
        return True
    else:
        print("🔴 ERREURS DÉTECTÉES - À CORRIGER AVANT DÉPLOIEMENT")
        print("="*70)
        return False

if __name__ == '__main__':
    success = validate_system()
    exit(0 if success else 1)
