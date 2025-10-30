# 🏡 Guides Katikias 33 - Documentation

## 🌐 Site Live
**URL** : https://jfg23130.github.io/Guide-depart/

---

## 📚 Structure des Fichiers

```
Guide-depart/
├── index.html                   # Page d'accueil avec navigation
├── arrival_guide.html           # Guide d'arrivée (codes, procédures)
├── apartment_guide.html         # Guide de l'appartement (équipements, règles)
├── departure_procedure.html     # Procédure de départ (checklist)
├── tips_and_tricks.html         # Astuces & Conseils pratiques
└── README.md                    # Ce fichier
```

---

## 🚀 Déploiement

### Méthode 1 : Git Command Line
```bash
cd C:\Users\gaecd\Dev\Airbnb\Guide-depart
git add .
git commit -m "📝 Mise à jour des guides"
git push origin main
```

### Méthode 2 : Script Automatique
Lancer `deploy_guides_to_github.bat` depuis `KatikiasDeployer_v5\`

---

## ✏️ Modifier les Guides

### Codes d'Accès
Modifier dans chaque fichier HTML :
- **Porte** : `Code: 1234`
- **Wi-Fi** : `Katikias33 / Welcome2024!`
- **Piscine** : `Code: 5678`

### Numéros de Téléphone
Rechercher et remplacer dans les fichiers :
- `+33 6 XX XX XX XX` (Propriétaire)
- `+33 5 XX XX XX XX` (Gestionnaire)

### Contenus Personnalisés
1. Ouvrir le fichier HTML avec un éditeur de texte
2. Chercher la section à modifier
3. Éditer le contenu
4. Sauvegarder et déployer

---

## 🎨 Personnalisation Avancée

### Couleurs
- **Arrivée** : `#4CAF50` (vert)
- **Appartement** : `#2196F3` (bleu)
- **Départ** : `#FF9800` (orange)

### Polices
- Police principale : `'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`

### Images
Pour ajouter des images :
1. Uploader l'image sur GitHub
2. Utiliser `<img src="nom_image.jpg" alt="Description">`

---

## 📱 QR Codes

Les QR codes sont générés automatiquement par l'application **KatikiasDeployer_v5**.

### URLs des QR Codes
- **Arrivée** : `https://jfg23130.github.io/Guide-depart/arrival_guide.html`
- **Appartement** : `https://jfg23130.github.io/Guide-depart/apartment_guide.html`
- **Départ** : `https://jfg23130.github.io/Guide-depart/departure_procedure.html`
- **Astuces** : `https://jfg23130.github.io/Guide-depart/tips_and_tricks.html`
- **Accueil** : `https://jfg23130.github.io/Guide-depart/`

---

## 🔧 Dépannage

### Les modifications n'apparaissent pas ?
1. Attendre 2-3 minutes après le push
2. Vider le cache du navigateur (Ctrl+F5)
3. Vérifier le commit sur GitHub

### Erreur de push ?
```bash
git pull origin main
# Résoudre les conflits si nécessaire
git push origin main
```

---

## 📞 Contact

Pour toute question ou assistance, contacter le développeur ou consulter la documentation complète dans `DEPLOIEMENT_REUSSI.md`.

---

*Système de guides digitaux pour Katikias 33 🌟*