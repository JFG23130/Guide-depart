/**
 * Pages pièce : après rendu dynamique (photos + légendes), réapplique les traductions
 * et synchronise les attributs alt des images sur le libellé courant du <li>.
 */
(function (global) {
    global.__guideAfterRoomPhotos = function () {
        if (typeof LanguageSystemHTML === 'undefined') return;
        LanguageSystemHTML.translatePage();
        if (typeof LanguageSystemHTML.syncRoomPhotoAlts === 'function') {
            LanguageSystemHTML.syncRoomPhotoAlts();
        }
        try {
            document.dispatchEvent(
                new CustomEvent('guideLanguageChanged', {
                    detail: { lang: LanguageSystemHTML.currentLanguage },
                })
            );
        } catch (e) {}
    };
})(window);
