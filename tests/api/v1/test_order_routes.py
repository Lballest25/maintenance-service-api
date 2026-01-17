def test_create_order_route(client):
    cat = client.post("/categories/", json={"name": "Tools"}).json()

    item = client.post(
        "/items/",
        json={
            "name": "Hammer",
            "sku": "HAM001",
            "price": 10,
            "stock": 5,
            "category_id": cat["id"],
        },
    ).json()

    payload = {
        "report_text": "Fix sink",
        "image_url": None,
        "items": [
            {
                "item_id": item["id"],
                "quantity": 2
            }
        ]
    }

    headers = {
        "X-Request-ID": "req-abc-123"
    }

    response = client.post(
        "/orders/",
        json=payload,
        headers=headers
    )

    assert response.status_code == 201
    assert response.json()["id"] is not None
