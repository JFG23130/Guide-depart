# 🎨 Visual Studio Code - Prévisualisation Markdown

## 🚀 Afficher la prévisualisation Markdown

### Méthode 1 : Raccourci clavier
1. Ouvrez un fichier `.md` (comme `COMMENT_AJOUTER_IMAGES.md`)
2. Appuyez sur **`Ctrl + Shift + V`**
3. La prévisualisation s'affiche à côté !

### Méthode 2 : Bouton dans la barre
1. Ouvrez un fichier `.md`
2. Cliquez sur l'icône **📖** en haut à droite (prévisualisation)
3. La vue se transforme en rendu HTML

### Méthode 3 : Côte à côte
1. Appuyez sur **`Ctrl + K`** puis **`V`**
2. Le code et la prévisualisation côte à côte !

## ⚙️ Améliorer l'affichage

### Activer le rendu en temps réel
Dans VS Code, allez dans les paramètres :
- **`Ctrl + ,`** (ouvre Settings)
- Cherchez "markdown"
- Activez **"Markdown: Update Preview on Key Up"**

### Installer des extensions

#### 1. **Markdown All in One** (Recommandé)
- Extensions → Cherchez "Markdown All in One"
- Fonctions : aperçu amélioré, raccourcis, table des matières

#### 2. **Markdown Preview Enhanced**
- Prévisualisation avancée avec export PDF/HTML
- Rendus mathématiques, diagrammes, etc.

#### 3. **Markdown Preview Mermaid Support**
- Pour les diagrammes Mermaid

## 📝 Activer la coloration syntaxique

Le markdown est déjà coloré, mais vous pouvez améliorer avec :

1. Ouvrez Settings (`Ctrl + ,`)
2. Cherchez `"editor.tokenColorCustomizations"`
3. Ajoutez :
```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "markup.heading",
        "settings": {
          "foreground": "#569cd6",
          "fontStyle": "bold"
        }
      }
    ]
  }
}
```

## 🎨 Thémes recommandés pour Markdown

- **One Dark Pro**
- **Material Theme**
- **Dracula Official**
- **GitHub Theme** (parfait pour .md)

## ✨ Trucs et astuces

### Générer une table des matières
1. Installez "Markdown All in One"
2. `Ctrl + Shift + P`
3. Tapez "Markdown: Create Table of Contents"

### Aperçu dans le navigateur
1. `Ctrl + Shift + P`
2. "Markdown: Open Preview to the Side"
3. Clic droit sur la prévisualisation
4. "Open in Browser"

### Export en HTML
1. Installez "Markdown Preview Enhanced"
2. Clic droit sur votre .md
3. "Markdown Preview Enhanced: Export (html)"

## 🎯 Résumé rapide

| Action | Raccourci |
|--------|-----------|
| Prévisualisation | `Ctrl + Shift + V` |
| Côte à côte | `Ctrl + K` puis `V` |
| Paramètres | `Ctrl + ,` |
| Extensions | `Ctrl + Shift + X` |

**Astuce :** Gardez toujours la prévisualisation ouverte en secondaire pour voir en temps réel !








