from fastapi import status
from fastapi.testclient import TestClient
from app.schemas.watch import PaginatedWatchResponse
from app.schemas.error import ErrorResponse


def test_search_by_single_keyword(client: TestClient):
    """
    Test GET /search with a single query term matching collection name.
    """
    response = client.get("/search?q=Daytona")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 3
    for watch in data.items:
        assert "Daytona" in watch.collection


def test_search_by_reference_number(client: TestClient):
    """
    Test GET /search by exact reference number keyword.
    """
    response = client.get("/search?q=126610LV")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 1
    assert data.items[0].reference == "126610LV"


def test_search_by_complication_keyword(client: TestClient):
    """
    Test GET /search matching complication text in description/complications list.
    """
    response = client.get("/search?q=Moonphase")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 1
    assert data.items[0].reference == "50535"


def test_search_multi_term_query(client: TestClient):
    """
    Test GET /search with multiple search terms (AND logic).
    """
    response = client.get("/search?q=Submariner+Green")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 1
    assert data.items[0].reference == "126610LV"


def test_search_with_collection_and_price_filters(client: TestClient):
    """
    Test GET /search combining text query with collection and min/max price parameters.
    """
    response = client.get("/search?q=Oystersteel&collection=Submariner&min_price=10000&max_price=11000")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 2
    for watch in data.items:
        assert watch.collection == "Submariner"
        assert watch.price is not None
        assert 10000 <= watch.price <= 11000


def test_search_pagination(client: TestClient):
    """
    Test GET /search pagination logic.
    """
    response = client.get("/search?q=Oystersteel&page=1&limit=2")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.page == 1
    assert data.limit == 2
    assert len(data.items) == 2


def test_search_no_results(client: TestClient):
    """
    Test GET /search with a query that yields no catalog matches.
    """
    response = client.get("/search?q=NonExistentRolexModelXYZ")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 0
    assert data.items == []


def test_search_missing_q_parameter(client: TestClient):
    """
    Negative Test: GET /search without required 'q' parameter returns HTTP 422.
    """
    response = client.get("/search")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "VALIDATION_ERROR"


def test_search_empty_q_parameter(client: TestClient):
    """
    Negative Test: GET /search with empty 'q' string returns HTTP 422.
    """
    response = client.get("/search?q=")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "VALIDATION_ERROR"


def test_search_invalid_price_range(client: TestClient):
    """
    Negative Test: GET /search with min_price > max_price returns HTTP 400.
    """
    response = client.get("/search?q=Submariner&min_price=30000&max_price=10000")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "BAD_REQUEST"
    assert "min_price cannot be greater than max_price" in error_data.error.message
