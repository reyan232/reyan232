"""Google Places API (New) als zweite Datenquelle.

Der Hebel liegt in der Feldmaske: `places.websiteUri` kommt direkt in der
Suchantwort mit. Die alte API brauchte dafür je Treffer einen zweiten
Details-Aufruf — zwanzig Betriebe hätten zwanzig zusätzliche Abfragen
gekostet statt keiner.

Zweiter Punkt, der den Aufbau bestimmt: `searchText` liefert höchstens 20
Treffer je Seite und 60 je Abfrage. Ganz München in einem Aufruf gibt es
nicht, also wird das Stadtgebiet gekachelt und je Kachel und Branche
gesucht.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

from .budget import Budget, BudgetExhausted
from .categories import Category
from .parse import Lead, Stats, normalize_phone

ENDPOINT = "https://places.googleapis.com/v1/places:searchText"

# Ohne websiteUri wäre der ganze Filter unmöglich, ohne addressComponents
# müssten wir formattedAddress mit Regex zerlegen. Beide liegen in derselben
# Abrechnungsstufe wie die Telefonnummer, kosten hier also nichts extra.
FIELD_MASK = ",".join(
    (
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.addressComponents",
        "places.nationalPhoneNumber",
        "places.websiteUri",
        "places.location",
        "nextPageToken",
    )
)

MAX_PAGES = 3  # Google gibt über nextPageToken nicht mehr als 60 Treffer her


@dataclass(frozen=True)
class BBox:
    sued: float
    west: float
    nord: float
    ost: float

    def as_rectangle(self) -> dict:
        return {
            "low": {"latitude": self.sued, "longitude": self.west},
            "high": {"latitude": self.nord, "longitude": self.ost},
        }


# Stadtgebiet München, grob umschlossen.
MUENCHEN = BBox(sued=48.06, west=11.36, nord=48.25, ost=11.72)


class GoogleAuthError(RuntimeError):
    """Key fehlt, ist ungültig oder die API ist nicht freigeschaltet."""


class GoogleError(RuntimeError):
    """Anfrage abgelehnt."""


class GoogleUnreachable(RuntimeError):
    """Netzwerk blockiert."""


def tiles(box: BBox = MUENCHEN, grid: int = 3) -> list[BBox]:
    """Gebiet in grid×grid Kacheln zerlegen.

    Mehr Kacheln heißt bessere Abdeckung *und* mehr Abfragen — der Parameter
    ist damit der wichtigste Kostenhebel und gehört bewusst gesetzt.
    """
    if grid < 1:
        raise ValueError("grid muss mindestens 1 sein")
    lat_step = (box.nord - box.sued) / grid
    lon_step = (box.ost - box.west) / grid
    return [
        BBox(
            sued=box.sued + row * lat_step,
            west=box.west + col * lon_step,
            nord=box.sued + (row + 1) * lat_step,
            ost=box.west + (col + 1) * lon_step,
        )
        for row in range(grid)
        for col in range(grid)
    ]


def scrub(text: str, api_key: str) -> str:
    """Key aus Text entfernen, bevor er irgendwo landet.

    Fehlermeldungen wandern in Logs und Bugreports. Ein Key, der einmal dort
    steht, ist verbrannt — also lieber einmal zu viel ersetzt.
    """
    if api_key and api_key in text:
        return text.replace(api_key, "***")
    return text


def build_body(
    text_query: str, tile: BBox, page_token: str | None = None
) -> dict:
    body: dict = {
        "textQuery": text_query,
        "languageCode": "de",
        "regionCode": "DE",
        "maxResultCount": 20,
        "locationRestriction": {"rectangle": tile.as_rectangle()},
    }
    if page_token:
        body["pageToken"] = page_token
    return body


def _headers(api_key: str) -> dict[str, str]:
    # Key gehört in den Header, nicht in die URL: URLs landen in Proxy- und
    # Serverlogs, Header deutlich seltener.
    return {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    }


def search_page(
    text_query: str,
    tile: BBox,
    api_key: str,
    page_token: str | None = None,
    timeout: float = 30.0,
) -> dict:
    try:
        response = requests.post(
            ENDPOINT,
            json=build_body(text_query, tile, page_token),
            headers=_headers(api_key),
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise GoogleUnreachable(
            f"Google Places nicht erreichbar: {exc.__class__.__name__}"
        ) from exc

    if response.status_code in (401, 403):
        raise GoogleAuthError(
            "Google lehnt den Key ab (HTTP "
            f"{response.status_code}). Prüfe, ob der Key gültig ist, die "
            '"Places API (New)" im Projekt aktiviert wurde und die '
            "Key-Beschränkungen den Aufruf zulassen.\n"
            f"Antwort: {scrub(response.text[:300], api_key)}"
        )
    if not response.ok:
        raise GoogleError(
            f"HTTP {response.status_code}: "
            f"{scrub(response.text[:300], api_key)}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise GoogleError(f"Antwort war kein JSON: {exc}") from exc


def _component(place: dict, wanted: str) -> str:
    for component in place.get("addressComponents") or []:
        if wanted in (component.get("types") or []):
            return component.get("longText") or component.get("shortText") or ""
    return ""


def place_to_lead(place: dict, kategorie: str) -> Lead | None:
    name = ((place.get("displayName") or {}).get("text") or "").strip()
    if not name:
        return None

    strasse = _component(place, "route")
    hausnummer = _component(place, "street_number")
    plz = _component(place, "postal_code")
    ort = _component(place, "locality")

    raw_phone = (place.get("nationalPhoneNumber") or "").strip()
    telefon = normalize_phone(raw_phone) or raw_phone

    location = place.get("location") or {}
    lat = location.get("latitude")
    lon = location.get("longitude")
    place_id = place.get("id", "")

    return Lead(
        name=name,
        strasse=strasse,
        hausnummer=hausnummer,
        plz=plz,
        ort=ort,
        adresse=(place.get("formattedAddress") or "").strip(),
        telefon=telefon,
        kategorie=kategorie,
        quell_id=place_id,
        lat=lat,
        lon=lon,
        quell_link=(
            f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            if place_id
            else ""
        ),
        maps_link=(
            f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            if lat is not None and lon is not None
            else ""
        ),
    )


def has_website(place: dict) -> bool:
    return bool((place.get("websiteUri") or "").strip())


def address_complete(lead: Lead) -> bool:
    return bool(lead.strasse and lead.hausnummer and lead.plz)


def collect(
    categories: list[Category],
    api_key: str,
    budget: Budget,
    grid: int = 3,
    box: BBox = MUENCHEN,
    require_phone: bool = True,
    max_pages: int = MAX_PAGES,
    on_progress=None,
    search=search_page,
) -> tuple[list[Lead], Stats]:
    """Alle Kacheln × Branchen abfragen, bis Budget oder Daten enden.

    `search` ist injizierbar, damit sich das Zusammenspiel aus Paginierung,
    Budget und Deduplizierung ohne Netz und ohne Key prüfen lässt.
    """
    stats = Stats()
    leads: list[Lead] = []
    seen: set[str] = set()
    grid_tiles = tiles(box, grid)

    for category in categories:
        for tile in grid_tiles:
            page_token: str | None = None
            for _ in range(max_pages):
                try:
                    budget.check()
                except BudgetExhausted:
                    # Kein Fehler: bis hierher gesammelte Leads sind gültig
                    # und werden vom Aufrufer geschrieben.
                    return _finish(leads, stats)

                payload = search(category.label, tile, api_key, page_token)
                budget.spend()
                if on_progress:
                    on_progress(category.label, budget)

                for place in payload.get("places") or []:
                    stats.elemente += 1

                    if has_website(place):
                        stats.mit_webseite += 1
                        continue

                    lead = place_to_lead(place, category.label)
                    if lead is None:
                        stats.ohne_name += 1
                        continue
                    if lead.quell_id in seen:
                        stats.duplikate += 1
                        continue

                    if not lead.telefon:
                        stats.ohne_telefon += 1
                        if require_phone:
                            continue
                    elif not lead.telefon.startswith("+"):
                        stats.telefon_unparsbar += 1

                    if not address_complete(lead):
                        stats.adresse_unvollstaendig += 1

                    seen.add(lead.quell_id)
                    leads.append(lead)
                    stats.kategorien[category.label] = (
                        stats.kategorien.get(category.label, 0) + 1
                    )

                page_token = payload.get("nextPageToken")
                if not page_token:
                    break

    return _finish(leads, stats)


def _finish(leads: list[Lead], stats: Stats) -> tuple[list[Lead], Stats]:
    stats.leads = len(leads)
    return leads, stats


def estimate_requests(categories: int, grid: int, max_pages: int = 1) -> int:
    """Untergrenze der Abfragen: Branchen × Kacheln × Seiten.

    Untergrenze, nicht Schätzung — wie viele Seiten tatsächlich kommen, weiß
    man erst nach der ersten. Für die Kostenwarnung ist die Untergrenze der
    ehrlichere Wert, weil sie nicht kleiner ausfallen kann als die Realität.
    """
    return categories * grid * grid * max_pages
