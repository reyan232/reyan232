import json
import sys
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


@pytest.fixture
def overpass_payload() -> dict:
    path = Path(__file__).parent / "fixtures" / "overpass_muenchen.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def elements(overpass_payload) -> list[dict]:
    return overpass_payload["elements"]
