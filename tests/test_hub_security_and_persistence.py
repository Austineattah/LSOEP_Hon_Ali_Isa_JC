import os
import unittest
from unittest.mock import Mock, patch

import requests
import streamlit as st
from streamlit.testing.v1 import AppTest

import auth
import panels
import persistence


class HubSecurityTests(unittest.TestCase):
    def test_restricted_routes_require_passcode_before_data_or_panels(self):
        routes = (
            ("ADMIN_GATEWAY_CHECKPOINT", "admin"),
            ("ADMIN_HUB_DASHBOARD", "admin"),
            ("📊 Master Registry Matrix", "admin"),
            ("DIRECT_AGENT_GATE", "agent"),
            ("STANDALONE_AGENT_INPUT_SCREEN", "agent"),
            ("DIRECT_COLLATION_GATE", "collation"),
            ("DIRECT_COLLATION_SCREEN", "collation"),
        )
        for route, role in routes:
            with self.subTest(route=route):
                with (
                    patch.object(auth, "_authorization_config", return_value={}),
                    patch.object(persistence, "list_submissions", return_value=[]) as read,
                    patch.object(panels, "list_submissions", read),
                    patch.object(panels, "agent_panel") as agent_panel,
                    patch.object(panels, "ward_collation_officer_panel") as ward_panel,
                ):
                    app = AppTest.from_file("main.py", default_timeout=120)
                    app.session_state.current_route = route
                    app.run()
                    self.assertFalse(app.exception)
                    self.assertEqual(len(app.text_input), 1)
                    read.assert_not_called()
                    agent_panel.assert_not_called()
                    ward_panel.assert_not_called()

                    app.text_input[0].set_value("wrong")
                    app.button(key=f"passcode_unlock_{role}").click().run()
                    self.assertTrue(any("Incorrect passcode" in item.value for item in app.error))
                    read.assert_not_called()
                    agent_panel.assert_not_called()
                    ward_panel.assert_not_called()

                    app.text_input[0].set_value("ali2027")
                    app.button(key=f"passcode_unlock_{role}").click().run()
                    self.assertFalse(app.exception)
                    self.assertTrue(app.session_state[f"passcode_authenticated_{role}"])
                    if role == "admin" and route != "📊 Master Registry Matrix":
                        read.assert_called_once_with()
                        self.assertTrue(
                            any("No saved submissions" in item.value for item in app.info)
                        )
                    elif route == "📊 Master Registry Matrix":
                        read.assert_called_once()
                    elif role == "agent":
                        agent_panel.assert_called_once()
                    else:
                        ward_panel.assert_called_once()

    def test_configured_role_allowlist_still_requires_login(self):
        with (
            patch.object(
                auth,
                "_authorization_config",
                return_value={"passcode": "custom", "admin_emails": ["admin@example.org"]},
            ),
            patch.object(auth, "is_logged_in", return_value=False),
            patch.object(persistence, "list_submissions", return_value=[]) as read,
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "ADMIN_HUB_DASHBOARD"
            app.run()
            app.text_input[0].set_value("custom")
            app.button(key="passcode_unlock_admin").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any("Sign in" in item.value for item in app.info))
            read.assert_not_called()

    def test_telemetry_displays_the_underlying_error(self):
        with (
            patch.object(auth, "_authorization_config", return_value={}),
            patch.object(
                persistence,
                "list_submissions",
                side_effect=persistence.PersistenceError("Saved submissions could not be loaded: network unavailable"),
            ),
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "ADMIN_HUB_DASHBOARD"
            app.session_state.passcode_authenticated_admin = True
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(
                any("network unavailable" in item.value for item in app.error)
            )

    def test_admin_logout_clears_passcode_access_without_oidc(self):
        with (
            patch.object(auth, "_authorization_config", return_value={}),
            patch.object(persistence, "list_submissions", return_value=[]),
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "ADMIN_HUB_DASHBOARD"
            app.session_state.passcode_authenticated_admin = True
            app.run()
            app.button(key="admin_hub_logout_btn").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state.current_route, "HOME")
            self.assertNotIn("passcode_authenticated_admin", app.session_state)

    def test_connection_failure_keeps_home_and_admin_grid_available(self):
        for route in ("HOME", "ADMIN_HUB_DASHBOARD"):
            with self.subTest(route=route):
                st.cache_data.clear()
                with (
                    patch.object(auth, "_authorization_config", return_value={}),
                    patch.object(
                        persistence,
                        "_supabase_config",
                        return_value=("https://example.test", "key"),
                    ),
                    patch.object(
                        requests.Session,
                        "get",
                        side_effect=requests.ConnectionError("network unavailable"),
                    ),
                ):
                    app = AppTest.from_file("main.py", default_timeout=120)
                    app.session_state.current_route = route
                    app.session_state.passcode_authenticated_admin = True
                    app.run()
                    self.assertFalse(app.exception)
                    self.assertTrue(
                        any("network unavailable" in item.value for item in app.warning)
                    )
                    self.assertFalse(
                        any("No saved submissions" in item.value for item in app.info)
                    )
                    if route == "HOME":
                        self.assertTrue(app.button(key="nav_card_0"))
                    else:
                        self.assertTrue(app.button(key="admin_grid_card_0"))
                        self.assertFalse(app.dataframe)


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        st.cache_data.clear()

    def tearDown(self):
        st.cache_data.clear()

    def test_empty_results_are_cached_and_successful_write_invalidates_them(self):
        empty_response = Mock(ok=True)
        empty_response.json.return_value = []
        saved_response = Mock(status_code=201)
        saved_response.json.return_value = [{"id": "saved"}]

        with (
            patch.object(persistence, "_supabase_config", return_value=("https://example.test", "key")),
            patch.object(requests.Session, "get", return_value=empty_response) as get,
            patch.object(requests, "post", return_value=saved_response),
        ):
            self.assertEqual(persistence.list_submissions(), [])
            self.assertEqual(persistence.list_submissions(), [])
            self.assertEqual(get.call_count, 1)
            persistence.submit_submission("announcement", {"message": "hello"})
            self.assertEqual(persistence.list_submissions(), [])
            self.assertEqual(get.call_count, 2)

    def test_credentials_are_cleaned_and_service_role_takes_precedence(self):
        secrets = {
            "supabase": {
                "url": '  "https://example.test/" \r\n',
                "service_role_key": '  \'"service-key"\' \r\n',
                "anon_key": "anon-key",
            }
        }
        with (
            patch.object(st, "secrets", secrets),
            patch.dict(os.environ, {"SUPABASE_SERVICE_ROLE_KEY": "env-key"}, clear=True),
        ):
            self.assertEqual(
                persistence._supabase_config(), ("https://example.test", "service-key")
            )

    def test_environment_fallback_and_anonymous_key(self):
        with (
            patch.object(st, "secrets", {}),
            patch.dict(
                os.environ,
                {"SUPABASE_URL": " 'https://example.test/' ", "SUPABASE_ANON_KEY": ' "anon-key" '},
                clear=True,
            ),
        ):
            self.assertEqual(
                persistence._supabase_config(), ("https://example.test", "anon-key")
            )

    def test_environment_service_role_precedes_secrets_anon_key(self):
        with (
            patch.object(st, "secrets", {"supabase": {"anon_key": "anon-key"}}),
            patch.dict(
                os.environ,
                {"SUPABASE_URL": "https://example.test", "SUPABASE_SERVICE_ROLE_KEY": "service-key"},
                clear=True,
            ),
        ):
            self.assertEqual(
                persistence._supabase_config(), ("https://example.test", "service-key")
            )

    def test_invalid_key_or_secrets_section_is_reported(self):
        with (
            patch.object(st, "secrets", {"supabase": {"url": "https://example.test", "service_role_key": "bad\nkey"}}),
            patch.dict(os.environ, {}, clear=True),
        ):
            with self.assertRaisesRegex(persistence.PersistenceError, "invalid"):
                persistence._supabase_config()
        with patch.object(st, "secrets", {"supabase": "not a table"}):
            with self.assertRaisesRegex(persistence.PersistenceError, "must be a table"):
                persistence._supabase_config()

    def test_connection_error_returns_none_and_is_not_cached(self):
        with (
            patch.object(persistence, "_supabase_config", return_value=("https://example.test", "key")),
            patch.object(requests.Session, "get", side_effect=requests.ConnectionError("network unavailable")) as get,
            patch.object(st, "warning") as warning,
            self.assertLogs("persistence", level="WARNING") as logs,
        ):
            self.assertIsNone(persistence.list_submissions())
            self.assertIsNone(persistence.list_submissions())
            self.assertEqual(get.call_count, 2)
            self.assertIn("network unavailable", warning.call_args.args[0])
            self.assertIn("connectivity", logs.output[0])

    def test_unauthorized_returns_none_and_reports_key_hint(self):
        response = requests.Response()
        response.status_code = 401
        response.url = "https://example.test/rest/v1/portal_submissions"
        response._content = b'{"message":"Invalid API key"}'
        with (
            patch.object(persistence, "_supabase_config", return_value=("https://example.test", "key")),
            patch.object(requests.Session, "get", return_value=response),
            patch.object(st, "warning") as warning,
            self.assertLogs("persistence", level="WARNING") as logs,
        ):
            self.assertIsNone(persistence.list_submissions())
            self.assertIn("HTTP 401", warning.call_args.args[0])
            self.assertIn("service role key", warning.call_args.args[0])
            self.assertIn("service role key", logs.output[0])

    def test_rest_requests_use_authentication_headers(self):
        get_response = Mock(ok=True)
        get_response.json.return_value = []
        post_response = Mock(status_code=201)
        post_response.json.return_value = [{"id": "saved"}]
        with (
            patch.object(persistence, "_supabase_config", return_value=("https://example.test", "key")),
            patch.object(requests.Session, "get", return_value=get_response) as get,
            patch.object(requests, "post", return_value=post_response) as post,
            patch.object(requests, "delete", return_value=Mock()) as delete,
        ):
            persistence.list_submissions(["announcement"], limit=1)
            persistence.submit_submission("announcement", {"message": "hello"})
            persistence._delete_evidence("https://example.test", "key", "evidence.pdf")
            for call in (get.call_args, post.call_args, delete.call_args):
                headers = call.kwargs["headers"]
                self.assertEqual(headers["apikey"], "key")
                self.assertEqual(headers["Authorization"], "Bearer key")
                self.assertEqual(headers["Content-Type"], "application/json")

    def test_evidence_upload_preserves_mime_type_and_authentication(self):
        uploaded_file = Mock(type="application/pdf")
        uploaded_file.getvalue.return_value = b"%PDF-1.0\n"
        with patch.object(requests, "post", return_value=Mock()) as post:
            persistence._upload_evidence(
                "https://example.test", "key", "form", "document", uploaded_file
            )
        headers = post.call_args.kwargs["headers"]
        self.assertEqual(headers["apikey"], "key")
        self.assertEqual(headers["Authorization"], "Bearer key")
        self.assertEqual(headers["Content-Type"], "application/pdf")

    def test_http_error_includes_server_details(self):
        response = requests.Response()
        response.status_code = 404
        response.url = "https://example.test/rest/v1/portal_submissions"
        response._content = b'{"message":"relation does not exist"}'
        with (
            patch.object(persistence, "_supabase_config", return_value=("https://example.test", "key")),
            patch.object(requests.Session, "get", return_value=response),
        ):
            with self.assertRaisesRegex(persistence.PersistenceError, "relation does not exist"):
                persistence.list_submissions()


if __name__ == "__main__":
    unittest.main()
