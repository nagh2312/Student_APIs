"""Countries, geography, weather, books, currency, time tests."""


def test_countries_list(client):
    r = client.get("/v1/countries")
    assert r.status_code == 200
    assert r.json()["error"] is None
    assert len(r.json()["data"]) >= 1


def test_country_by_code(client):
    r = client.get("/v1/countries/US")
    assert r.status_code == 200
    assert r.json()["data"]["code"] == "US"


def test_country_states(client):
    r = client.get("/v1/countries/US/states")
    assert r.status_code == 200
    assert len(r.json()["data"]) >= 1


def test_invalid_country_code(client):
    r = client.get("/v1/countries/X")
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"


def test_geocode(client):
    r = client.get("/v1/geocode", params={"q": "pittsburgh"})
    assert r.status_code == 200
    assert r.json()["data"][0]["latitude"]


def test_distance(client):
    r = client.get(
        "/v1/distance",
        params={
            "from_lat": 40.44,
            "from_lon": -79.99,
            "to_lat": 51.50,
            "to_lon": -0.12,
        },
    )
    assert r.status_code == 200
    assert r.json()["data"]["distance_km"] > 0


def test_weather_current(client):
    r = client.get("/v1/weather", params={"lat": 40.44, "lon": -79.99})
    assert r.status_code == 200
    data = r.json()["data"]
    assert "temperature" in data
    assert data["source"] == "mock"


def test_weather_forecast(client):
    r = client.get("/v1/weather/forecast", params={"lat": 40.44, "lon": -79.99, "days": 3})
    assert r.status_code == 200
    assert len(r.json()["data"]["daily"]) == 3


def test_books_search(client):
    r = client.get("/v1/books/search", params={"q": "Pride"})
    assert r.status_code == 200
    assert any("Pride" in b["title"] for b in r.json()["data"])


def test_book_by_isbn(client):
    r = client.get("/v1/books/isbn/0141439513")
    assert r.status_code == 200
    assert r.json()["data"]["title"]


def test_currency_convert(client):
    r = client.get("/v1/convert", params={"from": "USD", "to": "EUR", "amount": 100})
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["converted_amount"] > 0
    assert data["from_currency"] == "USD"


def test_rates(client):
    r = client.get("/v1/rates/USD")
    assert r.status_code == 200
    assert "EUR" in r.json()["data"]["rates"]


def test_timezones(client):
    r = client.get("/v1/timezones", params={"q": "New_York"})
    assert r.status_code == 200
    assert "America/New_York" in r.json()["data"]


def test_time_convert(client):
    r = client.get(
        "/v1/time/convert",
        params={"from": "America/New_York", "to": "Asia/Kolkata"},
    )
    assert r.status_code == 200
    assert r.json()["data"]["to_timezone"] == "Asia/Kolkata"


def test_health(client):
    assert client.get("/health").status_code == 200
    assert client.get("/health/live").status_code == 200


def test_catalog(client):
    r = client.get("/v1/catalog")
    assert r.status_code == 200
    slugs = {a["slug"] for a in r.json()["data"]}
    assert {"universities", "weather", "books"} <= slugs


def test_api_key_lifecycle(client):
    create = client.post("/v1/auth/api-keys", json={"name": "test-key"})
    assert create.status_code == 201
    raw = create.json()["data"]["raw_key"]
    assert raw.startswith("sap_")
    key_id = create.json()["data"]["id"]

    listed = client.get("/v1/auth/api-keys")
    assert any(k["id"] == key_id for k in listed.json()["data"])
    assert all(k.get("raw_key") is None for k in listed.json()["data"])

    deleted = client.delete(f"/v1/auth/api-keys/{key_id}")
    assert deleted.status_code == 200


def test_rate_limit_headers(client):
    r = client.get("/v1/countries")
    assert "X-RateLimit-Limit" in r.headers
    assert "X-Request-ID" in r.headers


def test_envelope_shape(client):
    r = client.get("/v1/countries/US")
    body = r.json()
    assert set(body.keys()) == {"data", "meta", "error"}
