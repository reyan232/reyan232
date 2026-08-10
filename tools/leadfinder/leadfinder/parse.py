"""OSM-Elemente in Leads übersetzen.

Zwei Dinge tun hier mehr Arbeit als erwartet: Telefonnummern stehen in OSM in
jeder erdenklichen Schreibweise, und Adressen sind oft unvollständig. Beides
wird nicht stillschweigend geschluckt, sondern in Stats gezählt — die Quoten
sind das eigentliche Ergebnis des Testlaufs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .categories import Category, selector_index
from .query import WEBSITE_TAGS

PHONE_TAGS = ("phone", "contact:phone", "contact:mobile", "mobile")

# Ein Betrieb mit Facebook-Seite, aber ohne Webseite, ist der stärkste Lead im
# Datensatz: Sichtbarkeit ist ihm offensichtlich wichtig, eine eigene Seite hat
# er trotzdem nicht. OSM kennt diese Profile mit und ohne contact:-Präfix.
SOCIAL_TAGS = (
    "contact:facebook",
    "facebook",
    "contact:instagram",
    "instagram",
)

# Trennzeichen innerhalb einer Nummer, die keine Ziffern sind.
_PHONE_NOISE = re.compile(r"[\s\-‐-―./()\[\]]+")


@dataclass
class Lead:
    name: str
    strasse: str
    hausnummer: str
    plz: str
    ort: str
    adresse: str
    telefon: str
    kategorie: str
    quell_id: str
    lat: float | None
    lon: float | None
    quell_link: str
    maps_link: str
    social: str = ""


@dataclass
class Stats:
    elemente: int = 0
    ohne_name: int = 0
    ohne_telefon: int = 0
    telefon_unparsbar: int = 0
    adresse_unvollstaendig: int = 0
    duplikate: int = 0
    mit_webseite: int = 0
    mit_social: int = 0
    leads: int = 0
    kategorien: dict[str, int] = field(default_factory=dict)

    def as_lines(self) -> list[str]:
        quote = (
            f"{100 * self.leads / self.elemente:.0f}%" if self.elemente else "–"
        )
        lines = [
            f"  Treffer gesamt             {self.elemente}",
            f"  ohne Namen (übersprungen)  {self.ohne_name}",
            f"  ohne Telefonnummer         {self.ohne_telefon}",
            f"  Telefon nicht normierbar   {self.telefon_unparsbar}",
            f"  Adresse unvollständig      {self.adresse_unvollstaendig}",
            f"  Duplikate entfernt         {self.duplikate}",
            f"  brauchbare Leads           {self.leads}  ({quote} der Treffer)",
        ]
        if self.mit_webseite:
            lines.append(
                f"  mit Webseite (aussortiert) {self.mit_webseite}"
            )
        if self.mit_social:
            lines.append(
                f"  davon mit Social Media     {self.mit_social}"
                "   <- heißeste Leads, stehen oben"
            )
        if self.kategorien:
            lines.append("  je Branche:")
            for name, count in sorted(self.kategorien.items()):
                lines.append(f"    {name:<22} {count}")
        return lines


def normalize_phone(raw: str) -> str | None:
    """Deutsche Schreibweisen auf E.164 bringen, sonst None.

    Bewusst konservativ: eine Nummer ohne führende 0, +, oder 00 lässt keine
    Vorwahl erkennen. Sie zu raten würde falsche Nummern erzeugen, und eine
    falsche Nummer ist im Vertrieb teurer als eine fehlende.
    """
    if not raw:
        return None
    first = raw.split(";")[0]
    cleaned = _PHONE_NOISE.sub("", first)
    if not cleaned:
        return None

    if cleaned.startswith("+"):
        digits = cleaned[1:]
        prefix = "+"
    elif cleaned.startswith("00"):
        digits = cleaned[2:]
        prefix = "+"
    elif cleaned.startswith("0"):
        digits = cleaned[1:]
        prefix = "+49"
    else:
        return None

    if not digits.isdigit() or len(digits) < 5:
        return None
    return prefix + digits


def pick_phone(tags: dict[str, str]) -> tuple[str, bool]:
    """(Nummer, normiert?) — bei Fehlschlag bleibt der Rohwert erhalten.

    Ein Rohwert nützt beim Anruf immer noch; ihn wegzuwerfen, nur weil das
    Format ungewohnt ist, würde Leads ohne Not vernichten.
    """
    for tag in PHONE_TAGS:
        raw = tags.get(tag, "").strip()
        if not raw:
            continue
        normalized = normalize_phone(raw)
        if normalized:
            return normalized, True
        return raw, False
    return "", True


def social_profile(tags: dict[str, str]) -> str:
    """Erstes gefundenes Social-Profil, sonst leer.

    Reihenfolge von SOCIAL_TAGS entscheidet: contact:-Präfix zuerst, weil das
    die vom OSM-Wiki empfohlene Schreibweise ist und häufiger gepflegt wird.
    """
    for tag in SOCIAL_TAGS:
        value = tags.get(tag, "").strip()
        if value:
            return value
    return ""


def has_website(tags: dict[str, str]) -> bool:
    return any(tags.get(tag, "").strip() for tag in WEBSITE_TAGS)


def build_address(tags: dict[str, str]) -> tuple[str, bool]:
    """Adresse zusammensetzen; zweiter Wert sagt, ob sie vollständig ist."""
    street = tags.get("addr:street", "").strip()
    number = tags.get("addr:housenumber", "").strip()
    postcode = tags.get("addr:postcode", "").strip()
    city = tags.get("addr:city", "").strip()

    line1 = " ".join(p for p in (street, number) if p)
    line2 = " ".join(p for p in (postcode, city) if p)
    address = ", ".join(p for p in (line1, line2) if p)
    return address, bool(street and number and postcode)


def detect_category(tags: dict[str, str]) -> Category | None:
    index = selector_index()
    for key, value in tags.items():
        cat = index.get((key, value))
        if cat:
            return cat
    return None


def _coords(element: dict) -> tuple[float | None, float | None]:
    """Nodes tragen lat/lon direkt, Ways und Relations nur über `out center`."""
    if "lat" in element and "lon" in element:
        return element.get("lat"), element.get("lon")
    center = element.get("center") or {}
    return center.get("lat"), center.get("lon")


def element_to_lead(element: dict) -> Lead | None:
    tags = element.get("tags") or {}
    name = tags.get("name", "").strip()
    if not name:
        return None

    category = detect_category(tags)
    address, _ = build_address(tags)
    phone, _ = pick_phone(tags)
    lat, lon = _coords(element)
    quell_id = f"{element.get('type')}/{element.get('id')}"

    return Lead(
        name=name,
        strasse=tags.get("addr:street", "").strip(),
        hausnummer=tags.get("addr:housenumber", "").strip(),
        plz=tags.get("addr:postcode", "").strip(),
        ort=tags.get("addr:city", "").strip(),
        adresse=address,
        telefon=phone,
        kategorie=category.label if category else "",
        quell_id=quell_id,
        lat=lat,
        lon=lon,
        quell_link=f"https://www.openstreetmap.org/{quell_id}",
        maps_link=(
            f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            if lat is not None and lon is not None
            else ""
        ),
        social=social_profile(tags),
    )


def parse_elements(
    elements: list[dict], require_phone: bool = True
) -> tuple[list[Lead], Stats]:
    stats = Stats()
    leads: list[Lead] = []
    seen: set[str] = set()

    for element in elements:
        stats.elemente += 1
        tags = element.get("tags") or {}

        if has_website(tags):
            stats.mit_webseite += 1
            continue

        lead = element_to_lead(element)
        if lead is None:
            stats.ohne_name += 1
            continue

        if lead.quell_id in seen:
            stats.duplikate += 1
            continue

        phone, normalized = pick_phone(tags)
        if not phone:
            stats.ohne_telefon += 1
            if require_phone:
                continue
        elif not normalized:
            stats.telefon_unparsbar += 1

        _, complete = build_address(tags)
        if not complete:
            stats.adresse_unvollstaendig += 1

        seen.add(lead.quell_id)
        leads.append(lead)
        if lead.social:
            stats.mit_social += 1
        if lead.kategorie:
            stats.kategorien[lead.kategorie] = (
                stats.kategorien.get(lead.kategorie, 0) + 1
            )

    # Social-Leads nach oben: wer sein Facebook pflegt, aber keine Webseite
    # hat, ist der naheliegendste Anruf. Name als zweites Kriterium hält die
    # Reihenfolge stabil und damit testbar.
    leads.sort(key=lambda lead: (0 if lead.social else 1, lead.name.casefold()))
    stats.leads = len(leads)
    return leads, stats
