"""HTTP gegen Overpass — als einzige Netzwerkstelle, damit alles andere
ohne Netz testbar bleibt.

Overpass ist ein Spendendienst von Freiwilligen, keine kommerzielle API. Die
Nutzungsregeln sind darum eingebaut und nicht optional: ein Request zur Zeit,
Backoff statt Nachbohren, sprechender User-Agent, Spiegelwechsel erst nach
Fehlschlag. Wer hier drängelt, wird gesperrt — zu Recht.
"""

from __future__ import annotations

import time

import requests

MIRRORS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
)

DEFAULT_USER_AGENT = (
    "leadfinder/0.1 (OSM-Gewerberecherche München; Kontakt bitte in "
    "--user-agent eintragen)"
)

# Overpass signalisiert Überlast mit diesen Codes; sie sind kein Fehler des
# Aufrufers, sondern eine Bitte zu warten.
RETRY_STATUS = (429, 502, 503, 504)


class OverpassUnreachable(RuntimeError):
    """Kein Spiegel war erreichbar — typisch für gesperrte Netze."""


class OverpassError(RuntimeError):
    """Server erreicht, aber Abfrage abgelehnt."""


def check_reachability(
    mirrors: tuple[str, ...] = MIRRORS,
    timeout: float = 12.0,
    user_agent: str = DEFAULT_USER_AGENT,
) -> list[tuple[str, str]]:
    """(Spiegel, Status) je Server. Status ist 'ok', 'blockiert' oder HTTP-Code.

    Bewusst ein eigener, billiger Aufruf gegen /api/status: eine klare Aussage
    "das Netz lässt dich nicht raus" ist mehr wert als eine leere Ergebnisliste,
    die nach einem Datenproblem aussieht.
    """
    results: list[tuple[str, str]] = []
    for mirror in mirrors:
        status_url = mirror.replace("/api/interpreter", "/api/status")
        try:
            response = requests.get(
                status_url,
                timeout=timeout,
                headers={"User-Agent": user_agent},
            )
        except requests.RequestException:
            results.append((mirror, "blockiert"))
            continue
        results.append(
            (mirror, "ok" if response.ok else f"HTTP {response.status_code}")
        )
    return results


def fetch(
    query: str,
    mirrors: tuple[str, ...] = MIRRORS,
    timeout: float = 300.0,
    user_agent: str = DEFAULT_USER_AGENT,
    max_attempts: int = 3,
    sleep=time.sleep,
) -> dict:
    """Abfrage senden und JSON zurückgeben.

    `sleep` ist injizierbar, damit Tests das Backoff-Verhalten prüfen können,
    ohne tatsächlich zu warten.
    """
    last_error: str = "keine Spiegel konfiguriert"

    for mirror in mirrors:
        for attempt in range(1, max_attempts + 1):
            try:
                response = requests.post(
                    mirror,
                    data={"data": query},
                    timeout=timeout,
                    headers={"User-Agent": user_agent},
                )
            except requests.RequestException as exc:
                last_error = f"{mirror}: {exc.__class__.__name__}"
                break  # Netzproblem: Spiegel wechseln statt zu wiederholen

            if response.status_code in RETRY_STATUS:
                last_error = f"{mirror}: HTTP {response.status_code}"
                if attempt < max_attempts:
                    sleep(2 ** attempt)
                    continue
                break

            if not response.ok:
                raise OverpassError(
                    f"{mirror} lehnte die Abfrage ab: HTTP "
                    f"{response.status_code} — {response.text[:300]}"
                )

            try:
                return response.json()
            except ValueError as exc:
                raise OverpassError(
                    f"{mirror} lieferte kein JSON: {exc}"
                ) from exc

    raise OverpassUnreachable(
        f"Kein Overpass-Spiegel erreichbar (zuletzt: {last_error})"
    )
