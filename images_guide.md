# 📸 Guide de Gestion des Images

## 📋 Format et Taille Recommandés

### Formats acceptés
- **JPG** (recommanded pour photos)
- **PNG** (recommandé pour logos/schémas)
- **WebP** (moderne, léger)
- **SVG** (pour schémas simples)

### Tailles optimales
- **Télécommandes, petits appareils** : 200-400px de largeur
- **Photos d'ensemble** : 600-800px de largeur
- **Plans, schémas** : 400-600px de largeur
- **Résolution** : 72-96 DPI suffit pour le web

### Poids maximum
- **Petites images** (< 300px) : < 50 KB
- **Images moyennes** (< 600px) : < 150 KB
- **Grandes images** (< 800px) : < 300 KB

## 🔧 Configuration HTML

### Code recommandé pour les images

```html
<div class="image-container">
    <img src="nom_image.jpg" 
         alt="Description de l'image"
         style="max-width: 300px; height: auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
         loading="lazy"
         onerror="this.parentElement.innerHTML='<div style=\'background:#f0f0f0;padding:40px;text-align:center;border-radius:10px;border:2px dashed #ccc;\'><p style=\'color:#666;\'>📷 Image à venir</p><p style=\'font-size:0.9rem;color:#999;\'>Ajoutez l\'image dans le dossier</p></div>'">
    </img>
</div>
```

## 🚀 Script d'optimisation automatique

Créez un fichier `optimize_images.bat` :

```batch
@echo off
echo Optimisation des images pour le guide...

cd Guide-depart

REM Installer ImageMagick ou utiliser PIL Python
REM python optimize_images.py

echo Images optimisees!
pause
```

## 📁 Structure des dossiers recommandée

```
Guide-depart/
├── images/
│   ├── telecommandes/
│   │   ├── somfy.png
│   │   └── clim.png
│   ├── equipements/
│   │   ├── cuisine.jpg
│   │   └── douche.jpg
│   └── plans/
│       └── residence.jpg
├── index.html
└── ...
```

## ✅ Bonnes Pratiques

1. **Nommage** : Utilisez des noms clairs (pas d'espaces)
   - ✅ `telecommande_somfy.png`
   - ❌ `IMG_2024_01_15.png`

2. **Compression** : Comprimez avant upload
   - Outil : TinyPNG, Squoosh, ou Photoshop

3. **Fallback** : Toujours prévoir un fallback
   - Le code ci-dessus gère automatiquement

4. **Lazy loading** : Pour améliorer les performances
   - Attribut `loading="lazy"`

5. **Responsive** : Toujours utiliser `max-width: 100%`
   - S'adapte aux petits écrans

## 🛠️ Outils Recommandés

- **Compression** : TinyPNG.com, Squoosh.app
- **Redimensionnement** : Paint.NET (gratuit), GIMP
- **Conversion** : CloudConvert.com
- **Optimisation** : Sharp (Node.js), PIL (Python)





