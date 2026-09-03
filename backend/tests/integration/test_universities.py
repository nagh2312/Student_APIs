"""University API tests."""


def test_list_universities(client):
    r = client.get("/v1/universities")
    assert r.status_code == 200
    body = r.json()
    assert body["error"] is None
    assert isinstance(body["data"], list)
    assert body["meta"]["total"] >= 1
    assert "request_id" in body["meta"]


def test_filter_by_country(client):
    r = client.get("/v1/universities", params={"country": "US"})
    assert r.status_code == 200
    for item in r.json()["data"]:
        assert item["country_code"] == "US"


def test_search_by_name(client):
    r = client.get("/v1/universities", params={"name": "Carnegie"})
    assert r.status_code == 200
    data = r.json()["data"]
    assert any("Carnegie" in u["name"] for u in data)


def test_get_university(client):
    r = client.get("/v1/universities/cmu")
    assert r.status_code == 200
    assert r.json()["data"]["id"] == "cmu"


def test_university_not_found(client):
    r = client.get("/v1/universities/does-not-exist")
    assert r.status_code == 404
    body = r.json()
    assert body["data"] is None
    assert body["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_programs(client):
    r = client.get("/v1/universities/cmu/programs")
    assert r.status_code == 200
    assert isinstance(r.json()["data"], list)


def test_pagination(client):
    r = client.get("/v1/universities", params={"page": 1, "limit": 2})
    assert r.status_code == 200
    body = r.json()
    assert len(body["data"]) <= 2
    assert body["meta"]["limit"] == 2
    assert body["meta"]["has_next"] is True
