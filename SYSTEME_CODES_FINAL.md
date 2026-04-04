# 🔐 Système de codes d'accès unifié Katikias 33

## ✅ Architecture finale

Ce document décrit le système unifié qui réutilise le code existant et fonctionnel de `KatikiasDeployer_v5`.

---

## 📁 Structure des fichiers

```
Guide-depart/
├── generate_all_codes.py           ✨ Script Python unifié
├── access_codes.json               📝 Codes au format JSON
├── access_codes.js                 📝 Codes au format JS (window.__ACCESS_CODES__)
├── codes_invites.md                📋 Table de suivi des codes
├── hub.html                        🚪 Page d'accueil avec QR codes
├── codes-acces.html                🔐 Page d'affichage des codes (WiFi + Portail)
├── assets/
│   ├── codes-config-generated.js   ⚙️ Config pour codes-acces.html
│   └── lang.js                     🌍 Gestion multilingue
└── KatikiasDeployer_v5/
    └── reservations_final.csv      📊 Source de vérité (export Airbnb)
```

---

## 🔄 Flux de travail

### 1️⃣ Exportation Airbnb

Exportez les réservations depuis Airbnb au format CSV avec ces colonnes:

```
Nom de l'invité, Langue, Date d'arrivée, Date de départ,
Nombre de nuits, Nombre d'invités, Nombre d'enfants, Nombre de bébés,
Code de confirmation, Pays, Devise
```

Sauvegardez le fichier dans: `KatikiasDeployer_v5/reservations_final.csv`

### 2️⃣ Génération des codes

Exécutez le script Python:

```bash
python generate_all_codes.py
```

**Ce script va:**

- ✅ Lire `reservations_final.csv`
- ✅ Filtrer les réservations expirées (départ < aujourd'hui)
- ✅ Générer des codes sécurisés au format `KATI-XXXXXXX` (SHA256 + base32)
- ✅ Créer 4 fichiers:
  - `access_codes.json` - Format compatible avec access.html
  - `access_codes.js` - Format `window.__ACCESS_CODES__`
  - `codes_invites.md` - Table de suivi lisible
  - `assets/codes-config-generated.js` - Config pour codes-acces.html

### 3️⃣ Affichage des codes

**Option A: Via hub.html**

```
https://guide.katikias33.fr/hub.html?code=KATI-XXXXXXX
```

- Entrée du code d'accès
- Affichage des codes WiFi + Portail
- QR codes générés automatiquement

**Option B: Lien direct dans l'email**

```
https://guide.katikias33.fr/hub.html?code=KATI-CN47SBA
```

Le code est pré-rempli, l'invité n'a qu'à cliquer.

---

## 🔐 Format des codes

### Code d'accès invité

```
KATI-CN47SBA
```

**Génération:**

```python
def _generate_code(reservation_code: str, arrival: date) -> str:
    key = f"{reservation_code}|{arrival.isoformat()}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    token = base64.b32encode(digest).decode("ascii").rstrip("=")
    return f"KATI-{token[:4]}{token[-3:]}"
```

**Caractéristiques:**

- ✅ **Unique**: Basé sur le code de confirmation Airbnb + date d'arrivée
- ✅ **Sécurisé**: SHA256 (non-prévisible)
- ✅ **Déterministe**: Même réservation → même code
- ✅ **Court**: 7 caractères alphanumériques

### Codes affichés après authentification

**WiFi:**

```
SSID: Katikias33
Mot de passe: [dans codes-config-generated.js]
```

**Portail:**

```
Code: 9999
```

---

## 📊 Structure CSV (reservations_final.csv)

### Colonnes requises

```csv
Nom de l'invité,Langue,Date d'arrivée,Date de départ,Code de confirmation
```

### Exemple

```csv
Nom de l'invité,Langue,Date d'arrivée,Date de départ,Nombre de nuits,Nombre d'invités,Nombre d'enfants,Nombre de bébés,Code de confirmation,Pays,Devise
Paul Daniel,Anglais,01/05/2026,05/06/2026,35,2,0,0,HMSNMTRKTH,Irlande,EUR
Jennifer Ruhnau,Allemand,27/06/2026,11/07/2026,14,2,0,0,HMEFDYCBXA,Allemagne,EUR
```

### Formats de date acceptés

- `DD/MM/YYYY` (recommandé - export Airbnb)
- `DD-MM-YYYY`
- `YYYY-MM-DD`
- `DD/MM/YY`

---

## 🎯 Fichiers générés

### 1. access_codes.json

```json
[
  { "code": "KATI-CN47SBA", "guest": "Paul Daniel" },
  { "code": "KATI-MO7U2QA", "guest": "Jennifer Ruhnau" }
]
```

**Usage:** Compatible avec `_archive/access.html` (système historique)

### 2. access_codes.js

```javascript
window.__ACCESS_CODES__ = [
  { code: "KATI-CN47SBA", guest: "Paul Daniel" },
  { code: "KATI-MO7U2QA", guest: "Jennifer Ruhnau" },
];
```

**Usage:** Chargé par `hub.html` et `codes-acces.html`

### 3. codes_invites.md

```markdown
| Invité      | Arrivée    | Départ     | Code           | Lien direct                                            |
| ----------- | ---------- | ---------- | -------------- | ------------------------------------------------------ |
| Paul Daniel | 01/05/2026 | 05/06/2026 | `KATI-CN47SBA` | https://guide.katikias33.fr/hub.html?code=KATI-CN47SBA |
```

**Usage:** Référence interne, envoi d'emails

### 4. assets/codes-config-generated.js

```javascript
const CODES_DATABASE = {
  "KATI-CN47SBA": {
    expires: "2026-06-05",
    guest: "Paul Daniel",
    wifi: "Katikias33",
    portail: "9999",
    notes: "Code de réservation: HMSNMTRKTH",
  },
};
```

**Usage:** Chargé par `codes-acces.html` pour affichage WiFi + Portail

---

## 🚀 Déploiement

### Workflow complet

```bash
# 1. Mettre à jour les réservations
# Copier l'export Airbnb → KatikiasDeployer_v5/reservations_final.csv

# 2. Générer les codes
python generate_all_codes.py

# 3. Vérifier les fichiers générés
cat access_codes.js
cat codes_invites.md

# 4. Déployer sur le serveur
# Les fichiers sont prêts à être poussés sur GitHub Pages
git add access_codes.* codes_invites.md assets/codes-config-generated.js
git commit -m "🔄 Mise à jour codes invités"
git push
```

### Automatisation possible

Créer un script `update_codes.bat` (Windows):

```batch
@echo off
echo 🔄 Mise à jour des codes invités...
python generate_all_codes.py
if %ERRORLEVEL% EQU 0 (
    echo ✅ Codes générés avec succès
    git add access_codes.* codes_invites.md assets/codes-config-generated.js
    git commit -m "🔄 Mise à jour codes invités"
    git push
    echo ✅ Déployé sur GitHub Pages
) else (
    echo ❌ Erreur lors de la génération
    exit /b 1
)
```

---

## 🔒 Sécurité

### Ce qui est sécurisé ✅

- Codes générés par SHA256 (non-prévisibles)
- Basés sur code de confirmation Airbnb (unique)
- Expiration automatique (départ < aujourd'hui)
- Pas de codes WiFi/Portail dans le CSV (séparés dans config)

### Ce qui n'est PAS sécurisé ⚠️

- Codes stockés en clair dans `access_codes.js` (fichier public)
- Pas d'authentification serveur (tout est côté client)
- Codes WiFi/Portail statiques (pas de rotation)

### Recommandations

1. **Rotation régulière** du mot de passe WiFi
2. **Surveillance** des accès (logs du routeur)
3. **Changement du code portail** entre saisons
4. **Limitation de validité** des codes (expiration automatique déjà implémentée)

---

## 🛠️ Dépannage

### ❌ Erreur: "Fichier CSV introuvable"

```bash
# Vérifier le chemin
ls KatikiasDeployer_v5/reservations_final.csv

# Copier le CSV depuis le bon emplacement
cp /chemin/vers/export_airbnb.csv KatikiasDeployer_v5/reservations_final.csv
```

### ❌ Erreur: "Colonnes manquantes"

Le CSV doit avoir ces colonnes (exactement):

- `Nom de l'invité`
- `Date d'arrivée`
- `Date de départ`
- `Code de confirmation`

### ❌ Aucune réservation trouvée

- Vérifier les dates dans le CSV (format DD/MM/YYYY)
- Vérifier que la date de départ est dans le futur
- Vérifier que les lignes ne sont pas vides

### ❌ Code invalide dans l'interface

```bash
# Régénérer les codes
python generate_all_codes.py

# Vider le cache du navigateur (Ctrl+Shift+R)
```

---

## 📧 Email type à envoyer aux invités

```
Bonjour {{Nom}},

Bienvenue à Katikias 33! 🏡

Voici votre code d'accès personnel pour consulter le guide de bienvenue:

🔐 Code: KATI-XXXXXXX

👉 Lien direct: https://guide.katikias33.fr/hub.html?code=KATI-XXXXXXX

Vous y trouverez:
- Les codes WiFi et portail
- Le guide d'arrivée
- Les informations pratiques
- Les recommandations locales

À bientôt,
L'équipe Katikias 33
```

---

## 📝 Changelog

### Version 3.0 (05/02/2026)

- ✅ Script unifié `generate_all_codes.py`
- ✅ Réutilisation de `generate_guest_codes.py` de KatikiasDeployer_v5
- ✅ Format `KATI-XXXXXXX` (SHA256 + base32)
- ✅ Génération de 4 fichiers (JSON, JS, MD, Config)
- ✅ Filtrage automatique des réservations expirées
- ✅ Support des liens directs pré-remplis

### Version 2.0 (Février 2026)

- Simplification: seulement WiFi + Portail (pas de code porte/piscine/parking)
- Intégration avec système existant de KatikiasDeployer_v5

### Version 1.0 (Janvier 2026)

- Système initial avec 5 codes (porte, WiFi, piscine, portail, parking)
- Codes séquentiels KATI0101, KATI0201, etc.

---

## 🔗 Références

- **Script principal**: [generate_all_codes.py](generate_all_codes.py)
- **Interface hub**: [hub.html](hub.html)
- **Affichage codes**: [codes-acces.html](codes-acces.html)
- **Système original**: [../KatikiasDeployer_v5/generate_guest_codes.py](../KatikiasDeployer_v5/generate_guest_codes.py)
