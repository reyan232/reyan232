"""Abfragezähler mit Monatsgrenze.

Google Places rechnet pro Abfrage ab. Ein Tippfehler in der Kachelzahl kann
darum Geld kosten, ohne dass man es merkt — deshalb zählt das Tool jede
Abfrage mit und bricht an einer selbstgesetzten Grenze ab.

Bewusst *nicht* enthalten: Googles Freikontingent-Regeln. Die ändern sich, und
eine geratene Grenze wäre schlimmer als gar keine. Hier werden Abfragen
gezählt; welche davon frei sind, steht in der Google-Cloud-Konsole.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

DEFAULT_PATH = Path.home() / ".leadfinder" / "budget.json"
DEFAULT_LIMIT = 50


class BudgetExhausted(RuntimeError):
    """Monatsgrenze erreicht — kein Fehler, sondern die Bremse."""


class Budget:
    def __init__(
        self,
        limit: int = DEFAULT_LIMIT,
        path: Path | str = DEFAULT_PATH,
        today: date | None = None,
    ) -> None:
        self.limit = limit
        self.path = Path(path)
        self.month = (today or date.today()).strftime("%Y-%m")
        self._counts = self._load()

    def _load(self) -> dict[str, int]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        return data if isinstance(data, dict) else {}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._counts, indent=2, sort_keys=True), encoding="utf-8"
        )

    @property
    def used(self) -> int:
        return int(self._counts.get(self.month, 0))

    @property
    def remaining(self) -> int:
        return max(0, self.limit - self.used)

    def check(self) -> None:
        if self.remaining <= 0:
            raise BudgetExhausted(
                f"Monatsgrenze erreicht: {self.used}/{self.limit} Abfragen im "
                f"{self.month} verbraucht. Höher setzen mit "
                f"--max-requests-month, oder bis zum Monatswechsel warten."
            )

    def spend(self, count: int = 1) -> None:
        """Sofort schreiben, damit ein Absturz den Zähler nicht zurücksetzt.

        Lieber einmal zu viel gezählt als eine Rechnung, die niemand erwartet
        hat.
        """
        self._counts[self.month] = self.used + count
        self._save()

    def status(self) -> str:
        return f"{self.used}/{self.limit} Abfragen im {self.month} verbraucht"
