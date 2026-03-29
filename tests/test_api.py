from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_report_endpoint() -> None:
    client.post("/api/reset")
    response = client.get("/api/report")
    assert response.status_code == 200
    data = response.json()
    assert data["water"] == 300
    assert data["milk"] == 200
    assert data["coffee"] == 100
    assert data["money"] == 0.0


def test_order_insufficient_funds() -> None:
    client.post("/api/reset")
    response = client.post(
        "/api/order",
        json={
            "drink": "latte",
            "coins": {"quarters": 1, "dimes": 0, "nickels": 0, "pennies": 0},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Sorry that's not enough money. Money refunded."


def test_order_success() -> None:
    client.post("/api/reset")
    response = client.post(
        "/api/order",
        json={
            "drink": "espresso",
            "coins": {"quarters": 6, "dimes": 0, "nickels": 0, "pennies": 0},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Here is your espresso. Enjoy!" in data["message"]

