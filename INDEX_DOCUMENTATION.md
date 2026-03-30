# 📋 INDEX DE LA DOCUMENTATION - KATIKIAS 33

## 🎯 Par où commencer?

### 🚀 Vous débutez?

**→ [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)**

- Installation en 3 étapes
- Génération des codes
- Déploiement

### 🏗️ Vous voulez comprendre l'architecture?

**→ [ARCHITECTURE_VISUELLE.md](ARCHITECTURE_VISUELLE.md)**

- Schémas et diagrammes
- Flux de données
- Structure des fichiers

### 📘 Vous cherchez la documentation technique?

**→ [SYSTEME_CODES_FINAL.md](SYSTEME_CODES_FINAL.md)**

- Architecture complète
- Format des codes
- Sécurité
- API et interfaces

### 📖 Documentation originale GitHub Pages

**→ [README.md](README.md)**

- Configuration du site web
- Déploiement GitHub Pages
- Structure HTML

---

## 📁 Fichiers importants

### Scripts Python

| Fichier                                                    | Description                  | Utilisation                          |
| ---------------------------------------------------------- | ---------------------------- | ------------------------------------ |
| [generate_all_codes.py](generate_all_codes.py)             | Génération des codes d'accès | `python generate_all_codes.py`       |
| [validate_system_final.py](validate_system_final.py)       | Validation du système        | `python validate_system_final.py`    |
| [qrcode_manager.py](qrcode_manager.py)                     | Gestion des QR codes         | `python qrcode_manager.py health`    |
| [translate_all_content_v2.py](translate_all_content_v2.py) | Traductions automatiques     | `python translate_all_content_v2.py` |

### Scripts Batch (Windows)

| Fichier                                                | Description                 | Utilisation                                |
| ------------------------------------------------------ | --------------------------- | ------------------------------------------ |
| [update_codes_workflow.bat](update_codes_workflow.bat) | Workflow automatisé complet | Double-clic ou `update_codes_workflow.bat` |

### Fichiers générés (ne pas éditer manuellement)

| Fichier                          | Description            | Format                              |
| -------------------------------- | ---------------------- | ----------------------------------- |
| access_codes.json                | Codes au format JSON   | `[{"code": "...", "guest": "..."}]` |
| access_codes.js                  | Codes au format JS     | `window.__ACCESS_CODES__ = [...]`   |
| codes_invites.md                 | Table de suivi lisible | Markdown table                      |
| assets/codes-config-generated.js | Config complète        | `CODES_DATABASE = {...}`            |

### Fichiers source (éditer avec précaution)

| Fichier                                    | Description                      | Langage |
| ------------------------------------------ | -------------------------------- | ------- |
| hub.html                                   | Page d'accueil avec QR codes     | HTML/JS |
| codes-acces.html                           | Affichage des codes WiFi/Portail | HTML/JS |
| KatikiasDeployer_v5/reservations_final.csv | Export Airbnb                    | CSV     |

---

## 🔄 Workflows communs

### Nouvelle réservation

```bash
# 1. Exporter depuis Airbnb
# → Sauvegarder dans KatikiasDeployer_v5/reservations_final.csv

# 2. Générer les codes
python generate_all_codes.py

# 3. Valider
python validate_system_final.py

# 4. Déployer
git add access_codes.* codes_invites.md assets/codes-config-generated.js
git commit -m "🔄 Nouvelle réservation"
git push
```

**Ou version automatique:**

```batch
update_codes_workflow.bat
```

### Changement de mot de passe WiFi

```bash
# 1. Éditer le mot de passe dans generate_all_codes.py
# Ligne ~165: wifi: 'NouveauMotDePasse'

# 2. Régénérer
python generate_all_codes.py

# 3. Déployer
git push
```

### Ajout d'une nouvelle langue

```bash
# 1. Traduire le contenu
python translate_all_content_v2.py --lang pt  # Portugais par exemple

# 2. Déployer
git add *_pt.html
git commit -m "✨ Ajout langue portugaise"
git push
```

---

## 🆘 Dépannage rapide

| Problème           | Solution rapide                               | Doc complète                                                              |
| ------------------ | --------------------------------------------- | ------------------------------------------------------------------------- |
| CSV introuvable    | Copier dans `KatikiasDeployer_v5/`            | [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md#-csv-introuvable)               |
| Code invalide      | `python generate_all_codes.py` + Ctrl+Shift+R | [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md#-code-invalide)                 |
| Aucune réservation | Vérifier dates (DD/MM/YYYY)                   | [SYSTEME_CODES_FINAL.md](SYSTEME_CODES_FINAL.md#formats-de-date-acceptés) |
| Git push échoue    | Vérifier auth: `git remote -v`                | [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md#-git-push-échoue)               |

---

## 📊 Vue d'ensemble rapide

```
┌─────────────────────────────────────────────────┐
│         Export Airbnb (CSV)                     │
└──────────────┬──────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────┐
│      generate_all_codes.py                      │
│      (SHA256 → KATI-XXXXXXX)                    │
└──────────┬─────────┬─────────┬──────────────────┘
           │         │         │
           ▼         ▼         ▼
     JSON       JS        MD       Config
           │         │         │
           └─────┬───┴─────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│         hub.html + codes-acces.html             │
│         (Interface web invité)                   │
└─────────────────────────────────────────────────┘
```

**Détails:** [ARCHITECTURE_VISUELLE.md](ARCHITECTURE_VISUELLE.md)

---

## 🔗 Liens externes

- **Site live:** https://guide.katikias33.fr (ou votre URL GitHub Pages)
- **Repository GitHub:** https://github.com/votre-username/Guide-depart
- **Airbnb:** https://www.airbnb.fr (pour exporter les réservations)

---

## 📝 Historique des versions

| Version | Date     | Changements majeurs                         | Doc                                                         |
| ------- | -------- | ------------------------------------------- | ----------------------------------------------------------- |
| 3.0     | Fév 2026 | Système unifié, SHA256, workflow automatisé | [SYSTEME_CODES_FINAL.md](SYSTEME_CODES_FINAL.md#-changelog) |
| 2.0     | Fév 2026 | Simplification (WiFi + Portail uniquement)  | -                                                           |
| 1.0     | Jan 2026 | Version initiale (5 codes)                  | -                                                           |

---

## 💡 Astuces

### Génération rapide

```bash
# Alias recommandé (Linux/Mac)
alias katikias='cd /chemin/vers/Guide-depart && python generate_all_codes.py'

# Puis simplement:
katikias
```

### Édition des codes WiFi/Portail

```python
# Dans generate_all_codes.py, ligne ~165
js_content += f"""    '{code}': {{
    wifi: 'VotreSSID',      # ← Modifier ici
    portail: '1234',        # ← Modifier ici
}}
```

### Test local avant déploiement

```bash
# Ouvrir dans le navigateur
start hub.html?code=KATI-CN47SBA

# Ou avec Python
python -m http.server 8000
# → http://localhost:8000/hub.html?code=KATI-CN47SBA
```

---

## 🎯 Checklist avant déploiement

- [ ] Export Airbnb à jour
- [ ] `python generate_all_codes.py` sans erreur
- [ ] `python validate_system_final.py` OK
- [ ] Test local: `hub.html?code=KATI-XXX` fonctionne
- [ ] Codes WiFi/Portail corrects
- [ ] `git status` propre
- [ ] Commit descriptif

---

## 📧 Support

**Questions?** Consultez d'abord:

1. [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md) - FAQ et problèmes courants
2. [SYSTEME_CODES_FINAL.md](SYSTEME_CODES_FINAL.md) - Documentation technique
3. [ARCHITECTURE_VISUELLE.md](ARCHITECTURE_VISUELLE.md) - Schémas

**Toujours bloqué?**

- Créez une issue GitHub
- Relisez les messages d'erreur
- Vérifiez les logs

---

**Dernière mise à jour:** Février 2026  
**Version du système:** 3.0  
**Auteur:** jfgir
