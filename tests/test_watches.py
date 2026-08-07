from fastapi import status
from fastapi.testclient import TestClient
from app.schemas.watch import PaginatedWatchResponse, WatchReferenceDetailResponse
from app.schemas.error import ErrorResponse

# ============================================================================
# GET /watches Test Cases
# ============================================================================


def test_list_watches_default_pagination(client: TestClient):
    """
    Test GET /watches with default query parameters.
    """
    response = client.get("/watches")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    validated = PaginatedWatchResponse.model_validate(data)

    assert validated.total == 10
    assert validated.page == 1
    assert validated.limit == 20
    assert validated.total_pages == 1
    assert len(validated.items) == 10


def test_list_watches_custom_pagination(client: TestClient):
    """
    Test GET /watches with explicit page and limit pagination.
    """
    # Page 1 with limit 3
    response_p1 = client.get("/watches?page=1&limit=3")
    assert response_p1.status_code == status.HTTP_200_OK
    data_p1 = PaginatedWatchResponse.model_validate(response_p1.json())
    assert data_p1.page == 1
    assert data_p1.limit == 3
    assert data_p1.total == 10
    assert data_p1.total_pages == 4
    assert len(data_p1.items) == 3

    # Page 2 with limit 3
    response_p2 = client.get("/watches?page=2&limit=3")
    assert response_p2.status_code == status.HTTP_200_OK
    data_p2 = PaginatedWatchResponse.model_validate(response_p2.json())
    assert data_p2.page == 2
    assert len(data_p2.items) == 3

    # Items on page 1 and page 2 should be distinct
    p1_ids = {w.id for w in data_p1.items}
    p2_ids = {w.id for w in data_p2.items}
    assert p1_ids.isdisjoint(p2_ids)


def test_list_watches_filter_by_collection(client: TestClient):
    """
    Test GET /watches filtered by collection (case-insensitive).
    """
    response = client.get("/watches?collection=submariner")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 3
    for watch in data.items:
        assert watch.collection == "Submariner"


def test_list_watches_filter_by_price_range(client: TestClient):
    """
    Test GET /watches filtered by min_price and max_price.
    """
    response = client.get("/watches?min_price=10000&max_price=15000")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total > 0
    for watch in data.items:
        assert watch.price is not None
        assert 10000 <= watch.price <= 15000


def test_list_watches_filter_by_size_range(client: TestClient):
    """
    Test GET /watches filtered by min_size and max_size.
    """
    response = client.get("/watches?min_size=28&max_size=39")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 2  # 28mm (Lady-Datejust) and 39mm (Cellini)
    sizes = [w.size for w in data.items]
    assert sorted(sizes) == [28, 39]


def test_list_watches_filter_by_complication(client: TestClient):
    """
    Test GET /watches filtered by complication.
    """
    response = client.get("/watches?complication=Chronograph")
    assert response.status_code == status.HTTP_200_OK

    data = PaginatedWatchResponse.model_validate(response.json())
    assert data.total == 3
    for watch in data.items:
        assert "Chronograph" in watch.complications


def test_list_watches_filter_by_is_por(client: TestClient):
    """
    Test GET /watches filtered by is_por boolean flag.
    """
    # Test POR watches only
    response_por = client.get("/watches?is_por=true")
    assert response_por.status_code == status.HTTP_200_OK
    data_por = PaginatedWatchResponse.model_validate(response_por.json())
    assert data_por.total == 2
    for watch in data_por.items:
        assert watch.is_por is True
        assert watch.price is None

    # Test non-POR watches
    response_non_por = client.get("/watches?is_por=false")
    assert response_non_por.status_code == status.HTTP_200_OK
    data_non_por = PaginatedWatchResponse.model_validate(response_non_por.json())
    assert data_non_por.total == 8
    for watch in data_non_por.items:
        assert watch.is_por is False
        assert watch.price is not None


def test_list_watches_sorting(client: TestClient):
    """
    Test GET /watches sorting by price asc/desc and reference asc.
    """
    # Sort by price asc
    res_price_asc = client.get("/watches?sort_by=price&sort_order=asc&limit=10")
    data_price_asc = PaginatedWatchResponse.model_validate(res_price_asc.json())
    priced_asc = [w.price for w in data_price_asc.items if w.price is not None]
    assert priced_asc == sorted(priced_asc)

    # Sort by price desc
    res_price_desc = client.get("/watches?sort_by=price&sort_order=desc&limit=10")
    data_price_desc = PaginatedWatchResponse.model_validate(res_price_desc.json())
    priced_desc = [w.price for w in data_price_desc.items if w.price is not None]
    assert priced_desc == sorted(priced_desc, reverse=True)


def test_list_watches_invalid_min_max_price(client: TestClient):
    """
    Negative Test: GET /watches with min_price > max_price returns HTTP 400.
    """
    response = client.get("/watches?min_price=20000&max_price=10000")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "BAD_REQUEST"
    assert "min_price cannot be greater than max_price" in error_data.error.message


def test_list_watches_invalid_min_max_size(client: TestClient):
    """
    Negative Test: GET /watches with min_size > max_size returns HTTP 400.
    """
    response = client.get("/watches?min_size=42&max_size=38")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "BAD_REQUEST"
    assert "min_size cannot be greater than max_size" in error_data.error.message


def test_list_watches_invalid_sort_by(client: TestClient):
    """
    Negative Test: GET /watches with invalid sort_by parameter returns HTTP 422.
    """
    response = client.get("/watches?sort_by=unsupported_field")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "VALIDATION_ERROR"


def test_list_watches_invalid_page_and_limit(client: TestClient):
    """
    Negative Test: GET /watches with page=0 or limit=101 returns HTTP 422.
    """
    res_page = client.get("/watches?page=0")
    assert res_page.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    res_limit = client.get("/watches?limit=101")
    assert res_limit.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ============================================================================
# GET /watches/{reference} Test Cases
# ============================================================================


def test_get_watch_by_reference_success(client: TestClient):
    """
    Test GET /watches/{reference} returns HTTP 200 with reference details.
    """
    response = client.get("/watches/116500LN")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    validated = WatchReferenceDetailResponse.model_validate(data)

    assert validated.reference == "116500LN"
    assert validated.collection == "Cosmograph Daytona"
    assert validated.variants_count == 1
    assert validated.min_price == 14500.0
    assert validated.max_price == 14500.0
    assert len(validated.variants) == 1
    assert validated.variants[0].id == "watch-001-116500ln"


def test_get_watch_by_reference_case_insensitive(client: TestClient):
    """
    Test GET /watches/{reference} is case-insensitive.
    """
    response = client.get("/watches/126610lv")
    assert response.status_code == status.HTTP_200_OK

    data = WatchReferenceDetailResponse.model_validate(response.json())
    assert data.reference == "126610LV"
    assert data.collection == "Submariner"


def test_get_watch_by_reference_not_found(client: TestClient):
    """
    Negative Test: GET /watches/{reference} for non-existent reference returns HTTP 404.
    """
    response = client.get("/watches/UNKNOWN_REF_99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_data = ErrorResponse.model_validate(response.json())
    assert error_data.error.code == "NOT_FOUND"
    assert "UNKNOWN_REF_99999" in error_data.error.message
