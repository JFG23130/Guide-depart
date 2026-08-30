@echo off
chcp 65001 >nul
color 0A
setlocal

set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" --version >nul 2>&1
if errorlevel 1 set "PY=python"
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set "DESKTOP_CSV=%USERPROFILE%\OneDrive\Bureau\reservations.csv"
set "DESKTOP_CSV_FINAL=%USERPROFILE%\OneDrive\Bureau\reservations_final.csv"
set "DESKTOP_WORKFLOW=%USERPROFILE%\OneDrive\Bureau\Katikias_Workflow.bat"
set "GUIDE_CSV=%USERPROFILE%\OneDrive\Documents\JFG\Appartement Katikias\Guide\reservations.csv"
set "TARGET_CSV=%ROOT%reservations.csv"

echo ╔══════════════════════════════════════════════════════════════╗
echo ║        🔐 WORKFLOW SÉCURISÉ - KATIKIAS 33                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/5] 📁 Export Airbnb
echo Placez reservations.csv uniquement dans "%GUIDE_CSV%"
start "" "%USERPROFILE%\OneDrive\Documents\JFG\Appartement Katikias"
start "" "%USERPROFILE%\OneDrive\Documents\JFG\Appartement Katikias\Guide"
echo.
pause

if exist "%GUIDE_CSV%" (
    copy /Y "%GUIDE_CSV%" "%TARGET_CSV%" >nul
    echo ✅ Fichier CSV copié depuis le dossier Guide
) else if exist "%TARGET_CSV%" (
    echo ✅ Fichier CSV trouvé dans le dossier du guide
) else (
    echo ❌ reservations.csv introuvable.
    echo Déposez-le dans le dossier Guide, puis relancez.
    pause
    exit /b 1
)

if exist "%DESKTOP_CSV%" del /Q "%DESKTOP_CSV%" >nul 2>&1
if exist "%DESKTOP_CSV_FINAL%" del /Q "%DESKTOP_CSV_FINAL%" >nul 2>&1
if exist "%DESKTOP_WORKFLOW%" del /Q "%DESKTOP_WORKFLOW%" >nul 2>&1

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

echo [4/5] 🔎 Vérification sécurité Git
cd /d "%ROOT%"

git ls-files --error-unmatch assets/codes-config-private.js >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ ERREUR: assets/codes-config-private.js est suivi par Git.
    echo Supprimez-le du suivi et relancez.
    pause
    exit /b 1
)

git ls-files --error-unmatch reservations.csv >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ ERREUR: reservations.csv est suivi par Git.
    echo Supprimez-le du suivi et relancez.
    pause
    exit /b 1
)

git status --short | findstr /v "^??" | findstr /i "codes-config-private.js reservations.csv" >nul 2>&1
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
git add assets\lang-*.js assets\init-translations.js assets\lang-manager.js assets\codes-config-generated.js assets\guard-access.js assets\load-guide-captions.js assets\guide-content.json
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
endlocal
