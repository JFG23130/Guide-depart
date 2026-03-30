#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GESTIONNAIRE OPTIMISÉ DE QR CODES
Affichage, gestion et génération de QR codes pour hub.html
Inspiré du système Airbnb: cache, réutilisabilité, optimisation
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════

class QRCodeManager:
    """Gère les QR codes de manière performante"""
    
    def __init__(self):
        self.qrcodes_dir = Path('qrcodes')
        self.qrcodes_dir.mkdir(exist_ok=True)
        self.cache_dir = Path('.qr_cache')
        self.cache_dir.mkdir(exist_ok=True)
        
    def list_qrcodes(self):
        """Liste tous les QR codes disponibles"""
        qrcodes = list(self.qrcodes_dir.glob('*.png'))
        
        if not qrcodes:
            print("❌ Aucun QR code trouvé dans le dossier 'qrcodes/'")
            return []
        
        print("\n" + "="*60)
        print("📊 QR CODES DISPONIBLES")
        print("="*60)
        
        for i, qrcode in enumerate(sorted(qrcodes), 1):
            size = qrcode.stat().st_size / 1024  # En KB
            print(f"{i}. {qrcode.name:<30} ({size:.1f} KB)")
        
        return qrcodes
    
    def get_qrcode_info(self, filename):
        """Récupère les infos d'un QR code"""
        path = self.qrcodes_dir / filename
        
        if not path.exists():
            return None
        
        stat = path.stat()
        return {
            'name': filename,
            'path': str(path),
            'size': stat.st_size,
            'size_kb': stat.st_size / 1024,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'url': f'qrcodes/{filename}'
        }
    
    def generate_html_display(self, qrcode_filename='qrcode_hub_noir.png', width=200):
        """Génère du HTML pour afficher un QR code"""
        
        info = self.get_qrcode_info(qrcode_filename)
        if not info:
            return f"<!-- QR code '{qrcode_filename}' non trouvé -->"
        
        html = f"""
<!-- QR Code Display (hub.html) -->
<div class="qr-code-display">
    <h3>📱 Scanner pour accéder aux codes</h3>
    <img src="{info['url']}" 
         alt="QR Code" 
         width="{width}px" 
         height="{width}px">
    <p>Scannez ce code avec votre téléphone</p>
</div>
"""
        return html
    
    def generate_markdown_docs(self):
        """Génère documentation des QR codes"""
        qrcodes = self.list_qrcodes()
        
        markdown = """# 📱 Gestion des QR Codes

## Codes disponibles

"""
        for qrcode in sorted(qrcodes):
            info = self.get_qrcode_info(qrcode.name)
            markdown += f"""
### {qrcode.name}
- **Taille:** {info['size_kb']:.1f} KB
- **Chemin:** `{info['url']}`
- **Dernière mise à jour:** {info['modified'].strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        markdown += """
## Utilisation

### Dans hub.html
```html
<div class="qr-code">
    <img src="qrcodes/qrcode_hub_noir.png" alt="QR Code" width="250px">
</div>
```

### Affichage dans l'appartement
1. Imprimer le format `qrcode_hub_noir.png` (noir & blanc, meilleur contraste)
2. Tailler à 10cm × 10cm (A5)
3. Plastifier pour durabilité
4. Afficher près de la porte d'entrée

### Formats disponibles
- **qrcode_hub_noir.png** ← Recommandé (contraste maximal)
- **qrcode_hub_couleur.png** (design Airbnb blue)
- **qrcode_hub_gradient.png** (design moderne)

## Régénération

Si vous changez l'URL du hub.html:
```bash
python generate_qrcode_hub.py
```

Le script détectera automatiquement les changements et régénérera les codes.
"""
        
        return markdown
    
    def check_health(self):
        """Vérifie la santé des QR codes"""
        qrcodes = list(self.qrcodes_dir.glob('*.png'))
        
        print("\n" + "="*60)
        print("🏥 HEALTH CHECK - QR CODES")
        print("="*60)
        
        if not qrcodes:
            print("❌ ERREUR: Aucun QR code trouvé!")
            return False
        
        print(f"✅ QR codes trouvés: {len(qrcodes)}")
        for qrcode in sorted(qrcodes):
            size = qrcode.stat().st_size
            if size < 1000:
                print(f"⚠️  {qrcode.name}: {size} bytes (anormalement petit)")
            else:
                print(f"✅ {qrcode.name}: {size/1024:.1f} KB")
        
        # Vérifier hub.html
        hub_path = Path('hub.html')
        if hub_path.exists():
            content = hub_path.read_text(encoding='utf-8')
            if 'qrcodes/' in content:
                print("\n✅ hub.html contient des références aux QR codes")
            else:
                print("\n⚠️  hub.html ne référence pas les QR codes")
        
        print("\n" + "="*60)
        return True

# ═══════════════════════════════════════════════════════════════════

def show_menu():
    """Affiche le menu interactif"""
    
    manager = QRCodeManager()
    
    while True:
        print("\n" + "="*60)
        print("🎯 QR CODE MANAGER - MENU")
        print("="*60)
        print("1. Lister les QR codes")
        print("2. Vérifier santé (health check)")
        print("3. Générer HTML pour hub.html")
        print("4. Générer documentation")
        print("5. Quitter")
        print("="*60)
        
        choice = input("Choisir une option (1-5): ").strip()
        
        if choice == '1':
            manager.list_qrcodes()
        
        elif choice == '2':
            manager.check_health()
        
        elif choice == '3':
            filename = input("Nom du fichier QR code (ex: qrcode_hub_noir.png): ").strip()
            html = manager.generate_html_display(filename)
            print("\n" + html)
            
            # Proposer de sauvegarder
            save = input("\nSauvegarder dans un fichier ? (o/n): ").strip().lower()
            if save == 'o':
                output_file = 'qr_display.html'
                Path(output_file).write_text(html, encoding='utf-8')
                print(f"✅ Sauvegardé dans {output_file}")
        
        elif choice == '4':
            markdown = manager.generate_markdown_docs()
            output_file = 'QR_CODES_DOCS.md'
            Path(output_file).write_text(markdown, encoding='utf-8')
            print(f"\n✅ Documentation générée: {output_file}")
        
        elif choice == '5':
            print("\n👋 Au revoir!")
            break
        
        else:
            print("❌ Option invalide")

# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Mode ligne de commande
        command = sys.argv[1]
        manager = QRCodeManager()
        
        if command == 'list':
            manager.list_qrcodes()
        elif command == 'health':
            manager.check_health()
        elif command == 'docs':
            markdown = manager.generate_markdown_docs()
            Path('QR_CODES_DOCS.md').write_text(markdown, encoding='utf-8')
            print("✅ Documentation générée: QR_CODES_DOCS.md")
    else:
        # Mode menu interactif
        show_menu()
