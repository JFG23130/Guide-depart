// Initialiser le système multilingue pour les pages HTML
// Charger les 4 fichiers de langue et configurer la traduction automatique

console.log('🚀 Initialisation du système multilingue...');

// Vérifier que les traductions sont chargées
let retries = 0;
const maxRetries = 50; // 5 secondes max

function waitForTranslations() {
    retries++;
    
    if (typeof translationsFR !== 'undefined' && 
        typeof translationsEN !== 'undefined' && 
        typeof translationsDE !== 'undefined' && 
        typeof translationsES !== 'undefined' &&
        typeof translationsNL !== 'undefined' &&
        typeof translationsIT !== 'undefined') {
        
        console.log('✅ Tous les fichiers de langue chargés');
        console.log('FR:', Object.keys(translationsFR).length, 'clés');
        console.log('EN:', Object.keys(translationsEN).length, 'clés');
        console.log('DE:', Object.keys(translationsDE).length, 'clés');
        console.log('ES:', Object.keys(translationsES).length, 'clés');
        console.log('NL:', Object.keys(translationsNL).length, 'clés');
        console.log('IT:', Object.keys(translationsIT).length, 'clés');
        
        // Initialiser le système
        initLanguageSystem();
    } else if (retries < maxRetries) {
        console.log(`⏳ Attente des fichiers de langue... (${retries}/${maxRetries})`);
        setTimeout(waitForTranslations, 100);
    } else {
        console.error('❌ Timeout: impossible de charger les fichiers de langue');
        console.log('FR:', typeof translationsFR);
        console.log('EN:', typeof translationsEN);
        console.log('DE:', typeof translationsDE);
        console.log('ES:', typeof translationsES);
        console.log('NL:', typeof translationsNL);
        console.log('IT:', typeof translationsIT);
    }
}

// Système de gestion des langues
const LanguageSystemHTML = {
    currentLanguage: (() => {
        try {
            return localStorage.getItem('katikias_language') || 'fr';
        } catch (e) {
            console.warn('⚠️ localStorage non disponible:', e.message);
            return 'fr';
        }
    })(),
    
    // Récupérer une traduction
    get(key) {
        const lang = this.currentLanguage;
        const allTranslations = {
            'fr': typeof translationsFR !== 'undefined' ? translationsFR : {},
            'en': typeof translationsEN !== 'undefined' ? translationsEN : {},
            'de': typeof translationsDE !== 'undefined' ? translationsDE : {},
            'es': typeof translationsES !== 'undefined' ? translationsES : {},
            'nl': typeof translationsNL !== 'undefined' ? translationsNL : {},
            'it': typeof translationsIT !== 'undefined' ? translationsIT : {}
        };
        
        const translations = allTranslations[lang] || allTranslations['fr'];
        const result = translations[key] || key;
        return result;
    },
    
    // Définir la langue
    setLanguage(lang) {
        if (!['fr', 'en', 'de', 'es', 'nl', 'it'].includes(lang)) {
            console.error('❌ Langue inconnue:', lang);
            return;
        }
        
        this.currentLanguage = lang;
        
        // Sauvegarder dans localStorage si disponible
        try {
            localStorage.setItem('katikias_language', lang);
        } catch (e) {
            console.warn('⚠️ Impossible de sauvegarder dans localStorage:', e.message);
        }
        
        console.log(`✅ Langue changée en: ${lang}`);
        
        // Traduire toute la page
        this.translatePage();
    },
    
    /** Libellés des équipements (li) après traduction : met à jour alt des photos associées */
    syncRoomPhotoAlts() {
        document.querySelectorAll('.content ul li').forEach((li) => {
            const wrap = li.nextElementSibling;
            if (!wrap || !wrap.classList || !wrap.classList.contains('item-photo')) return;
            const label = li.textContent.trim();
            wrap.querySelectorAll('img').forEach((img) => {
                img.alt = label;
            });
        });
    },

    // Traduire la page entière
    translatePage() {
        console.log(`🌐 Traduction de la page en ${this.currentLanguage}`);
        
        // Trouver tous les éléments avec data-lang-key
        document.querySelectorAll('[data-lang-key]').forEach(element => {
            const key = element.getAttribute('data-lang-key');
            const translation = this.get(key);
            const optional = element.getAttribute('data-i18n-optional') === 'true';
            
            if (!translation || translation === key) {
                if (optional) return;
                console.warn(`⚠️ Clé non trouvée: ${key}`);
                return;
            }
            
            // Injecter la traduction (HTML autorisé pour les liens)
            element.innerHTML = translation;
        });
        
        // Mettre à jour l'attribut lang du document
        document.documentElement.lang = this.currentLanguage;

        if (typeof this.syncRoomPhotoAlts === 'function') {
            this.syncRoomPhotoAlts();
        }
    }
};

// Initialiser le système après le chargement du DOM
function initLanguageSystem() {
    // Rendre l'objet global
    window.LanguageSystemHTML = LanguageSystemHTML;
    
    // Traduire la page immédiatement
    LanguageSystemHTML.translatePage();
    
    console.log('✅ Système multilingue prêt');
}

// Démarrer l'attente des traductions
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', waitForTranslations);
} else {
    waitForTranslations();
}

// Forcer après 5 secondes
setTimeout(() => {
    if (typeof window.LanguageSystemHTML === 'undefined') {
        console.warn('⚠️ Timeout: initialisation forcée');
        initLanguageSystem();
    }
}, 5000);
