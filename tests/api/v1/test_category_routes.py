def test_create_category(client):
    payload = {
        "name": "Furniture"
    }

    response = client.post("/categories/", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Furniture"


def test_get_categories(client):
    client.post("/categories/", json={"name": "One"})
    client.post("/categories/", json={"name": "Two"})

    response = client.get("/categories/")

    assert response.status_code == 200
    assert len(response.json()) == 2
