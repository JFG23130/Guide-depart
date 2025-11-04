# Documentation Complète du Guide Katikias 33

## Vue d'ensemble

Guide interactif pour location Airbnb avec navigation par pièces, images multiples, liens PDF et déploiement GitHub Pages.

## Structure du Projet

### Fichiers Principaux

- `index.html` - Page d'accueil avec navigation principale
- `apartment_guide.html` - Plan interactif de l'appartement
- `tips_and_tricks.html` - Essentiels à l'arrivée (codes, WiFi, etc.)
- `residence.html` - Informations sur la résidence
- `departure_procedure.html` - Procédure de départ
- `emergencies.html` - Numéros d'urgence

### Pages de Pièces

- `chambre.html` - Chambre à coucher
- `salon.html` - Salon
- `salle_manger.html` - Salle à manger
- `cuisine.html` - Cuisine
- `terrasse.html` - Terrasse
- `salle_deau.html` - Salle d'eau
- `wc.html` - WC
- `placard_bleu.html` - Placard

## Fonctionnalités Avancées

### 1. Gestion Automatique des Images

Chaque page de pièce charge automatiquement les images basées sur le nom de l'équipement.

#### Règles de Nommage

Les images doivent respecter ces règles :
1. **Minuscules uniquement** : `a-z`, `0-9`, `_`
2. **Sans accents** : é → e, à → a, ç → c
3. **Sans espaces** : remplacés par `_`
4. **Sans caractères spéciaux** : + → supprimé, - → _

**Exemples** :
```
"Box Canal+" → box_canal.png
"Mini réfrigérateur" → mini_refrigerateur.png
"Radiateur salle de bain" → radiateur_salle_de_bain.png
"Volets roulants" → volets_roulants.png
```

#### Format des Images

- **Extensions** : `.jpg`, `.jpeg`, `.png`, `.webp`
- **Poids recommandé** : < 300KB
- **Résolution** : Max 1920px
- **Placement** : Dossier `images/`

#### Images Multiples pour un Équipement

Ajouter des images supplémentaires :

1. **Image principale** : `nom_equipement.png`
2. **Images supplémentaires** : `nom_equipement_2.png`, `nom_equipement_3.png`, etc.

```html
<li>Four</li>
```

Chargera automatiquement :
- `four.png` (image principale)
- `four_2.png` (deuxième image)
- `four_3.png` (troisième image)

### 2. Légendes pour les Images

Ajouter des légendes avec l'attribut `data-captions` :

```html
<li data-captions="Vue d'ensemble | Télécommande face avant | Télécommande face arrière">Climatisation</li>
```

**Important** :
- La **première légende** (avant le premier `|`) = image principale
- La **deuxième légende** = `_2.png`
- La **troisième légende** = `_3.png`
- Séparer avec `|`

**Exemple de résultat** :
```
Climatisation
[image climatisation.png]
Vue d'ensemble

[image climatisation_2.png]
Télécommande face avant

[image climatisation_3.png]
Télécommande face arrière
```

### 3. Liens PDF (Manuels d'utilisation)

Ajouter un lien PDF sur une image :

```html
<li data-pdf="pdfs/bouilloire_sana.pdf">Bouilloire</li>
```

**Comportement** :
- L'image devient cliquable
- Clic → ouvre le PDF dans un nouvel onglet
- Curseur pointer sur l'image

**Placement des PDFs** :
- Dossier `pdfs/`
- Nommage avec underscores : `nom_equipement.pdf`

### 4. Combinaisons Avancées

Vous pouvez combiner `data-captions` et `data-pdf` :

```html
<li data-captions="Image 1 | Image 2" data-pdf="pdfs/equipement.pdf">Équipement</li>
```

**Comportement** :
- Image 1 : cliquable → ouvre le PDF
- Image 2 : normale (pas de PDF)

### 5. Plan Interactif

Le plan de l'appartement (`apartment_guide.html`) utilise des zones cliquables CSS.

**Structure** :
```html
<div style="position: relative;">
    <img src="images/plan_appartement_cliquable.png" />
    
    <!-- Zone cliquable -->
    <a href="salon.html" class="clickable-zone" 
       style="top: 33%; left: 14%; width: 84%; height: 24%;">
        <span class="zone-label">🛋️ Salon</span>
    </a>
</div>
```

**Ajustement des zones** :
- `top`, `left` : position (pourcentage)
- `width`, `height` : dimensions (pourcentage)

## Workflow de Développement

### 1. Modifications Locales

```bash
# 1. Ouvrir le fichier à modifier
# Exemple : salon.html, cuisine.html, etc.

# 2. Ajouter un équipement
<li>Nom de l'équipement</li>

# 3. Ajouter l'image correspondante
# → images/nom_de_lequipement.png

# 4. Tester localement
start salon.html
```

### 2. Compression des Images

Avant de déployer, compresser les images volumineuses :

```bash
python compress_images.py
```

**Le script** :
- Compresse automatiquement les images > 300KB
- Réduit jusqu'à 90% la taille
- Redimensionne si nécessaire
- Convertit PNG lourds en JPG

### 3. Déploiement GitHub Pages

```bash
.\deploy_auto.bat
```

**Ce que fait le script** :
- Vérifie l'état Git
- Ajoute tous les fichiers modifiés
- Crée un commit avec horodatage
- Push vers GitHub Pages
- Affiche l'URL du site

**Résultat** :
- Site en ligne en 1-2 minutes
- Accessible sur : https://jfg23130.github.io/Guide-depart/

## Guide Rapide par Tâche

### Ajouter un Nouvel Équipement

**1. Ajouter dans le HTML** :
```html
<li>Nom de l'équipement</li>
```

**2. Ajouter l'image** :
- Nommer : `nom_de_lequipement.png`
- Placer dans : `images/`
- < 300KB recommandé

**3. Tester** :
```bash
cd Guide-depart
start nom_page.html
```

### Ajouter Plusieurs Images à un Équipement

**1. Ajouter avec légendes** :
```html
<li data-captions="Image 1 | Image 2 | Image 3">Équipement</li>
```

**2. Ajouter les images** :
- `equipement.png`
- `equipement_2.png`
- `equipement_3.png`

### Ajouter un PDF Manuel

**1. Copier le PDF** :
```bash
Copy-Item "chemin/vers/manuel.pdf" "pdfs/nom_equipement.pdf"
```

**2. Ajouter dans le HTML** :
```html
<li data-pdf="pdfs/nom_equipement.pdf">Équipement</li>
```

### Compresser les Images

**Exécuter le script** :
```bash
python compress_images.py
```

**Résultat attendu** :
```
Compression des images volumineuses...

equipement.png : 1200.00 KB -> compression... OK: 120.00 KB (-90.0%)

45 image(s) compressee(s)
25102.57 KB economises
```

### Déployer en Ligne

**Exécuter** :
```bash
.\deploy_auto.bat
```

**Résultat** :
```
Deploiement termine !
Site disponible sur :
   https://jfg23130.github.io/Guide-depart/

Les modifications seront visibles dans 1-2 minutes
```

## Exemples Concrets

### Exemple 1 : Ajouter un Frigidaire

**HTML** :
```html
<li>Frigidaire</li>
```

**Image** :
- Fichier : `images/frigidaire.png`

**Résultat** : L'image s'affiche automatiquement sous "Frigidaire"

### Exemple 2 : TV avec 3 Images et PDF

**HTML** :
```html
<li data-captions="TV principale | Télécommande | Réglages" data-pdf="pdfs/TV.pdf">TV Salon</li>
```

**Images** :
- `tv_salon.png`
- `tv_salon_2.png`
- `tv_salon_3.png`

**PDF** :
- `pdfs/TV.pdf`

**Résultat** :
- 3 images avec légendes
- Image 1 cliquable → PDF
- Images 2 et 3 normales

### Exemple 3 : Équipement Simple

**HTML** :
```html
<li>Radiateur</li>
```

**Image** :
- `radiateur.png`

**Résultat** : Image unique, aucun PDF, aucune légende

## Notes Techniques

### Slugification Automatique

Le script convertit automatiquement le nom de l'équipement :
- Minuscules : `TV` → `tv`
- Suppression accents : `réfrigérateur` → `refrigerateur`
- Remplacement espaces : `Box TV` → `box_tv`
- Suppression caractères spéciaux : `Canal+` → `canal`

### Ordre de Recherche des Images

Pour "Box Canal+" dans `salon.html`, le script cherche :
1. `salon_box_canal.png`
2. `box_canal.png`

### Formats Supportés

Les images sont cherchées dans cet ordre :
1. `.jpg`
2. `.jpeg`
3. `.png`
4. `.webp`

### Performance

**Optimisations** :
- `loading="lazy"` sur les images
- Cache busting avec timestamp
- Compression < 300KB
- Redimensionnement max 1920px

## Page Spécifique : Tips & Tricks

Cette page a une structure spéciale :
- **Pas de script automatique** d'images
- **Images manuelles** avec `onerror` fallback
- **Sections collapsibles** pour organisation
- **Style distinct** (fond dégradé violet)

**Modifications** :
- Éditer directement le HTML
- Ajouter les sections `.section`
- Utiliser `.tip-card` pour chaque item

## Dépannage

### Image Ne S'Affiche Pas

**Vérifier** :
1. ✅ Nom de l'image correspond au slug : "Box Canal+" → `box_canal.png`
2. ✅ Extension correcte : `.png`, `.jpg`, `.jpeg`
3. ✅ Emplacement correct : `images/`
4. ✅ Poids raisonnable : < 1MB
5. ✅ Cache navigateur : Ctrl+F5

**Solution** :
```bash
# Vérifier le nom exact
ls images | grep -i canal

# Renommer si besoin
ren "Box Canal.png" box_canal.png
```

### PDF Ne S'Ouvre Pas

**Vérifier** :
1. ✅ Chemin correct : `pdfs/nom.pdf`
2. ✅ Fichier existe dans `pdfs/`
3. ✅ Attribut `data-pdf` bien formaté

**Solution** :
```bash
# Vérifier le fichier
ls pdfs/

# Tester le lien
start pdfs/bouilloire_sana.pdf
```

### Images Multiples Ne S'Affichent Pas

**Vérifier** :
1. ✅ `data-captions` présent sur le `<li>`
2. ✅ Nommage correct : `_2.png`, `_3.png`
3. ✅ Fichiers dans `images/`

**Solution** :
```html
<!-- Invalide -->
<li>Four</li>
<!-- Nécessite data-captions pour afficher _2.png -->

<!-- Valide -->
<li data-captions="Principal | Second">Four</li>
```

### Compression Échoue

**Installer Pillow** :
```bash
pip install Pillow
```

**Vérifier** :
```bash
python -c "import PIL; print('OK')"
```

### Déploiement Échoue

**Problème Git** :
```bash
# Vérifier l'état
git status

# Pull avant push
git pull origin main

# Réessayer
.\deploy_auto.bat
```

## Règles d'Or

### Images

✅ **FAIRE** :
- Utiliser minuscules + underscores
- Tester avant de déployer
- Compresser si > 300KB
- Utiliser des extensions standards

❌ **ÉVITER** :
- Espaces, accents, caractères spéciaux
- Fichiers > 1MB
- Compresser plusieurs fois
- Renommer après déploiement

### PDFs

✅ **FAIRE** :
- Placer dans `pdfs/`
- Nommer avec underscores
- Tester le lien

❌ **ÉVITER** :
- Espaces dans les noms
- Fichiers > 5MB
- PDFs brisés ou corrompus

### Déploiement

✅ **FAIRE** :
- Compresser les images avant
- Tester localement
- Commit descriptif
- Vérifier après déploiement

❌ **ÉVITER** :
- Déployer sans test local
- Oublier les fichiers
- Commit vide

## Support et Ressources

### Fichiers de Documentation

- `README.md` - Vue d'ensemble
- `GUIDE_RAPIDE.md` - Guide rapide
- `WORKFLOW_COMPLET.md` - Workflow détaillé
- `NOM_IMAGE_REGLE.md` - Règles de nommage
- `IMAGES_MULTIPLES.md` - Images multiples
- `pdf_integration.md` - Intégration PDF
- `COMPRESSION_IMAGES.md` - Compression
- `DOCUMENTATION_COMPLETE.md` - Cette page

### Scripts Utilitaires

- `compress_images.py` - Compression automatique
- `deploy_auto.bat` - Déploiement GitHub
- `generate_qrcodes.py` - Génération QR codes

### URLs Importantes

- **Site** : https://jfg23130.github.io/Guide-depart/
- **Menu** : https://jfg23130.github.io/Guide-depart/index.html
- **Essentiels** : https://jfg23130.github.io/Guide-depart/tips_and_tricks.html
- **Équipements** : https://jfg23130.github.io/Guide-depart/apartment_guide.html
- **Résidence** : https://jfg23130.github.io/Guide-depart/residence.html
- **Départ** : https://jfg23130.github.io/Guide-depart/departure_procedure.html


