@echo off
chcp 65001 >nul
color 0A
setlocal

set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "DESKTOP_CSV=%USERPROFILE%\OneDrive\Bureau\reservations_final.csv"
set "TARGET_CSV=%ROOT%KatikiasDeployer_v5\reservations_final.csv"

echo ╔══════════════════════════════════════════════════════════════╗
echo ║        🔐 WORKFLOW SÉCURISÉ - KATIKIAS 33                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/5] 📁 Export Airbnb
echo Placez reservations_final.csv sur le Bureau (OneDrive) OU dans KatikiasDeployer_v5
start "" "%USERPROFILE%\OneDrive\Bureau"
start "" "%ROOT%KatikiasDeployer_v5"
echo.
pause

if exist "%DESKTOP_CSV%" (
    copy /Y "%DESKTOP_CSV%" "%TARGET_CSV%" >nul
    echo ✅ Fichier CSV copié depuis le Bureau
) else if exist "%TARGET_CSV%" (
    echo ✅ Fichier CSV trouvé dans KatikiasDeployer_v5
) else (
    echo ❌ reservations_final.csv introuvable.
    echo Déposez-le sur le Bureau ou dans KatikiasDeployer_v5, puis relancez.
    pause
    exit /b 1
)

echo [2/5] 🔄 Génération des codes
"%PY%" "%ROOT%generate_all_codes.py"
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de la génération.
    pause
    exit /b 1
)
echo ✅ Codes générés
echo.

echo [3/5] 📨 Envoi aux invités
echo Ouverture de codes_invites.md
start "" "%ROOT%codes_invites.md"
echo.
pause

echo [4/5] 🔎 Vérification sécurité Git
cd /d "%ROOT%"

git ls-files --error-unmatch assets/codes-config-private.js >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ ERREUR: assets/codes-config-private.js est suivi par Git.
    echo Supprimez-le du suivi et relancez.
    pause
    exit /b 1
)

git ls-files --error-unmatch KatikiasDeployer_v5/reservations_final.csv >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ ERREUR: reservations_final.csv est suivi par Git.
    echo Supprimez-le du suivi et relancez.
    pause
    exit /b 1
)

git status --short | findstr /v "^??" | findstr /i "codes-config-private.js reservations_final.csv" >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ ERREUR: un fichier sensible est en cours de commit.
    echo Vérifiez git status et relancez.
    pause
    exit /b 1
)

echo ✅ Aucun fichier sensible suivi
echo.

echo [5/5] ☁️ Déploiement GitHub Pages (fichiers publics seulement)
git add index.html apartment_guide.html residence.html proximity.html departure_procedure.html tips_and_tricks.html emergencies.html
git add chambre.html cuisine.html salle_deau.html salle_manger.html salon.html terrasse.html wc.html placard_bleu.html codes-acces.html
git add access_codes.json access_codes.js codes_invites.md
git add assets\lang-*.js assets\init-translations.js assets\lang-manager.js assets\codes-config-generated.js assets\guard-access.js
git add images\* pdfs\* _headers CNAME >nul 2>&1

git status --short
echo.
git commit -m "🔐 Mise à jour sécurisée - %date% %time%" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Aucun changement à commiter
) else (
    echo ✅ Commit créé
)

git push origin main
if %errorlevel% neq 0 (
    echo ❌ Erreur lors du push
    pause
    exit /b 1
)

echo.
echo ✅ Déploiement réussi
echo 🌐 https://jfg23130.github.io/Guide-depart/
echo.
pause
endlocal
