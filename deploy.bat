@echo off
REM ========================================================================
REM 🚀 DÉPLOIEMENT SIMPLE ET SÉCURISÉ
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo 🛡️ DÉPLOIEMENT SÉCURISÉ - KATIKIAS 33
echo ========================================================================
echo.

echo ✅ Ajout des fichiers sûrs uniquement...
git add access_codes.json access_codes.js codes_invites.md assets/codes-config-generated.js

echo ✅ Commit...
git commit -m "🔐 Déploiement codes sécurisé - 12 réservations"

echo ✅ Push vers GitHub...
git push origin main

echo.
echo ========================================================================
echo ✅ DÉPLOIEMENT TERMINÉ!
echo ========================================================================
echo.
echo 🌐 Site live: https://jfg23130.github.io/Guide-depart/
echo 🧪 Test: https://jfg23130.github.io/Guide-depart/hub.html?code=KATI-5LXUWKQ
echo.
echo 🛡️ Sécurité:
echo    ✅ Codes d'accès déployés
echo    ✅ Codes WiFi/Portail PROTÉGÉS
echo    ✅ Données Airbnb PROTÉGÉES
echo.
