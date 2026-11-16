import ast
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

import auth
import panels
import persistence
from panels import election_war_room, recruitment_panel


def button_with_label(app, label):
    return next(button for button in app.button if button.label == label)


def legacy_route(suffix):
    tree = ast.parse(Path("main.py").read_text(encoding="utf-8"))
    navigation = next(
        node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "NAVIGATION_OPTIONS"
            for target in node.targets
        )
    )
    return next(
        label for label in ast.literal_eval(navigation) if label.endswith(suffix)
    )


class NewPanelRoutingTests(unittest.TestCase):
    def test_recruitment_navigation_and_admin_toggle(self):
        with (
            patch.object(persistence, "list_submissions", return_value=[]),
            patch.object(recruitment_panel, "render_recruitment_panel") as render,
        ):
            app = AppTest.from_file("main.py", default_timeout=120).run()
            button_with_label(app, "Jobs Vacancy & Federal Grants").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(
                app.session_state.current_route, "Jobs Vacancy & Federal Grants"
            )
            render.assert_called_with(is_admin_mode=False)
            app.toggle(key="recruitment_admin_mode").set_value(True).run()
            self.assertFalse(app.exception)
            render.assert_called_with(is_admin_mode=True)

    def test_election_route_is_gated_before_telemetry_and_panel(self):
        with (
            patch.object(auth, "require_role", return_value=False) as require,
            patch.object(persistence, "list_submissions") as read,
            patch.object(election_war_room, "render_election_war_room") as render,
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "Election Situation Room (War Room)"
            app.run()
            self.assertFalse(app.exception)
            require.assert_called_once_with("agent")
            read.assert_not_called()
            render.assert_not_called()

    def test_election_navigation_renders_after_agent_access(self):
        with (
            patch.object(auth, "require_role", return_value=True) as require,
            patch.object(persistence, "list_submissions", return_value=[]),
            patch.object(election_war_room, "render_election_war_room") as render,
        ):
            app = AppTest.from_file("main.py", default_timeout=120).run()
            button_with_label(app, "Election Situation Room (War Room)").click().run()
            self.assertFalse(app.exception)
            require.assert_called_with("agent")
            render.assert_called_once_with()
            app.button(key="global_return_nav_btn").click().run()
            self.assertEqual(app.session_state.current_route, "HOME")

    def test_existing_public_routes_still_dispatch_to_legacy_panels(self):
        routes = (
            ("LEGISLATIVE PROGRESS TRACKER", "render_progress_tracker"),
            ("LEGISLATIVE FOOTPRINTS", "render_sponsored_bills_panel"),
            ("JOB VACANCY VERIFICATION", "render_job_verification_panel"),
        )
        for suffix, handler in routes:
            with self.subTest(route=suffix):
                with (
                    patch.object(persistence, "list_submissions", return_value=[]),
                    patch.object(panels, handler) as render,
                ):
                    app = AppTest.from_file("main.py", default_timeout=120)
                    app.session_state.current_route = legacy_route(suffix)
                    app.run()
                    self.assertFalse(app.exception)
                    render.assert_called_once_with()

    def test_existing_beyond_rhetorics_route_renders_document_viewer(self):
        with patch.object(persistence, "list_submissions", return_value=[]):
            app = AppTest.from_file("main.py", default_timeout=120).run()
            button_with_label(
                app, legacy_route("BEYOND RHETORICS PROJECT EXECUTION")
            ).click().run()
            self.assertFalse(app.exception)
            self.assertTrue(
                any(item.label == "Choose a ledger segment:" for item in app.selectbox)
            )
            self.assertTrue(app.button(key="next_Cover_compressed.pdf"))

    def test_if_elif_chains_have_no_duplicate_conditions(self):
        tree = ast.parse(Path("main.py").read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            seen = set()
            current = node
            while True:
                condition = ast.dump(current.test, include_attributes=False)
                self.assertNotIn(condition, seen)
                seen.add(condition)
                if len(current.orelse) != 1 or not isinstance(current.orelse[0], ast.If):
                    break
                current = current.orelse[0]


if __name__ == "__main__":
    unittest.main()
