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
    candidates = []
    for var_name in ("NAVIGATION_OPTIONS", "ADMIN_COMMAND_HUBS"):
        assign = next(
            (
                node.value
                for node in tree.body
                if isinstance(node, ast.Assign)
                and any(
                    isinstance(target, ast.Name) and target.id == var_name
                    for target in node.targets
                )
            ),
            None,
        )
        if assign is not None:
            candidates.extend(ast.literal_eval(assign))
    return next(label for label in candidates if suffix in label)


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

    def test_standalone_agent_route_is_gated_before_agent_panel(self):
        with (
            patch.object(auth, "require_role", return_value=False) as require,
            patch.object(panels, "agent_panel") as render,
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "STANDALONE_AGENT_INPUT_SCREEN"
            app.session_state.portal_layer_unlocked = True
            app.run()
            self.assertFalse(app.exception)
            require.assert_called_once_with("agent")
            render.assert_not_called()

    def test_ground_truth_ec8a_route_renders_admin_submissions(self):
        with (
            patch.object(auth, "require_role", return_value=True),
            patch.object(persistence, "list_submissions", return_value=[]),
            patch.object(panels, "render_admin_submissions") as render,
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = legacy_route("Ground Truth Form EC8A Data")
            app.session_state.portal_layer_unlocked = True
            app.run()
            self.assertFalse(app.exception)
            render.assert_called_once_with(["ward_collation", "polling_unit_tally"])
            app.button(key="global_return_nav_btn").click().run()
            self.assertEqual(app.session_state.current_route, "ADMIN_HUB_DASHBOARD")

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
