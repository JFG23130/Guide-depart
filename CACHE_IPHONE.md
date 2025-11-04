# Instructions pour vider le cache sur iPhone

Si les images ou le site ne s'actualisent pas sur iPhone malgré le déploiement, voici comment vider le cache :

## Méthode 1 : Vider le cache Safari (Recommandé)

1. Allez dans **Réglages** > **Safari**
2. Descendez jusqu'à **Effacer l'historique et les données de sites web**
3. Appuyez sur **Effacer l'historique et les données**
4. Confirmez l'effacement

## Méthode 2 : Vider le cache pour un site spécifique

1. Ouvrez Safari
2. Maintenez appuyé sur le bouton **Recharger** (flèche circulaire) dans la barre d'adresse
3. Sélectionnez **Recharger sans contenu en cache**

## Méthode 3 : Mode navigation privée (Temporaire)

1. Ouvrez Safari
2. Appuyez sur l'icône d'onglets (deux carrés)
3. Appuyez sur **Privé** en bas à gauche
4. Naviguez vers le site - il chargera sans cache

## Méthode 4 : Redémarrer Safari complètement

1. Appuyez deux fois sur le bouton d'accueil (iPhone ancien) ou faites glisser depuis le bas (iPhone récent)
2. Faites glisser Safari vers le haut pour le fermer
3. Rouvrez Safari

## Améliorations techniques

Le site inclut maintenant :

✅ **Meta tags anti-cache** dans tous les fichiers HTML
✅ **Cache busting amélioré** avec timestamp dynamique
✅ **Headers HTTP anti-cache** (si supporté par GitHub Pages)

Ces améliorations forcent le rechargement à chaque visite, mais le cache Safari peut parfois persister. Dans ce cas, utilisez les méthodes ci-dessus.

## Vérification

Après avoir vidé le cache :
1. Visitez : https://jfg23130.github.io/Guide-depart/
2. Les images devraient se charger avec un timestamp dans l'URL (visible dans l'inspecteur)
3. Si vous voyez `?v=1234567890` dans l'URL des images, le cache busting fonctionne
