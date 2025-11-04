# Intégration des PDFs d'Équipements

## Fonctionnement

Pour ajouter un PDF (manuel d'utilisation) à un équipement, ajoutez l'attribut `data-pdf` sur l'élément `<li>` :

```html
<li data-pdf="pdfs/nom_du_fichier.pdf">Nom de l'équipement</li>
```

## Placement des PDFs

Tous les PDFs doivent être placés dans le dossier `pdfs/` du projet.

## Pages Concernées

Cette fonctionnalité est disponible sur **toutes les pages de pièces** :

- ✅ `salon.html`
- ✅ `cuisine.html`
- ✅ `chambre.html`
- ✅ `terrasse.html`
- ✅ `salle_deau.html`
- ✅ `wc.html`
- ✅ `placard_bleu.html`
- ✅ `salle_manger.html`

## Déploiement

Lors de l'exécution de `deploy_auto.bat`, le dossier `pdfs/` sera automatiquement inclus dans le déploiement GitHub Pages.

Les liens PDF fonctionneront sur la version en ligne du guide.

## Exemples

**Dans salon.html** :
```html
<li data-pdf="pdfs/TV_Salon.pdf">TV Salon</li>
```

**Dans cuisine.html** :
```html
<li data-pdf="pdfs/bouilloire_sana.pdf">Bouilloire</li>
```

## Dossier PDFs

Le dossier `pdfs/` contient actuellement :
- bouilloire_sana.pdf
- Climatisation.pdf
- Congelateur.pdf
- Four.pdf
- Lave Vaisselle.pdf
- Lave-linge.pdf
- Plaques de cuisson.pdf
- Radiateur Salle de Bain.pdf
- Radiateur Salon.pdf
- Senseo.pdf
- Somfy telecommande 2679167.pdf
- TV_Salon.pdf

## Note

Les PDFs avec espaces ou caractères spéciaux peuvent nécessiter un renommage pour éviter les problèmes d'URL.


