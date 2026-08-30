#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VALIDATION DU SYSTÈME DE CODES D'ACCÈS UNIFIÉ
Vérifie que tous les fichiers sont cohérents et fonctionnels
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Set

def _get_downloads_dir() -> Path:
    candidates: List[Path] = []

    if sys.platform == "win32":
        try:
            import winreg

            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            value_name = "{374DE290-123F-4565-9164-39C4925E467B}"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                raw, _ = winreg.QueryValueEx(key, value_name)
                candidates.append(Path(os.path.expandvars(raw)))
        except OSError:
            pass

    candidates.append(Path.home() / "Downloads")
    candidates.append(Path(r"K:\Downloads"))

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent
DOWNLOADS_DIR = _get_downloads_dir()
CSV_FILE = DOWNLOADS_DIR / "reservations_final.csv"
ACCESS_JSON = PROJECT_ROOT / "access_codes.json"
ACCESS_JS = PROJECT_ROOT / "access_codes.js"
CODES_MD = PROJECT_ROOT / "codes_invites.md"
CONFIG_JS = PROJECT_ROOT / "assets" / "codes-config-generated.js"

# Codes d'accès acceptés :
# - KATI-XXXXXXX (ancien format dédié)
# - Code de réservation Airbnb typique : 2 lettres + 8 alphanum (ex. HM39DMKK8A)
RE_CODE_KATI = re.compile(r"^KATI-[A-Z0-9]{7}$")
RE_CODE_AIRBNB_RESA = re.compile(r"^[A-Z]{2}[A-Z0-9]{8}$")
RE_CODE_IN_BACKTICKS = re.compile(
    r"`((?:KATI-[A-Z0-9]{7}|[A-Z]{2}[A-Z0-9]{8}))`"
)
RE_CODE_CONFIG_KEY = re.compile(
    r"'((?:KATI-[A-Z0-9]{7}|[A-Z]{2}[A-Z0-9]{8}))':\s*\{"
)


def _is_known_code_format(code: str) -> bool:
    return bool(RE_CODE_KATI.match(code) or RE_CODE_AIRBNB_RESA.match(code))


class Colors:
    """Couleurs ANSI pour terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_section(title: str) -> None:
    """Affiche un titre de section"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_success(message: str) -> None:
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message: str) -> None:
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message: str) -> None:
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def print_info(message: str) -> None:
    """Affiche une information"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")


def check_csv_exists() -> bool:
    """Vérifie que le CSV source existe"""
    if CSV_FILE.exists():
        print_success(f"CSV source trouvé: {CSV_FILE.name}")
        return True
    else:
        print_error(f"CSV source introuvable: {CSV_FILE}")
        return False


def check_generated_files() -> Dict[str, bool]:
    """Vérifie que tous les fichiers générés existent"""
    files = {
        "access_codes.json": ACCESS_JSON,
        "access_codes.js": ACCESS_JS,
        "codes_invites.md": CODES_MD,
        "codes-config-generated.js": CONFIG_JS,
    }
    
    results = {}
    for name, path in files.items():
        if path.exists():
            print_success(f"{name} existe")
            results[name] = True
        else:
            print_error(f"{name} manquant: {path}")
            results[name] = False
    
    return results


def validate_access_json() -> Set[str]:
    """Valide access_codes.json et retourne les codes"""
    codes = set()
    
    if not ACCESS_JSON.exists():
        print_error("access_codes.json manquant")
        return codes
    
    try:
        with ACCESS_JSON.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print_error("access_codes.json: doit être un tableau")
            return codes
        
        for item in data:
            if not isinstance(item, dict):
                print_error(f"access_codes.json: entrée invalide: {item}")
                continue
            
            if "code" not in item or "guest" not in item:
                print_error(f"access_codes.json: clés manquantes dans {item}")
                continue
            
            code = item["code"]
            if not _is_known_code_format(code):
                print_warning(f"Format de code inhabituel: {code}")
            
            codes.add(code)
        
        print_success(f"access_codes.json: {len(codes)} codes valides")
        
    except json.JSONDecodeError as e:
        print_error(f"access_codes.json: JSON invalide: {e}")
    except Exception as e:
        print_error(f"access_codes.json: erreur: {e}")
    
    return codes


def validate_access_js() -> Set[str]:
    """Valide access_codes.js et retourne les codes"""
    codes = set()
    
    if not ACCESS_JS.exists():
        print_error("access_codes.js manquant")
        return codes
    
    try:
        with ACCESS_JS.open("r", encoding="utf-8") as f:
            content = f.read()
        
        # Extraire window.__ACCESS_CODES__
        match = re.search(r'window\.__ACCESS_CODES__\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if not match:
            print_error("access_codes.js: window.__ACCESS_CODES__ introuvable")
            return codes
        
        json_str = match.group(1)
        data = json.loads(json_str)
        
        if not isinstance(data, list):
            print_error("access_codes.js: __ACCESS_CODES__ doit être un tableau")
            return codes
        
        for item in data:
            if "code" not in item or "guest" not in item:
                print_error(f"access_codes.js: clés manquantes dans {item}")
                continue
            
            codes.add(item["code"])
        
        print_success(f"access_codes.js: {len(codes)} codes valides")
        
    except json.JSONDecodeError as e:
        print_error(f"access_codes.js: JSON invalide: {e}")
    except Exception as e:
        print_error(f"access_codes.js: erreur: {e}")
    
    return codes


def validate_codes_md() -> Set[str]:
    """Valide codes_invites.md et retourne les codes"""
    codes = set()
    
    if not CODES_MD.exists():
        print_error("codes_invites.md manquant")
        return codes
    
    try:
        with CODES_MD.open("r", encoding="utf-8") as f:
            content = f.read()
        
        # Codes entre backticks (table + éventuels exemples KATI- ou HMxxxxxxxx)
        codes = set(RE_CODE_IN_BACKTICKS.findall(content))
        
        if codes:
            print_success(f"codes_invites.md: {len(codes)} codes trouvés")
        else:
            print_warning("codes_invites.md: aucun code trouvé")
        
    except Exception as e:
        print_error(f"codes_invites.md: erreur: {e}")
    
    return codes


def validate_config_js() -> Set[str]:
    """Valide assets/codes-config-generated.js et retourne les codes"""
    codes = set()
    
    if not CONFIG_JS.exists():
        print_error("codes-config-generated.js manquant")
        return codes
    
    try:
        with CONFIG_JS.open("r", encoding="utf-8") as f:
            content = f.read()
        
        codes = set(RE_CODE_CONFIG_KEY.findall(content))
        
        print_success(f"codes-config-generated.js: {len(codes)} codes valides")
        
    except Exception as e:
        print_error(f"codes-config-generated.js: erreur: {e}")
    
    return codes


def check_consistency(json_codes: Set[str], js_codes: Set[str], md_codes: Set[str], config_codes: Set[str]) -> bool:
    """Vérifie la cohérence entre tous les fichiers"""
    all_consistent = True
    
    # Vérifier JSON vs JS
    if json_codes != js_codes:
        print_error("Incohérence entre access_codes.json et access_codes.js")
        print_info(f"   JSON only: {json_codes - js_codes}")
        print_info(f"   JS only: {js_codes - json_codes}")
        all_consistent = False
    else:
        print_success("access_codes.json et access_codes.js sont cohérents")
    
    # Vérifier JSON vs MD
    if json_codes != md_codes:
        print_error("Incohérence entre access_codes.json et codes_invites.md")
        print_info(f"   JSON only: {json_codes - md_codes}")
        print_info(f"   MD only: {md_codes - json_codes}")
        all_consistent = False
    else:
        print_success("access_codes.json et codes_invites.md sont cohérents")
    
    # Vérifier JSON vs Config
    if json_codes != config_codes:
        print_error("Incohérence entre access_codes.json et codes-config-generated.js")
        print_info(f"   JSON only: {json_codes - config_codes}")
        print_info(f"   Config only: {config_codes - json_codes}")
        all_consistent = False
    else:
        print_success("access_codes.json et codes-config-generated.js sont cohérents")
    
    return all_consistent


def check_expiration(config_codes: Set[str]) -> None:
    """Vérifie les dates d'expiration"""
    if not CONFIG_JS.exists():
        return
    
    try:
        with CONFIG_JS.open("r", encoding="utf-8") as f:
            content = f.read()
        
        today = date.today()
        expired_codes = []
        future_codes = []
        
        # Extraire les dates d'expiration
        for code in config_codes:
            match = re.search(rf"'{code}':\s*\{{\s*expires:\s*'(\d{{4}}-\d{{2}}-\d{{2}})'", content)
            if match:
                expires_str = match.group(1)
                expires = datetime.strptime(expires_str, "%Y-%m-%d").date()
                
                if expires < today:
                    expired_codes.append((code, expires_str))
                else:
                    future_codes.append((code, expires_str))
        
        if expired_codes:
            print_warning(f"{len(expired_codes)} code(s) expiré(s) trouvé(s):")
            for code, expires in expired_codes:
                print(f"   • {code} (expiré le {expires})")
        
        if future_codes:
            print_success(f"{len(future_codes)} code(s) valide(s) trouvé(s):")
            for code, expires in future_codes:
                print(f"   • {code} (valide jusqu'au {expires})")
    
    except Exception as e:
        print_error(f"Erreur vérification expiration: {e}")


def main() -> int:
    """Point d'entrée principal"""
    try:
        # Windows/PowerShell peut être en cp1252 → évite UnicodeEncodeError (emojis, accents)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print_section("🔍 VALIDATION DU SYSTÈME DE CODES D'ACCÈS")
    
    # Étape 1: Vérifier le CSV source
    print_section("📁 Vérification du fichier source")
    csv_ok = check_csv_exists()
    
    if not csv_ok:
        print_error("\n⛔ Validation échouée: CSV source manquant")
        return 1
    
    # Étape 2: Vérifier l'existence des fichiers générés
    print_section("📝 Vérification des fichiers générés")
    files_status = check_generated_files()
    
    if not all(files_status.values()):
        print_error("\n⛔ Validation échouée: fichiers manquants")
        print_info("Exécutez: python generate_all_codes.py")
        return 1
    
    # Étape 3: Valider le contenu de chaque fichier
    print_section("🔬 Validation du contenu")
    json_codes = validate_access_json()
    js_codes = validate_access_js()
    md_codes = validate_codes_md()
    config_codes = validate_config_js()
    
    # Étape 4: Vérifier la cohérence
    print_section("🔗 Vérification de la cohérence")
    consistent = check_consistency(json_codes, js_codes, md_codes, config_codes)
    
    # Étape 5: Vérifier les expirations
    print_section("📅 Vérification des dates d'expiration")
    check_expiration(config_codes)
    
    # Résultat final
    print_section("📊 RÉSULTAT FINAL")
    
    if consistent and json_codes:
        print_success(f"✅ Système validé avec succès!")
        print_success(f"   • {len(json_codes)} code(s) d'accès actif(s)")
        print_success(f"   • Tous les fichiers sont cohérents")
        print_success(
            "   • Formats reconnus : KATI-XXXXXXX ou code réservation Airbnb (ex. HMxxxxxxxx)"
        )
        return 0
    else:
        print_error("⛔ Validation échouée")
        if not consistent:
            print_error("   • Incohérences détectées entre les fichiers")
        if not json_codes:
            print_error("   • Aucun code d'accès trouvé")
        print_info("\nExécutez: python generate_all_codes.py")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

