# 🚀 Guide de démarrage rapide - Katikias 33

**Chemin canonique du CSV (PC jfgir)** : `C:\Users\jfgir\Dev\Airbnb\KatikiasDeployer_v5\reservations_final.csv`

## ⚡ En 3 étapes

### 1️⃣ Exporter les réservations Airbnb

1. Connectez-vous à votre compte Airbnb hôte
2. Allez dans **Réservations** → **Toutes les réservations**
3. Cliquez sur **Exporter** (icône téléchargement)
4. Sélectionnez **Format CSV**
5. Sauvegardez le fichier sous **`C:\Users\jfgir\Dev\Airbnb\KatikiasDeployer_v5\reservations_final.csv`** (dossier `KatikiasDeployer_v5` à la racine du dépôt Git, pas dans `Guide-depart`).

**Format attendu:**

```csv
Nom de l'invité,Langue,Date d'arrivée,Date de départ,Code de confirmation,...
Paul Daniel,Anglais,01/05/2026,05/06/2026,HMSNMTRKTH,...
```

---

### 2️⃣ Générer les codes

**Option A: Workflow automatisé (recommandé)**

```batch
update_codes_workflow.bat
```

**Option B: Étape par étape**

```bash
# Générer les codes
python generate_all_codes.py

# Valider le système
python validate_system_final.py

# Voir les codes générés
cat codes_invites.md
```

**Résultat attendu:**

```
✅ 2 réservation(s) future(s) trouvée(s)
✅ JSON mis à jour
✅ JS mis à jour
✅ Markdown créé
✅ Config V2 créée
```

---

### 3️⃣ Déployer sur GitHub Pages

```bash
git add access_codes.* codes_invites.md assets/codes-config-generated.js
git commit -m "🔄 Mise à jour codes invités"
git push
```

**Vérification:**

- Les codes sont visibles sur: `https://guide.katikias33.fr`
- Test: `https://guide.katikias33.fr/hub.html?code=KATI-CN47SBA`

---

## 📧 Envoyer les codes aux invités

### Copier depuis codes_invites.md

Ouvrez `codes_invites.md` et copiez:

- Le code: `KATI-CN47SBA`
- Le lien direct: `https://guide.katikias33.fr/hub.html?code=KATI-CN47SBA`

### Template d'email

```
Objet: 🏡 Bienvenue à Katikias 33 - Votre code d'accès

Bonjour {{Nom}},

Nous sommes ravis de vous accueillir à Katikias 33!

🔐 Votre code d'accès:
{{CODE}}

👉 Lien direct:
{{LIEN}}

Ce lien vous donne accès à:
✅ Codes WiFi et portail
✅ Guide d'arrivée complet
✅ Informations pratiques

📅 Votre séjour: {{DATE_ARRIVÉE}} → {{DATE_DÉPART}}

À bientôt!
L'équipe Katikias 33
```

**Personnalisation:**

- Remplacez `{{Nom}}` par le nom de l'invité
- Remplacez `{{CODE}}` par le code d'accès
- Remplacez `{{LIEN}}` par le lien direct
- Remplacez `{{DATE_ARRIVÉE}}` et `{{DATE_DÉPART}}` par les dates

---

## ✅ Checklist de vérification

### Avant de générer les codes

- [ ] Export Airbnb à jour
- [ ] Fichier CSV dans `KatikiasDeployer_v5/reservations_final.csv`
- [ ] Format CSV correct (colonnes requises présentes)
- [ ] Dates au format DD/MM/YYYY

### Après génération

- [ ] `access_codes.json` créé
- [ ] `access_codes.js` créé
- [ ] `codes_invites.md` créé
- [ ] `assets/codes-config-generated.js` créé
- [ ] Validation réussie (`python validate_system_final.py`)

### Avant déploiement

- [ ] Codes vérifiés dans `codes_invites.md`
- [ ] Pas de codes expirés (départ > aujourd'hui)
- [ ] Git status propre
- [ ] Test local: ouvrir `hub.html` dans le navigateur

### Après déploiement

- [ ] Push GitHub réussi
- [ ] Site accessible: `https://guide.katikias33.fr`
- [ ] Test d'un code: `hub.html?code=KATI-XXXXXXX`
- [ ] Codes WiFi + Portail affichés correctement

---

## 🆘 Problèmes courants

### ❌ "Fichier CSV introuvable"

**Cause:** Le fichier `reservations_final.csv` n'existe pas

**Solution:**

```bash
# Vérifier l'emplacement
ls KatikiasDeployer_v5/reservations_final.csv

# Copier depuis le bon emplacement
cp /chemin/vers/export_airbnb.csv KatikiasDeployer_v5/reservations_final.csv
```

---

### ❌ "Colonnes manquantes dans CSV"

**Cause:** Le CSV n'a pas les colonnes requises

**Colonnes obligatoires:**

- `Nom de l'invité`
- `Date d'arrivée`
- `Date de départ`
- `Code de confirmation`

**Solution:** Exporter à nouveau depuis Airbnb avec toutes les colonnes

---

### ❌ "Aucune réservation future détectée"

**Cause:** Toutes les réservations sont expirées

**Solution:**

1. Vérifier les dates dans le CSV
2. S'assurer que `Date de départ` > aujourd'hui
3. Vérifier le format des dates: `DD/MM/YYYY`

---

### ❌ "Code invalide" dans l'interface

**Cause:** Cache du navigateur ou codes non synchronisés

**Solution:**

```bash
# 1. Régénérer les codes
python generate_all_codes.py

# 2. Vider le cache du navigateur
# Windows: Ctrl + Shift + R
# Mac: Cmd + Shift + R

# 3. Ou ouvrir en navigation privée
```

---

### ❌ "Git push échoue"

**Cause:** Problème d'authentification ou de connexion

**Solution:**

```bash
# Vérifier le statut Git
git status

# Vérifier la branche
git branch

# Vérifier le remote
git remote -v

# Forcer l'authentification
git push -u origin main
```

---

## 🔧 Commandes utiles

### Afficher les codes générés

```bash
# Voir tous les codes
cat codes_invites.md

# Compter les codes
python -c "import json; print(len(json.load(open('access_codes.json'))))"

# Chercher un invité spécifique
grep "Paul Daniel" codes_invites.md
```

### Régénérer tout

```bash
# Supprimer les anciens fichiers
rm access_codes.* codes_invites.md assets/codes-config-generated.js

# Régénérer
python generate_all_codes.py
```

### Tester localement

```bash
# Ouvrir dans le navigateur
start hub.html

# Ou avec un code pré-rempli
start hub.html?code=KATI-CN47SBA
```

---

## 📁 Structure des fichiers

```
Guide-depart/
├── generate_all_codes.py              ← Script principal
├── validate_system_final.py           ← Validation
├── update_codes_workflow.bat          ← Workflow automatisé
│
├── access_codes.json                  ← Codes générés (JSON)
├── access_codes.js                    ← Codes générés (JS)
├── codes_invites.md                   ← Suivi des codes
│
├── hub.html                           ← Page d'accueil
├── codes-acces.html                   ← Affichage des codes
│
├── assets/
│   └── codes-config-generated.js      ← Config pour codes-acces.html
│
└── KatikiasDeployer_v5/
    └── reservations_final.csv         ← Export Airbnb
```

---

## 🎯 Workflow hebdomadaire recommandé

### Chaque nouvelle réservation

1. Exporter CSV depuis Airbnb
2. Lancer `update_codes_workflow.bat`
3. Envoyer code par email à l'invité

### Chaque semaine

1. Vérifier les codes expirés

   ```bash
   python validate_system_final.py
   ```

2. Nettoyer si nécessaire
   ```bash
   # Régénérer pour supprimer les expirés
   python generate_all_codes.py
   ```

### Chaque mois

1. Changer le mot de passe WiFi
2. Mettre à jour `assets/codes-config-generated.js`
3. Redéployer

---

## 📚 Documentation complète

Pour plus de détails, consultez:

- **Architecture**: [ARCHITECTURE_VISUELLE.md](ARCHITECTURE_VISUELLE.md)
- **Système complet**: [SYSTEME_CODES_FINAL.md](SYSTEME_CODES_FINAL.md)
- **Code source**: [generate_all_codes.py](generate_all_codes.py)

---

## 💡 Astuces

### Envoi d'emails groupés

Utilisez `codes_invites.md` comme source:

```markdown
| Paul Daniel | 01/05/2026 | ... | `KATI-CN47SBA` | https://... |
```

→ Copiez-collez dans votre template d'email

### QR codes physiques

Générez des QR codes pour chaque réservation:

```python
import qrcode

code = "KATI-CN47SBA"
url = f"https://guide.katikias33.fr/hub.html?code={code}"

qr = qrcode.make(url)
qr.save(f"qrcode_{code}.png")
```

### Raccourci clavier

Créez un alias (Linux/Mac):

```bash
# Dans ~/.bashrc ou ~/.zshrc
alias katikias-update='python generate_all_codes.py && python validate_system_final.py'
```

Puis:

```bash
katikias-update
```

---

## 🎉 C'est tout!

Vous êtes maintenant prêt à gérer les codes d'accès de vos invités de manière professionnelle et sécurisée.

**Questions?** Consultez la documentation complète ou relisez ce guide.

**Problème?** Vérifiez la section "Problèmes courants" ci-dessus.

Bon succès avec Katikias 33! 🏡
