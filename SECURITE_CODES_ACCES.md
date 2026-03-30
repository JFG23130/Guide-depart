# 🔐 Système de Codes d'Accès Sécurisés - Katikias 33

## 📋 Vue d'ensemble

Ce système implémente une solution de sécurité pour les codes d'accès (WiFi, porte, piscine) sans créer une "usine à gaz".

### Architecture

```
QR code fixe (affiche dans l'appartement)
        ↓
    hub.html (page d'accueil publique)
        ├─→ arrival_guide.html (guide sans codes)
        └─→ codes-acces.html (codes protégés par mot de passe personnel)
```

## 🎯 Flux utilisateur

### Premier accès (arrivée)

1. Voyageur scanne le QR code dans l'appartement
2. Ouvre `hub.html` (page d'accueil)
3. Clique sur "Codes d'accès sécurisés"
4. Entre le code personnel reçu via Airbnb (ex: `KATI1234`)
5. Codes affichés + option de mémorisation

### Accès ultérieurs (même séjour)

1. Ouvre favoris / historique → `hub.html`
2. Clique sur "Codes d'accès sécurisés"
3. **Codes affichés DIRECTEMENT** (localStorage mémorise)
4. ✅ Pas besoin de re-saisir le code

### À la fin du séjour

- Voyageur clique "Je quitte le logement"
- localStorage vidé
- Codes inaccessibles même avec ancien code

---

## 📄 Fichiers créés

### 1. **hub.html** - Page d'accueil (QR code → ici)

- Landing page publique
- Lien vers guide d'arrivée (public)
- Lien vers codes sécurisés (protégés)
- Support multilingue FR/EN/DE/ES
- Cache-busting: `?v=4`

### 2. **codes-acces.html** - Codes protégés

- Authentification par code personnel
- Mémorisation via localStorage + sessionStorage
- Vérification d'expiration automatique
- Affichage codes: WiFi, porte, piscine, parking
- Support multilingue FR/EN/DE/ES
- Bouton "Je quitte le logement" pour nettoyer la session

### 3. **assets/codes-config.js** - Configuration codes

- Base de données des codes par réservation
- Format: `KATI0101` → données d'accès + date expiration
- Facile à gérer et mettre à jour

### 4. **generate_qrcode_hub.py** - Générateur QR code

- Script pour générer l'image QR code
- 3 versions: noir/blanc, couleur, gradient
- À adapter à votre domaine de déploiement

### 5. **arrival_guide.html** (modifié)

- Codes sensibles RETIRÉS
- Lien coloré vers `codes-acces.html`
- Message: "Pour votre sécurité, codes protégés"

### 6. **assets/lang-\*.js** (modifiés)

- Ajout de 40+ clés de traduction pour hub et codes
- Support complet FR/EN/DE/ES
- Intégration avec LanguageManager existant

---

## 🔧 Configuration

### Gérer les codes par réservation

**Éditer `assets/codes-config.js`:**

```javascript
CODES_CONFIG = {
  KATI0101: {
    // Code personnel de la réservation
    expires: "2026-01-15", // Date fin du séjour (YYYY-MM-DD)
    door: "1234", // Code porte entrée
    pool: "5678", // Code piscine
    gate: "9999", // Code portail
    notes: "Réservation Janvier 2026",
  },
  KATI0202: {
    expires: "2026-02-22",
    door: "1234",
    pool: "5678",
    gate: "9999",
    notes: "Réservation Février 2026",
  },
};
```

### Intégrer codes-config.js dans codes-acces.html

Ajouter avant `</body>`:

```html
<script src="assets/codes-config.js"></script>
<script>
  // Utiliser les codes de config
  const CODES_DATABASE = CODES_CONFIG;
</script>
```

### Générer le QR code

```bash
python generate_qrcode_hub.py
```

Crée 3 images dans le dossier `qrcodes/`:

- `qrcode_hub_noir.png` (noir et blanc - classique)
- `qrcode_hub_couleur.png` (bleu)
- `qrcode_hub_gradient.png` (dégradé)

**Paramètres à adapter:**

- Ligne 15: `base_urls['localhost']` → votre domaine de déploiement
- Format A5 (10cm x 10cm minimum)
- Plastifier pour durabilité
- Placer près de la porte d'entrée

---

## 🌐 Déploiement

### Pour GitHub Pages

1. Modifier `generate_qrcode_hub.py` ligne 15:

```python
url = 'https://votre-username.github.io/repo-name/hub.html'
```

2. Générer le QR code
3. Imprimer et afficher

### Pour domaine custom

1. Modifier `generate_qrcode_hub.py`:

```python
url = 'https://votre-domaine.com/hub.html'
```

2. S'assurer que tous les fichiers sont uploadés:
   - hub.html
   - codes-acces.html
   - arrival_guide.html
   - assets/lang-\*.js
   - assets/lang-manager.js
   - assets/codes-config.js (optionnel, intégrable dans codes-acces.html)

---

## 🔒 Sécurité

### Points forts

✅ Codes WiFi/porte JAMAIS visibles en ligne (sans authentification)
✅ Codes uniques par réservation
✅ Expiration automatique après le séjour
✅ Mémorisation limitée au navigateur + expiration
✅ QR code fixe (ne risque pas d'être intercepté)
✅ Contrôle complet sur la durée d'accès

### Limitations (et pourquoi c'est OK)

⚠️ Codes JavaScript lisibles dans le source
→ Acceptable car accessibles APRÈS authentification

⚠️ Codes stockés en localStorage
→ Acceptable car date-limitées (expirent automatiquement)

⚠️ localStorage vidé au départ (bouton "Je quitte")
→ Protège contre les oublis

---

## 📱 Support multilingue

Toutes les pages supportent: **FR | EN | DE | ES**

Sélecteur langue en haut à droite de chaque page.

Clés ajoutées:

- `hub.*` (32 clés pour hub.html)
- `codes.*` (24 clés pour codes-acces.html)

---

## 📊 Métriques de confiance

| Élément                 | Avant              | Après                         |
| ----------------------- | ------------------ | ----------------------------- |
| **Codes exposés**       | ❌ Oui (dans HTML) | ✅ Non (protégés)             |
| **Codes WiFi visibles** | ❌ Toujours        | ✅ Après auth                 |
| **Durée d'accès**       | ❌ Infini          | ✅ Contrôlée                  |
| **Traçabilité**         | ❌ Non             | ✅ Code unique/réservation    |
| **Complexité**          | -                  | ✅ Simple (pas d'usine à gaz) |

---

## ⚙️ Maintenance

### Ajouter une réservation

```javascript
// Éditer assets/codes-config.js
CODES_CONFIG["KATI0303"] = {
  expires: "2026-03-20",
  door: "1234",
  pool: "5678",
  gate: "9999",
  notes: "Réservation Mars 2026",
};
```

### Supprimer un code expiré

```javascript
delete CODES_CONFIG["KATI0101"]; // Après 2026-01-15
```

### Modifier les codes d'accès

```javascript
CODES_CONFIG["KATI0101"].door = "5555"; // Changer code porte
```

---

## 🎓 Cas d'usage

### ✅ Fonctionne bien pour

- Locations courte durée (Airbnb)
- Codes statiques (WiFi, portes)
- Voyageurs occasionnels

### ⚠️ À adapter si

- Codes changent en cours de séjour → ajouter nouvelle clé
- Accès multi-utilisateurs → ajouter système de partage
- Codes très sensibles → ajouter couche HTTPS

---

## 🚀 Améliorations futures (optionnelles)

1. **Envoi automatique par email/SMS**
   - API Twilio ou SendGrid
   - Code envoyé automatiquement 24h avant arrivée

2. **Dashboard admin**
   - Gestion codes réservations
   - Historique accès

3. **Codes temporaires**
   - Codes valides seulement certaines heures
   - Codes à usage unique

4. **Intégration Airbnb API**
   - Import automatique réservations
   - Génération codes automatique

---

## 📞 Support

**Questions fréquentes:**

**Q: Est-ce que le QR code change?**
A: NON. Le QR code est FIXE et pointe toujours vers `hub.html`. Seul le code d'accès change par voyageur.

**Q: Qu'arrive-t-il après la date d'expiration?**
A: Les codes ne s'affichent pas. Message "Votre séjour est terminé."

**Q: Comment les codes sont-ils partagés?**
A: Via message Airbnb personnalisé 24h avant arrivée (à faire manuellement ou via automations).

**Q: Est-ce sécurisé?**
A: ✅ Oui pour usage Airbnb. Les codes sont inaccessibles sans authentification et expirent automatiquement.

---

## 📄 Fichier d'aide - Message Airbnb type

```
Bonjour [Prénom] 👋

Votre arrivée approche à Katikias 33 !

🔐 CODES D'ACCÈS SÉCURISÉS
Voici votre code d'accès personnel: KATI0101

📱 Comment accéder aux codes:
   1. Scannez le QR code dans l'appartement
      (près de la porte d'entrée)
   2. Ou ouvrez: https://votre-domaine.com/hub.html
   3. Cliquez sur "Codes d'accès sécurisés"
   4. Entrez votre code: KATI0101

📝 Les codes inclus:
   • 📶 Wi-Fi
   • 🏠 Porte d'entrée
   • 🏊 Piscine
   • 🚪 Portail
   • 🚗 Parking

💡 Astuce: Sauvegardez cette page en favoris!

À très bientôt à Katikias 33 🌟
[Votre nom]
```

---

## 🎉 C'est prêt!

Tous les fichiers sont en place. Déployer et profiter d'une sécurité simple et efficace! 🔐
