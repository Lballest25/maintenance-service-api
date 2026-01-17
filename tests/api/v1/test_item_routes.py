def test_get_items_empty(client):
    """
    Test retrieving items when none exist.
    """
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client):
    """
    Test creating an item successfully.
    """
    category = {
        "name": "Electronics"
    }

    cat_response = client.post("/categories/", json=category)
    assert cat_response.status_code == 201

    item_payload = {
        "name": "Phone",
        "sku": "PHN001",
        "price": 1000,
        "stock": 3,
        "category_id": cat_response.json()["id"],
    }

    response = client.post("/items/", json=item_payload)
    assert response.status_code == 201
    assert response.json()["sku"] == "PHN001"
