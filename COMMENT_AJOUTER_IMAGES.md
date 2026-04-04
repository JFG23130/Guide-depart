# 📸 Guide Pratique : Comment ajouter des images

## 🔍 Où se trouve actuellement l'image dans le code ?

Dans le fichier `tips_and_tricks.html`, ligne 167, le code cherche l'image ici :
```html
<img src="telecommande_somfy.png" ...>
```

Cela signifie que l'image doit être **dans le même dossier** que `tips_and_tricks.html`.

## 📁 Structure actuelle

```
C:\Users\jfgir\Dev\Airbnb\Guide-depart\
├── index.html
├── tips_and_tricks.html        ← Le code cherche ici
├── telecommande_somfy.png      ← ← ← À AJOUTER ICI (dans Guide-depart)
├── images\
│   └── README.md
└── ...
```

## ✅ Méthode Simple : Ajouter directement dans Guide-depart

### Option 1 : Copier-Coller le fichier

1. **Trouvez votre image** sur votre ordinateur
   - Par exemple : `C:\Users\jfgir\OneDrive\Documents\Images\telecommande_somfy.png`

2. **Copiez le fichier** (Ctrl+C)

3. **Ouvrez le dossier** :
   ```
   C:\Users\jfgir\Dev\Airbnb\Guide-depart
   ```

4. **Collez le fichier** (Ctrl+V)
   - Le fichier `telecommande_somfy.png` doit maintenant être **dans le dossier Guide-depart**

5. **Vérifiez** : Vous devriez voir :
   ```
   Guide-depart\
   ├── telecommande_somfy.png   ← Votre image !
   ├── tips_and_tricks.html
   ├── index.html
   └── ...
   ```

### Option 2 : Drag & Drop dans l'explorateur Windows

1. Ouvrez deux fenêtres de l'explorateur Windows :
   - **Fenêtre 1** : Votre image (source)
   - **Fenêtre 2** : `C:\Users\jfgir\Dev\Airbnb\Guide-depart`

2. **Glissez** votre image de la fenêtre 1 vers la fenêtre 2
   - L'image est copiée automatiquement

## 🎨 Format et taille recommandés

### Pour la télécommande Somfy :
- **Format** : `.png` ou `.jpg`
- **Taille** : Maximum 800px de largeur
- **Poids** : Moins de 200 KB

### Comment optimiser ?

**Si l'image est trop lourde :**
1. Ouvrez-la avec **Paint** (intégré à Windows)
2. Cliquez sur **Redimensionner** (onglet Image)
3. Choisissez **300 pixels** de largeur
4. Enregistrez (Ctrl+S)

## 🔧 Méthode Alternative : Dossier images/ (plus organisé)

Si vous voulez organiser toutes les images dans un dossier dédié :

### 1. Créer le dossier (déjà fait !)
```
Guide-depart\images\
```

### 2. Ajouter votre image dans ce dossier
```
Guide-depart\images\
├── telecommande_somfy.png   ← Ajoutez ici
└── README.md
```

### 3. Modifier le code
Dans `tips_and_tricks.html`, ligne 167, changez :
```html
<img src="telecommande_somfy.png" ...>
```
en :
```html
<img src="images/telecommande_somfy.png" ...>
```

## ✅ Vérification

### Test rapide
1. Ouvrez `C:\Users\jfgir\Dev\Airbnb\Guide-depart\`
2. Vérifiez que `telecommande_somfy.png` est visible dans le dossier
3. Ouvrez `tips_and_tricks.html` dans votre navigateur
4. L'image devrait s'afficher !

### Si l'image ne s'affiche pas
- Vérifiez que le nom est **exactement** `telecommande_somfy.png`
- Vérifiez que l'extension est `.png` ou `.jpg`
- Vérifiez que l'image n'est pas dans un sous-dossier par erreur

## 🚀 Résumé en 3 étapes

1. **Trouvez votre image** sur votre PC
2. **Copiez-la** dans `C:\Users\jfgir\Dev\Airbnb\Guide-depart\`
3. **Nommez-la** `telecommande_somfy.png`

**C'est tout !** 🎉

## 📍 Chemin complet

```
C:\Users\jfgir\Dev\Airbnb\Guide-depart\telecommande_somfy.png
```

C'est là que doit se trouver le fichier !








