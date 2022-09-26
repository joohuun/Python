from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg":"Hello World"}
    
    
def test_read_item():
    response = client.get("/items/foo", headers={"X-Token":"coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }
    
    
def test_read_item_bad_token():
    response = client.get("items/foo", headers={"X-Token":"bad_token"})
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Invalid X-Token header"
    }
    
    
def test_read_inexistent_itme():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {
        "detail":"Item not found"
    }
    
    
def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token":"coneofsilence"},
        json={"id":"foobar", "title":"Foo Bar", "description":"The Foo barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id":"foobar",
        "title":"Foo Bar",
        "description":"The Foo barters",
    }
    

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token":"bad_token"},
        json={"id":"foobar", "title":"Foo Bar", "description":"The Foo barters"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Invalid X-Token header"
    }
    

def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token":"coneofsilence"},
        json={
            "id":"foo",
            "title":"The Foo ID Stealers",
            "description":"There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Item already exists"
    }