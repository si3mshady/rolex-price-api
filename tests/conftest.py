import pytest
from typing import Generator, List
from fastapi.testclient import TestClient

from app.main import app
from app.models.watch import Watch
from app.services.rolex_service import rolex_service


@pytest.fixture
def sample_watches() -> List[Watch]:
    """
    Fixture providing a deterministic dataset of Watch instances for testing.
    """
    return [
        Watch(
            id="watch-001-116500ln",
            reference="116500LN",
            collection="Cosmograph Daytona",
            description="Oystersteel with Black Cerachrom Bezel and Black Dial",
            size=40,
            rrp="14500.0",
            price=14500.0,
            is_por=False,
            complications=["Chronograph", "Small Seconds", "Tachymeter"],
        ),
        Watch(
            id="watch-002-116503",
            reference="116503",
            collection="Cosmograph Daytona",
            description="Yellow Rolesor with White Dial and Gold Bezel",
            size=40,
            rrp="18500.0",
            price=18500.0,
            is_por=False,
            complications=["Chronograph", "Small Seconds"],
        ),
        Watch(
            id="watch-003-116508",
            reference="116508",
            collection="Cosmograph Daytona",
            description="18 ct Yellow Gold with Green Dial",
            size=40,
            rrp="POR",
            price=None,
            is_por=True,
            complications=["Chronograph", "Small Seconds"],
        ),
        Watch(
            id="watch-004-126610ln",
            reference="126610LN",
            collection="Submariner",
            description="Oystersteel with Black Cerachrom Bezel",
            size=41,
            rrp="10250.0",
            price=10250.0,
            is_por=False,
            complications=["Date"],
        ),
        Watch(
            id="watch-005-126610lv",
            reference="126610LV",
            collection="Submariner",
            description="Oystersteel with Green Cerachrom Bezel and Black Dial",
            size=41,
            rrp="10800.0",
            price=10800.0,
            is_por=False,
            complications=["Date"],
        ),
        Watch(
            id="watch-006-124060",
            reference="124060",
            collection="Submariner",
            description="Oystersteel without Date",
            size=41,
            rrp="9100.0",
            price=9100.0,
            is_por=False,
            complications=[],
        ),
        Watch(
            id="watch-007-126334",
            reference="126334",
            collection="Datejust",
            description="White Rolesor with Blue Fluted Dial",
            size=41,
            rrp="10500.0",
            price=10500.0,
            is_por=False,
            complications=["Date"],
        ),
        Watch(
            id="watch-008-279174",
            reference="279174",
            collection="Datejust",
            description="White Rolesor Lady-Datejust Pink Dial",
            size=28,
            rrp="8250.0",
            price=8250.0,
            is_por=False,
            complications=["Date"],
        ),
        Watch(
            id="watch-009-126710blro",
            reference="126710BLRO",
            collection="GMT-Master II",
            description="Oystersteel with Red and Blue Cerachrom Bezel (Pepsi)",
            size=40,
            rrp="10900.0",
            price=10900.0,
            is_por=False,
            complications=["Date", "GMT", "Dual Time Zone"],
        ),
        Watch(
            id="watch-010-50535",
            reference="50535",
            collection="Cellini",
            description="18 ct Everose Gold with White Dial",
            size=39,
            rrp="POR",
            price=None,
            is_por=True,
            complications=["Moonphase", "Date"],
        ),
    ]


@pytest.fixture
def mock_rolex_service(sample_watches: List[Watch]) -> Generator[None, None, None]:
    """
    Fixture that replaces the in-memory watches with sample test data and restores original catalog upon teardown.
    """
    original_watches = rolex_service._watches
    rolex_service.set_watches(sample_watches)
    yield
    rolex_service.set_watches(original_watches)


@pytest.fixture
def client(mock_rolex_service: None) -> Generator[TestClient, None, None]:
    """
    Fixture providing a FastAPI TestClient configured with mock dataset.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def real_catalog_client() -> Generator[TestClient, None, None]:
    """
    Fixture providing a FastAPI TestClient using the real catalog JSON file.
    """
    with TestClient(app) as test_client:
        yield test_client
