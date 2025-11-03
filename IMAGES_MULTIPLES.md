# Images Multiples avec Légendes

## Fonctionnement

Pour ajouter plusieurs photos avec des légendes à un même équipement, utilisez :
1. Un système de numérotation pour les fichiers
2. Un attribut `data-captions` pour les légendes

## Règle de Nommage

Pour un équipement nommé "Climatisation" dans `<li>Climatisation</li>`, vous pouvez ajouter :

1. **Image principale** : `climatisation.png` ou `salle_manger_climatisation.png`
2. **Images supplémentaires** : `climatisation_2.png`, `climatisation_3.png`, ..., `climatisation_10.png`

## Ajout de Légendes

Pour ajouter des légendes aux images, utilisez l'attribut `data-captions` sur l'élément `<li>` :

```html
<li data-captions="Légende image 1 | Légende image 2 | Légende image 3">Climatisation</li>
```

**Important** :
- La **première légende** (avant le premier `|`) correspond à l'image principale
- La **deuxième légende** correspond à `_2.png`, la troisième à `_3.png`, etc.
- Utilisez `|` pour séparer les légendes

## Exemples

### Équipement avec légendes : "Climatisation"

**Dans le HTML** :
```html
<li data-captions="Vue d'ensemble | Télécommande face avant | Télécommande face arrière">Climatisation</li>
```

**Fichiers images** :
- `climatisation.png` → Légende : "Vue d'ensemble"
- `climatisation_2.png` → Légende : "Télécommande face avant"
- `climatisation_3.png` → Légende : "Télécommande face arrière"

### Équipement simple : "Radiateur"

**Dans le HTML** :
```html
<li>Radiateur</li>
```

**Fichiers images** :
- `radiateur.png` - image principale (sans légende)
- `radiateur_2.png` - deuxième image (sans légende)

## Pages Concernées

Cette fonctionnalité est disponible sur **toutes les pages de pièces** :

- ✅ `salle_manger.html`
- ✅ `salon.html`
- ✅ `chambre.html`
- ✅ `cuisine.html`
- ✅ `terrasse.html`
- ✅ `salle_deau.html`
- ✅ `wc.html`
- ✅ `placard_bleu.html`

## Affichage

- Les images supplémentaires s'affichent **automatiquement sous l'image principale**, avec un espacement de 10px entre elles
- Les légendes s'affichent en **italique gris** sous chaque image

## Limite

Jusqu'à **10 images** par équipement (2 à 10 pour les supplémentaires).

## Format de Fichiers Supportés

- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

