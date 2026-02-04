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
        typeof translationsES !== 'undefined') {
        
        console.log('✅ Tous les fichiers de langue chargés');
        
        // Initialiser le système
        initLanguageSystem();
    } else if (retries < maxRetries) {
        console.log(`⏳ Attente des fichiers de langue... (${retries}/${maxRetries})`);
        setTimeout(waitForTranslations, 100);
    } else {
        console.error('❌ Timeout: impossible de charger les fichiers de langue');
    }
}

// Système de gestion des langues
const LanguageSystemHTML = {
    currentLanguage: localStorage.getItem('katikias_language') || 'fr',
    
    // Récupérer une traduction
    get(key) {
        const lang = this.currentLanguage;
        const allTranslations = {
            'fr': translationsFR,
            'en': translationsEN,
            'de': translationsDE,
            'es': translationsES
        };
        
        const translations = allTranslations[lang] || allTranslations['fr'];
        return translations[key] || translations[key] || key;
    },
    
    // Définir la langue
    setLanguage(lang) {
        if (!['fr', 'en', 'de', 'es'].includes(lang)) {
            console.error('❌ Langue inconnue:', lang);
            return;
        }
        
        this.currentLanguage = lang;
        localStorage.setItem('katikias_language', lang);
        console.log(`✅ Langue changée en: ${lang}`);
        
        // Traduire toute la page
        this.translatePage();
    },
    
    // Traduire la page entière
    translatePage() {
        console.log(`🌐 Traduction de la page en ${this.currentLanguage}`);
        
        // Trouver tous les éléments avec data-lang-key
        document.querySelectorAll('[data-lang-key]').forEach(element => {
            const key = element.getAttribute('data-lang-key');
            const translation = this.get(key);
            
            if (!translation || translation === key) {
                console.warn(`⚠️ Clé non trouvée: ${key}`);
                return;
            }
            
            // Nettoyer le contenu précédent
            element.innerHTML = '';
            
            // Ajouter le texte traduit
            element.appendChild(document.createTextNode(translation));
        });
        
        // Mettre à jour l'attribut lang du document
        document.documentElement.lang = this.currentLanguage;
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
    if (typeof translationsFR === 'undefined') {
        console.warn('⚠️ Timeout: initialisation forcée même sans tous les fichiers');
        if (typeof LanguageSystemHTML !== 'undefined') {
            initLanguageSystem();
        }
    }
}, 5000);
