# Mémo — Où et comment ajouter les traductions

> **Réservations Airbnb (hors traductions)** : fichier unique `C:\Users\jfgir\Dev\Airbnb\KatikiasDeployer_v5\reservations_final.csv` — voir aussi `MEMOS_SOLUTION.md` à la racine du dépôt.

## Fichiers des langues

Tout se passe dans **`Guide-depart/assets/`** :

| Fichier           | Langue   |
|-------------------|----------|
| `lang-fr.js`      | Français (référence) |
| `lang-en.js`      | Anglais  |
| `lang-de.js`      | Allemand |
| `lang-es.js`      | Espagnol |
| `lang-nl.js`      | Néerlandais |
| `lang-it.js`      | Italien  |

Chaque fichier exporte un objet du type `window.translationsFR = { "clé": "texte", ... }` (remplacer `FR` par `EN`, `DE`, etc.).

**Règle** : ajouter **la même clé** dans **les six fichiers** dès que possible. Si une langue manque, le site garde souvent le texte déjà affiché ou la clé (voir `init-translations.js`).

---

## 1. Textes statiques dans le HTML (titres, boutons, paragraphes)

1. Dans le HTML, mettre une **clé** sur l’élément :  
   `data-lang-key="ma.cle.unique"`
2. Mettre le **texte français par défaut** entre les balises (comme aujourd’hui).
3. Dans **`lang-fr.js`** (et les autres langues), ajouter :  
   `"ma.cle.unique": "Texte affiché pour cette langue"`

Exemple existant : `data-lang-key="cuisine.title"` → clé `cuisine.title` dans chaque `lang-*.js`.

---

## 2. Noms d’équipements (liste `<li>` sur les pages pièce)

1. **Clé** : même schéma que dans vos commentaires admin / PDF, du type  
   **`{page}.li.{identifiant}`**  
   Exemples : `cuisine.li.cafetière`, `chambre.li.lit_160`.
2. Sur le `<li>` :  
   `data-lang-key="cuisine.li.cafetière"`  
   **et** `data-slug="cafetiere"` (slug **stable** basé sur le nom français, pour les chemins d’images — ne pas le changer selon la langue).
3. Remplir la clé dans **`lang-fr.js`** … **`lang-it.js`**.

Référence : voir **`cuisine.html`** (liste déjà annotée).

---

## 3. Légendes sous les photos (commentaires par photo)

Les clés sont générées automatiquement à partir du JSON **`assets/guide-content.json`** (nom d’équipement + ordre d’affichage de la photo) :

**Convention** :  
`{pageKey}.caption.{slug_equipement}.{DisplayOrder}`

Exemples pour la page cuisine, équipement « Cafetière », photos d’ordre 20 et 30 :

- `cuisine.caption.cafetiere.20`
- `cuisine.caption.cafetiere.30`

- **`pageKey`** = nom de la page (`cuisine`, `chambre`, `wc`, …).
- **`slug_equipement`** = même logique que le slug du nom (sans accents, underscores) — identique au merge dans **`load-guide-captions.js`**.
- **`DisplayOrder`** = valeur numérique dans l’admin pour cette photo (souvent 10, 20, 30…).

Ajouter ces clés dans **les six** `lang-*.js` avec le texte voulu pour chaque langue.

---

## 4. Ordre de chargement (pour mémoire)

Le sélecteur de langue utilise **`assets/init-translations.js`**, qui lit les `lang-*.js` puis applique les clés à tous les éléments `[data-lang-key]`.  
Les pages pièce rechargent aussi les légendes dynamiques après **`guide-content.json`** (`guide-room-i18n.js`).

---

## 5. Après modification des fichiers de langue

Recharger la page (vidage de cache si besoin : les scripts ont souvent un paramètre `?v=`).  
Pour un test fiable du JSON + `fetch`, servir le dossier en **HTTP local** plutôt qu’en `file://`.

---

## 6. Outil intégré — Guide Appartement Admin (onglet « Traductions »)

Dans l’application **GuideDepartAdmin** :

1. Onglet **Traductions** : tableau avec les **titres de page** (clés `*.title`), les **noms d’équipements** (clé `Clé:` dans le commentaire de fiche, sinon `{page}.li.{slug}`), et les **légendes** pour chaque photo ayant un commentaire (`*.caption.*`).
2. **Recharger le tableau** : relit `guide-content.json` et les valeurs actuelles des six `lang-*.js`.
3. **Sauver brouillon (JSON)** : écrit `assets/guide-translation-draft.json` (sauvegarde de travail, optionnel).
4. **Transférer vers lang-\*.js** : fusionne les textes du tableau dans les six fichiers (les autres clés du site, hors tableau, sont **conservées**). Un backup est créé sous **`Guide-depart/_backups_lang/<horodatage>/`**.

Les textes généraux du site (hors équipements) restent à éditer à la main dans les `lang-*.js` ou via un futur complément.

---

## Récap express

| Contenu              | Où éditer                         |
|----------------------|-----------------------------------|
| Texte UI général     | HTML + `lang-*.js`                |
| Nom d’un équipement  | `<li data-lang-key data-slug>` + `lang-*.js` |
| Légende d’une photo  | Clé `page.caption.slug.ordre` dans `lang-*.js` (texte FR dans le JSON / admin inchangé pour la source) |
| Tableau admin        | Onglet **Traductions** → **Transférer vers lang-\*.js** |
