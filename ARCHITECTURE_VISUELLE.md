# 📊 Architecture du système de codes d'accès Katikias 33

## 🎯 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SYSTÈME UNIFIÉ V3.0                            │
│                   Réutilise KatikiasDeployer_v5                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  Export Airbnb CSV  │  ← Réservations depuis Airbnb
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 reservations_final.csv                              │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Nom | Langue | Arrivée | Départ | Code confirmation | ... │   │
│  │ Paul Daniel | Anglais | 01/05/2026 | 05/06/2026 | HMSN... │   │
│  │ Jennifer Ruhnau | Allemand | 27/06/2026 | 11/07/2026 | HME..│   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────┬──────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│              generate_all_codes.py                                  │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ 1. Lit reservations_final.csv                              │   │
│  │ 2. Filtre les réservations expirées                        │   │
│  │ 3. Génère codes SHA256: KATI-XXXXXXX                       │   │
│  │ 4. Écrit 4 fichiers de sortie                              │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────┬──────────────────────────────────────────────────────────┘
           │
           ├───────────────┬───────────────┬──────────────┐
           │               │               │              │
           ▼               ▼               ▼              ▼
┌──────────────┐  ┌─────────────┐  ┌────────────┐  ┌─────────────────┐
│access_codes  │  │access_codes │  │codes_invites│ │codes-config-    │
│   .json      │  │    .js      │  │   .md      │  │  generated.js   │
└──────┬───────┘  └──────┬──────┘  └──────┬─────┘  └────────┬────────┘
       │                 │                │                  │
       │        ┌────────┴────────┐       │                  │
       │        │                 │       │                  │
       ▼        ▼                 ▼       ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INTERFACE WEB                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐   │
│  │   hub.html     │  │codes-acces.html│  │  codes_invites.md  │   │
│  │                │  │                │  │                    │   │
│  │ • QR codes     │  │ • Authentif.   │  │ • Suivi interne    │   │
│  │ • Entrée code  │  │ • Affiche WiFi │  │ • Liste codes      │   │
│  │ • Redirect     │  │ • Affiche      │  │ • Liens directs    │   │
│  │                │  │   Portail      │  │                    │   │
│  └────────────────┘  └────────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         INVITÉ                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ 1. Reçoit email avec code: KATI-CN47SBA                    │   │
│  │ 2. Clique sur lien: hub.html?code=KATI-CN47SBA             │   │
│  │ 3. Voit les codes WiFi + Portail                            │   │
│  │ 4. Accède au guide complet                                  │   │
│  └────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Génération des codes

### Algorithme cryptographique

```python
def _generate_code(reservation_code: str, arrival: date) -> str:
    """
    Génère un code unique à partir de:
    - Code de confirmation Airbnb (ex: HMSNMTRKTH)
    - Date d'arrivée (ex: 2026-05-01)

    Résultat: KATI-CN47SBA
    """
    # 1. Clé unique
    key = f"{reservation_code}|{arrival.isoformat()}"
    # Exemple: "HMSNMTRKTH|2026-05-01"

    # 2. Hash SHA256
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    # Résultat: 32 bytes binaires

    # 3. Encodage base32
    token = base64.b32encode(digest).decode("ascii").rstrip("=")
    # Résultat: "CN47SBAKL3MNO..." (52 caractères)

    # 4. Extraction + préfixe
    return f"KATI-{token[:4]}{token[-3:]}"
    # Résultat: "KATI-CN47SBA" (7 caractères alphanumériques)
```

### Avantages de ce format

✅ **Sécurisé**: SHA256 = non-prévisible, non-réversible  
✅ **Unique**: Basé sur code Airbnb + date d'arrivée  
✅ **Déterministe**: Même entrée → même code  
✅ **Court**: 7 caractères (facile à taper)  
✅ **Reconnaissable**: Préfixe KATI-

---

## 📁 Fichiers générés

### 1. access_codes.json

```json
[
  { "code": "KATI-CN47SBA", "guest": "Paul Daniel" },
  { "code": "KATI-MO7U2QA", "guest": "Jennifer Ruhnau" }
]
```

**Format**: JSON standard  
**Usage**: Compatible avec système historique (\_archive/access.html)  
**Taille**: ~100 bytes par code

---

### 2. access_codes.js

```javascript
window.__ACCESS_CODES__ = [
  { code: "KATI-CN47SBA", guest: "Paul Daniel" },
  { code: "KATI-MO7U2QA", guest: "Jennifer Ruhnau" },
];
```

**Format**: JavaScript global  
**Usage**: Chargé par hub.html et codes-acces.html  
**Avantage**: Pas de requête AJAX nécessaire  
**Fallback**: Si JSON échoue, ce fichier est utilisé

---

### 3. codes_invites.md

```markdown
| Invité      | Arrivée    | Départ     | Code           | Lien direct                                            |
| ----------- | ---------- | ---------- | -------------- | ------------------------------------------------------ |
| Paul Daniel | 01/05/2026 | 05/06/2026 | `KATI-CN47SBA` | https://guide.katikias33.fr/hub.html?code=KATI-CN47SBA |
```

**Format**: Markdown table  
**Usage**:

- Référence interne (suivi des réservations)
- Source pour emails aux invités
- Documentation  
  **Affichage**: Rendu joliment sur GitHub

---

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

**Format**: Objet JavaScript avec config complète  
**Usage**: Chargé par codes-acces.html pour afficher WiFi + Portail  
**Contenu**:

- Date d'expiration
- Nom de l'invité
- Code WiFi (SSID)
- Code portail
- Notes (code de réservation Airbnb)

---

## 🔄 Workflow complet

### Workflow manuel

```bash
# 1. Exporter réservations depuis Airbnb
# → Sauvegarder dans KatikiasDeployer_v5/reservations_final.csv

# 2. Générer les codes
python generate_all_codes.py

# 3. Valider le système
python validate_system_final.py

# 4. Vérifier les codes générés
cat codes_invites.md

# 5. Déployer sur GitHub Pages
git add access_codes.* codes_invites.md assets/codes-config-generated.js
git commit -m "🔄 Mise à jour codes invités"
git push
```

### Workflow automatisé

```batch
# Sous Windows
update_codes_workflow.bat

# Le script fait tout automatiquement:
# ✅ Génération
# ✅ Validation
# ✅ Affichage résumé
# ✅ Proposition de déploiement
```

---

## 🎨 Interface utilisateur

### hub.html (Page d'accueil)

```
┌─────────────────────────────────────────────────┐
│          🏡 BIENVENUE À KATIKIAS 33            │
├─────────────────────────────────────────────────┤
│                                                 │
│   [QR CODE]      [QR CODE]      [QR CODE]     │
│   Guide FR        Guide EN       Guide DE      │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│   🔐 Code d'accès:                             │
│   [ KATI-__________ ]                          │
│   [    Valider     ]                           │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Fonctionnalités**:

- Scan de QR codes (mobile)
- Saisie manuelle de code
- Support des liens directs (`?code=KATI-XXX`)
- Redirection automatique vers codes-acces.html

---

### codes-acces.html (Affichage des codes)

```
┌─────────────────────────────────────────────────┐
│       ✅ ACCÈS AUTORISÉ - Paul Daniel          │
├─────────────────────────────────────────────────┤
│                                                 │
│   📶 CODE WIFI                                 │
│   ┌─────────────────────────────────────────┐ │
│   │ Réseau: Katikias33                      │ │
│   │ Mot de passe: **************           │ │
│   │ [Copier] [QR Code]                      │ │
│   └─────────────────────────────────────────┘ │
│                                                 │
│   🚪 CODE PORTAIL                              │
│   ┌─────────────────────────────────────────┐ │
│   │ Code: 9999                              │ │
│   │ [Copier]                                │ │
│   └─────────────────────────────────────────┘ │
│                                                 │
│   [Accéder au guide complet]                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Fonctionnalités**:

- Affichage des codes WiFi + Portail
- Boutons "Copier" pour faciliter
- QR code WiFi généré dynamiquement
- Persistance via localStorage
- Lien vers le guide complet

---

## 📧 Email type

```
Objet: Bienvenue à Katikias 33 🏡 - Votre code d'accès

Bonjour Paul,

Bienvenue à Katikias 33! Nous sommes ravis de vous accueillir.

🔐 Votre code d'accès personnel:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   KATI-CN47SBA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 Accès direct au guide:
https://guide.katikias33.fr/hub.html?code=KATI-CN47SBA

Ce lien vous donnera accès à:
✅ Codes WiFi et portail
✅ Guide d'arrivée étape par étape
✅ Informations sur l'appartement
✅ Recommandations locales
✅ Procédures d'urgence

📅 Votre séjour:
Du 01/05/2026 au 05/06/2026 (35 nuits)

💡 Conseil: Enregistrez ce lien dans vos favoris!

À très bientôt,
L'équipe Katikias 33

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 contact@katikias33.fr
🌐 https://guide.katikias33.fr
```

---

## 🛠️ Validation et débogage

### Commandes de diagnostic

```bash
# Vérifier l'existence des fichiers
ls -la access_codes.* codes_invites.md

# Afficher les codes générés
cat codes_invites.md

# Compter les codes
python -c "import json; print(len(json.load(open('access_codes.json'))))"

# Tester un code spécifique
python -c "
import json
code = 'KATI-CN47SBA'
codes = json.load(open('access_codes.json'))
result = [c for c in codes if c['code'] == code]
print(result)
"

# Valider tout le système
python validate_system_final.py
```

### Erreurs courantes

| Erreur                 | Cause                           | Solution                                                   |
| ---------------------- | ------------------------------- | ---------------------------------------------------------- |
| `CSV introuvable`      | reservations_final.csv manquant | Copier export Airbnb dans KatikiasDeployer_v5/             |
| `Colonnes manquantes`  | Format CSV incorrect            | Vérifier colonnes: Nom, Arrivée, Départ, Code confirmation |
| `Aucune réservation`   | Toutes expirées                 | Vérifier dates dans CSV (format DD/MM/YYYY)                |
| `Incohérence détectée` | Fichiers désynchronisés         | Relancer: `python generate_all_codes.py`                   |
| `Code invalide`        | Ancien code en cache            | Vider cache navigateur (Ctrl+Shift+R)                      |

---

## 🔒 Sécurité

### ✅ Ce qui est sécurisé

| Aspect              | Implémentation                            |
| ------------------- | ----------------------------------------- |
| Génération de codes | SHA256 (cryptographiquement sûr)          |
| Unicité             | Basé sur code Airbnb + date               |
| Non-prévisibilité   | Hash cryptographique                      |
| Expiration          | Filtre automatique (départ < aujourd'hui) |
| Isolation           | Un code = un invité = une réservation     |

### ⚠️ Limitations

| Aspect           | Limitation                    | Recommandation                        |
| ---------------- | ----------------------------- | ------------------------------------- |
| Stockage         | Codes en clair dans JS public | Acceptable pour usage temporaire      |
| Authentification | Côté client uniquement        | Pas de données sensibles affichées    |
| WiFi/Portail     | Codes statiques               | Rotation régulière (manuelle)         |
| Révocation       | Pas de blocage individuel     | Régénérer tous les codes si compromis |

### 🛡️ Bonnes pratiques

1. **Rotation des mots de passe**

   ```
   WiFi: Changer tous les 3-6 mois
   Portail: Changer entre saisons
   ```

2. **Monitoring**

   ```
   - Logs du routeur WiFi
   - Surveillance du portail
   - Alertes sur accès inhabituels
   ```

3. **Mise à jour régulière**
   ```bash
   # Après chaque nouvelle réservation
   python generate_all_codes.py
   git push
   ```

---

## 📊 Statistiques

### Performance

| Opération             | Temps    | Résultat    |
| --------------------- | -------- | ----------- |
| Génération (10 codes) | ~0.5s    | 4 fichiers  |
| Validation complète   | ~0.3s    | OK/NOK      |
| Déploiement Git       | ~5s      | Push réussi |
| **Total workflow**    | **<10s** | ✅          |

### Taille des fichiers

| Fichier                   | Taille (10 codes) | Taille (100 codes) |
| ------------------------- | ----------------- | ------------------ |
| access_codes.json         | ~1 KB             | ~10 KB             |
| access_codes.js           | ~1 KB             | ~10 KB             |
| codes_invites.md          | ~2 KB             | ~15 KB             |
| codes-config-generated.js | ~2 KB             | ~20 KB             |
| **Total**                 | **~6 KB**         | **~55 KB**         |

---

## 🚀 Évolutions futures

### Court terme

- [ ] Script PowerShell (alternative à .bat)
- [ ] Support multi-propriétés (plusieurs appartements)
- [ ] Export PDF des codes (impression)

### Moyen terme

- [ ] API backend pour validation serveur
- [ ] Révocation individuelle de codes
- [ ] Statistiques d'utilisation (Analytics)

### Long terme

- [ ] Intégration OAuth Airbnb (sync auto)
- [ ] App mobile dédiée
- [ ] Génération automatique QR codes physiques

---

## 📚 Références

- **Script principal**: [generate_all_codes.py](generate_all_codes.py)
- **Validation**: [validate_system_final.py](validate_system_final.py)
- **Workflow**: [update_codes_workflow.bat](update_codes_workflow.bat)
- **Documentation**: [SYSTEME_CODES_FINAL.md](SYSTEME_CODES_FINAL.md)
- **Système original** (dossier à la racine du dépôt) : [../KatikiasDeployer_v5/](../KatikiasDeployer_v5/)
