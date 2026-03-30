# -*- coding: utf-8 -*-
"""Met à jour Comment avec PDF: pdfs/... et resynchronise les <ul> des pages pièce (logique proche de GuideDepartAdmin)."""
import html as html_lib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "assets" / "guide-content.json"

ROOM_PAGES = [
    ("chambre.html", "chambre"),
    ("cuisine.html", "cuisine"),
    ("salle_deau.html", "salle_deau"),
    ("salle_manger.html", "salle_manger"),
    ("salon.html", "salon"),
    ("terrasse.html", "terrasse"),
    ("wc.html", "wc"),
    ("placard_bleu.html", "placard_bleu"),
]

# (nom JSON exact, sous-chaîne Catégorie obligatoire ou None, fichier sous pdfs/)
RULES = [
    ("Climatisation Chambre", None, "climatisation.pdf"),
    ("Climatisation", "Salle à Manger", "climatisation.pdf"),
    ("Mini réfrigérateur", None, "mini_refrigerateur.pdf"),
    ("Congélateur", None, "congelateur.pdf"),
    ("Four", None, "four.pdf"),
    ("Cafetière", None, "cafetiere.pdf"),
    ("Machine à café Senseo", None, "senseo.pdf"),
    ("Bouilloire", None, "bouilloire_sana.pdf"),
    ("Machine à laver", None, "lave_linge.pdf"),
    ("Plaque cuisson vitro céramique", None, "plaques_de_cuisson.pdf"),
    ("Lave-vaisselle", None, "lave_vaisselle.pdf"),
    ("Douche", None, "douche.pdf"),
    ("Radiateur sdb", None, "radiateur_sdb.pdf"),
    ("Miroir lumineux", None, "miroir_neo.pdf"),
    ("Radiateur", "Salle à Manger", "radiateur_salon.pdf"),
    ("Enceinte bluetooth", None, "enceinte_bluetooth.pdf"),
    ("Alexa", None, "alexa.pdf"),
    ("TV Salon", None, "tv_salon.pdf"),
    ("Box TV Orange", None, "box_tv_orange.pdf"),
    ("Volets roulants", None, "volets_roulants.pdf"),
]


def slugify(text: str) -> str:
    if not text:
        return ""
    norm = unicodedata.normalize("NFD", text)
    ascii_fold = "".join(c for c in norm if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_fold.lower())
    return re.sub(r"^_+|_+$", "", s)


def equipment_for_room(eq: dict, room_key: str) -> bool:
    piece = slugify(eq.get("Category") or "")
    if not piece:
        return False
    if room_key == "salle_deau":
        return "salle" in piece and "eau" in piece
    if room_key == "salle_manger":
        return "salle" in piece and "manger" in piece
    if room_key == "placard_bleu":
        return "placard" in piece
    compact = room_key.replace("_", "")
    return compact in piece.replace("_", "") or room_key in piece


def try_parse_pdf(comment: str) -> str | None:
    if not comment:
        return None
    for line in comment.splitlines():
        m = re.match(r"^PDF\s*:\s*(.+)$", line.strip(), re.I)
        if m:
            return m.group(1).strip().replace("\\", "/")
    return None


def try_parse_cle(comment: str) -> str | None:
    if not comment:
        return None
    for line in comment.splitlines():
        m = re.match(r"^Clé\s*:\s*(.+)$", line.strip(), re.I)
        if m:
            return m.group(1).strip()
    return None


def build_li_element(eq: dict) -> str:
    name = html_lib.escape(eq.get("Name") or "")
    attrs = []
    slug = slugify(eq.get("Name") or "")
    if slug:
        attrs.append(f'data-slug="{html_lib.escape(slug)}"')
    ck = try_parse_cle(eq.get("Comment") or "")
    if ck:
        attrs.append(f'data-lang-key="{html_lib.escape(ck)}"')
    pdf_common = try_parse_pdf(eq.get("Comment") or "")
    photos = sorted(eq.get("Photos") or [], key=lambda p: p.get("DisplayOrder") or 0)

    def norm_caption(s: str) -> str:
        t = (s or "").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        return " ".join(t.split())

    cap_parts = [norm_caption(p.get("Comment") or "") for p in photos]
    if cap_parts and any(cap_parts):
        enc = "|".join(html_lib.escape(p) for p in cap_parts)
        attrs.append(f'data-captions="{enc}"')
    paths_entries = [
        ((p.get("Path") or "").strip().replace("\\", "/"), p)
        for p in photos
        if (p.get("Path") or "").strip()
    ]
    if paths_entries:
        paths = [x[0] for x in paths_entries]
        attrs.append('data-photo-paths="' + "|".join(html_lib.escape(p) for p in paths) + '"')
        pdf_slots = []
        for _, p in paths_entries:
            pp = (p.get("PdfPath") or p.get("pdfPath") or "").strip().replace("\\", "/")
            if pp:
                pdf_slots.append(pp)
            elif pdf_common:
                pdf_slots.append(pdf_common)
            else:
                pdf_slots.append("")
        if any(pdf_slots):
            attrs.append('data-photo-pdfs="' + "|".join(html_lib.escape(x) for x in pdf_slots) + '"')
    elif pdf_common:
        attrs.append(f'data-pdf="{html_lib.escape(pdf_common)}"')
    attr_s = (" " + " ".join(attrs)) if attrs else ""
    return f"                <li{attr_s}>{name}</li>"


def build_ul_for_room(equipments: list, room_key: str) -> str:
    rows = [
        e for e in equipments
        if e.get("IsActive", True) and equipment_for_room(e, room_key)
    ]
    rows.sort(
        key=lambda e: (
            e.get("DisplayOrder") or 0,
            (e.get("Name") or "").casefold(),
        )
    )
    lines = ["            <ul>"] + [build_li_element(e) for e in rows] + ["            </ul>"]
    return "\n".join(lines)


def sync_room_html_ul(data: dict) -> int:
    equipments = data.get("Equipments") or []
    changed = 0
    ul_re = re.compile(r"<ul>\s*.*?\s*</ul>", re.I | re.S)
    for fname, room_key in ROOM_PAGES:
        path = ROOT / fname
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "function runRoomPhotos" not in text:
            continue
        new_ul = build_ul_for_room(equipments, room_key)
        replaced, n = ul_re.subn(new_ul, text, count=1)
        if n and replaced != text:
            path.write_text(replaced, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    eqs = data.get("Equipments") or []
    pdf_dir = ROOT / "pdfs"
    available = {p.name.lower() for p in pdf_dir.glob("*.pdf")}

    def merge_comment(existing: str, pdf_line: str) -> str:
        lines = []
        seen_pdf = False
        for raw in (existing or "").splitlines():
            line = raw.strip()
            if line.upper().startswith("PDF:"):
                seen_pdf = True
                lines.append(pdf_line)
            elif line:
                lines.append(line)
        if not seen_pdf:
            lines.insert(0, pdf_line)
        return "\n".join(lines)

    updated = 0
    skipped = []
    for eq in eqs:
        name = eq.get("Name") or ""
        cat = eq.get("Category") or ""
        pdf_name = None
        for rule_name, cat_need, pdf in RULES:
            if name != rule_name:
                continue
            if cat_need is not None and cat_need not in cat:
                continue
            pdf_name = pdf
            break
        if not pdf_name:
            continue
        if pdf_name.lower() not in available:
            skipped.append((name, pdf_name, "fichier absent"))
            continue
        line = f"PDF: pdfs/{pdf_name}"
        new_c = merge_comment(eq.get("Comment") or "", line)
        if (eq.get("Comment") or "").strip() != new_c.strip():
            eq["Comment"] = new_c
            updated += 1

    data["UpdatedAtUtc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK — {updated} fiche(s) avec PDF. Vérifier pdfs/: {len(skipped)} rejet(s).")
    for s in skipped:
        print("  ", s)
    html_n = sync_room_html_ul(data)
    print(f"HTML — {html_n} page(s) <ul> resynchronisée(s).")


if __name__ == "__main__":
    main()
