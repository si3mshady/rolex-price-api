from fastapi import status
from fastapi.testclient import TestClient
from app.schemas.collection import CollectionListResponse
from app.schemas.error import ErrorResponse


def test_list_collections_default(client: TestClient):
    """
    Test GET /collections with default parameters returns HTTP 200 and CollectionListResponse.
    """
    response = client.get("/collections")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    validated = CollectionListResponse.model_validate(data)

    assert validated.total_collections == 5  # Daytona, Submariner, Datejust, GMT-Master II, Cellini
    assert len(validated.collections) == 5


def test_list_collections_summary_aggregations(client: TestClient):
    """
    Test GET /collections aggregate metrics (min_price, max_price, avg_price, sizes, complications).
    """
    response = client.get("/collections")
    assert response.status_code == status.HTTP_200_OK

    data = CollectionListResponse.model_validate(response.json())
    daytona = next((c for c in data.collections if c.name == "Cosmograph Daytona"), None)
    assert daytona is not None
    assert daytona.watch_count == 3
    assert daytona.min_price == 14500.0
    assert daytona.max_price == 18500.0
    assert daytona.avg_price == 16500.0  # (14500 + 18500) / 2
    assert daytona.sizes == [40]
    assert "Chronograph" in daytona.complications


def test_list_collections_sort_by_name_asc_and_desc(client: TestClient):
    """
    Test GET /collections sorting by name ascending and descending.
    """
    res_asc = client.get("/collections?sort_by=name&sort_order=asc")
    assert res_asc.status_code == status.HTTP_200_OK
    names_asc = [c.name for c in CollectionListResponse.model_validate(res_asc.json()).collections]
    assert names_asc == sorted(names_asc, key=lambda x: x.lower())

    res_desc = client.get("/collections?sort_by=name&sort_order=desc")
    assert res_desc.status_code == status.HTTP_200_OK
    names_desc = [c.name for c in CollectionListResponse.model_validate(res_desc.json()).collections]
    assert names_desc == sorted(names_asc, key=lambda x: x.lower(), reverse=True)


def test_list_collections_sort_by_watch_count(client: TestClient):
    """
    Test GET /collections sorting by watch_count descending.
    """
    response = client.get("/collections?sort_by=watch_count&sort_order=desc")
    assert response.status_code == status.HTTP_200_OK

    counts = [c.watch_count for c in CollectionListResponse.model_validate(response.json()).collections]
    assert counts == sorted(counts, reverse=True)


def test_list_collections_sort_by_avg_price(client: TestClient):
    """
    Test GET /collections sorting by avg_price descending.
    """
    response = client.get("/collections?sort_by=avg_price&sort_order=desc")
    assert response.status_code == status.HTTP_200_OK

    prices = [c.avg_price for c in CollectionListResponse.model_validate(response.json()).collections if c.avg_price is not None]
    assert prices == sorted(prices, reverse=True)


def test_list_collections_invalid_sort_by(client: TestClient):
    """
    Negative Test: GET /collections with invalid sort_by parameter returns HTTP 422.
    """
    response = client.get("/collections?sort_by=invalid_param")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "VALIDATION_ERROR"


def test_list_collections_invalid_sort_order(client: TestClient):
    """
    Negative Test: GET /collections with invalid sort_order parameter returns HTTP 422.
    """
    response = client.get("/collections?sort_order=invalid_order")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "VALIDATION_ERROR"
