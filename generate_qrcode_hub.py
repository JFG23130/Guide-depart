#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un QR code pointant vers la page hub.html
Le QR code est fixe et ne change pas entre les réservations
"""

import qrcode
import os
from pathlib import Path

def generate_qr_code():
    """Générer un QR code vers la page hub.html"""
    
    # URL vers la page hub (à adapter à votre domaine)
    # Pour localhost: http://localhost:8000/hub.html
    # Pour production: https://votre-domaine.com/hub.html
    
    base_urls = {
        'localhost': 'http://localhost:8000/hub.html',
        'github': 'https://votre-github-pages.com/hub.html',  # À remplacer
        'custom': 'https://votre-domaine.com/hub.html'  # À remplacer
    }
    
    # Utiliser localhost par défaut
    url = base_urls['localhost']
    
    print("=" * 60)
    print("🔲 GÉNÉRATEUR DE QR CODE - Katikias 33")
    print("=" * 60)
    print(f"\n📱 URL pour le QR code: {url}")
    print("\n⚠️  À ADAPTER SELON VOTRE DÉPLOIEMENT:")
    print("   - Localhost: http://localhost:8000/hub.html")
    print("   - GitHub Pages: https://votre-username.github.io/repo-name/hub.html")
    print("   - Domaine custom: https://votre-domaine.com/hub.html")
    print("\n" + "=" * 60)
    
    # Créer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Créer les images
    img_default = qr.make_image(fill_color="black", back_color="white")
    
    # Créer un QR code coloré
    img_colored = qr.make_image(fill_color="#667eea", back_color="white")
    
    # Créer un QR code avec gradient simulé
    img_gradient = qr.make_image(fill_color="#764ba2", back_color="white")
    
    # Créer le dossier qrcodes s'il n'existe pas
    output_dir = Path(__file__).parent / "qrcodes"
    output_dir.mkdir(exist_ok=True)
    
    # Sauvegarder les images
    output_default = output_dir / "qrcode_hub_noir.png"
    output_colored = output_dir / "qrcode_hub_couleur.png"
    output_gradient = output_dir / "qrcode_hub_gradient.png"
    
    img_default.save(output_default)
    img_colored.save(output_colored)
    img_gradient.save(output_gradient)
    
    print(f"\n✅ QR codes générés avec succès!")
    print(f"\n📂 Fichiers créés dans le dossier 'qrcodes/':")
    print(f"   1. {output_default.name} (noir et blanc)")
    print(f"   2. {output_colored.name} (couleur)")
    print(f"   3. {output_gradient.name} (gradient)")
    
    print(f"\n📋 INSTRUCTIONS D'IMPRESSION:")
    print(f"   1. Choisir l'une des images QR")
    print(f"   2. Format recommandé: A5 (10cm x 10cm minimum)")
    print(f"   3. Plastifier pour durabilité")
    print(f"   4. Placer près de la porte d'entrée de l'appartement")
    
    print(f"\n🔗 URL codée: {url}")
    print(f"\n💡 Note: Le QR code est FIXE et ne change pas entre les réservations")
    print(f"   Seul le code d'accès à l'authentification change par voyageur")
    
    print("\n" + "=" * 60)
    print("🎉 C'est tout!")
    print("=" * 60 + "\n")

def update_url_in_code(base_url):
    """
    Fonction utilitaire pour mettre à jour l'URL du QR code
    Appeler après avoir changé votre domaine
    """
    print(f"📝 Pour mettre à jour l'URL du QR code, modifiez la variable 'url' dans ce script")
    print(f"   URL actuelle: {base_url}")

if __name__ == "__main__":
    try:
        generate_qr_code()
    except ImportError:
        print("❌ Erreur: qrcode n'est pas installé")
        print("   Installation: pip install qrcode[pil]")
    except Exception as e:
        print(f"❌ Erreur: {e}")
