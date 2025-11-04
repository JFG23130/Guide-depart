# 📐 Plan Appartement - Instructions

## 📋 Images à fournir

Vous avez fourni **2 images** du plan de l'appartement :

### 1️⃣ Image avec bordures noires (Recommandée)
Cette image contient des **bordures noires rectangulaires** autour des zones cliquables.
- Utiliser cette image pour repérer les zones cliquables
- Les bordures définissent exactement où placer les clics

### 2️⃣ Image sans bordures (Afficher)
Cette image est "propre" sans bordures.
- Utiliser cette image pour l'affichage
- Plus esthétique une fois les zones définies

## 🎯 Zones cliquables définies

D'après vos images, les zones suivantes sont configurées :

| Pièce | Position approximative | Dimensions |
|-------|------------------------|------------|
| 🛏️ **Chambre** | Bas gauche | 35% x 28% |
| 🛁 **Salle d'eau** | Bas droite | 18% x 23% |
| 🚻 **WC** | Bas droite | 18% x 8% |
| 🍽️ **Cuisine** | Milieu droite | 18% x 22% |
| 🛋️ **Salon** | Centre | 50% x 35% |
| 🌤️ **Terrasse** | Haut | 100% x 15% |
| 🗄️ **Placard Bleu** | Milieu droite | 15% x 20% |

## 📁 Installation des images

### Option 1 : Utiliser l'image SANS bordures (recommandée)

1. **Renommer** votre image sans bordures : `plan_appartement_cliquable.png`
2. **Placer** dans : `Guide-depart/images/plan_appartement_cliquable.png`
3. ✅ Le plan affichera cette image avec les zones transparentes

### Option 2 : Utiliser l'image AVEC bordures

1. **Renommer** votre image avec bordures : `plan_appartement_cliquable.png`
2. **Placer** dans : `Guide-depart/images/plan_appartement_cliquable.png`
3. ⚠️ Les zones cliquables seront toujours visibles

## 🔧 Ajustement des zones cliquables

Si les zones ne correspondent pas exactement à vos pièces, ajuster dans `apartment_guide.html` :

```html
<a href="chambre.html" class="clickable-zone" 
   style="top: X%; left: X%; width: X%; height: X%;">
```

### Comment ajuster ?

1. **Top** : Distance du haut (0% = tout en haut)
2. **Left** : Distance de la gauche (0% = tout à gauche)
3. **Width** : Largeur de la zone
4. **Height** : Hauteur de la zone

**Exemple :**
```html
<!-- Zone qui commence à 20% du haut, 10% de la gauche, fait 30% de large et 25% de haut -->
<a href="chambre.html" class="clickable-zone" 
   style="top: 20%; left: 10%; width: 30%; height: 25%;">
```

## 📐 Dimensions recommandées pour l'image

| Format | Largeur | Hauteur | Poids max |
|--------|---------|---------|-----------|
| PNG | 800-1200px | Variable | 300 KB |

## ✅ Test

1. Placer l'image dans `Guide-depart/images/`
2. Ouvrir `apartment_guide.html` dans le navigateur
3. Tester chaque zone cliquable
4. Ajuster si nécessaire

## 🎨 Comportement des zones

- **Au survol** : La zone devient bleue transparente avec une bordure
- **Au clic** : Redirige vers la page de la pièce
- **Si image absente** : Affiche une liste de liens de secours

## 📚 Fichiers concernés

- ✅ `apartment_guide.html` - Page du plan
- 📁 `images/plan_appartement_cliquable.png` - Image du plan
- 📄 `PLAN_APPARTEMENT_INSTRUCTIONS.md` - Ce fichier

---

**Astuce** : Utilisez un outil comme **GIMP** ou **Photoshop** pour aligner parfaitement les zones avec votre plan en mode superposition !


