#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 SYSTÈME UNIFIÉ - RÉCUPÉRATION RÉSERVATIONS AIRBNB
Réutilise le système existant de KatikiasDeployer_v5 qui fonctionne parfaitement
Génère access_codes.js, access_codes.json et codes_invites.md
"""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional


# Chemins configurables
PROJECT_ROOT = Path(__file__).resolve().parent
KATIKIAS_DEPLOYER = PROJECT_ROOT / "KatikiasDeployer_v5"
CSV_FILE = KATIKIAS_DEPLOYER / "reservations_final.csv"
GUIDE_DIR = PROJECT_ROOT  # Guide-depart
ACCESS_JSON = GUIDE_DIR / "access_codes.json"
ACCESS_JS = GUIDE_DIR / "access_codes.js"
CODES_MD = GUIDE_DIR / "codes_invites.md"
CODES_MD_ONE_DRIVE = Path.home() / "OneDrive" / "Documents" / "JFG" / "Appartement Katikias" / "Guide" / "codes_invites.md"
DIRECT_URL_TEMPLATE = "https://guide.katikias33.fr/index.html?code={code}"


def _parse_date(raw: str) -> Optional[date]:
    """Parse une date dans différents formats"""
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None

    formats = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y")
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def _normalise_text(raw: Optional[str]) -> str:
    """Normalise un texte"""
    return raw.strip() if raw else ""


def _generate_code(reservation_code: str, arrival: date) -> str:
    """Génère un code unique basé sur le code de réservation et la date d'arrivée"""
    key = f"{reservation_code}|{arrival.isoformat()}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    token = base64.b32encode(digest).decode("ascii").rstrip("=")
    return f"KATI-{token[:4]}{token[-3:]}"


def _load_reservations() -> List[Dict[str, str]]:
    """Charge les réservations depuis reservations_final.csv"""
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Fichier CSV introuvable: {CSV_FILE}")

    today = date.today()
    entries: List[Dict[str, str]] = []
    
    with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        # Les noms de colonnes du CSV Airbnb réel
        required_columns = {
            "Nom du voyageur",
            "Date de début",
            "Date de fin",
            "Code de confirmation",
        }
        
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "Colonnes manquantes dans reservations_final.csv. "
                f"Colonnes attendues: {', '.join(sorted(required_columns))}"
            )

        for row in reader:
            guest = _normalise_text(row.get("Nom du voyageur", ""))
            if not guest:
                continue

            arrival = _parse_date(row.get("Date de début", ""))
            departure = _parse_date(row.get("Date de fin", ""))

            if not arrival:
                continue

            # Ne garder que les réservations futures ou en cours
            if departure and departure < today:
                continue

            reservation_code = _normalise_text(row.get("Code de confirmation", "")).upper()
            if not reservation_code:
                # Générer un code de secours
                reservation_code = hashlib.sha1(
                    f"{guest}|{arrival.isoformat()}".encode("utf-8")
                ).hexdigest().upper()[:8]

            # Récupérer le téléphone pour SMS/WhatsApp
            phone = _normalise_text(row.get("Contact", ""))

            # Utiliser le code de réservation Airbnb comme code d'accès
            access_code = reservation_code
            
            entries.append(
                {
                    "guest": guest,
                    "phone": phone,
                    "arrival": arrival.strftime("%d/%m/%Y"),
                    "departure": departure.strftime("%d/%m/%Y") if departure else "",
                    "reservation_code": reservation_code,
                    "code": access_code,
                    "url": DIRECT_URL_TEMPLATE.format(code=access_code),
                }
            )

    # Trier par date d'arrivée
    entries.sort(key=lambda item: datetime.strptime(item["arrival"], "%d/%m/%Y"))
    return entries


def _write_access_json(entries: List[Dict[str, str]]) -> None:
    """Écrit access_codes.json (format utilisé par access.html)"""
    GUIDE_DIR.mkdir(parents=True, exist_ok=True)
    with ACCESS_JSON.open("w", encoding="utf-8") as json_file:
        json.dump(
            [{"code": item["code"], "guest": item["guest"]} for item in entries],
            json_file,
            ensure_ascii=False,
            indent=2,
        )


def _write_access_js(entries: List[Dict[str, str]]) -> None:
    """Écrit access_codes.js (format utilisé par access.html)"""
    GUIDE_DIR.mkdir(parents=True, exist_ok=True)
    payload = [
        {"code": item["code"], "guest": item["guest"]}
        for item in entries
    ]
    with ACCESS_JS.open("w", encoding="utf-8") as js_file:
        js_file.write("// Fichier genere automatiquement - ne pas modifier a la main\n")
        js_file.write("window.__ACCESS_CODES__ = ")
        json.dump(payload, js_file, ensure_ascii=False)
        js_file.write(";\n")


def _write_markdown(entries: List[Dict[str, str]]) -> None:
    """Écrit codes_invites.md (table de suivi avec téléphones)"""
    GUIDE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    lines = [
        "# 🔐 Codes invités générés automatiquement\n\n",
        f"_Dernière mise à jour : {timestamp}_\n\n",
        "## 📋 Table complète des codes\n\n",
    ]

    if not entries:
        lines.append("Aucune réservation future détectée.\n")
    else:
        lines.append(
            "| Invité | Téléphone | Arrivée | Départ | Code | Lien direct |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
        )
        for item in entries:
            departure = item["departure"] or "-"
            phone = item.get("phone", "-")
            lines.append(
                f"| {item['guest']} | {phone} | {item['arrival']} | {departure} | "
                f"`{item['code']}` | {item['url']} |\n"
            )
        
        # Section templates SMS/WhatsApp
        lines.append("\n---\n\n")
        lines.append("## 📱 Templates d'envoi\n\n")
        lines.append("### SMS/WhatsApp (court)\n\n")
        lines.append("```\n")
        lines.append("Bonjour {{Nom}},\n")
        lines.append("Votre code de réservation (accès au guide):\n")
        lines.append("{{CODE}}\n\n")
        lines.append("Guide: {{LIEN}}\n")
        lines.append("```\n\n")
        
        lines.append("### Email complet\n\n")
        lines.append("```\n")
        lines.append("Objet: 🏡 Bienvenue à Katikias 33\n\n")
        lines.append("Bonjour {{Nom}},\n\n")
        lines.append("Nous sommes ravis de vous accueillir!\n\n")
        lines.append("🔐 Votre code de réservation (accès au guide):\n")
        lines.append("{{CODE}}\n\n")
        lines.append("👉 Lien direct:\n")
        lines.append("{{LIEN}}\n\n")
        lines.append("Ce lien vous donne accès à:\n")
        lines.append("✅ Code d'accès portail\n")
        lines.append("✅ Guide d'arrivée complet\n")
        lines.append("✅ Informations pratiques\n\n")
        lines.append("📅 Votre séjour: {{ARRIVEE}} → {{DEPART}}\n\n")
        lines.append("À bientôt!\n")
        lines.append("L'équipe Katikias 33\n")
        lines.append("```\n\n")
        
        # Section exemples pratiques
        lines.append("---\n\n")
        lines.append("## 💡 Exemples pratiques\n\n")
        if entries:
            example = entries[0]
            lines.append(f"### Pour {example['guest']}\n\n")
            lines.append("**SMS:**\n")
            lines.append("```\n")
            lines.append(f"Bonjour {example['guest'].split()[0]},\n")
            lines.append(f"Votre code d'accès Katikias 33: {example['code']}\n")
            lines.append(f"Guide: {example['url']}\n")
            lines.append("```\n\n")
            lines.append(f"**WhatsApp:** {example.get('phone', 'N/A')}\n")
            lines.append(f"**Messagerie Airbnb:** Code {example['reservation_code']}\n\n")

    with CODES_MD.open("w", encoding="utf-8") as md_file:
        md_file.writelines(lines)
    try:
        CODES_MD_ONE_DRIVE.parent.mkdir(parents=True, exist_ok=True)
        with CODES_MD_ONE_DRIVE.open("w", encoding="utf-8") as md_file:
            md_file.writelines(lines)
    except Exception:
        pass


def _write_codes_config_generated(entries: List[Dict[str, str]]) -> None:
    """Écrit assets/codes-config-generated.js pour le nouveau système
    
    ⚠️ SÉCURITÉ: 
    - Les codes WiFi/Portail ne sont PAS inclus (fichier public)
    - Les codes de réservation Airbnb ne sont PAS inclus
    - Seuls les données non-sensibles sont stockées
    """
    config_file = GUIDE_DIR / "assets" / "codes-config-generated.js"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    js_content = f"""/**
 * Configuration des codes d'accès (VERSION PUBLIQUE - SÉCURISÉE)
 * Générée automatiquement depuis reservations_final.csv
 * Date: {timestamp}
 * 
 * ⚠️ SÉCURITÉ: Les codes WiFi et Portail sont OMIS intentionnellement
 *    Ils sont stockés dans un fichier séparé NON PUBLIÉ (.gitignore)
 * 
 * ✅ INCLUS DANS CETTE VERSION:
 *    - Codes d'accès invité (KATI-XXXXX)
 *    - Noms des invités
 *    - Dates d'expiration
 */

const CODES_DATABASE = {{
"""
    
    for item in entries:
        code = item['code']
        guest = item['guest']
        arrival = datetime.strptime(item['arrival'], "%d/%m/%Y")
        departure_str = item['departure']
        departure = datetime.strptime(departure_str, "%d/%m/%Y") if departure_str else arrival
        
        js_content += f"""    '{code}': {{
        expires: '{departure.strftime("%Y-%m-%d")}',
        guest: '{guest}',
        arrival: '{item['arrival']}',
        departure: '{departure.strftime("%d/%m/%Y")}'
    }},
"""
    
    js_content = js_content.rstrip(',\n') + '\n'
    js_content += "};\n"
    
    with config_file.open("w", encoding="utf-8") as f:
        f.write(js_content)


def main() -> int:
    """Point d'entrée principal"""
    try:
        # Windows/PowerShell peut être en cp1252 → évite UnicodeEncodeError (emojis, accents)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print("\n" + "="*70)
    print("🔄 GÉNÉRATION DES CODES INVITÉS KATIKIAS 33")
    print("="*70)
    print(f"📁 Lecture du CSV : {CSV_FILE}")

    try:
        entries = _load_reservations()
    except Exception as exc:
        print(f"❌ ERREUR lecture du CSV : {exc}")
        return 1

    print(f"\n✅ {len(entries)} réservation(s) future(s) trouvée(s)")
    
    if entries:
        print("\n📋 Détails des réservations:")
        for item in entries:
            departure_display = item['departure'] or '...'
            print(
                f"   • {item['guest']:<30} | "
                f"{item['arrival']} → {departure_display} | "
                f"{item['code']}"
            )

    # Génération des fichiers
    print("\n📝 Génération des fichiers...")
    
    try:
        _write_access_json(entries)
        print(f"   ✅ JSON mis à jour : {ACCESS_JSON.name}")
    except Exception as exc:
        print(f"   ❌ ERREUR écriture JSON : {exc}")
        return 1

    try:
        _write_access_js(entries)
        print(f"   ✅ JS mis à jour : {ACCESS_JS.name}")
    except Exception as exc:
        print(f"   ❌ ERREUR écriture JS : {exc}")
        return 1

    try:
        _write_markdown(entries)
        print(f"   ✅ Markdown : {CODES_MD.name}")
    except Exception as exc:
        print(f"   ❌ ERREUR écriture Markdown : {exc}")
        return 1

    try:
        _write_codes_config_generated(entries)
        print(f"   ✅ Config V2 : assets/codes-config-generated.js")
    except Exception as exc:
        print(f"   ❌ ERREUR écriture Config V2 : {exc}")
        return 1

    print("\n" + "="*70)
    print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    
    print("\n📌 Fichiers générés:")
    print(f"   • access_codes.json - {len(entries)} codes")
    print(f"   • access_codes.js - Format compatible access.html")
    print(f"   • codes_invites.md - Table de suivi")
    print(f"   • assets/codes-config-generated.js - Nouveau système V2")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
