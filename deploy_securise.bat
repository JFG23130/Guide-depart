@echo off
REM ========================================================================
REM 🛡️ DÉPLOIEMENT SÉCURISÉ - GITHUB PAGES
REM ========================================================================
REM
REM Ce script déploie SEULEMENT les fichiers sûrs sur GitHub Pages.
REM Les données sensibles (WiFi, Portail, Airbnb codes) sont PROTÉGÉES.
REM
REM Sécurité:
REM  ✅ assets/codes-config-private.js - IGNORÉ (.gitignore)
REM  ✅ reservations_final.csv - IGNORÉ (.gitignore)
REM  ✅ Aucun code WiFi/Portail déployé
REM  ✅ Aucun code Airbnb déployé
REM
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo 🛡️ DÉPLOIEMENT SÉCURISÉ - KATIKIAS 33
echo ========================================================================
echo.

REM Vérifications de sécurité
echo 🔍 VÉRIFICATIONS DE SÉCURITÉ...
echo.

REM 1. Vérifier .gitignore
if not exist .gitignore (
    echo ❌ ERREUR: .gitignore manquant!
    echo    Créez .gitignore avant de déployer.
    pause
    exit /b 1
)

REM 2. Vérifier que les fichiers sensibles ne sont pas staged
git status -s > temp_status.txt

REM Chercher les fichiers dangereux
findstr /i "private" temp_status.txt >nul
if %ERRORLEVEL% EQU 0 (
    echo ❌ ERREUR: Fichiers sensibles détectés en staging!
    echo.
    echo Exécutez:
    echo   git reset HEAD assets/codes-config-private.js
    echo.
    del temp_status.txt
    pause
    exit /b 1
)

findstr /i "reservations_final" temp_status.txt >nul
if %ERRORLEVEL% EQU 0 (
    echo ❌ ERREUR: reservations_final.csv détecté en staging!
    echo.
    echo Vérifiez .gitignore:
    echo   assets/codes-config-private.js
    echo   KatikiasDeployer_v5/reservations_final.csv
    echo.
    del temp_status.txt
    pause
    exit /b 1
)

del temp_status.txt

echo ✅ Vérifications de sécurité réussies
echo.

REM 3. Lister les fichiers qui vont être déployés
echo 📦 FICHIERS À DÉPLOYER:
echo.
echo   ✅ access_codes.json
echo   ✅ access_codes.js
echo   ✅ codes_invites.md
echo   ✅ assets/codes-config-generated.js (VERSION SÛRE)
echo.
echo 🔒 FICHIERS PROTÉGÉS (NON DÉPLOYÉS):
echo.
echo   🛡️  assets/codes-config-private.js (codes WiFi/Portail)
echo   🛡️  KatikiasDeployer_v5/reservations_final.csv (données Airbnb)
echo.

REM 4. Demander confirmation
set /p CONFIRM="Continuer le déploiement? (o/n): "

if /i NOT "%CONFIRM%"=="o" (
    echo.
    echo ⛔ Déploiement annulé.
    pause
    exit /b 0
)

echo.
echo 📝 AJOUT DES FICHIERS...
git add access_codes.json access_codes.js codes_invites.md assets/codes-config-generated.js

if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERREUR lors de git add
    pause
    exit /b 1
)

echo ✅ Fichiers ajoutés au staging
echo.

REM 5. Message de commit
echo 💬 MESSAGE DE COMMIT:
echo.

set /p COMMIT_MSG="Entrez le message de commit (par défaut: '🔐 Déploiement codes'): "

if "!COMMIT_MSG!"=="" (
    set COMMIT_MSG=🔐 Déploiement codes sécurisé
)

echo.
echo 📤 COMMIT...
git commit -m "!COMMIT_MSG!"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERREUR lors du commit
    pause
    exit /b 1
)

echo ✅ Commit réussi
echo.

REM 6. Push
echo 📤 PUSH VERS GITHUB...
git push origin main

if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERREUR lors du push
    echo.
    echo Vérifiez:
    echo   - Votre connexion Internet
    echo   - Vos credentials Git
    echo   - La branche remote: git remote -v
    echo.
    pause
    exit /b 1
)

echo ✅ Push réussi!
echo.

REM 7. Confirmation finale
echo ========================================================================
echo ✅ DÉPLOIEMENT SÉCURISÉ TERMINÉ!
echo ========================================================================
echo.
echo 🌐 Votre site est maintenant en ligne!
echo.
echo 📍 URL du site:
echo    https://jfg23130.github.io/Guide-depart/
echo.
echo 🧪 Test d'accès (copier-coller dans le navigateur):
echo    https://jfg23130.github.io/Guide-depart/hub.html?code=KATI-5LXUWKQ
echo.
echo 🛡️  Sécurité:
echo    ✅ Codes d'accès déployés (pour les invités)
echo    ✅ Codes WiFi/Portail PROTÉGÉS (.gitignore)
echo    ✅ Données Airbnb PROTÉGÉES (.gitignore)
echo.
echo 📋 Prochaines étapes:
echo    1. Envoyer les codes aux invités (depuis codes_invites.md)
echo    2. Tester l'interface avec un code réel
echo    3. Vérifier les stats (Google Analytics)
echo.

pause
exit /b 0
