"""Tests for the centralized application errors and FastAPI exception handlers."""

import logging
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI
from fastapi.testclient import TestClient

from seriousdb import main
from seriousdb.cache import Cache, require_db
from seriousdb.error_handlers import (
    INTERNAL_ERROR_DETAIL,
    register_exception_handlers,
)
from seriousdb.exceptions import (
    ApplicationError,
    ResourceNotFoundError,
    ServiceUnavailableError,
)


class ApplicationExceptionTests(unittest.TestCase):
    def test_subclasses_share_the_application_error_base(self):
        self.assertTrue(issubclass(ResourceNotFoundError, ApplicationError))
        self.assertTrue(issubclass(ServiceUnavailableError, ApplicationError))

    def test_detail_defaults_to_the_class_default(self):
        self.assertEqual(
            str(ResourceNotFoundError()), ResourceNotFoundError.default_detail
        )

    def test_detail_can_be_overridden(self):
        self.assertEqual(str(ResourceNotFoundError("no such key")), "no such key")

    def test_require_db_returns_the_loaded_database(self):
        cache = Cache()
        cache.db = {"default": "default"}
        self.assertIs(require_db(cache), cache.db)

    def test_require_db_raises_service_unavailable_without_a_database(self):
        cache = Cache()
        cache.filename = ".sdb"
        with self.assertRaises(ServiceUnavailableError) as ctx:
            require_db(cache)
        self.assertIn(".sdb", str(ctx.exception))


class HandlerTests(unittest.TestCase):
    """Handlers are exercised through a minimal app of their own."""

    def setUp(self):
        app = FastAPI()
        register_exception_handlers(app)

        @app.get("/not-found")
        def not_found():
            raise ResourceNotFoundError("nothing here")

        @app.get("/unavailable")
        def unavailable():
            raise ServiceUnavailableError("database is gone")

        @app.get("/boom")
        def boom():
            raise RuntimeError("connection string admin:hunter2 failed")

        self.client = TestClient(app, raise_server_exceptions=False)

    def test_resource_not_found_maps_to_404(self):
        response = self.client.get("/not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {"detail": "nothing here", "error": "resource_not_found"}
        )

    def test_service_unavailable_maps_to_503(self):
        response = self.client.get("/unavailable")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"detail": "database is gone", "error": "service_unavailable"},
        )

    def test_unexpected_error_is_logged_without_leaking_details(self):
        with self.assertLogs("seriousdb.error_handlers", level=logging.ERROR) as logs:
            response = self.client.get("/boom")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {"detail": INTERNAL_ERROR_DETAIL, "error": "internal_server_error"},
        )
        self.assertNotIn("hunter2", response.text)

        logged = "\n".join(logs.output)
        self.assertIn("hunter2", logged)
        self.assertIn("Traceback", logged)

    def test_unknown_route_uses_the_standard_error_structure(self):
        response = self.client.get("/no-such-route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(sorted(response.json()), ["detail", "error"])


class ApiErrorResponseTests(unittest.TestCase):
    """The real application returns the standard structure for its own errors."""

    def setUp(self):
        tmpdir = TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)

        original_db_file = main.DB_FILE
        main.DB_FILE = str(Path(tmpdir.name) / ".sdb")
        self.addCleanup(setattr, main, "DB_FILE", original_db_file)
        self.addCleanup(main.app.dependency_overrides.clear)

        self.client = TestClient(main.app)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def test_missing_key_returns_a_structured_404(self):
        response = self.client.get("/db", params={"key": "does-not-exist"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "detail": "No value set for key does-not-exist",
                "error": "resource_not_found",
            },
        )

    def test_unloaded_database_returns_503_on_get_and_put(self):
        unloaded = Cache()
        unloaded.filename = "missing.sdb"
        main.app.dependency_overrides[main.get_cache] = lambda: unloaded

        for response in (
            self.client.get("/db", params={"key": "name"}),
            self.client.put("/db", params={"key": "name", "value": "Alice"}),
        ):
            self.assertEqual(response.status_code, 503)
            self.assertEqual(response.json()["error"], "service_unavailable")
            self.assertIn("missing.sdb", response.json()["detail"])

    def test_missing_query_parameter_returns_a_structured_422(self):
        response = self.client.get("/db")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "request_validation_error")


if __name__ == "__main__":
    unittest.main()
