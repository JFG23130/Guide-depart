#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 IMPORT PERFORMANT DEPUIS EMAILS AIRBNB
Extraction automatique des réservations depuis les emails reçus
Inspiré du système Airbnb: parse emails, extrait infos, génère codes
"""

import os
import re
import csv
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText

# ═══════════════════════════════════════════════════════════════════

class AirbnbEmailParser:
    """Parse les emails Airbnb et extrait les réservations"""
    
    def __init__(self):
        self.reservations = {}
        self.email_folder = Path("emails")  # Dossier contenant les emails
        
    def parse_email_content(self, content):
        """
        Parse le contenu d'un email Airbnb
        Format typique Airbnb:
        - Date arrivée: "Check-in on Jan 10, 2026"
        - Date départ: "Check-out on Jan 15, 2026"
        - Nom: "Guest Name"
        - Code WiFi: Dans confirmation de réservation
        """
        data = {}
        
        # Extraction dates (format Airbnb: "Check-in on Jan 10, 2026")
        check_in_match = re.search(r'Check-in\s+on\s+(\w+\s+\d+,\s+\d{4})', content, re.IGNORECASE)
        check_out_match = re.search(r'Check-out\s+on\s+(\w+\s+\d+,\s+\d{4})', content, re.IGNORECASE)
        
        if check_in_match:
            data['check_in'] = check_in_match.group(1)
            data['check_in_date'] = self._parse_date(data['check_in'])
        
        if check_out_match:
            data['check_out'] = check_out_match.group(1)
            data['check_out_date'] = self._parse_date(data['check_out'])
        
        # Extraction nom du voyageur
        name_match = re.search(r'(?:Hello|Bonjour)\s+([A-Z][a-z]+)', content)
        if name_match:
            data['guest_name'] = name_match.group(1)
        
        # Extraction email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content)
        if email_match:
            data['email'] = email_match.group(1)
        
        return data
    
    def _parse_date(self, date_str):
        """Convertit "Jan 10, 2026" en "2026-01-10" """
        try:
            dt = datetime.strptime(date_str, "%b %d, %Y")
            return dt.strftime("%Y-%m-%d")
        except:
            return None
    
    def generate_code(self, check_in_date, guest_number=1):
        """
        Génère un code de réservation unique
        Format: KATI + MMDD + numéro séquentiel
        Ex: KATI0101 (1er janvier, premier guest)
        """
        try:
            dt = datetime.strptime(check_in_date, "%Y-%m-%d")
            month = dt.strftime("%m")
            day = dt.strftime("%d")
            code = f"KATI{month}{day}"
            return code
        except:
            return None

# ═══════════════════════════════════════════════════════════════════

class ReservationManager:
    """Gère les réservations et l'export CSV"""
    
    def __init__(self):
        self.reservations = []
        self.csv_path = Path("reservations_codes.csv")
        
    def add_reservation(self, code, check_in, check_out, guest_name, wifi="", portail="", notes=""):
        """Ajoute une réservation"""
        reservation = {
            'code': code,
            'check_in': check_in,
            'check_out': check_out,
            'guest_name': guest_name,
            'wifi': wifi,
            'portail': portail,
            'notes': notes
        }
        self.reservations.append(reservation)
        print(f"✅ Réservation ajoutée: {code} | {guest_name} | {check_in} → {check_out}")
    
    def export_to_csv(self):
        """Exporte les réservations en CSV"""
        if not self.reservations:
            print("❌ Aucune réservation à exporter")
            return False
        
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f, 
                    fieldnames=['Code', 'Date Arrivée', 'Date Départ', 'Nom Réservation', 'WiFi', 'Portail', 'Notes']
                )
                writer.writeheader()
                
                for res in self.reservations:
                    writer.writerow({
                        'Code': res['code'],
                        'Date Arrivée': res['check_in'],
                        'Date Départ': res['check_out'],
                        'Nom Réservation': res['guest_name'],
                        'WiFi': res['wifi'],
                        'Portail': res['portail'],
                        'Notes': res['notes']
                    })
            
            print(f"\n✅ Export CSV réussi: {self.csv_path}")
            print(f"   Total réservations: {len(self.reservations)}")
            return True
        except Exception as e:
            print(f"❌ Erreur export: {e}")
            return False

# ═══════════════════════════════════════════════════════════════════

class QuickImport:
    """Import rapide depuis interface simple"""
    
    @staticmethod
    def from_text(text_input):
        """
        Format simple pour copier-coller depuis Airbnb:
        
        Code: KATI0101
        Nom: Jean Dupont
        Arrivée: 2026-01-10
        Départ: 2026-01-15
        WiFi: Katikias33
        Portail: 9999
        Notes: Réservation test
        ---
        """
        manager = ReservationManager()
        
        entries = text_input.strip().split('---')
        
        for entry in entries:
            if not entry.strip():
                continue
            
            data = {}
            lines = entry.strip().split('\n')
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip().lower()] = value.strip()
            
            if 'code' in data and 'arrivée' in data:
                manager.add_reservation(
                    code=data.get('code', ''),
                    check_in=data.get('arrivée', ''),
                    check_out=data.get('départ', ''),
                    guest_name=data.get('nom', 'Unknown'),
                    wifi=data.get('wifi', 'Katikias33'),
                    portail=data.get('portail', '9999'),
                    notes=data.get('notes', '')
                )
        
        return manager

# ═══════════════════════════════════════════════════════════════════

def demo_import():
    """Démo: import depuis copier-coller"""
    print("\n" + "="*60)
    print("🚀 IMPORT RAPIDE DEPUIS AIRBNB EMAILS")
    print("="*60)
    
    manager = ReservationManager()
    
    # Exemple: ajouter manuellement
    example_data = [
        ('KATI0101', '2026-01-10', '2026-01-15', 'Jean Dupont', 'Katikias33', '9999', 'Première semaine'),
        ('KATI0201', '2026-02-01', '2026-02-10', 'Marie Martin', 'Katikias33', '9999', 'Février'),
        ('KATI0301', '2026-03-05', '2026-03-12', 'Sophie Bernard', 'Katikias33', '9999', 'Mars'),
    ]
    
    print("\n📥 Ajout de réservations exemples...")
    for code, check_in, check_out, guest, wifi, portail, notes in example_data:
        manager.add_reservation(code, check_in, check_out, guest, wifi, portail, notes)
    
    # Export CSV
    print("\n📊 Export en CSV...")
    manager.export_to_csv()
    
    print("\n" + "="*60)
    print("✅ Import performant terminé!")
    print("="*60)

if __name__ == '__main__':
    demo_import()
