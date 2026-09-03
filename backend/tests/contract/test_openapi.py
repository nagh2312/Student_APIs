"""Contract smoke test — OpenAPI available and lists key paths."""


def test_openapi_contains_core_paths(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]
    for p in [
        "/v1/universities",
        "/v1/countries",
        "/v1/geocode",
        "/v1/weather",
        "/v1/books",
        "/v1/convert",
        "/v1/timezones",
    ]:
        assert p in paths, f"missing {p}"
