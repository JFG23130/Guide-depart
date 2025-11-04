# 📸 Règles de Nommage des Images

## 🎯 Principes Généraux

Le système de chargement automatique d'images dans les pages HTML utilise un système de **slugification** pour trouver les images.

### Comment ça marche ?

1. Vous créez un élément `<li>Nom de l'équipement</li>` dans un fichier HTML
2. Le script **slugifie** automatiquement le nom :
   - "Enceinte bluetooth" → `enceinte_bluetooth`
   - "Jeux de société" → `jeux_de_societe`
   - "Box Canal+" → `box_canal`
3. Il cherche ensuite les images dans cet ordre :
   - `{page}_slug.png` (ex: `salon_enceinte_bluetooth.png`)
   - `slug.png` (ex: `enceinte_bluetooth.png`)
   - `{page}_slug.jpg`
   - `slug.jpg`
   - Puis avec webp, jpeg...

## ✅ Format Standard

### Règles de nommage
- ✅ **Tout en minuscules**
- ✅ **Espaces remplacés par underscores** (`_`)
- ✅ **Accents supprimés** (é → e, ç → c, etc.)
- ✅ **Caractères spéciaux supprimés** (+, -, @, etc.)
- ✅ **Extensions :** `.png`, `.jpg`, `.webp`, `.jpeg`

### Exemples

| Nom dans HTML | Image recherchée |
|---------------|------------------|
| `Enceinte bluetooth` | `enceinte_bluetooth.png` |
| `Jeux de société` | `jeux_de_societe.png` |
| `Box Canal+` | `box_canal.png` |
| `Climatisation` | `climatisation.png` |
| `Salle d'eau` | `salle_deau.png` |
| `TV Salon` | `tv_salon.png` |

## 📁 Pages et Noms de Préfixe

Le script cherche d'abord avec le préfixe de la page :

| Page | Préfixe recherché |
|------|-------------------|
| `salon.html` | `salon_*.png` puis `*.png` |
| `chambre.html` | `chambre_*.png` puis `*.png` |
| `cuisine.html` | `cuisine_*.png` puis `*.png` |
| `salle_manger.html` | `salle_manger_*.png` puis `*.png` |
| `terrasse.html` | `terrasse_*.png` puis `*.png` |
| `wc.html` | `wc_*.png` puis `*.png` |
| `salle_deau.html` | `salle_deau_*.png` puis `*.png` |

## 🔧 Outil de Slugification

Pour convertir un nom en slug, utilisez cette fonction JavaScript :

```javascript
function slugify(text) {
    return text.toLowerCase()
        .normalize('NFD').replace(/\p{Diacritic}/gu,'')  // Retire accents
        .replace(/[^a-z0-9]+/g,'_')                      // Remplace non-alphanumerique par _
        .replace(/^_+|_+$/g,'')                          // Retire _ en début/fin
        .replace(/_{2,}/g,'_');                          // Retire doubles _
}
```

## 📋 Liste des Images Standardisées

### Salons & Pièces communes
- `salon_climatisation.png` ou `climatisation.png`
- `salon_enceinte_bluetooth.png` ou `enceinte_bluetooth.png`
- `salon_alexa.png` ou `alexa.png`
- `salon_tv_salon.png` ou `tv_salon.png`
- `salon_box_tv_orange.png` ou `box_tv_orange.png`
- `salon_box_canal.png` ou `box_canal.jpg`
- `salon_jeux_de_societe.png` ou `jeux_de_societe.jpg`
- `salon_canape_convertible.png` ou `canape_convertible.png`
- `salon_radiateur.png` ou `radiateur.png`

### Chambre
- `chambre_lit_160.png` ou `lit_160.png`
- `chambre_radiateur.png` ou `radiateur.png`
- `chambre_tv.png` ou `tv_chambre.png`
- `chambre_box_tv_orange.png` ou `box_orange.png`

### Cuisine
- `cuisine_four_micro_onde.png` ou `four_micro_onde.png`
- `cuisine_plaque_cuisson.png` ou `plaque_cuisson.png`
- `cuisine_lave_vaisselle.png` ou `lave_vaisselle.png`
- `cuisine_mini_frigo_congel.png` ou `mini_frigo_congel.png`
- `cuisine_machine_a_cafe.png` ou `machine_a_cafe.png`

### Salle d'eau
- `salle_deau_douche.png` ou `douche.png`
- `salle_deau_radiateur_salle_de_bain.png` ou `radiateur_sdb.png`
- `salle_deau_table_a_langer.png` ou `table_a_langer.png`

### Terrasse
- `terrasse_barbecue.png` ou `barbecue.png`
- `terrasse_plancha.png` ou `plancha.png`
- `terrasse_seche_linge.png` ou `seche_linge.png`

## ⚙️ Standardisation Automatique

### Script PowerShell pour renommer les images

Créez un fichier `rename_images.ps1` :

```powershell
# Fonction de slugification
function Slugify-Text {
    param([string]$Text)
    $text = $Text.ToLower()
    $text = $text -replace '[àáâãäå]', 'a'
    $text = $text -replace '[èéêë]', 'e'
    $text = $text -replace '[ìíîï]', 'i'
    $text = $text -replace '[òóôõö]', 'o'
    $text = $text -replace '[ùúûü]', 'u'
    $text = $text -replace '[ñ]', 'n'
    $text = $text -replace '[ç]', 'c'
    $text = $text -replace '[^a-z0-9]+', '_'
    $text = $text -replace '^_+|_+$', ''
    $text = $text -replace '__+', '_'
    return $text
}

# Renommer toutes les images
Get-ChildItem "images\*.*" | Where-Object { $_.Extension -in @('.png','.jpg','.jpeg','.webp') } | ForEach-Object {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    $newName = Slugify-Text $baseName
    $newFullName = "images\$newName$($_.Extension)"
    
    if ($_.FullName -ne $newFullName) {
        Rename-Item $_.FullName $newFullName -Force
        Write-Host "Renamed: $($_.Name) -> $newName$($_.Extension)"
    }
}
```

## 🚨 Problèmes Courants

### L'image ne s'affiche pas

1. **Vérifier le nom** : Le nom doit être exactement en minuscules, underscores, pas d'accents
2. **Vérifier l'extension** : `.png`, `.jpg`, `.webp`, `.jpeg` sont supportés
3. **Vérifier le chemin** : Fichier dans `Guide-depart/images/`
4. **Vider le cache** : Ctrl+F5 dans le navigateur
5. **Vérifier la console** : F12 pour voir les erreurs de chargement

### Exemples d'erreurs

| Mauvais nom | Bon nom |
|-------------|---------|
| `Enceinte bluetooth.png` | `enceinte_bluetooth.png` |
| `Jeux de société.png` | `jeux_de_societe.png` |
| `Climatisation.JPG` | `climatisation.jpg` |
| `Box Canal+.png` | `box_canal.png` |
| `TV-Salon.png` | `tv_salon.png` |

## ✅ Checklist de Vérification

- [ ] Nom en minuscules
- [ ] Pas d'espaces (remplacer par `_`)
- [ ] Pas d'accents
- [ ] Pas de caractères spéciaux (+, -, @, etc.)
- [ ] Extension correcte (.png, .jpg, etc.)
- [ ] Fichier dans `Guide-depart/images/`
- [ ] Cache du navigateur vidé (Ctrl+F5)

---

**Astuce** : Utilisez le script PowerShell ci-dessus pour standardiser automatiquement tous vos noms de fichiers ! 🚀


