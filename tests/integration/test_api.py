"""Phase 4. API behaviour via FastAPI's TestClient. Override dependencies (api/deps.py) with
a test DB and a FakeLLMClient; never hit real services.
"""

import pytest

fastapi = pytest.importorskip("fastapi", reason="needs the 'api' extra")
from fastapi.testclient import TestClient  # noqa: E402

from blockwise.api.app import create_app  # noqa: E402

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Phase 4 not implemented")


@pytest.fixture
def client():
    return TestClient(create_app())


def test_health_ok(client):
    assert client.get("/health").status_code == 200


def test_plan_with_bad_date_is_422_not_500(client):
    assert client.post("/plans", json={"date": "not-a-date"}).status_code == 422


def test_unknown_plan_is_404(client):
    assert client.get("/plans/does-not-exist").status_code == 404


def test_cannot_submit_without_approval(client):
    pytest.skip("TODO(you): create a plan, try to submit before an approved decision -> 409")
