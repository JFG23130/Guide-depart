#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer les QR codes pour le guide Katikias 33
"""

import qrcode
from qrcode.image.pil import PilImage

# URLs - Utiliser le domaine personnalisé guide.katikias33.fr
# Le domaine est configuré et vérifié dans GitHub Pages ✅
BASE_URL = "https://guide.katikias33.fr"

# Définition des 3 QR codes
qr_codes = [
    {
        "name": "qrcode_menu",
        "url": f"{BASE_URL}/",  # Pas de index.html, la racine suffit
        "label": "Menu Global"
    },
    {
        "name": "qrcode_depart",
        "url": f"{BASE_URL}/departure_procedure.html",
        "label": "Départ"
    },
    {
        "name": "qrcode_urgences",
        "url": f"{BASE_URL}/emergencies.html",
        "label": "Urgences"
    }
]

def generate_qrcode(url, filename, label):
    """Génère un QR code et le sauvegarde"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Créer l'image avec un fond blanc et un border
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Sauvegarder
    img.save(f"images/{filename}.png")
    print(f"QR code genere : {filename}.png ({label})")
    print(f"   URL : {url}")

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Generation des QR codes pour Katikias 33\n")
    
    for qr_info in qr_codes:
        generate_qrcode(
            qr_info["url"],
            qr_info["name"],
            qr_info["label"]
        )
    
    print("\nTous les QR codes ont ete generes dans le dossier images/")
    print("\nPour mettre a jour avec votre domaine personnalise (guide.katikias33.fr),")
    print("modifiez la variable BASE_URL dans ce script et re-executez-le.")

