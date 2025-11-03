# 📸 Résumé - Gestion Automatique des Images

## ✅ Toutes les Pages Sont Déjà Configurées !

Toutes vos pages HTML (`salon.html`, `chambre.html`, `cuisine.html`, `terrasse.html`, `salle_deau.html`, `wc.html`, `placard_bleu.html`, `salle_manger.html`) utilisent **déjà le même système automatique** de gestion des images.

## 🎯 Fonctionnement Automatique

### Dans vos pages HTML

Vous créez simplement une liste :
```html
<ul>
    <li>Enceinte bluetooth</li>
    <li>Jeux de société</li>
    <li>Canapé convertible</li>
</ul>
```

Le script JavaScript **ajoute automatiquement** les images sous chaque élément !

## 📋 Règle Universelle de Nommage

### Formule Simple

```
Nom dans HTML → slug → nom du fichier image
```

### Transformation

| Étape | Exemple |
|-------|---------|
| Nom dans HTML | `Enceinte bluetooth` |
| → Slug | `enceinte_bluetooth` |
| → Nom fichier | `enceinte_bluetooth.png` |

### Règles à Retenir

1. **Tout en minuscules**
2. **Espaces → underscore** (`_`)
3. **Accents supprimés** (é → e, ç → c)
4. **Caractères spéciaux supprimés** (+, -, @, #)
5. **Extensions supportées** : `.png`, `.jpg`, `.webp`, `.jpeg`

### Exemples Pratiques

| Élément HTML | Nom Fichier Image |
|--------------|-------------------|
| `<li>Climatisation</li>` | `climatisation.png` |
| `<li>Enceinte bluetooth</li>` | `enceinte_bluetooth.png` |
| `<li>Jeux de société</li>` | `jeux_de_societe.png` |
| `<li>Box Canal+</li>` | `box_canal.jpg` |
| `<li>Canapé convertible</li>` | `canape_convertible.png` |
| `<li>Machine à laver</li>` | `machine_a_laver.png` |
| `<li>TV Salon</li>` | `tv_salon.png` |
| `<li>Plaque cuisson vitro céramique</li>` | `plaque_cuisson_vitro_ceramique.png` |

## 🔍 Ordre de Recherche des Images

Le script cherche les images dans cet ordre :

1. `{page}_{slug}.png` (ex: `salon_enceinte_bluetooth.png`)
2. `{slug}.png` (ex: `enceinte_bluetooth.png`)
3. `{page}_{slug}.jpg`
4. `{slug}.jpg`
5. `{page}_{slug}.webp`
6. `{slug}.webp`
7. `{page}_{slug}.jpeg`
8. `{slug}.jpeg`

**Si aucune image trouvée** : Aucune image ne s'affiche (pas d'erreur)

## 📁 Structure des Pages

Toutes les pages suivent la même structure :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Nom de la Pièce</title>
    <style>/* Styles identiques */</style>
</head>
<body>
    <a href="apartment_guide.html" class="back-button">← Retour</a>
    <div class="container">
        <div class="header">
            <h1>🏠 Nom de la Pièce</h1>
        </div>
        <div class="content">
            <ul>
                <li>Équipement 1</li>
                <li>Équipement 2</li>
                <!-- Ajoutez simplement des <li> ici ! -->
            </ul>
        </div>
    </div>
    <script>
        // Script automatique identique partout
    </script>
</body>
</html>
```

## 🚀 Comment Ajouter une Image ?

### Méthode Rapide (3 étapes)

1. **Créez l'élément HTML** :
   ```html
   <li>Mon Nouvel Équipement</li>
   ```

2. **Ajoutez l'image** dans `Guide-depart/images/` :
   - Nom : `mon_nouvel_equipement.png`
   - Tout en minuscules, underscores, pas d'accents

3. **C'est tout !** L'image s'affiche automatiquement

### Exemple Concret

Pour ajouter "Radio Bluetooth" dans le salon :

1. Ajoutez dans `salon.html` :
   ```html
   <li>Radio Bluetooth</li>
   ```

2. Placez l'image : `Guide-depart/images/radio_bluetooth.png`

3. Sauvegardez et testez !

## 📝 Liste des Pages Configurées

✅ **Toutes ces pages gèrent automatiquement les images** :

- `salon.html` → `salon_*.png` ou `*.png`
- `chambre.html` → `chambre_*.png` ou `*.png`
- `cuisine.html` → `cuisine_*.png` ou `*.png`
- `salle_manger.html` → `salle_manger_*.png` ou `*.png`
- `terrasse.html` → `terrasse_*.png` ou `*.png`
- `salle_deau.html` → `salle_deau_*.png` ou `*.png`
- `wc.html` → `wc_*.png` ou `*.png`
- `placard_bleu.html` → `placard_bleu_*.png` ou `*.png`

## ⚡ Optimisation : Page-Spécifique vs Générique

### Image Page-Spécifique (Priorité 1)
- Nom : `salon_climatisation.png`
- Utilisation : Si vous voulez une image différente de la climatisation selon la pièce

### Image Générique (Priorité 2)
- Nom : `climatisation.png`
- Utilisation : Une seule image pour toutes les pièces (plus pratique)

**Recommandation** : Utilisez des **images génériques** (`climatisation.png`) sauf si vous avez besoin d'images différentes par pièce.

## 🎨 Format des Images

| Type | Largeur recommandée | Hauteur | Format |
|------|---------------------|---------|--------|
| Petite (télécommande) | 300px | 200px | PNG |
| Moyenne (équipement) | 400px | 300px | PNG/JPG |
| Grande (plan) | 800px | 600px | PNG/JPG |

**Poids max** : 200 KB par image

## 🛠️ Script de Standardisation

Pour renommer **automatiquement toutes vos images** selon les règles :

```powershell
# Exécutez dans Guide-depart/images/
function Slugify-Text {
    param([string]$Text)
    $text = $Text.ToLower().Normalize([System.Text.NormalizationForm]::FormD)
    $text = $text -replace '\p{M}', ''  # Supprime accents
    $text = $text -replace '[^a-z0-9]+', '_'
    $text = $text -replace '^_+|_+$', ''
    $text = $text -replace '__+', '_'
    return $text
}

Get-ChildItem | Where-Object { $_.Extension -in @('.png','.jpg','.jpeg','.webp') } | ForEach-Object {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    $newName = Slugify-Text $baseName
    if ($baseName -ne $newName) {
        Rename-Item $_.FullName "$newName$($_.Extension)" -Force
        Write-Host "✅ $($_.Name) → $newName$($_.Extension)"
    }
}
```

## ✅ Vérification Rapide

Pour vérifier que vos images sont nommées correctement :

```powershell
# Liste les images avec problèmes potentiels
Get-ChildItem Guide-depart/images/*.* | Where-Object {
    $_.Name -match '[A-Z]' -or $_.Name -match ' ' -or $_.Name -match '[éèêëàâäôöùûü]'
} | Select-Object Name
```

**Si rien ne s'affiche** : Toutes vos images sont bien formatées ! ✅

## 🚨 Troubleshooting

### Image ne s'affiche pas ?

1. ✅ Vérifier le nom : minuscules, underscores, pas d'accents
2. ✅ Vérifier l'extension : `.png`, `.jpg`, `.webp`
3. ✅ Vérifier le dossier : `Guide-depart/images/`
4. ✅ Vider le cache : Ctrl+F5 dans le navigateur
5. ✅ Vérifier la console : F12 → onglet Console

### Débuggage Rapide

Ajoutez dans votre page HTML pour voir ce qui est recherché :

```javascript
document.querySelectorAll('ul li').forEach(li => {
    const slug = slugify(li.textContent.trim());
    console.log('Recherche : ' + slug);
});
```

## 📚 Pages de Référence

- **Détails techniques** : `NOM_IMAGE_REGLE.md`
- **Instructions images** : `COMMENT_AJOUTER_IMAGES.md`
- **Guide complet** : `images_guide.md`

---

## 🎉 Résumé Ultra-Rapide

**Pour ajouter une image dans n'importe quelle page :**

1. Ouvrez le fichier HTML (ex: `salon.html`)
2. Ajoutez `<li>Votre équipement</li>`
3. Placez l'image dans `images/` nommée `votre_equipement.png`
4. C'est tout ! ✨

**Les images s'affichent automatiquement !** 🚀

