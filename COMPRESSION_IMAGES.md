# Guide de Compression des Images

## Problème

Certaines images font plus de 300KB ou même 1000KB+, ce qui ralentit le chargement sur internet, surtout sur mobile.

## Solution Automatique

Un script Python compresse automatiquement toutes les images de plus de 150KB.

### Utilisation

```bash
cd Guide-depart
python compress_images.py
```

### Résultats

Le script :
- ✅ Compresse automatiquement les images > 150KB
- ✅ Réduit jusqu'à 90% la taille (de 1400KB à 60KB par exemple)
- ✅ Redimensionne si nécessaire (max 1200px pour le web)
- ✅ Convertit les PNG très lourds en JPG
- ✅ Qualité adaptative selon la taille de l'image
- ✅ Ne remplace que si la compression est efficace
- ✅ Conserve les originaux si la compression n'améliore pas

### Exemple de Compression

Avant :
```
lit_parapluie_bebe_2.png : 1493,54 KB
Box_TV_Orange.jpeg : 1492,02 KB
Four_micro_onde.png : 1433,55 KB
```

Après :
```
lit_parapluie_bebe_2.png : 148,10 KB (-90,1%)
Box_TV_Orange.jpeg : 629,31 KB (-57,8%)
Four_micro_onde.png : 173,06 KB (-87,9%)
```

### Économies Typiques

- **~20MB économisés** sur un guide complet (de ~30MB à ~7.5MB)
- **Taille moyenne** : ~100KB par image
- **Chargement 5-10x plus rapide** sur mobile
- **Meilleure expérience utilisateur** sur connexions lentes

## Compression Manuelle (Alternative)

Si vous préférez compresser manuellement :

### Outils Recommandés

1. **Online** :
   - https://tinypng.com/ (PNG)
   - https://compressjpeg.com/ (JPG)

2. **Logiciels** :
   - ImageMagick
   - Photoshop (Export > Web)
   - GIMP (Export optimisé)

### Paramètres Recommandés

- **JPG** : Qualité 50-75 selon la taille
- **PNG** : Si > 300KB, convertir en JPG
- **Résolution** : Max 1200px de large/haute
- **Poids cible** : < 150KB par image

## Règles Importantes

✅ **À faire** :
- Compresser les images avant de les ajouter
- Tester le rendu après compression
- Garder les originaux en backup

❌ **À éviter** :
- Compresser plusieurs fois (perte de qualité)
- Compresser les QR codes (ils doivent rester nets)
- Compresser les petits fichiers déjà optimisés (< 150KB)

## Quand Exécuter le Script

Exécutez le script :
- ✅ Après avoir ajouté de nouvelles images
- ✅ Avant le déploiement sur GitHub Pages
- ✅ Si vous remarquez des lenteurs de chargement

## Note Technique

Le script utilise Python + Pillow (PIL) pour :
- Redimensionnement intelligent
- Compression JPEG optimisée
- Conversion PNG → JPG si nécessaire
- Préservation de la qualité visuelle

## Fichiers Non Compressés

Les fichiers suivants sont **intentionnellement non compressés** :
- QR codes (.png)
- Fichiers < 150KB déjà optimisés

