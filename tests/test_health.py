import unittest

from fastapi.testclient import TestClient

from seriousdb.cache import Cache
from seriousdb.main import app, get_cache


class HealthEndpointTests(unittest.TestCase):
    def test_health_reports_ready_cache(self):
        cache = Cache()
        cache.db = {"default": "default"}
        app.dependency_overrides[get_cache] = lambda: cache

        try:
            response = TestClient(app).get("/health")
        finally:
            app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_reports_unavailable_cache(self):
        cache = Cache()
        app.dependency_overrides[get_cache] = lambda: cache

        try:
            response = TestClient(app).get("/health")
        finally:
            app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"detail": "Service unavailable"})


if __name__ == "__main__":
    unittest.main()
