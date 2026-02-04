#!/usr/bin/env python3
"""
Ajouter correctement le script changeLanguage à tous les fichiers HTML
"""

import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))

html_files = []
for file in os.listdir(base_dir):
    if file.endswith('.html') and file not in ['test-multilang.html', 'index_multilangue.html']:
        html_files.append(os.path.join(base_dir, file))

for html_file in html_files:
    filename = os.path.basename(html_file)
    print(f"🔄 {filename}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le script est déjà là
    if 'function changeLanguage(lang)' in content:
        print("   ✅ Déjà à jour")
        continue
    
    # Trouver les scripts de langues
    if 'assets/lang-fr.js' not in content:
        print("   ⚠️ Scripts de langue non trouvés")
        continue
    
    # Remplacer le bloc des scripts
    old_scripts = '''    <script src="assets/lang-fr.js"></script>
    <script src="assets/lang-en.js"></script>
    <script src="assets/lang-de.js"></script>
    <script src="assets/lang-es.js"></script>
    <script src="assets/init-translations.js"></script>
</body>'''
    
    new_scripts = '''    <script src="assets/lang-fr.js"></script>
    <script src="assets/lang-en.js"></script>
    <script src="assets/lang-de.js"></script>
    <script src="assets/lang-es.js"></script>
    <script src="assets/init-translations.js"></script>
    <script>
        function changeLanguage(lang) {
            console.log('📢 changeLanguage appelé avec:', lang);
            if (typeof LanguageSystemHTML === 'undefined') {
                console.error('❌ LanguageSystemHTML non défini');
                setTimeout(() => changeLanguage(lang), 500);
                return;
            }
            LanguageSystemHTML.setLanguage(lang);
            const sel = document.getElementById('langSelector');
            if (sel) sel.value = lang;
        }
        document.addEventListener('DOMContentLoaded', () => {
            let w = 0;
            const c = setInterval(() => {
                if (typeof LanguageSystemHTML !== 'undefined') {
                    clearInterval(c);
                    const sel = document.getElementById('langSelector');
                    if (sel) sel.value = LanguageSystemHTML.currentLanguage;
                } else if (++w > 50) clearInterval(c);
            }, 100);
        });
    </script>
</body>'''
    
    if old_scripts in content:
        content = content.replace(old_scripts, new_scripts)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Script ajouté")
    else:
        print("   ⚠️ Remplacement échoué")

print("\n✅ Terminé!")
