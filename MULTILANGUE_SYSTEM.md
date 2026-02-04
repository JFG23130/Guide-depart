# 🌐 Système Multilingue - Documentation

## 📋 Structure du Nouveau Système

Le système multilingue a été réorganisé pour une meilleure maintenabilité et validation :

### Fichiers de Langues Séparés

- `lang-fr.js` - Français 🇫🇷
- `lang-en.js` - English 🇬🇧
- `lang-de.js` - Deutsch 🇩🇪
- `lang-es.js` - Español 🇪🇸
- `lang-manager.js` - Gestionnaire et Validation

## 🚀 Utilisation

### 1. Import dans les fichiers HTML

```html
<!-- Importer les fichiers de langue -->
<script src="assets/lang-fr.js"></script>
<script src="assets/lang-en.js"></script>
<script src="assets/lang-de.js"></script>
<script src="assets/lang-es.js"></script>

<!-- Importer le gestionnaire (DERNIER) -->
<script src="assets/lang-manager.js"></script>
```

### 2. Utiliser les traductions dans le HTML

```html
<!-- Avec data-lang-key -->
<h1 data-lang-key="index.title">🏡 Katikias 33</h1>
<p data-lang-key="index.subtitle">Votre guide digital</p>

<!-- Pour les images -->
<img
  src="image.jpg"
  data-lang-alt="apartment_guide.p.image_du_plan_non_trouvée"
/>
```

### 3. Changer de langue

```javascript
// Changer la langue programmatiquement
LanguageManager.setLanguage("en"); // English
LanguageManager.setLanguage("de"); // Deutsch
LanguageManager.setLanguage("es"); // Español
LanguageManager.setLanguage("fr"); // Français (défaut)
```

### 4. Obtenir une traduction

```javascript
// Récupérer une clé spécifique
const title = LanguageManager.get("index.title");
console.log(title); // "🏡 Katikias 33"
```

## ✅ Validation des Traductions

### Vérifier la Complétude

Ouvrez la console du navigateur et exécutez :

```javascript
LanguageManager.validateTranslations();
```

Résultat exemple :

```
🔍 VALIDATION DES TRADUCTIONS
==================================================

📊 RÉSUMÉ PAR LANGUE:

✅ FR: 678/678 (100%)
✅ EN: 678/678 (100%)
✅ DE: 678/678 (100%)
✅ ES: 678/678 (100%)

✅ TOUTES LES TRADUCTIONS SONT COMPLÈTES!

==================================================
```

### Obtenir les Statistiques

```javascript
LanguageManager.getStats();
// Retour: { languages: { fr: 678, en: 678, de: 678, es: 678 }, total: 678, complete: true }
```

## 🔄 Migration depuis l'Ancien Système

### Avant (ancien fichier lang.js)

```javascript
const translations = {
  fr: {
    /* ... */
  },
  en: {
    /* ... */
  },
  de: {
    /* ... */
  },
  es: {
    /* ... */
  },
};
```

### Après (nouveaux fichiers)

```javascript
// lang-fr.js
const translationsFR = {
  /* ... */
};

// lang-en.js
const translationsEN = {
  /* ... */
};

// Etc.
```

## 📝 Ajouter une Nouvelle Traduction

### 1. Ajouter la clé dans tous les fichiers

**lang-fr.js:**

```javascript
"new.key": "Texte français",
```

**lang-en.js:**

```javascript
"new.key": "English text",
```

**lang-de.js:**

```javascript
"new.key": "Deutscher Text",
```

**lang-es.js:**

```javascript
"new.key": "Texto en español",
```

### 2. Utiliser dans le HTML

```html
<p data-lang-key="new.key">Texte français</p>
```

### 3. Valider

```javascript
LanguageManager.validateTranslations();
```

## 🛠️ Fonctions Disponibles

### Gestion des Langues

| Fonction                  | Description                     |
| ------------------------- | ------------------------------- |
| `setLanguage(lang)`       | Changer la langue active        |
| `getAvailableLanguages()` | Obtenir la liste des langues    |
| `getCurrentLanguage()`    | Obtenir la langue actuelle      |
| `saveLanguage(lang)`      | Sauvegarder la préférence       |
| `getSavedLanguage()`      | Récupérer la langue sauvegardée |

### Traductions

| Fonction                 | Description              |
| ------------------------ | ------------------------ |
| `get(key)`               | Obtenir une traduction   |
| `translatePage()`        | Traduire toute la page   |
| `validateTranslations()` | Valider la complétude    |
| `getStats()`             | Obtenir les statistiques |
| `exportToJSON()`         | Exporter en JSON         |
| `importFromJSON(json)`   | Importer depuis JSON     |

## 🔍 Détecter les Traductions Manquantes

### Dans la Console

```javascript
// Obtenir toutes les clés manquantes par langue
const report = LanguageManager.validateTranslations();
console.table(report.missingByLanguage);
```

### Rechercher une Clé Spécifique

```javascript
// Vérifier si une clé existe dans tous les fichiers
const key = "index.title";
LanguageManager.getAvailableLanguages().forEach((lang) => {
  const text = LanguageManager.allLanguages[lang][key];
  console.log(`${lang}: ${text ? "✓" : "✗"}`);
});
```

## 💾 Sauvegarder les Préférences

La préférence de langue est automatiquement sauvegardée dans `localStorage` :

```javascript
// Les utilisateurs retrouveront leur langue lors du retour
// La détection se fait aussi automatiquement selon le navigateur
```

## ⚠️ Fallback Automatique

Si une traduction est manquante :

1. **Le système cherche d'abord** dans la langue sélectionnée
2. **Puis en français** (langue par défaut)
3. **Affiche une erreur** si non trouvée

```
⚠️ Clé manquante en en: new.key -> Fallback FR
```

## 🎯 Checklist pour les Mises à Jour

- [ ] Ajouter la clé dans **lang-fr.js**
- [ ] Ajouter la traduction dans **lang-en.js**
- [ ] Ajouter la traduction dans **lang-de.js**
- [ ] Ajouter la traduction dans **lang-es.js**
- [ ] Utiliser `data-lang-key` dans le HTML
- [ ] Exécuter `LanguageManager.validateTranslations()`
- [ ] Vérifier que toutes les langues sont à 100%

## 📊 Exemple Complet

### HTML

```html
<div data-lang-key="index.title"></div>
<select id="langSelector">
  <option value="fr">Français</option>
  <option value="en">English</option>
  <option value="de">Deutsch</option>
  <option value="es">Español</option>
</select>
```

### JavaScript

```javascript
document.getElementById("langSelector").addEventListener("change", (e) => {
  LanguageManager.setLanguage(e.target.value);
});

// Initialiser
LanguageManager.init();
```

## 🐛 Dépannage

### Traduction non affichée

```javascript
// Vérifier si la clé existe
console.log(LanguageManager.get("votre.clé"));

// Valider les traductions
LanguageManager.validateTranslations();
```

### Les fichiers ne sont pas chargés

```javascript
// Vérifier l'ordre des imports (lang-manager.js DOIT être dernier)
// Vérifier que tous les fichiers sont présents
console.log(LanguageManager.allLanguages);
```

## 📈 Statistiques Actuelles

**Total de clés:** 678  
**Français:** 678/678 (100%) ✅  
**English:** 678/678 (100%) ✅  
**Deutsch:** 678/678 (100%) ✅  
**Español:** 678/678 (100%) ✅

---

**Dernière mise à jour:** 4 février 2026  
**Version:** 2.0 (Système séparé avec validation)
