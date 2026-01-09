import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_underage_blocks_profanity(monkeypatch):
    async def fake_get_user_age(_auth_header: str) -> int:
        return 12

    # Patch where it's imported in the route module
    import app.routes.convert as convert_route
    monkeypatch.setattr(convert_route, "get_user_age", fake_get_user_age)

    # Make request with profanity_filter=true but no real file for now
    # This test is mainly checking the 403 happens before conversion.
    r = client.post(
        "/api/v1/convert/",
        headers={"Authorization": "Bearer fake"},
        data={"target_format": "txt", "profanity_filter": "true", "spell_check": "false"},
        files={"file": ("test.txt", b"hello", "text/plain")}
    )

    assert r.status_code == 403
