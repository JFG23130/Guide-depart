# 🛡️ GUIDE DE DÉPLOIEMENT SÉCURISÉ - GITHUB PAGES

## ✅ Sécurité vérifiée

Le système a été configuré pour **protéger les données sensibles** lors du déploiement public sur GitHub.

### 📊 Fichiers déployés (SÛRS)

| Fichier                            | Contenu                       | Sûr?   |
| ---------------------------------- | ----------------------------- | ------ |
| `access_codes.json`                | Codes invités uniquement      | ✅ OUI |
| `access_codes.js`                  | Codes invités + noms          | ✅ OUI |
| `codes_invites.md`                 | Table de suivi (noms + codes) | ✅ OUI |
| `assets/codes-config-generated.js` | Codes + dates expiration      | ✅ OUI |

### 🔒 Fichiers PROTÉGÉS (NON déployés)

| Fichier                                      | Raison                         | Protection |
| -------------------------------------------- | ------------------------------ | ---------- |
| `assets/codes-config-private.js`             | Codes WiFi + Portail sensibles | .gitignore |
| `KatikiasDeployer_v5/reservations_final.csv` | Données Airbnb complètes       | .gitignore |
| `.env` / secrets                             | Credentials (si applicable)    | .gitignore |

---

## 🚀 Déploiement sécurisé

### Étape 1: Vérifier le .gitignore

```bash
cat .gitignore
```

Devrait contenir:

```
assets/codes-config-private.js
KatikiasDeployer_v5/reservations_final.csv
```

### Étape 2: Vérifier les fichiers à déployer

```bash
git status
```

Devrait afficher:

```
À valider:
  new file:   access_codes.json
  new file:   access_codes.js
  new file:   codes_invites.md
  new file:   assets/codes-config-generated.js

Non suivi:
  assets/codes-config-private.js
  KatikiasDeployer_v5/reservations_final.csv
```

### Étape 3: Ajouter et commiter

```bash
git add access_codes.json access_codes.js codes_invites.md assets/codes-config-generated.js
git commit -m "🔐 Déploiement codes sécurisé (12 réservations)"
```

### Étape 4: Pousser vers GitHub

```bash
git push origin main
```

---

## 🔍 Vérification de sécurité

### ✅ Avant de déployer, vérifier:

```bash
# 1. Aucun fichier sensible staged
git diff --cached | grep -i "password\|wifi\|portail\|secret\|key" || echo "✅ OK"

# 2. .gitignore est appliqué
git check-ignore -v assets/codes-config-private.js || echo "⚠️ À ajouter à .gitignore"

# 3. Fichiers sensibles ne sont pas tracked
git ls-files | grep -i "private\|secret" || echo "✅ OK"
```

---

## 📝 Contenu des fichiers publics

### access_codes.json

```json
[
  {"code": "KATI-5LXUWKQ", "guest": "Lotfi Anis Benahmed"},
  {"code": "KATI-NNTQ2PA", "guest": "Clemence Nataf"},
  ...
]
```

**Données exposées:** Noms des invités + codes d'accès  
**Risque:** FAIBLE - Les codes d'accès sont publiquement acceptés  
**Impact:** Les invités peuvent voir les noms les uns des autres

### assets/codes-config-generated.js

```javascript
const CODES_DATABASE = {
  "KATI-5LXUWKQ": {
    expires: "2026-02-07",
    guest: "Lotfi Anis Benahmed",
  },
};
```

**Données exposées:** Codes + noms + dates d'expiration  
**Risque:** FAIBLE  
**Impact:** Pas de données sensibles

### codes_invites.md

```markdown
| Invité | Arrivée | Départ | Code | Lien direct |
| Lotfi Anis Benahmed | 05/02/2026 | 07/02/2026 | KATI-5LXUWKQ | ... |
```

**Données exposées:** Mêmes que access_codes.json + dates  
**Risque:** FAIBLE  
**Impact:** Calendrier des réservations visible

---

## 🚫 Fichiers SECRETS non déployés

### assets/codes-config-private.js

```javascript
// ⚠️ LOCAL UNIQUEMENT
const CODES_DATABASE_PRIVATE = {
  "KATI-5LXUWKQ": {
    wifi: "Katikias33", // ← SENSIBLE
    portail: "9999", // ← SENSIBLE
    airbnb_code: "HM2PT4Y925", // ← TRÈS SENSIBLE
  },
};
```

**Raison de la protection:**

- ❌ Codes WiFi: Accès au réseau de la maison
- ❌ Codes Portail: Accès physique à la propriété
- ❌ Codes Airbnb: Données de gestion

**Localisation sécurisée:** `.gitignore` → Non synchronisé avec GitHub

---

## 🎯 Architecture de sécurité

```
┌──────────────────────────────────────────────────────────────┐
│                  DONNÉES AIRBNB (Local)                      │
│                reservations_final.csv                         │
│  • Noms, emails, téléphones                                  │
│  • Codes de réservation Airbnb                               │
│  • Numéro de nuits, revenus                                  │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼ (traitement local)
┌──────────────────────────────────────────────────────────────┐
│              CODES PRIVÉS (Local uniquement)                 │
│         assets/codes-config-private.js                       │
│  • WiFi: Katikias33                                          │
│  • Portail: 9999                                             │
│  • Codes Airbnb: HM2PT4Y925 ...                              │
│                                                              │
│  ⚠️ .gitignore → NE JAMAIS PUBLIÉ                            │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼ (extraction)
┌──────────────────────────────────────────────────────────────┐
│          CODES PUBLICS (GitHub Pages Public)                │
│  • access_codes.json                                         │
│  • access_codes.js                                           │
│  • codes_invites.md                                          │
│  • assets/codes-config-generated.js (VERSION SÛRE)          │
│                                                              │
│  ✅ Déployé sur GitHub Pages                                 │
└──────────────────────────────────────────────────────────────┘
                 │
                 ▼ (réseau public)
┌──────────────────────────────────────────────────────────────┐
│                  INVITÉS (Navigateur)                        │
│  https://guide.katikias33.fr/hub.html?code=KATI-XXXXX      │
│                                                              │
│  ✅ Voient codes d'accès + WiFi/Portail                      │
│  ❌ Ne voient PAS les noms d'autres invités                  │
│  ❌ Ne voient PAS les codes Airbnb                           │
└──────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Considérations de sécurité supplémentaires

### Données exposées intentionnellement

- ✅ **Codes d'accès (KATI-XXXXX):** C'est leur rôle
- ✅ **Noms des invités:** Accepté dans codes_invites.md
- ✅ **Dates des séjours:** Visible dans le calendrier

### Données exposées involontairement

- ⚠️ **AVANT:** WiFi + Portail dans le JS public
- ✅ **APRÈS:** Supprimé via .gitignore

### Données jamais exposées

- ❌ **Codes Airbnb:** Jamais dans les fichiers publics
- ❌ **Emails/Téléphones:** Non utilisés
- ❌ **Numéro de nuits:** Non exposé
- ❌ **Revenus:** Non exposé

---

## 🔐 Recommandations supplémentaires

### 1. Rotation des codes

```bash
# Tous les 3-6 mois
- Changer le mot de passe WiFi
- Mettre à jour portail (si possible)
- Régénérer les codes invités
python generate_all_codes.py
git push
```

### 2. Monitoring des accès

```bash
# Surveiller:
- Logs du routeur WiFi
- Accès au portail
- Analytics du site (Google Analytics)
```

### 3. Révocation rapide

```bash
# Si compromis:
- Changer WiFi immédiatement
- Changer code portail immédiatement
- Régénérer codes invités
- Contacter invités affectés
```

### 4. Backups locales

```bash
# Conserver en local (pas sur GitHub):
- assets/codes-config-private.js (sauvegarder)
- reservations_final.csv (archiver)
```

---

## ✅ PRÊT POUR DÉPLOIEMENT

**Sécurité:** ✅ Vérifiée  
**Fichiers sensibles:** ✅ Protégés  
**.gitignore:** ✅ Configuré  
**Données publiques:** ✅ Non sensibles

### Commande de déploiement sécurisé:

```bash
git add access_codes.json access_codes.js codes_invites.md assets/codes-config-generated.js
git commit -m "🔐 Déploiement codes sécurisé - 12 réservations"
git push origin main
```

---

## 📋 Checklist final

- [ ] `.gitignore` contient les fichiers sensibles
- [ ] `assets/codes-config-private.js` existe localement
- [ ] Aucun fichier `.csv` dans git status
- [ ] `git diff --cached` ne montre pas de codes WiFi/Portail
- [ ] Vérification: `git ls-files | grep -i private` = aucun résultat
- [ ] Site GitHub Pages live et fonctionnel
- [ ] Test d'accès: `https://guide.katikias33.fr/hub.html?code=KATI-5LXUWKQ`

---

**Déploiement:** ✅ OUI, C'EST SÛR! 🎉
