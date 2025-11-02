@echo off
chcp 65001 >nul
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║     🚀 DEPLOIEMENT GUIDE KATIKIAS 33 SUR GITHUB PAGES        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/4] 📦 Vérification de l'état Git...
git status --short
echo.

echo [2/4] ➕ Ajout des fichiers modifiés...
git add .
echo ✅ Fichiers ajoutés
echo.

echo [3/4] 💾 Création du commit...
git commit -m "📝 Mise à jour guide Katikias 33 - %date% %time%" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Aucun changement à commiter
) else (
    echo ✅ Commit créé
)
echo.

echo [4/4] ☁️  Envoi sur GitHub Pages...
git push origin main
if %errorlevel% equ 0 (
    echo ✅ Déploiement réussi !
) else (
    echo ❌ Erreur lors du push
    echo.
    echo 💡 Essayez de faire un pull d'abord :
    echo    git pull origin main
    pause
    exit /b 1
)
echo.

echo ════════════════════════════════════════════════════════════════
echo                    ✅ DÉPLOIEMENT TERMINÉ !
echo ════════════════════════════════════════════════════════════════
echo.
echo 🌐 Site disponible sur :
echo    https://jfg23130.github.io/Guide-depart/
echo.
echo ⏱️  Les modifications seront visibles dans 1-2 minutes
echo 💡 Videz le cache si besoin : Ctrl + F5
echo.
echo 📱 QR Codes à mettre à jour :
echo    - Menu Principal : https://jfg23130.github.io/Guide-depart/
echo    - Guide Pratique : https://jfg23130.github.io/Guide-depart/tips_and_tricks.html
echo    - Équipements    : https://jfg23130.github.io/Guide-depart/apartment_guide.html
echo    - Résidence      : https://jfg23130.github.io/Guide-depart/residence.html
echo    - Départ         : https://jfg23130.github.io/Guide-depart/departure_procedure.html
echo.
echo ════════════════════════════════════════════════════════════════

timeout /t 5 >nul

