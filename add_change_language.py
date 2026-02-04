#!/usr/bin/env python3
"""
Ajouter la fonction changeLanguage à tous les fichiers HTML
"""

import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))

html_files = []
for file in os.listdir(base_dir):
    if file.endswith('.html') and file not in ['test-multilang.html', 'index_multilangue.html']:
        html_files.append(os.path.join(base_dir, file))

change_language_script = '''    <script>
        // Fonction pour changer la langue
        function changeLanguage(lang) {
            if (typeof LanguageSystemHTML !== 'undefined') {
                LanguageSystemHTML.setLanguage(lang);
                // Mettre à jour le sélecteur
                const selector = document.getElementById('langSelector');
                if (selector) selector.value = lang;
            } else {
                console.error('❌ LanguageSystemHTML non disponible');
            }
        }
        
        // Au chargement, définir la langue du sélecteur
        document.addEventListener('DOMContentLoaded', () => {
            if (typeof LanguageSystemHTML !== 'undefined') {
                const selector = document.getElementById('langSelector');
                if (selector) selector.value = LanguageSystemHTML.currentLanguage;
            }
        });
    </script>'''

for html_file in html_files:
    print(f"\n🔄 {os.path.basename(html_file)}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si c'est déjà fait
    if 'function changeLanguage(lang)' in content:
        print("   ✅ Déjà à jour")
        continue
    
    # Ajouter le script avant </body>
    if '</body>' in content:
        # Insérer avant </body>
        content = content.replace('    </body>', change_language_script + '\n    </body>', 1)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Script ajouté")
    else:
        print("   ⚠️ Balise </body> non trouvée")

print("\n✅ Toutes les pages ont changeLanguage!")
