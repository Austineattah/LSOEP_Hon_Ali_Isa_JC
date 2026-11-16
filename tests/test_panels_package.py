import unittest
from unittest.mock import patch

import panels


class PanelsPackageTests(unittest.TestCase):
    def test_existing_submission_handler_uses_package_globals(self):
        with patch.object(panels, "submit_submission") as submit:
            self.assertTrue(panels._commit_submission("example", {"value": 1}))
        submit.assert_called_once_with(
            "example", {"value": 1}, uploads=None, dedupe_fields=None
        )


if __name__ == "__main__":
    unittest.main()
