#!/usr/bin/env python3
"""
Corriger le script changeLanguage pour vérifier la disponibilité
"""

import os

base_dir = os.path.dirname(os.path.abspath(__file__))

html_files = []
for file in os.listdir(base_dir):
    if file.endswith('.html') and file not in ['test-multilang.html', 'index_multilangue.html']:
        html_files.append(os.path.join(base_dir, file))

new_script = '''    <script>
        // Fonction pour changer la langue
        function changeLanguage(lang) {
            console.log('📢 changeLanguage appelé avec:', lang);
            
            if (typeof LanguageSystemHTML === 'undefined') {
                console.error('❌ LanguageSystemHTML non défini, attente...');
                // Réessayer après 500ms
                setTimeout(() => changeLanguage(lang), 500);
                return;
            }
            
            console.log('✅ LanguageSystemHTML trouvé');
            LanguageSystemHTML.setLanguage(lang);
            
            // Mettre à jour le sélecteur
            const selector = document.getElementById('langSelector');
            if (selector) {
                selector.value = lang;
                console.log('✅ Sélecteur mis à jour');
            }
        }
        
        // Au chargement, définir la langue du sélecteur
        document.addEventListener('DOMContentLoaded', () => {
            console.log('📋 DOMContentLoaded triggered');
            
            // Attendre que LanguageSystemHTML soit disponible
            let waits = 0;
            const checkReady = setInterval(() => {
                waits++;
                if (typeof LanguageSystemHTML !== 'undefined') {
                    clearInterval(checkReady);
                    const selector = document.getElementById('langSelector');
                    if (selector) {
                        selector.value = LanguageSystemHTML.currentLanguage;
                        console.log('✅ Sélecteur initialisé avec:', LanguageSystemHTML.currentLanguage);
                    }
                } else if (waits > 50) {
                    clearInterval(checkReady);
                    console.warn('⚠️ LanguageSystemHTML non disponible après 5s');
                }
            }, 100);
        });
    </script>'''

for html_file in html_files:
    print(f"🔄 {os.path.basename(html_file)}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver et remplacer le script changeLanguage
    if 'function changeLanguage(lang)' in content:
        # Trouver le début et la fin du script
        start = content.find('    <script>\n        // Fonction pour changer la langue')
        if start > 0:
            # Trouver la fin (</script>)
            end = content.find('    </script>', start) + len('    </script>')
            
            # Remplacer
            new_content = content[:start] + new_script + content[end:]
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("   ✅ Script mis à jour")
        else:
            print("   ⚠️ Script non trouvé")
    else:
        print("   ⚠️ changeLanguage non trouvé")

print("\n✅ Tous les scripts ont été mis à jour!")
