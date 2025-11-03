#!/usr/bin/env python3
"""
Script de compression des images volumineuses
Réduit automatiquement les images de plus de 300KB
"""

import os
from pathlib import Path
from PIL import Image
import sys

def compress_image(input_path, output_path, quality=85, max_size_kb=300):
    """Compresse une image pour atteindre une taille maximale"""
    try:
        img = Image.open(input_path)
        
        # Si l'image est trop grande, redimensionner
        max_dimension = 1200  # Largeur/hauteur max réduit à 1200px pour le web
        
        if img.width > max_dimension or img.height > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        # Convertir RGBA en RGB pour JPG
        if str(output_path).lower().endswith(('.jpg', '.jpeg')):
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
        
        # Sauvegarder avec compression
        img.save(output_path, optimize=True, quality=quality)
        
        new_size_kb = os.path.getsize(output_path) / 1024
        return new_size_kb
        
    except Exception as e:
        print(f"   ERREUR : {e}")
        return None

def main():
    print("Compression des images volumineuses...")
    print("")
    
    image_dir = Path("images")
    target_size_kb = 150  # Réduit à 150KB pour de meilleures performances web
    compressed_count = 0
    total_saved = 0
    
    for img_file in image_dir.iterdir():
        if not img_file.is_file() or img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            continue
        
        size_kb = img_file.stat().st_size / 1024
        
        if size_kb > target_size_kb:
            print(f"{img_file.name} : {size_kb:.2f} KB -> compression...", end=" ")
            
            # Créer le fichier de sortie
            output_path = image_dir / f"{img_file.stem}_compressed{img_file.suffix}"
            
            # Déterminer le format de sortie et la qualité
            if img_file.suffix.lower() in ['.jpg', '.jpeg']:
                output_path = output_path.with_suffix('.jpg')
                # Qualité adaptative pour JPG selon taille
                if size_kb > 200:
                    quality = 50
                elif size_kb > 150:
                    quality = 55
                else:
                    quality = 60
            elif size_kb > 300:  # PNG > 300KB → convertir en JPG
                output_path = output_path.with_suffix('.jpg')
                quality = 55
            else:
                quality = 80  # PNG < 300KB conservé mais compressé
            
            new_size_kb = compress_image(img_file, output_path, quality)
            
            if new_size_kb and new_size_kb > 0:
                reduction = (1 - new_size_kb / size_kb) * 100
                saved_kb = size_kb - new_size_kb
                
                # Ne remplacer que si on a réduit la taille
                if new_size_kb < size_kb:
                    print(f"OK: {new_size_kb:.2f} KB (-{reduction:.1f}%)")
                    
                    # Remplacer l'original par la version compressée
                    img_file.unlink()
                    output_path.rename(img_file)
                    
                    compressed_count += 1
                    total_saved += saved_kb
                else:
                    print(f"SKIP: {new_size_kb:.2f} KB (+{-reduction:.1f}%) - conserver original")
                    output_path.unlink()  # Supprimer le fichier compressé sans avantage
            else:
                print("ERREUR")
    
    print("")
    if compressed_count > 0:
        print(f"{compressed_count} image(s) compressee(s)")
        print(f"{total_saved:.2f} KB economises")
    else:
        print("Aucune image a compresser")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur")
        sys.exit(1)
    except ImportError:
        print("Module PIL (Pillow) non installe")
        print("")
        print("Installation:")
        print("   pip install Pillow")
        sys.exit(1)

