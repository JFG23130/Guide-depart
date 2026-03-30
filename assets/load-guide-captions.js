/**
 * Applique data-captions sur chaque <li> depuis assets/guide-content.json
 * (même logique que l'admin : Pièce = pageKey, Nom = libellé de la ligne).
 * À utiliser sur les pages pièce (cuisine, chambre, …) avant le script qui charge les images.
 */
(function (global) {
    function slugify(text) {
        if (!text) return '';
        return String(text)
            .toLowerCase()
            .normalize('NFD')
            .replace(/\p{Diacritic}/gu, '')
            .replace(/[^a-z0-9]+/g, '_')
            .replace(/^_+|_+$/g, '')
            .replace(/_{2,}/g, '_');
    }

    /**
     * Même tolérance que GuideDepartAdmin (IsEquipmentForRoom) : ex. « Salle à Manger » → salle_a_manger ≠ salle_manger.
     */
    /** @returns {{ pdf: string, langKey: string }} chemins issus des lignes PDF: … et Clé: … dans Comment */
    function metaFromEquipmentComment(comment) {
        var pdf = '';
        var langKey = '';
        if (!comment) return { pdf: pdf, langKey: langKey };
        String(comment).split(/\r?\n/).forEach(function (line) {
            var t = line.trim();
            var m = /^PDF\s*:\s*(.+)$/i.exec(t);
            if (m) pdf = m[1].trim().replace(/\\/g, '/');
            m = /^Clé\s*:\s*(.+)$/i.exec(t);
            if (m) langKey = m[1].trim();
        });
        return { pdf: pdf, langKey: langKey };
    }

    function matchesRoomPage(pieceSlug, pageKey) {
        if (!pieceSlug || !pageKey) return false;
        if (pieceSlug === pageKey) return true;
        switch (pageKey) {
            case 'salle_deau':
                return pieceSlug.indexOf('salle') >= 0 && pieceSlug.indexOf('eau') >= 0;
            case 'salle_manger':
                return pieceSlug.indexOf('salle') >= 0 && pieceSlug.indexOf('manger') >= 0;
            case 'placard_bleu':
                return pieceSlug.indexOf('placard') >= 0;
            default: {
                var compact = pageKey.replace(/_/g, '');
                return pieceSlug.indexOf(compact) >= 0 || pieceSlug.indexOf(pageKey) >= 0;
            }
        }
    }

    /**
     * @param {string} pageKey ex. 'cuisine', 'chambre'
     * @returns {Promise<void>}
     */
    global.__guideMergeCaptionsFromJson = function (pageKey) {
        return fetch('assets/guide-content.json?cb=' + Date.now())
            .then(function (r) {
                if (!r.ok) return Promise.reject();
                return r.json();
            })
            .then(function (data) {
                var eqs = data.Equipments || data.equipments;
                if (!eqs || !eqs.length) return;
                var map = {};
                for (var i = 0; i < eqs.length; i++) {
                    var eq = eqs[i];
                    if (eq.IsActive === false) continue;
                    var pieceSlug = slugify(eq.Category || '');
                    if (!matchesRoomPage(pieceSlug, pageKey)) continue;
                    var eqSlug = slugify(eq.Name || eq.name || '');
                    var meta = metaFromEquipmentComment(eq.Comment || eq.comment || '');
                    if (meta.pdf) {
                        map[eqSlug + '__pdf'] = meta.pdf;
                    }
                    if (meta.langKey) {
                        map[eqSlug + '__langkey'] = meta.langKey;
                    } else {
                        map[eqSlug + '__langkey'] = pageKey + '.li.' + eqSlug;
                    }
                    var photos = (eq.Photos || eq.photos || []).slice().sort(function (a, b) {
                        return (a.DisplayOrder || a.displayOrder || 0) - (b.DisplayOrder || b.displayOrder || 0);
                    });
                    if (!photos.length) continue;
                    var photosWithPath = photos.filter(function (p) {
                        return (p.Path || p.path || '').trim();
                    });
                    var pathParts = photosWithPath.map(function (p) {
                        return (p.Path || p.path || '').trim().replace(/\\/g, '/');
                    });
                    if (pathParts.length) {
                        map[eqSlug + '__photos'] = pathParts.join('|');
                        var photoPdfParts = photosWithPath.map(function (p) {
                            var pp = (p.PdfPath || p.pdfPath || '').trim().replace(/\\/g, '/');
                            if (pp) return pp;
                            return meta.pdf || '';
                        });
                        if (photoPdfParts.some(function (x) { return !!x; })) {
                            map[eqSlug + '__photopdfs'] = photoPdfParts.join('|');
                        }
                    }
                    var parts = photos.map(function (p) {
                        return (p.Comment || p.comment || '').trim();
                    });
                    if (parts.some(function (c) { return !!c; })) {
                        map[eqSlug] = parts.join('|');
                        var keyParts = photos.map(function (p) {
                            var order = p.DisplayOrder || p.displayOrder || 0;
                            var comment = (p.Comment || p.comment || '').trim();
                            if (!comment) return '';
                            return pageKey + '.caption.' + eqSlug + '.' + order;
                        });
                        map[eqSlug + '__keys'] = keyParts.join('|');
                    }
                }
                document.querySelectorAll('.content ul li').forEach(function (li) {
                    var slug = li.getAttribute('data-slug') || slugify(li.textContent.trim());
                    if (map[slug]) {
                        li.setAttribute('data-captions', map[slug]);
                    }
                    var keys = map[slug + '__keys'];
                    if (keys) {
                        li.setAttribute('data-caption-keys', keys);
                    }
                    var pp = map[slug + '__photos'];
                    if (pp) {
                        li.setAttribute('data-photo-paths', pp);
                    }
                    var photoPdfsM = map[slug + '__photopdfs'];
                    if (photoPdfsM) {
                        li.setAttribute('data-photo-pdfs', photoPdfsM);
                    } else {
                        var pdfA = map[slug + '__pdf'];
                        if (pdfA) {
                            li.setAttribute('data-pdf', pdfA);
                        }
                    }
                    var lk = map[slug + '__langkey'];
                    if (lk) {
                        li.setAttribute('data-lang-key', lk);
                    }
                });
            })
            .catch(function () {
                /* file:// ou JSON absent : on garde les data-captions déjà dans le HTML */
            });
    };
})(window);
