# ⚡ Guide Rapide - Modifier le Guide Katikias 33

## 🎯 En 3 étapes

### 1️⃣ Modifier en local
```bash
Ouvrir : C:\Users\gaecd\Dev\Airbnb\Guide-depart\
Éditer : tips_and_tricks.html (ou autre)
```

### 2️⃣ Tester
```bash
Double-cliquer sur : index.html
Vérifier dans le navigateur
```

### 3️⃣ Déployer
```bash
Double-cliquer sur : deploy_auto.bat
Attendre 1-2 minutes
```

**C'EST TOUT !** ✨

## 📁 Fichiers à modifier

| Fichier | Contenu |
|---------|---------|
| `index.html` | Page d'accueil avec menu |
| `tips_and_tricks.html` | **Guide Pratique** - Instructions détaillées |
| `apartment_guide.html` | Équipements & Présentation |
| `residence.html` | Infos résidence |
| `departure_procedure.html` | Procédure départ |
| `images\*.png` | Vos images |

## 🔍 Chercher dans les fichiers

### Rechercher un texte
Dans VS Code : `Ctrl + F`

### Exemples de modifications

**Changer le code Wi-Fi :**
```bash
Chercher : CMXPLqYdfcu7qCyL3n
Remplacer : VotreNouveauCode
```

**Changer un numéro :**
```bash
Chercher : +33 6 XX XX XX XX
Remplacer : +33 6 12 34 56 78
```

## 📸 Ajouter des images

1. Copier l'image dans `Guide-depart\images\`
2. Nommer : `telecommande_somfy.png`
3. C'est tout ! Le HTML la trouve automatiquement

## ✅ Vérification

**Avant déploiement :**
- [ ] Test en local OK
- [ ] Images s'affichent
- [ ] Textes corrects
- [ ] Liens fonctionnent

**Après déploiement :**
- [ ] Aller sur https://jfg23130.github.io/Guide-depart/
- [ ] Ctrl + F5 (vider cache)
- [ ] Vérifier les modifications

## 🆘 Problème ?

**L'image ne s'affiche pas ?**
→ Regardez le nom exact dans `onerror="..."`

**Les changements n'apparaissent pas ?**
→ Attendez 2 minutes + Ctrl+F5

**Erreur de déploiement ?**
→ Ouvrir PowerShell dans Guide-depart
→ `git pull origin main`
→ `git push origin main`

## 📚 Documentation complète

- `WORKFLOW_COMPLET.md` - Guide détaillé
- `COMMENT_AJOUTER_IMAGES.md` - Ajouter images
- `images_guide.md` - Standards images

---

**Astuce :** Gardez `deploy_auto.bat` sur votre bureau pour accès rapide ! 🚀




