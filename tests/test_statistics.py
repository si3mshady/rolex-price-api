import statistics
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.statistics import StatisticsResponse
from app.services.rolex_service import rolex_service


def test_get_statistics_success(client: TestClient):
    """
    Test GET /statistics returns HTTP 200 and matches StatisticsResponse schema.
    """
    response = client.get("/statistics")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    validated = StatisticsResponse.model_validate(data)

    assert validated.total_watches == 10
    assert validated.total_unique_references == 10
    assert validated.total_collections == 5


def test_statistics_price_metrics(client: TestClient):
    """
    Test price metrics calculations (min, max, mean, median, POR count).
    """
    response = client.get("/statistics")
    assert response.status_code == status.HTTP_200_OK

    stats = StatisticsResponse.model_validate(response.json())
    price_stats = stats.price_stats

    assert price_stats.total_priced_watches == 8
    assert price_stats.total_por_watches == 2
    assert price_stats.min_price == 8250.0
    assert price_stats.max_price == 18500.0

    expected_prices = [
        14500.0,
        18500.0,
        10250.0,
        10800.0,
        9100.0,
        10500.0,
        8250.0,
        10900.0,
    ]
    expected_avg = round(statistics.mean(expected_prices), 2)
    expected_median = round(statistics.median(expected_prices), 2)

    assert price_stats.avg_price == expected_avg
    assert price_stats.median_price == expected_median


def test_statistics_size_metrics(client: TestClient):
    """
    Test size metrics calculations (min, max, mean, distribution).
    """
    response = client.get("/statistics")
    assert response.status_code == status.HTTP_200_OK

    stats = StatisticsResponse.model_validate(response.json())
    size_stats = stats.size_stats

    assert size_stats.min_size == 28
    assert size_stats.max_size == 41
    assert size_stats.size_distribution == {28: 1, 39: 1, 40: 4, 41: 4}


def test_statistics_highlights(client: TestClient):
    """
    Test most and least expensive watch highlight lists.
    """
    response = client.get("/statistics")
    assert response.status_code == status.HTTP_200_OK

    stats = StatisticsResponse.model_validate(response.json())

    assert len(stats.most_expensive_watches) == 5
    assert len(stats.least_expensive_watches) == 5

    # Check order of most expensive (18500, 14500, 10900, 10800, 10500)
    most_exp_prices = [w.price for w in stats.most_expensive_watches]
    assert most_exp_prices == [18500.0, 14500.0, 10900.0, 10800.0, 10500.0]

    # Check order of least expensive (8250, 9100, 10250, 10500, 10800)
    least_exp_prices = [w.price for w in stats.least_expensive_watches]
    assert least_exp_prices == [8250.0, 9100.0, 10250.0, 10500.0, 10800.0]


def test_statistics_empty_catalog(client: TestClient):
    """
    Edge Test: GET /statistics when watch catalog is empty.
    """
    rolex_service.set_watches([])
    response = client.get("/statistics")
    assert response.status_code == status.HTTP_200_OK

    stats = StatisticsResponse.model_validate(response.json())
    assert stats.total_watches == 0
    assert stats.total_unique_references == 0
    assert stats.total_collections == 0
    assert stats.price_stats.total_priced_watches == 0
    assert stats.price_stats.total_por_watches == 0
    assert stats.price_stats.min_price is None
    assert stats.price_stats.max_price is None
    assert stats.price_stats.avg_price is None
    assert stats.price_stats.median_price is None
    assert stats.most_expensive_watches == []
    assert stats.least_expensive_watches == []
