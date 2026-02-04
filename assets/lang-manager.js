// Gestionnaire de traductions multilingues avec validation
// Katikias 33 - Language Management System

/**
 * Système de gestion des traductions avec détection des clés manquantes
 */
const LanguageManager = {
    // Objet pour stocker toutes les traductions
    allLanguages: {
        'fr': {},
        'en': {},
        'de': {},
        'es': {}
    },

    // Langue actuelle
    currentLanguage: 'fr',
    
    /**
     * Initialiser avec les fichiers de langue chargés
     */
    loadLanguages: function() {
        console.log('🔄 Chargement des langues...');
        console.log('FR:', typeof translationsFR, Object.keys(translationsFR || {}).length, 'clés');
        console.log('EN:', typeof translationsEN, Object.keys(translationsEN || {}).length, 'clés');
        console.log('DE:', typeof translationsDE, Object.keys(translationsDE || {}).length, 'clés');
        console.log('ES:', typeof translationsES, Object.keys(translationsES || {}).length, 'clés');
        
        if (typeof translationsFR !== 'undefined') this.allLanguages['fr'] = translationsFR;
        if (typeof translationsEN !== 'undefined') this.allLanguages['en'] = translationsEN;
        if (typeof translationsDE !== 'undefined') this.allLanguages['de'] = translationsDE;
        if (typeof translationsES !== 'undefined') this.allLanguages['es'] = translationsES;
        
        console.log('✅ Langues chargées avec succès');
    },

    /**
     * Initialiser le système de langues
     */
    init: function() {
        const savedLang = this.getSavedLanguage();
        this.setLanguage(savedLang);
        console.log('✓ Système multilingue initialisé:', savedLang);
    },

    /**
     * Définir la langue active
     */
    setLanguage: function(lang) {
        if (this.allLanguages[lang]) {
            this.currentLanguage = lang;
            this.saveLanguage(lang);
            document.documentElement.lang = lang;
            this.translatePage();
            return true;
        }
        console.warn('⚠️ Langue non disponible:', lang);
        return false;
    },

    /**
     * Obtenir une clé de traduction
     */
    get: function(key) {
        const translations = this.allLanguages[this.currentLanguage];
        if (translations && translations[key]) {
            return translations[key];
        }
        
        // Fallback vers le français
        if (this.currentLanguage !== 'fr') {
            const frTranslations = this.allLanguages['fr'];
            if (frTranslations && frTranslations[key]) {
                console.warn(`⚠️ Clé manquante en ${this.currentLanguage}:`, key, '-> Fallback FR');
                return frTranslations[key];
            }
        }
        
        console.error('❌ Clé de traduction non trouvée:', key);
        return `[${key}]`;
    },

    /**
     * Traduire toute la page
     */
    translatePage: function() {
        document.querySelectorAll('[data-lang-key]').forEach(element => {
            const key = element.getAttribute('data-lang-key');
            const translation = this.get(key);
            element.textContent = translation;
        });
        
        document.querySelectorAll('img[data-lang-alt], img[data-lang-title]').forEach(img => {
            const altKey = img.getAttribute('data-lang-alt');
            const titleKey = img.getAttribute('data-lang-title');
            if (altKey) img.alt = this.get(altKey);
            if (titleKey) img.title = this.get(titleKey);
        });
    },

    /**
     * Sauvegarder la préférence de langue
     */
    saveLanguage: function(lang) {
        if (typeof Storage !== 'undefined') {
            localStorage.setItem('preferredLanguage', lang);
        }
    },

    /**
     * Récupérer la langue sauvegardée
     */
    getSavedLanguage: function() {
        if (typeof Storage !== 'undefined') {
            const saved = localStorage.getItem('preferredLanguage');
            if (saved && this.allLanguages[saved]) {
                return saved;
            }
        }
        
        // Détection basée sur le navigateur
        const browserLang = (navigator.language || navigator.userLanguage).split('-')[0].toLowerCase();
        return this.allLanguages[browserLang] ? browserLang : 'fr';
    },

    /**
     * Obtenir toutes les langues disponibles
     */
    getAvailableLanguages: function() {
        return Object.keys(this.allLanguages);
    },

    /**
     * Valider la complétude des traductions
     */
    validateTranslations: function() {
        console.log('\n🔍 VALIDATION DES TRADUCTIONS\n' + '='.repeat(50));
        
        const allKeys = {};
        
        // Collecter toutes les clés
        for (const lang in this.allLanguages) {
            const translations = this.allLanguages[lang];
            for (const key in translations) {
                if (!allKeys[key]) {
                    allKeys[key] = {};
                }
                allKeys[key][lang] = true;
            }
        }

        const totalKeys = Object.keys(allKeys).length;
        const languages = this.getAvailableLanguages();
        const report = {
            total: totalKeys,
            languages: {},
            missingByLanguage: {},
            missingKeys: []
        };

        // Analyser chaque langue
        languages.forEach(lang => {
            const translations = this.allLanguages[lang];
            const translatedKeys = Object.keys(translations);
            report.languages[lang] = {
                count: translatedKeys.length,
                percentage: Math.round((translatedKeys.length / totalKeys) * 100)
            };

            const missing = [];
            for (const key in allKeys) {
                if (!allKeys[key][lang]) {
                    missing.push(key);
                }
            }

            if (missing.length > 0) {
                report.missingByLanguage[lang] = missing;
            }
        });

        // Afficher le rapport
        console.log('📊 RÉSUMÉ PAR LANGUE:\n');
        languages.forEach(lang => {
            const stats = report.languages[lang];
            const emoji = stats.percentage === 100 ? '✅' : '⚠️';
            console.log(`${emoji} ${lang.toUpperCase()}: ${stats.count}/${totalKeys} (${stats.percentage}%)`);
        });

        // Afficher les clés manquantes
        if (Object.keys(report.missingByLanguage).length > 0) {
            console.log('\n⚠️ CLÉS MANQUANTES:\n');
            for (const lang in report.missingByLanguage) {
                console.log(`\n${lang}:`);
                report.missingByLanguage[lang].forEach(key => {
                    console.log(`  - ${key}`);
                });
            }
        } else {
            console.log('\n✅ TOUTES LES TRADUCTIONS SONT COMPLÈTES!');
        }

        console.log('\n' + '='.repeat(50) + '\n');
        return report;
    },

    /**
     * Exporter toutes les traductions en JSON
     */
    exportToJSON: function() {
        return JSON.stringify(this.allLanguages, null, 2);
    },

    /**
     * Importer des traductions depuis JSON
     */
    importFromJSON: function(jsonString) {
        try {
            const imported = JSON.parse(jsonString);
            for (const lang in imported) {
                if (this.allLanguages[lang]) {
                    Object.assign(this.allLanguages[lang], imported[lang]);
                }
            }
            console.log('✓ Traductions importées avec succès');
            return true;
        } catch (e) {
            console.error('❌ Erreur lors de l\'import:', e);
            return false;
        }
    },

    /**
     * Obtenir les statistiques de traduction
     */
    getStats: function() {
        const stats = {
            languages: {},
            total: 0,
            complete: false
        };

        for (const lang in this.allLanguages) {
            const count = Object.keys(this.allLanguages[lang]).length;
            stats.languages[lang] = count;
            if (!stats.total) {
                stats.total = count;
            }
        }

        stats.complete = Object.values(stats.languages).every(count => count === stats.total);
        return stats;
    },

    /**
     * Mettre à jour une traduction
     */
    updateTranslation: function(lang, key, value) {
        if (this.allLanguages[lang]) {
            this.allLanguages[lang][key] = value;
            return true;
        }
        return false;
    },

    /**
     * Récupérer une traduction pour édition
     */
    getTranslation: function(lang, key) {
        if (this.allLanguages[lang]) {
            return this.allLanguages[lang][key] || '';
        }
        return '';
    }
};

// Fonction legacy pour compatibilité avec l'ancien système
function changeLanguage(lang) {
    LanguageManager.setLanguage(lang);
}

// Fonction legacy pour compatibilité
function initLanguage() {
    LanguageManager.init();
}

// Initialiser au chargement
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        LanguageManager.init();
    });
} else {
    LanguageManager.init();
}
