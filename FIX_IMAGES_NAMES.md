# Correction Automatique des Noms d'Images

## Problème

Les fichiers images avec des majuscules, accents, espaces ou caractères spéciaux ne correspondaient pas aux slugs générés par le script JavaScript, causant des images manquantes sur la version en ligne.

## Solution

Le script `fix_image_names.py` renomme automatiquement tous les fichiers images pour correspondre aux slugs JavaScript :

- **Minuscules uniquement** : `TV_Salon.jpg` → `tv_salon.jpg`
- **Sans accents** : `Cafetière.png` → `cafetiere.png`
- **Sans espaces** : `carte Bandol.jpg` → `carte_bandol.jpg`
- **Extensions en minuscules** : `plan_acces.JPG` → `plan_acces.jpg`

## Utilisation

```bash
cd Guide-depart
python fix_image_names.py
```

Le script :
- ✅ Analyse tous les fichiers dans `images/`
- ✅ Génère le slug correspondant pour chaque fichier
- ✅ Renomme avec `git mv` pour que Git suive les changements
- ✅ Évite les conflits (skip si le fichier cible existe déjà)
- ✅ Affiche un résumé des renommages

## Exemple de Sortie

```
Analyse et correction des noms de fichiers images...

RENOMME (git): Box_canal_2.png -> box_canal_2.png
RENOMME (git): Cafetiere.png -> cafetiere.png
RENOMME (git): Climatisation.jpg -> climatisation.jpg
...

16 fichier(s) renomme(s)
62 fichier(s) deja correct(s)
```

## Quand Utiliser

Exécutez ce script :

- ✅ Après avoir ajouté de nouvelles images avec des majuscules/accents
- ✅ Si des images ne s'affichent pas sur la version en ligne
- ✅ Avant chaque déploiement pour garantir la cohérence

## Règles de Nommage

Le script applique les mêmes règles que le JavaScript `slugify` :

1. **Minuscules** : `A-Z` → `a-z`
2. **Sans accents** : `é` → `e`, `à` → `a`
3. **Sans espaces** : ` ` → `_`
4. **Sans caractères spéciaux** : `+` → supprimé, `-` → `_`
5. **Extensions en minuscules** : `.JPG` → `.jpg`

## Fichiers Ignorés

Le script ignore :
- Les fichiers déjà correctement nommés
- Les fichiers non-images (`.md`, `.txt`, etc.)
- Les fichiers où le nom cible existe déjà

## Notes Techniques

- Le script utilise `git mv` pour préserver l'historique Git
- Compatible Windows (gère les systèmes de fichiers insensibles à la casse)
- Gère les encodages Unicode (accents, caractères spéciaux)

## Résultat

Après exécution, tous les fichiers images correspondent aux slugs générés par le script JavaScript, garantissant que toutes les images s'affichent correctement sur la version en ligne.
