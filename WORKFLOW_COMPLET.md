# 🔄 Workflow Complet - Guide Katikias 33

## 🎯 Philosophie : MODIFIER EN LOCAL, DÉPLOYER SUR GITHUB

### ✅ Méthode recommandée : **Local → GitHub Pages**

**Pourquoi ?**
- ✅ Test en local avant mise en ligne
- ✅ Historique des modifications
- ✅ Annulation possible
- ✅ Autonomie complète

## 📍 Où modifier ?

### 🏠 **En LOCAL** (recommandé)

```
C:\Users\gaecd\Dev\Airbnb\Guide-depart\
├── index.html                   ← Modifier ICI
├── tips_and_tricks.html         ← Modifier ICI
├── apartment_guide.html         ← Modifier ICI
├── residence.html               ← Modifier ICI
├── images\                      ← Ajouter vos images ICI
│   ├── telecommande_somfy.png
│   ├── plan_residence.jpg
│   └── ...
└── README.md
```

**Éditeurs recommandés :**
- **Visual Studio Code** (le meilleur pour HTML/MD)
- **Notepad++** (simple, efficace)
- **Bloc-notes** (basique)

### ⚠️ **PAS directement sur GitHub**
- Plus difficile à modifier
- Moins de contrôle
- Pas de test avant publication

## 🔧 Comment modifier ?

### 1️⃣ **Ouvrir le fichier**
```bash
# Ouvrir dans VS Code
code "C:\Users\gaecd\Dev\Airbnb\Guide-depart\tips_and_tricks.html"

# Ou double-cliquer sur le fichier
```

### 2️⃣ **Faire vos modifications**

#### Modifier du texte
Cherchez le texte et remplacez-le :
```html
<!-- AVANT -->
<p>Code Wi-Fi : Katikias33</p>

<!-- APRÈS -->
<p>Code Wi-Fi : Livebox-6A50</p>
```

#### Ajouter une image
1. Copiez votre image dans `Guide-depart\images\`
2. Ajoutez dans le HTML :
```html
<img src="images/votre_image.jpg" alt="Description">
```

#### Ajouter une section
Cherchez où ajouter et copiez une card existante :
```html
<div class="tip-card">
    <h3>🆕 Nouvelle section</h3>
    <p>Votre contenu ici</p>
</div>
```

### 3️⃣ **Tester en local**
```bash
# Ouvrir dans le navigateur
start "C:\Users\gaecd\Dev\Airbnb\Guide-depart\index.html"
```

### 4️⃣ **Sauvegarder** (Ctrl+S)

## 🚀 Comment déployer automatiquement ?

### Méthode 1 : Script automatique (RECOMMANDÉ ✨)

Créez `deploy_auto.bat` dans `Guide-depart\` :

```batch
@echo off
echo ==========================================
echo   DEPLOIEMENT GUIDE KATIKIAS 33
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/4] Commit des modifications...
git add .
git commit -m "📝 Mise à jour guide Katikias 33"

echo.
echo [2/4] Envoi sur GitHub...
git push origin main

echo.
echo [3/4] Verification...
timeout /t 3 >nul

echo.
echo [4/4] ✅ DEPLOIEMENT TERMINE !
echo.
echo 🌐 Site : https://jfg23130.github.io/Guide-depart/
echo.
echo ⏱️  Attendre 1-2 minutes pour voir les changements
echo.
pause
```

**Utilisation :**
1. Double-cliquez sur `deploy_auto.bat`
2. C'est tout ! Le site est mis à jour

### Méthode 2 : Manuel

```bash
cd C:\Users\gaecd\Dev\Airbnb\Guide-depart
git add .
git commit -m "📝 Description de vos modifications"
git push origin main
```

## 🔄 Workflow complet simplifié

```
┌─────────────────────────────────────┐
│  1. Modifier les fichiers HTML      │
│     en local avec VS Code           │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  2. Tester dans le navigateur       │
│     (ouvrir index.html)             │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  3. Exécuter deploy_auto.bat        │
│     (ou git push manuel)            │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  4. Attendre 1-2 minutes            │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  5. Vérifier sur le site            │
│     https://jfg23130.github.io/...  │
└─────────────────────────────────────┘
```

## 📸 Ajouter des images : Processus complet

### Étapes détaillées

1. **Préparer l'image**
   - Trouvez votre image sur votre PC
   - Réduire si trop grande (max 800px de large)
   - Renommer : pas d'espaces, minuscules

2. **Copier dans Guide-depart**
   ```
   Source : C:\Users\jfgir\Images\telecommande.jpg
   Dest : C:\Users\gaecd\Dev\Airbnb\Guide-depart\images\telecommande_somfy.png
   ```

3. **Mettre à jour le code** (si nécessaire)
   - Vérifiez le chemin dans le HTML
   - `src="telecommande_somfy.png"` (même dossier)
   - OU `src="images/telecommande_somfy.png"` (dans images/)

4. **Tester**
   - Ouvrez `tips_and_tricks.html` dans le navigateur
   - Vérifiez que l'image s'affiche

5. **Déployer**
   - `deploy_auto.bat` ou `git push`

## 🎨 Personnalisation avancée

### Changer les couleurs

Dans chaque fichier HTML, cherchez :
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
Changez les valeurs hex (#667eea, #764ba2) selon vos goûts.

### Ajouter des emojis

Utilisez les emojis Windows (Win + .) ou copiez-collez de emojipedia.org

### Modifier le style

Les fichiers HTML ont le CSS intégré dans la balise `<style>` en haut du fichier.

## 🔐 Sécurité

- ✅ Toutes vos modifications sont sauvegardées sur GitHub
- ✅ Vous pouvez revenir en arrière avec `git log`
- ✅ Le site est visible publiquement (c'est normal)
- ✅ Les images sont publiques aussi

## ⚡ Trucs et astuces

### Raccourci clavier VS Code
1. Modifier le fichier
2. `Ctrl + S` (sauvegarder)
3. `Ctrl + Shift + B` (créer une task pour déployer)

### Voir les changements en temps réel
- Installez "Live Server" dans VS Code
- Clic droit sur index.html → "Open with Live Server"
- La page se rafraîchit automatiquement !

### Git graphique
Installez **GitHub Desktop** pour voir visuellement vos modifications.

## ❓ Problèmes courants

### L'image ne s'affiche pas
- Vérifiez le nom exact (majuscules/minuscules)
- Vérifiez le chemin : `images/` ou pas
- Regardez la console du navigateur (F12)

### Les changements n'apparaissent pas sur le site
- Attendez 2-3 minutes
- Videz le cache : `Ctrl + F5`
- Vérifiez le commit sur GitHub

### Erreur de push
```bash
git pull origin main  # Récupérer les dernières modifs
git push origin main  # Réessayer
```

## 📋 Checklist rapide

- [ ] Modifier le fichier HTML en local
- [ ] Sauvegarder (Ctrl+S)
- [ ] Tester dans le navigateur
- [ ] Exécuter deploy_auto.bat
- [ ] Attendre 1-2 minutes
- [ ] Vérifier sur le site

## 🎯 Résumé

**Modifiez EN LOCAL, déployez sur GITHUB, c'est tout !** ✨


