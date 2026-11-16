import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from streamlit.testing.v1 import AppTest

import auth
from panels import election_war_room as election
from panels import recruitment_panel as recruitment


_LISTING = {
    "title": "MDA Regularization Batch",
    "category": "Federal Civil Service",
    "office_verified": False,
    "source_badge": "Pending Office Verification",
    "slots": "Unconfirmed - Pending Quota Allocation",
    "deadline": "Not confirmed",
    "status": "Availability unconfirmed",
    "url": "",
}


def element_with_label(elements, label):
    return next(element for element in elements if element.label == label)


class RecruitmentPanelTests(unittest.TestCase):
    def test_badges_and_quotas_do_not_invent_verification(self):
        self.assertEqual(recruitment._badge(_LISTING), "Pending Office Verification")
        self.assertEqual(recruitment._quota(_LISTING), recruitment._UNCONFIRMED_QUOTA)
        self.assertEqual(
            recruitment._badge({**_LISTING, "office_verified": "true"}),
            "Pending Office Verification",
        )
        self.assertEqual(
            recruitment._badge({**_LISTING, "office_verified": True}),
            "Verified Constituency Office Registry",
        )
        self.assertEqual(recruitment._quota({**_LISTING, "slots": 20}), "20")
        self.assertEqual(
            recruitment._badge({**_LISTING, "source_badge": "Live Agency Feed"}),
            "Live Agency Feed",
        )

    def test_admin_mode_requires_allowlist_and_login_before_reading(self):
        app_code = (
            "from panels.recruitment_panel import render_recruitment_panel\n"
            "render_recruitment_panel(is_admin_mode=True)\n"
        )
        with (
            patch.object(recruitment, "fetch_live_federal_listings", return_value=[_LISTING]),
            patch.object(recruitment, "_authorization_config", return_value={}),
            patch.object(recruitment, "list_submissions") as read,
        ):
            app = AppTest.from_string(app_code, default_timeout=45).run()
            self.assertFalse(app.exception)
            self.assertTrue(any("admin_emails" in item.value for item in app.error))
            read.assert_not_called()

        config = {"admin_emails": ["admin@example.org"]}
        with (
            patch.object(recruitment, "fetch_live_federal_listings", return_value=[_LISTING]),
            patch.object(recruitment, "_authorization_config", return_value=config),
            patch.object(auth, "_authorization_config", return_value=config),
            patch.object(auth, "is_logged_in", return_value=False),
            patch.object(recruitment, "list_submissions") as read,
        ):
            app = AppTest.from_string(app_code, default_timeout=45)
            app.session_state.passcode_authenticated_admin = True
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(any("Sign in" in item.value for item in app.info))
            read.assert_not_called()

        with (
            patch.object(recruitment, "fetch_live_federal_listings", return_value=[_LISTING]),
            patch.object(recruitment, "_authorization_config", return_value=config),
            patch.object(auth, "_authorization_config", return_value=config),
            patch.object(auth, "is_logged_in", return_value=True),
            patch.object(auth, "current_email", return_value="other@example.org"),
            patch.object(recruitment, "list_submissions") as read,
        ):
            app = AppTest.from_string(app_code, default_timeout=45)
            app.session_state.passcode_authenticated_admin = True
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(any("not authorized" in item.value for item in app.error))
            read.assert_not_called()

    def test_application_requires_fields_and_persists_valid_submission(self):
        app_code = (
            "from panels.recruitment_panel import render_recruitment_panel\n"
            "render_recruitment_panel()\n"
        )
        with (
            patch.object(recruitment, "fetch_live_federal_listings", return_value=[_LISTING]),
            patch.object(recruitment, "submit_submission") as save,
        ):
            app = AppTest.from_string(app_code, default_timeout=45).run()
            element_with_label(app.button, "Submit application").click().run()
            self.assertTrue(any("required" in item.value for item in app.error))
            save.assert_not_called()

            element_with_label(app.selectbox, "LGA").select("Balanga").run()
            element_with_label(app.text_input, "Full Name").input("Test Applicant")
            element_with_label(app.text_input, "Phone").input("08012345678")
            element_with_label(app.text_input, "NIN / Voter ID").input("12345678901")
            element_with_label(app.selectbox, "Ward").select("Gelengu")
            element_with_label(app.selectbox, "Target Program").select(0)
            element_with_label(app.button, "Submit application").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(save.call_count, 1)
            args, kwargs = save.call_args
            self.assertEqual(args[0], "recruitment_application")
            self.assertEqual(args[1]["ward"], "Gelengu")
            self.assertEqual(args[1]["identity_number"], "12345678901")
            self.assertIn("program_source", kwargs["dedupe_fields"])

    def test_registry_changes_are_atomic_and_clear_scraper_cache(self):
        baseline = [{**_LISTING, "description": "Original description"}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            with (
                patch.object(recruitment, "_BASELINE_PATH", path),
                patch.object(recruitment, "fetch_live_federal_listings") as fetch,
            ):
                raw, _ = recruitment._read_baseline()
                recruitment._save_baseline(raw, 0, True, 12)
                result = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(result[0]["office_verified"])
                self.assertEqual(result[0]["slots"], 12)
                self.assertEqual(result[0]["description"], "Original description")
                fetch.clear.assert_called_once()
                with self.assertRaisesRegex(ValueError, "changed"):
                    recruitment._save_baseline(raw, 0, False, 2)
                self.assertEqual(result, json.loads(path.read_text(encoding="utf-8")))

    def test_authorized_admin_can_review_application(self):
        records = [
            {
                "id": "test-application",
                "submission_type": "recruitment_application",
                "payload": {
                    "name": "Test Applicant",
                    "phone": "08012345678",
                    "identity_number": "12345678901",
                    "lga": "Balanga",
                    "ward": "Gelengu",
                    "target_program": "MDA Regularization Batch",
                },
            }
        ]
        app_code = (
            "from panels.recruitment_panel import render_recruitment_panel\n"
            "render_recruitment_panel(is_admin_mode=True)\n"
        )
        with (
            patch.object(recruitment, "fetch_live_federal_listings", return_value=[_LISTING]),
            patch.object(recruitment, "_admin_access", return_value=True),
            patch.object(recruitment, "list_submissions", return_value=records),
            patch.object(recruitment, "submit_submission") as save,
            patch.object(recruitment, "current_email", return_value="admin@example.org"),
        ):
            app = AppTest.from_string(app_code, default_timeout=45).run()
            self.assertFalse(app.exception)
            element_with_label(app.radio, "Decision").set_value("Rejected")
            element_with_label(app.button, "Save decision").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(save.call_args.args[0], "recruitment_vetting_decision")
            self.assertEqual(save.call_args.args[1]["application_id"], "test-application")
            self.assertEqual(save.call_args.args[1]["decision"], "Rejected")

    def test_admin_registry_form_updates_verification_and_quota(self):
        app_code = (
            "from panels.recruitment_panel import render_recruitment_panel\n"
            "render_recruitment_panel(is_admin_mode=True)\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            path.write_text(json.dumps([_LISTING]), encoding="utf-8")
            with (
                patch.object(recruitment, "_BASELINE_PATH", path),
                patch.object(
                    recruitment, "fetch_live_federal_listings", return_value=[_LISTING]
                ) as fetch,
                patch.object(recruitment, "_admin_access", return_value=True),
                patch.object(recruitment, "list_submissions", return_value=[]),
            ):
                app = AppTest.from_string(app_code, default_timeout=45).run()
                element_with_label(app.checkbox, "Office verified").check()
                element_with_label(app.checkbox, "Quota confirmed").check()
                element_with_label(app.number_input, "Confirmed slot count").set_value(33)
                element_with_label(app.button, "Save registry changes").click().run()
                self.assertFalse(app.exception)
                entry = json.loads(path.read_text(encoding="utf-8"))[0]
                self.assertIs(entry["office_verified"], True)
                self.assertEqual(entry["slots"], 33)
                fetch.clear.assert_called_once()


class ElectionWarRoomTests(unittest.TestCase):
    def test_requires_agent_access_before_session_data_is_rendered(self):
        with patch.object(election, "require_role", return_value=False):
            app = AppTest.from_string(
                "from panels.election_war_room import render_election_war_room\n"
                "render_election_war_room()\n",
                default_timeout=45,
            ).run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.metric), 0)

    def test_evidence_validation_rejects_bad_signatures_and_sizes(self):
        fake = Mock(type="application/pdf")
        fake.getvalue.return_value = b"not a pdf"
        self.assertIn("does not match", election._validate_evidence(fake))
        fake.getvalue.return_value = b"%PDF-1.7\nexample"
        self.assertIsNone(election._validate_evidence(fake))
        fake.getvalue.return_value = b"%PDF-" + b"x" * election.MAX_EVIDENCE_BYTES
        self.assertIn("10 MB", election._validate_evidence(fake))

    def test_session_result_upload_filters_and_duplicate_protection(self):
        upload = Mock(name="upload")
        upload.name = "ec8a.pdf"
        upload.type = "application/pdf"
        upload.getvalue.return_value = b"%PDF-1.7\nexample"
        app_code = (
            "from panels.election_war_room import render_election_war_room\n"
            "render_election_war_room()\n"
        )
        with (
            patch.object(election, "require_role", return_value=True),
            patch.object(election.st, "file_uploader", return_value=upload),
        ):
            app = AppTest.from_string(app_code, default_timeout=45).run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.metric), 4)
            element_with_label(app.selectbox, "LGA").select("Balanga")
            for label, value in (
                ("Ward", "Gelengu"),
                ("Polling Unit Code", "PU001"),
                ("Polling Unit Name", "Test Unit"),
                ("BVAS Serial", "BVAS001"),
                ("Agent", "Test Agent"),
            ):
                element_with_label(app.text_input, label).input(value)
            for label, value in (
                ("Accredited Voters", 100),
                ("Total Votes Cast", 90),
                ("Party A Votes", 50),
                ("Party B Votes", 30),
            ):
                element_with_label(app.number_input, label).set_value(value)
            element_with_label(app.button, "Add polling unit result").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.session_state.election_data), 1)
            row = app.session_state.election_data[0]
            self.assertEqual(set(row), set(election._COLUMNS))
            self.assertEqual(row["Party_A"], 50)
            self.assertEqual(row["Form_EC8A_Status"], "Uploaded - Awaiting Verification")
            self.assertEqual(
                app.session_state.election_evidence[("Balanga", "Gelengu", "PU001")]["data"],
                upload.getvalue(),
            )
            element_with_label(app.number_input, "Party A Votes").set_value(100)
            element_with_label(app.button, "Add polling unit result").click().run()
            self.assertTrue(any("cannot exceed" in item.value for item in app.error))
            self.assertEqual(len(app.session_state.election_data), 1)
            element_with_label(app.number_input, "Party A Votes").set_value(50)
            element_with_label(app.button, "Add polling unit result").click().run()
            self.assertTrue(any("already" in item.value for item in app.error))
            self.assertEqual(len(app.session_state.election_data), 1)
            app.session_state.election_data.append(
                {**row, "LGA": "Billiri", "PU_Code": "PU002"}
            )
            app.run()
            element_with_label(app.selectbox, "Filter by LGA").select("Billiri").run()
            self.assertEqual(element_with_label(app.metric, "Polling units").value, "1")


if __name__ == "__main__":
    unittest.main()
