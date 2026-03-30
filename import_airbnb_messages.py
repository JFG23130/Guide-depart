#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 RÉCUPÉRATION DES CODES DEPUIS EMAILS AIRBNB
Génère access_codes.js et access_codes.json depuis les emails reçus
Réutilise la structure existante et fonctionnelle du projet Airbnb
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from string import ascii_uppercase, digits
from random import choice

# ═══════════════════════════════════════════════════════════════════

class AirbnbMessageParser:
    """Parse messages Airbnb et récupère les réservations"""
    
    def __init__(self):
        self.codes = []
        self.email_patterns = {
            # Pattern 1: Check-in/Check-out dates
            'dates': r'(?:Check-in|Arrivée)\s+(?:on|le)\s+(\w+\s+\d{1,2},?\s+\d{4})',
            # Pattern 2: Guest name
            'name': r'(?:Bonjour|Hello|Hi)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            # Pattern 3: Email address
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        }
    
    def parse_message_text(self, text):
        """Parse un texte de message Airbnb"""
        data = {}
        
        # Extraire nom (chercher "Guest:" ou après "Bonjour")
        guest_match = re.search(r'Guest:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text, re.IGNORECASE)
        if guest_match:
            data['guest'] = guest_match.group(1)
        else:
            # Fallback: chercher après "Bonjour"
            hello_match = re.search(r'(?:Bonjour|Hello|Hi)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text)
            if hello_match:
                data['guest'] = hello_match.group(1)
        
        # Extraire dates (Check-in, Check-out, Arrivée, Départ)
        dates = re.findall(r'(?:Check-in|Arrivée|Check-out|Départ)\s+(?:on|le)\s+([A-Za-z\s\d,]+)', text)
        if dates:
            data['check_in'] = dates[0].strip()
            if len(dates) > 1:
                data['check_out'] = dates[1].strip()
        
        # Extraire email
        emails = re.findall(self.email_patterns['email'], text)
        if emails:
            data['email'] = emails[0]
        
        return data
    
    def generate_code(self):
        """Génère un code unique au format KATI-XXXXXXX"""
        chars = ascii_uppercase + digits
        random_part = ''.join(choice(chars) for _ in range(7))
        return f"KATI-{random_part}"
    
    def add_reservation(self, guest_name, email=None, dates=None):
        """Ajoute une réservation"""
        code = self.generate_code()
        
        entry = {
            'code': code,
            'guest': guest_name,
            'email': email or '',
            'dates': dates or ''
        }
        
        self.codes.append(entry)
        print(f"✅ Code généré: {code} | {guest_name}")
        
        return code
    
    def export_access_codes_js(self, output_file='access_codes.js'):
        """Exporte en format JS (compatible avec l'existing)"""
        
        # Format: window.__ACCESS_CODES__ = [...]
        js_array = []
        for entry in self.codes:
            js_array.append({
                'code': entry['code'],
                'guest': entry['guest']
            })
        
        js_content = f"""// Fichier genere automatiquement - ne pas modifier a la main
window.__ACCESS_CODES__ = {json.dumps(js_array)};
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"✅ Exporte: {output_file}")
        return output_file
    
    def export_access_codes_json(self, output_file='access_codes.json'):
        """Exporte en format JSON"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.codes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exporte: {output_file}")
        return output_file
    
    def export_codes_config(self, output_file='reservations_codes.csv'):
        """Exporte en format CSV pour notre system V2"""
        
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['Code', 'Date Arrivée', 'Date Départ', 'Nom Réservation', 'WiFi', 'Portail', 'Notes']
            )
            writer.writeheader()
            
            for entry in self.codes:
                writer.writerow({
                    'Code': entry['code'],
                    'Date Arrivée': entry.get('dates', ''),
                    'Date Départ': entry.get('dates', ''),
                    'Nom Réservation': entry['guest'],
                    'WiFi': 'Katikias33',
                    'Portail': '9999',
                    'Notes': f"Email: {entry.get('email', '')}"
                })
        
        print(f"✅ Exporte: {output_file}")
        return output_file

# ═══════════════════════════════════════════════════════════════════

class EmailImportManager:
    """Gère l'import depuis messages Airbnb copiés"""
    
    @staticmethod
    def from_clipboard_paste(text):
        """Import depuis texte copié depuis Airbnb"""
        
        parser = AirbnbMessageParser()
        
        # Splitter par messages multiples (delimiter: ---)
        messages = text.strip().split('---')
        
        for msg in messages:
            if not msg.strip():
                continue
            
            data = parser.parse_message_text(msg)
            if 'guest' in data:
                parser.add_reservation(
                    guest_name=data['guest'],
                    email=data.get('email'),
                    dates=data.get('check_in', '')
                )
        
        return parser
    
    @staticmethod
    def interactive_input():
        """Mode interactif pour ajouter des réservations"""
        
        parser = AirbnbMessageParser()
        
        print("\n" + "="*60)
        print("📧 AJOUT INTERACTIF DE RÉSERVATIONS")
        print("="*60)
        print("Entrez les informations des voyageurs (laisser vide pour terminer)\n")
        
        while True:
            guest = input("Nom du voyageur: ").strip()
            if not guest:
                break
            
            email = input("Email (optionnel): ").strip()
            dates = input("Dates de séjour (optionnel): ").strip()
            
            parser.add_reservation(guest, email, dates)
            print()
        
        return parser

# ═══════════════════════════════════════════════════════════════════

def demo_from_airbnb_messages():
    """Démo: import depuis messages Airbnb typiques"""
    
    print("\n" + "="*60)
    print("📧 IMPORT DEPUIS EMAILS AIRBNB")
    print("="*60)
    
    # Exemple de messages Airbnb
    sample_messages = """
Bonjour Béatrix,

Vous avez une nouvelle réservation!

Check-in on January 10, 2026
Check-out on January 15, 2026

Guest: Jean Dupont
Email: jean.dupont@example.com

---

Bonjour Béatrix,

Nouvelle réservation confirmée!

Check-in on February 1, 2026
Check-out on February 10, 2026

Guest: Marie Martin
Email: marie.martin@example.com

---

Bonjour Béatrix,

Réservation reçue!

Arrivée le March 5, 2026
Départ le March 12, 2026

Guest: Sophie Bernard
Email: sophie.bernard@example.com
"""
    
    parser = EmailImportManager.from_clipboard_paste(sample_messages)
    
    print(f"\n✅ Total réservations importées: {len(parser.codes)}")
    print("\n📋 Codes générés:")
    for entry in parser.codes:
        print(f"   {entry['code']} | {entry['guest']}")
    
    # Exporter
    print("\n📁 Exports...")
    parser.export_access_codes_js('access_codes.js')
    parser.export_access_codes_json('access_codes.json')
    parser.export_codes_config('reservations_codes.csv')
    
    print("\n" + "="*60)
    print("✅ IMPORT TERMINÉ!")
    print("="*60)
    
    return parser

# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        # Mode interactif
        parser = EmailImportManager.interactive_input()
        
        if parser.codes:
            print("\n📁 Exports...")
            parser.export_access_codes_js('access_codes.js')
            parser.export_access_codes_json('access_codes.json')
            parser.export_codes_config('reservations_codes.csv')
            
            print("\n✅ Import terminé!")
    else:
        # Mode démo
        demo_from_airbnb_messages()
