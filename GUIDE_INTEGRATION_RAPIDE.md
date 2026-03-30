# 🚀 Guide d'intégration rapide - Codes sécurisés

## ✅ Checklist d'implémentation

### 1. Fichiers créés ✓

- [x] `hub.html` - Page d'accueil
- [x] `codes-acces.html` - Codes protégés
- [x] `arrival_guide.html` - Modifiée (codes retirés)
- [x] `assets/lang-*.js` - Traductions ajoutées (FR/EN/DE/ES)
- [x] `assets/codes-config.js` - Configuration codes
- [x] `generate_qrcode_hub.py` - Générateur QR code
- [x] `qrcodes/` - Dossier avec images QR code
- [x] `SECURITE_CODES_ACCES.md` - Documentation complète

### 2. Configuration codes (À faire)

- [ ] Éditer `assets/codes-config.js` avec vos codes réels
- [ ] Adapter dates d'expiration par réservation

### 3. QR code (À faire)

- [ ] Adapter URL dans `generate_qrcode_hub.py` (ligne 15)
  - GitHub Pages: `https://username.github.io/repo/hub.html`
  - Domaine custom: `https://votre-domaine.com/hub.html`
- [ ] Relancer: `python generate_qrcode_hub.py`
- [ ] Télécharger image QR code
- [ ] Imprimer format A5 (10cm x 10cm)
- [ ] Plastifier
- [ ] Afficher dans l'appartement

### 4. Déploiement

- [ ] Uploader tous les fichiers .html, .js, .md
- [ ] Vérifier que LanguageManager.js existe (`assets/lang-manager.js`)
- [ ] Tester sur localhost: `python -m http.server 8000`

### 5. Message Airbnb

- [ ] Créer message type avec code d'accès
- [ ] Mentionner le QR code ou URL directe
- [ ] Envoyer 24h avant l'arrivée

---

## 🧪 Test sur localhost

```bash
# 1. Démarrer le serveur
python -m http.server 8000

# 2. Ouvrir dans le navigateur
# http://localhost:8000/hub.html

# 3. Tester:
#    - Cliquer sur "Guide d'arrivée"
#    - Cliquer sur "Codes d'accès sécurisés"
#    - Entrer code: KATI9999 (code de test)
#    - Codes doivent s'afficher
#    - Tester mémorisation
#    - Tester déconnexion
```

---

## 📋 Codes d'accès à configurer

### Ajouter dans `assets/codes-config.js`:

```javascript
CODES_CONFIG["KATI0101"] = {
  expires: "2026-01-15", // À adapter
  door: "1234",
  pool: "5678",
  gate: "9999",
  notes: "Votre note",
};
```

**Format du code:** `KATI` + 4 chiffres
**Date:** `YYYY-MM-DD` (fin du séjour)

---

## 🔗 URLs importantes

| Page            | URL                           | Accès                 |
| --------------- | ----------------------------- | --------------------- |
| Hub (accueil)   | `/hub.html`                   | Public                |
| Codes sécurisés | `/codes-acces.html`           | Protégé (code requis) |
| Guide d'arrivée | `/arrival_guide.html`         | Public                |
| QR code         | `qrcodes/qrcode_hub_noir.png` | À imprimer            |

---

## 📱 Multilingue

Chaque page supporte 4 langues via sélecteur:

- 🇫🇷 Français (FR)
- 🇬🇧 English (EN)
- 🇩🇪 Deutsch (DE)
- 🇪🇸 Español (ES)

Paramètre de cache: `?v=4` (augmenter si modifications)

---

## 🔐 Test codes d'accès

**Code de test inclus (valide jusqu'en 2099):**

```
KATI9999
```

À supprimer après tests avant déploiement!

---

## ⚡ Optimisations possibles

1. **Intégrer codes-config.js dans codes-acces.html**

   ```html
   <script>
     const CODES_DATABASE = {
         'KATI0101': { ... }
     };
   </script>
   ```

2. **Augmenter version cache après modifications**

   ```html
   <script src="lang-fr.js?v=5"></script>
   ```

3. **Ajouter validation côté serveur** (optionnel)

---

## 🆘 Dépannage

### "Cannot convert undefined or null to object"

→ Vérifier que `lang-manager.js` est chargé

### Codes ne s'affichent pas après entrée du code

→ Vérifier la date d'expiration dans `codes-config.js`

### Langage ne change pas

→ Vérifier que `lang-*.js` sont chargés avec version cache

### QR code mène à erreur 404

→ Vérifier l'URL dans `generate_qrcode_hub.py`

---

## 📚 Documentation complète

Voir: [SECURITE_CODES_ACCES.md](./SECURITE_CODES_ACCES.md)

---

## 🎉 Prêt à déployer!

1. ✅ Configurer codes dans `assets/codes-config.js`
2. ✅ Adapter URL QR code dans `generate_qrcode_hub.py`
3. ✅ Générer QR code: `python generate_qrcode_hub.py`
4. ✅ Uploader fichiers
5. ✅ Imprimer et plastifier QR code
6. ✅ Afficher dans l'appartement
7. ✅ Ajouter code d'accès au message Airbnb

C'est tout! 🚀
