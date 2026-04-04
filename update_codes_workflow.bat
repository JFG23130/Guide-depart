@echo off
REM ========================================================================
REM 🔄 WORKFLOW AUTOMATISÉ - MISE À JOUR DES CODES INVITÉS
REM ========================================================================
REM
REM Ce script:
REM 1. Génère les codes d'accès depuis reservations_final.csv
REM 2. Valide la cohérence du système
REM 3. Propose de déployer sur GitHub Pages
REM
REM Prérequis:
REM - Python 3.x installé
REM - Git configuré
REM - reservations_final.csv à jour dans ..\KatikiasDeployer_v5\ (racine du dépôt Git)
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo 🔄 WORKFLOW AUTOMATISÉ KATIKIAS 33
echo ========================================================================
echo.

REM Couleurs Windows (limitées)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM ========================================================================
REM ÉTAPE 1: Génération des codes
REM ========================================================================

echo %BLUE%[1/4] Génération des codes d'accès...%NC%
echo.

python generate_all_codes.py
if %ERRORLEVEL% NEQ 0 (
    echo %RED%❌ ERREUR: La génération des codes a échoué%NC%
    echo.
    echo Vérifiez que:
    echo   - Python est installé
    echo   - reservations_final.csv existe dans le dossier KatikiasDeployer_v5 à la racine du dépôt
    echo   - Le format du CSV est correct
    echo.
    pause
    exit /b 1
)

echo.
echo %GREEN%✅ Codes générés avec succès%NC%
echo.

REM ========================================================================
REM ÉTAPE 2: Validation
REM ========================================================================

echo %BLUE%[2/4] Validation du système...%NC%
echo.

python validate_system_final.py
if %ERRORLEVEL% NEQ 0 (
    echo %RED%❌ ERREUR: La validation a échoué%NC%
    echo.
    echo Des incohérences ont été détectées.
    echo Relancez la génération: python generate_all_codes.py
    echo.
    pause
    exit /b 1
)

echo.
echo %GREEN%✅ Système validé%NC%
echo.

REM ========================================================================
REM ÉTAPE 3: Affichage du résumé
REM ========================================================================

echo %BLUE%[3/4] Résumé des fichiers générés...%NC%
echo.

if exist access_codes.json (
    echo %GREEN%✅%NC% access_codes.json
) else (
    echo %RED%❌%NC% access_codes.json manquant
)

if exist access_codes.js (
    echo %GREEN%✅%NC% access_codes.js
) else (
    echo %RED%❌%NC% access_codes.js manquant
)

if exist codes_invites.md (
    echo %GREEN%✅%NC% codes_invites.md
) else (
    echo %RED%❌%NC% codes_invites.md manquant
)

if exist assets\codes-config-generated.js (
    echo %GREEN%✅%NC% assets\codes-config-generated.js
) else (
    echo %RED%❌%NC% assets\codes-config-generated.js manquant
)

echo.

REM ========================================================================
REM ÉTAPE 4: Déploiement (optionnel)
REM ========================================================================

echo %BLUE%[4/4] Déploiement sur GitHub Pages...%NC%
echo.

:deploy_choice
set /p DEPLOY="Voulez-vous déployer sur GitHub Pages? (o/n): "

if /i "%DEPLOY%"=="o" (
    echo.
    echo %YELLOW%Ajout des fichiers à Git...%NC%
    git add access_codes.json access_codes.js codes_invites.md assets\codes-config-generated.js
    
    if %ERRORLEVEL% NEQ 0 (
        echo %RED%❌ ERREUR: git add a échoué%NC%
        pause
        exit /b 1
    )
    
    echo.
    set /p COMMIT_MSG="Message de commit (défaut: 'Mise à jour codes invités'): "
    if "!COMMIT_MSG!"=="" set "COMMIT_MSG=🔄 Mise à jour codes invités"
    
    echo.
    echo %YELLOW%Commit...%NC%
    git commit -m "!COMMIT_MSG!"
    
    if %ERRORLEVEL% NEQ 0 (
        echo %YELLOW%⚠️  Aucun changement à commiter (ou erreur)%NC%
    ) else (
        echo.
        echo %YELLOW%Push vers GitHub...%NC%
        git push
        
        if %ERRORLEVEL% NEQ 0 (
            echo %RED%❌ ERREUR: git push a échoué%NC%
            echo.
            echo Vérifiez votre connexion et vos credentials Git
            pause
            exit /b 1
        )
        
        echo.
        echo %GREEN%✅ Déployé avec succès sur GitHub Pages!%NC%
    )
    
) else if /i "%DEPLOY%"=="n" (
    echo.
    echo %YELLOW%⚠️  Déploiement ignoré%NC%
    echo.
    echo Pour déployer manuellement plus tard:
    echo   git add access_codes.* codes_invites.md assets\codes-config-generated.js
    echo   git commit -m "🔄 Mise à jour codes invités"
    echo   git push
    
) else (
    echo %RED%Réponse invalide. Veuillez répondre 'o' ou 'n'%NC%
    goto deploy_choice
)

echo.
echo ========================================================================
echo ✅ WORKFLOW TERMINÉ AVEC SUCCÈS!
echo ========================================================================
echo.
echo Prochaines étapes:
echo   1. Vérifier codes_invites.md pour les codes générés
echo   2. Tester l'interface: hub.html?code=KATI-XXXXXXX
echo   3. Envoyer les codes aux invités par email
echo.

pause
exit /b 0
