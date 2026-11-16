import json
import unittest
from unittest.mock import Mock, mock_open, patch

import requests

from intelligence import scrapers


def response(text="", status_error=None):
    result = Mock()
    result.is_redirect = False
    result.text = text
    result.raise_for_status.side_effect = status_error
    return result


class FederalListingsTests(unittest.TestCase):
    def setUp(self):
        scrapers.fetch_live_federal_listings.clear()
        self.addCleanup(scrapers.fetch_live_federal_listings.clear)

    def test_failed_feeds_return_unverified_baseline_and_report_errors(self):
        error = requests.Timeout("feed timed out")
        with patch.object(scrapers.requests, "get", side_effect=error) as get:
            with patch.object(scrapers.st, "warning") as warning:
                listings = scrapers.fetch_live_federal_listings()

        self.assertEqual(len(listings), 3)
        self.assertTrue(
            all(
                item["source_badge"] == "Pending Office Verification"
                for item in listings
            )
        )
        self.assertTrue(
            all(
                item["slots"] == "Unconfirmed - Pending Quota Allocation"
                for item in listings
            )
        )
        self.assertIn("feed timed out", warning.call_args.args[0])
        self.assertEqual(get.call_count, 5)
        self.assertTrue(
            all(
                call.kwargs == {"timeout": 4, "allow_redirects": False}
                for call in get.call_args_list
            )
        )

    def test_live_titles_have_agency_provenance_without_invented_openings(self):
        def get(url, **kwargs):
            if "recruitment.fedcivilservice.gov.ng" in url:
                return response(
                    "<div><h3>Medical Laboratory Scientist II</h3>"
                    "<span>Closed</span></div>"
                )
            if "nitda.gov.ng" in url:
                return response(
                    '<a href="https://dl4all.nitda.gov.ng/">'
                    "Digital Literacy for ALL</a>"
                    '<a href="https://unrelated.example/">'
                    "Digital Skills Training</a>"
                )
            return response("<html></html>")

        with patch.object(scrapers.requests, "get", side_effect=get):
            listings = scrapers.fetch_live_federal_listings()

        live = [
            item for item in listings if item["source_badge"] == "Live Agency Feed"
        ]
        self.assertEqual(
            {item["title"] for item in live},
            {"Medical Laboratory Scientist II", "Digital Literacy for ALL"},
        )
        self.assertEqual(live[0]["status"], "Closed")
        self.assertEqual(live[1]["status"], "Availability unconfirmed")
        self.assertTrue(all(item["slots"] == "Not published" for item in live))
        self.assertTrue(
            any(item["title"] == "MDA Regularization Batch" for item in listings)
        )

    def test_empty_successful_feeds_fall_back_without_claiming_vacancies(self):
        with patch.object(
            scrapers.requests, "get", return_value=response("<html></html>")
        ):
            with patch.object(scrapers.st, "info") as info:
                listings = scrapers.fetch_live_federal_listings()

        self.assertEqual(len(listings), 3)
        info.assert_called_once()

    def test_generic_navigation_and_shared_badge_are_not_vacancies(self):
        listings = scrapers._live_listings(
            "FCSC Recruitment",
            "https://recruitment.fedcivilservice.gov.ng/vacancies",
            "fedcivilservice.gov.ng",
            "Federal Civil Service",
            "<div><h3>Open Vacancies</h3><h3>Analyst Position</h3>"
            "<span>Open</span></div><div><h3>Open Vacancies</h3>"
            "<span>Open</span></div>",
            "2025-01-01",
        )
        self.assertEqual(listings, [])

    def test_only_explicit_boolean_true_verifies_office_registry(self):
        baseline = [
            {
                "title": f"Programme {index}",
                "category": "Capacity Building",
                "slots": 20,
                "office_verified": value,
            }
            for index, value in enumerate((True, False, "true"))
        ]
        with patch("builtins.open", mock_open(read_data=json.dumps(baseline))):
            listings = scrapers._constituency_baseline()

        self.assertEqual(
            [item["source_badge"] for item in listings],
            [
                "Verified Constituency Office Registry",
                "Pending Office Verification",
                "Pending Office Verification",
            ],
        )
        self.assertEqual([item["slots"] for item in listings], [20, 20, 20])

    def test_invalid_baseline_is_reported_instead_of_fabricating_slots(self):
        with patch("builtins.open", mock_open(read_data="{invalid json")):
            with patch.object(scrapers.st, "error") as error:
                listings = scrapers._constituency_baseline()

        self.assertEqual(listings, [])
        self.assertIn("could not be loaded", error.call_args.args[0])

    def test_http_errors_and_untrusted_redirects_are_reported(self):
        redirect = Mock()
        redirect.is_redirect = True
        redirect.headers = {"Location": "https://unrelated.example/"}
        http_error = requests.HTTPError("403 Forbidden")
        with patch.object(
            scrapers.requests,
            "get",
            side_effect=[redirect, response(status_error=http_error)]
            + [response("<html></html>")] * 3,
        ) as get:
            with patch.object(scrapers.st, "warning") as warning:
                listings = scrapers.fetch_live_federal_listings()

        self.assertEqual(len(listings), 3)
        self.assertEqual(get.call_count, 5)
        message = warning.call_args.args[0]
        self.assertIn("untrusted redirect", message)
        self.assertIn("403 Forbidden", message)

    def test_cache_avoids_refetch_until_cleared(self):
        with patch.object(
            scrapers.requests, "get", return_value=response("<html></html>")
        ) as get:
            with patch.object(scrapers.st, "info"):
                first = scrapers.fetch_live_federal_listings()
                second = scrapers.fetch_live_federal_listings()
                self.assertEqual(get.call_count, 5)
                self.assertEqual(first, second)
                scrapers.fetch_live_federal_listings.clear()
                scrapers.fetch_live_federal_listings()
                self.assertEqual(get.call_count, 10)


if __name__ == "__main__":
    unittest.main()
