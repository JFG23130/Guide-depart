# 📂 STRUCTURE FICHIERS - SYSTÈME CODES SÉCURISÉS

## 📋 Vue d'ensemble

```
Guide-depart/
├── 🏠 Pages publiques
│   ├── hub.html .......................... ⭐ NOUVELLE - Page d'accueil
│   ├── arrival_guide.html ............... ✏️ MODIFIÉE - Codes retirés
│   ├── index.html ........................ Autres pages (inchangées)
│   ├── chambre.html
│   └── ... (autres pages)
│
├── 🔐 Système codes sécurisés
│   ├── codes-acces.html ................. ⭐ NOUVELLE - Codes protégés
│   └── assets/
│       ├── codes-config.js .............. ⭐ NOUVELLE - Config manuelle
│       └── codes-config-generated.js ... ⭐ NOUVELLE - Config depuis CSV
│
├── 🌐 Traductions (multilingues)
│   ├── assets/lang-fr.js ................ ✏️ MODIFIÉE - +40 clés
│   ├── assets/lang-en.js ................ ✏️ MODIFIÉE - +40 clés
│   ├── assets/lang-de.js ................ ✏️ MODIFIÉE - +40 clés
│   ├── assets/lang-es.js ................ ✏️ MODIFIÉE - +40 clés
│   ├── assets/lang-manager.js ........... (inchangé)
│   └── assets/init-translations.js ...... (inchangé)
│
├── 📊 Gestion réservations
│   └── reservations_codes.csv ........... ⭐ NOUVELLE - Codes par réservation
│
├── 🐍 Scripts Python
│   ├── generate_qrcode_hub.py ........... ⭐ NOUVELLE - Génère QR codes
│   └── csv_to_codes_config.py ........... ⭐ NOUVELLE - CSV → JavaScript
│
├── 🔲 QR Codes
│   └── qrcodes/
│       ├── qrcode_hub_noir.png .......... ⭐ NOUVELLE - Noir & blanc
│       ├── qrcode_hub_couleur.png ....... ⭐ NOUVELLE - Bleu
│       └── qrcode_hub_gradient.png ...... ⭐ NOUVELLE - Dégradé
│
└── 📚 Documentation
    ├── SECURITE_CODES_ACCES.md .......... ⭐ NOUVELLE - Doc complète
    ├── GUIDE_INTEGRATION_RAPIDE.md ...... ⭐ NOUVELLE - Quick start
    ├── DEPLOIEMENT_COMPLET.md ........... ⭐ NOUVELLE - Full deploy
    ├── CHANGELOG.md ...................... ⭐ NOUVELLE - Changements
    └── STRUCTURE_FICHIERS.md ............ ⭐ NOUVELLE - Ce fichier
```

---

## 📄 DÉTAIL FICHIERS

### 🏠 PAGES HTML

#### `hub.html` ⭐ NOUVEAU

**Rôle:** Landing page pour QR code  
**Taille:** ~20 KB  
**Contenu:**

- Header bienvenue
- 2 cartes: Guide + Codes
- Sélecteur multilingue (FR/EN/DE/ES)
- Footer avec tip
- Design gradients

**Accès:** Public  
**Charge:** `lang-*.js`, `lang-manager.js`  
**Cache-busting:** `?v=4`

**Flux:**

```
QR code → hub.html
          ├─→ Guide d'arrivée
          └─→ Codes d'accès sécurisés
```

#### `codes-acces.html` ⭐ NOUVEAU

**Rôle:** Authentification codes  
**Taille:** ~22 KB  
**Contenu:**

- Formulaire saisie code
- Affichage codes (après auth)
- Gestion localStorage/sessionStorage
- Vérification expiration
- Support multilingue

**Accès:** Protégé (code requis)  
**Charge:** `lang-*.js`, `lang-manager.js`, `codes-config-generated.js`  
**Cache-busting:** `?v=4`, `?v=1`

**Authentification:**

```javascript
{
  KATI1234: {
    expires: "2026-01-15",
    door: "1234",
    pool: "5678",
    gate: "9999"
  }
}
```

#### `arrival_guide.html` ✏️ MODIFIÉ

**Changement:** Codes sensibles retirés, lien ajouté  
**Impact:** Sécurité accrue  
**Avant:** 3 cartes avec codes directs  
**Après:** 1 carte avec lien sécurisé vers codes-acces.html

---

### 🔐 CONFIGURATION CODES

#### `assets/codes-config.js` ⭐ NOUVEAU

**Rôle:** Config manuelle des codes  
**Format:** JavaScript object  
**Utilité:** Alternative à CSV (pour édits rapides)

**Exemple:**

```javascript
const CODES_CONFIG = {
  KATI1234: {
    expires: "2026-01-15",
    door: "1234",
    pool: "5678",
    gate: "9999",
    notes: "Réservation Janvier",
  },
};
```

**À faire:**

- Ajouter codes réservations
- Adapter dates d'expiration
- Charger dans codes-acces.html

#### `assets/codes-config-generated.js` ⭐ NOUVEAU (auto-généré)

**Rôle:** Config générée depuis CSV  
**Format:** JavaScript object (même que codes-config.js)  
**Source:** reservations_codes.csv  
**Génération:** `python csv_to_codes_config.py`

**Avantage:** Facile de gérer via Excel/Sheets

---

### 🌐 TRADUCTIONS

#### `assets/lang-fr.js` ✏️ MODIFIÉ (+40 clés)

**Changement:** Clés ajoutées pour hub.html et codes-acces.html

Clés ajoutées:

- `hub.*` (12 clés)
- `codes.*` (28 clés)

Exemple:

```javascript
"hub.title": "🏠 Katikias 33 - Bienvenue",
"codes.error": "❌ Code incorrect...",
```

#### `assets/lang-en.js` ✏️ MODIFIÉ (+40 clés)

**Changement:** Traduction anglaise des nouvelles clés

#### `assets/lang-de.js` ✏️ MODIFIÉ (+40 clés)

**Changement:** Traduction allemande des nouvelles clés

#### `assets/lang-es.js` ✏️ MODIFIÉ (+40 clés)

**Changement:** Traduction espagnole des nouvelles clés

#### `assets/lang-manager.js` (inchangé)

**Rôle:** Gestionnaire translations  
**Utilité:** Charger/switcher langues  
**Références:** hub.html, codes-acces.html

---

### 📊 GESTION RÉSERVATIONS

#### `reservations_codes.csv` ⭐ NOUVEAU

**Rôle:** Gérer codes d'accès par réservation  
**Format:** CSV (Excel-compatible)

**Colonnes:**

```
Code | Date Arrivée | Date Départ | Nom Réservation | Porte | Piscine | Portail | Notes
```

**Exemple:**

```csv
KATI0101,2026-01-10,2026-01-15,Réservation Janvier,1234,5678,9999,Première semaine
KATI0102,2026-01-20,2026-01-31,Réservation Janvier,1234,5678,9999,Deuxième semaine
```

**À faire:**

1. Ouvrir dans Excel/Sheets
2. Ajouter lignes pour chaque réservation
3. Adapter dates et codes
4. Sauvegarder en CSV

---

### 🐍 SCRIPTS PYTHON

#### `generate_qrcode_hub.py` ⭐ NOUVEAU

**Rôle:** Générer images QR code  
**Dépendance:** `qrcode[pil]`  
**Installation:** `pip install qrcode[pil]`

**Usage:**

```bash
python generate_qrcode_hub.py
```

**Sortie:**

- `qrcodes/qrcode_hub_noir.png`
- `qrcodes/qrcode_hub_couleur.png`
- `qrcodes/qrcode_hub_gradient.png`

**À adapter:**
Ligne 15: URL de destination

```python
url = 'https://votre-domaine.com/hub.html'
```

#### `csv_to_codes_config.py` ⭐ NOUVEAU

**Rôle:** Convertir CSV en JavaScript  
**Source:** `reservations_codes.csv`  
**Sortie:** `assets/codes-config-generated.js`

**Usage:**

```bash
python csv_to_codes_config.py
```

**Features:**

- Parse CSV
- Génère JavaScript
- Affiche codes actifs/expirés
- Validation dates

---

### 🔲 QR CODES

#### `qrcodes/qrcode_hub_noir.png` ⭐ NOUVEAU

**Rôle:** QR code noir & blanc  
**Recommandation:** À imprimer  
**Taille:** ~2-3 KB  
**Format:** 10cm × 10cm (A5)  
**Plastification:** Recommandée

#### `qrcodes/qrcode_hub_couleur.png` ⭐ NOUVEAU

**Rôle:** QR code bleu  
**Style:** Coloré  
**Utilité:** Branding

#### `qrcodes/qrcode_hub_gradient.png` ⭐ NOUVEAU

**Rôle:** QR code dégradé  
**Style:** Design moderne  
**Utilité:** Esthétique

---

### 📚 DOCUMENTATION

#### `SECURITE_CODES_ACCES.md` ⭐ NOUVEAU

**Longueur:** 350+ lignes  
**Contenu:**

- Architecture du système
- Flux utilisateur
- Fichiers expliqués
- Configuration
- Sécurité
- Cas d'usage
- Améliorations futures

**Lire:** Pour comprendre le système globalement

#### `GUIDE_INTEGRATION_RAPIDE.md` ⭐ NOUVEAU

**Longueur:** 100+ lignes  
**Contenu:**

- Checklist (5 points)
- Test sur localhost
- Configuration codes
- QR code (personnalisation)
- Dépannage

**Lire:** Pour déployer rapidement

#### `DEPLOIEMENT_COMPLET.md` ⭐ NOUVEAU

**Longueur:** 400+ lignes  
**Contenu:**

- Vue d'ensemble
- Statistiques
- Phases de déploiement (6)
- Checklist détaillée
- Guide utilisateur final
- Maintenance
- Tests
- Performance

**Lire:** Pour un déploiement professionnel

#### `CHANGELOG.md` ⭐ NOUVEAU

**Longueur:** 350+ lignes  
**Contenu:**

- Historique changements
- Fichiers créés/modifiés
- Code before/after
- Statistiques
- Features ajoutées
- Sécurité améliorée
- Notes de déploiement

**Lire:** Pour connaître les changements

#### `STRUCTURE_FICHIERS.md` ⭐ NOUVEAU

**Ce fichier**  
**Contenu:**

- Vue globale architecture
- Détail chaque fichier
- Rôles et responsabilités
- Tailles fichiers
- Dépendances

**Lire:** Pour naviguer le projet

---

## 📊 RÉSUMÉ CRÉATIONS

| Type           | Créé | Modifié | Total |
| -------------- | ---- | ------- | ----- |
| **HTML**       | 2    | 1       | 3     |
| **JavaScript** | 2    | 4       | 6     |
| **Python**     | 2    | -       | 2     |
| **CSV**        | 1    | -       | 1     |
| **PNG**        | 3    | -       | 3     |
| **Markdown**   | 4    | -       | 4     |
| **TOTAL**      | 14   | 5       | 19    |

---

## 🔄 DÉPENDANCES

```
hub.html
├─ assets/lang-fr.js
├─ assets/lang-en.js
├─ assets/lang-de.js
├─ assets/lang-es.js
└─ assets/lang-manager.js

codes-acces.html
├─ assets/lang-fr.js
├─ assets/lang-en.js
├─ assets/lang-de.js
├─ assets/lang-es.js
├─ assets/lang-manager.js
└─ assets/codes-config-generated.js

arrival_guide.html
└─ (lien vers codes-acces.html)

csv_to_codes_config.py
├─ reservations_codes.csv (entrée)
└─ assets/codes-config-generated.js (sortie)

generate_qrcode_hub.py
└─ qrcodes/*.png (sortie)
```

---

## ⚙️ CONFIGURATION NÉCESSAIRE

### Avant déploiement

1. **Éditer `reservations_codes.csv`**
   - Ajouter réservations
   - Adapter dates

2. **Exécuter `csv_to_codes_config.py`**
   - Génère `assets/codes-config-generated.js`

3. **Adapter `generate_qrcode_hub.py`**
   - Changer URL ligne 15
   - Générer QR codes

4. **Imprimer QR code**
   - Format A5 (10cm × 10cm)
   - Plastifier

5. **Tester sur localhost**
   - `python -m http.server 8000`

---

## 🚀 DÉPLOIEMENT

### Fichiers à uploader

```
✅ hub.html
✅ codes-acces.html
✅ arrival_guide.html (modifié)
✅ assets/lang-fr.js (modifié)
✅ assets/lang-en.js (modifié)
✅ assets/lang-de.js (modifié)
✅ assets/lang-es.js (modifié)
✅ assets/lang-manager.js (inchangé)
✅ assets/codes-config-generated.js (nouveau)
✅ Documentation Markdown (optionnel)
✅ QR codes (impression seulement)
```

### Fichiers locaux seulement

```
📂 reservations_codes.csv (gestion locale)
🐍 generate_qrcode_hub.py (génération)
🐍 csv_to_codes_config.py (conversion)
🐍 assets/codes-config.js (optionnel)
```

---

## 💾 STOCKAGE

### Fichier | Taille | Emplacement | Backup

|
| hub.html | 20 KB | Root | ✅
| codes-acces.html| 22 KB | Root | ✅
| lang-fr.js | +10KB | assets/ | ✅
| lang-en.js | +10KB | assets/ | ✅
| lang-de.js | +10KB | assets/ | ✅
| lang-es.js | +10KB | assets/ | ✅
| codes-config-\* | 2 KB | assets/ | ✅
| QR code PNG | 3 KB | qrcodes/ | ✅
| CSV | 1 KB | Root | ✅ (local)

---

## ✅ CHECKLIST INTÉGRATION

- [ ] Lire GUIDE_INTEGRATION_RAPIDE.md
- [ ] Éditer reservations_codes.csv
- [ ] Exécuter csv_to_codes_config.py
- [ ] Adapter URL dans generate_qrcode_hub.py
- [ ] Exécuter generate_qrcode_hub.py
- [ ] Tester sur localhost
- [ ] Uploader fichiers en production
- [ ] Imprimer QR code
- [ ] Mettre en place processus Airbnb

---

## 🎯 RÉSUMÉ

✅ **Système complet et documenté**

- Fichiers: 19 (14 créés, 5 modifiés)
- Documentation: 4 fichiers Markdown
- Code: 2500+ lignes
- Traductions: 160 clés
- QR codes: 3 formats

**Prêt à déployer en 30 minutes!** 🚀
