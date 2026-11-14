import builtins
import io
import os
import unittest
from unittest.mock import patch

import pypdfium2 as pdfium
import streamlit as st
from streamlit.testing.v1 import AppTest

import persistence


def make_pdf(page_count):
    with pdfium.PdfDocument.new() as pdf:
        for _ in range(page_count):
            page = pdf.new_page(200, 300)
            page.close()
        output = io.BytesIO()
        pdf.save(output)
        return output.getvalue()


class PdfViewerTests(unittest.TestCase):
    def setUp(self):
        st.cache_data.clear()

    def tearDown(self):
        st.cache_data.clear()

    def test_real_documents_render_and_navigation_keeps_page_per_document(self):
        with (
            patch.object(persistence, "list_submissions", return_value=[]),
            patch.object(st, "image", wraps=st.image) as image,
            patch.object(
                pdfium.PdfPage, "render", autospec=True, side_effect=pdfium.PdfPage.render
            ) as render,
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "🏛️ BEYOND RHETORICS PROJECT EXECUTION"
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(image.call_args.args[0].startswith(b"\x89PNG\r\n\x1a\n"))
            self.assertEqual(render.call_count, 1)
            self.assertTrue(app.button(key="prev_Cover_compressed.pdf").disabled)
            self.assertTrue(any("Page 1 of 4" in item.value for item in app.markdown))

            app.button(key="next_Cover_compressed.pdf").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(render.call_count, 2)
            self.assertTrue(any("Page 2 of 4" in item.value for item in app.markdown))

            app.selectbox[0].select("📄 Page 1 - Project Milestone Overview").run()
            self.assertFalse(app.exception)
            self.assertEqual(render.call_count, 3)
            self.assertTrue(any("Page 1 of 34" in item.value for item in app.markdown))
            app.selectbox[0].select("📖 Document Cover Page").run()
            self.assertFalse(app.exception)
            self.assertEqual(render.call_count, 3)
            self.assertTrue(any("Page 2 of 4" in item.value for item in app.markdown))
            app.button(key="prev_Cover_compressed.pdf").click().run()
            self.assertTrue(any("Page 1 of 4" in item.value for item in app.markdown))

    def test_replaced_pdf_invalidates_cache_and_clamps_page(self):
        contents = [make_pdf(2)]
        original_open = builtins.open

        def open_document(file, mode="r", *args, **kwargs):
            if (
                isinstance(file, (str, os.PathLike))
                and os.path.basename(file) == "Cover_compressed.pdf"
                and mode == "rb"
            ):
                return io.BytesIO(contents[0])
            return original_open(file, mode, *args, **kwargs)

        with (
            patch.object(persistence, "list_submissions", return_value=[]),
            patch("builtins.open", side_effect=open_document),
        ):
            app = AppTest.from_file("main.py", default_timeout=120)
            app.session_state.current_route = "🏛️ BEYOND RHETORICS PROJECT EXECUTION"
            app.run()
            self.assertFalse(app.exception)
            app.button(key="next_Cover_compressed.pdf").click().run()
            self.assertTrue(any("Page 2 of 2" in item.value for item in app.markdown))

            contents[0] = make_pdf(1)
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(any("Page 1 of 1" in item.value for item in app.markdown))
            self.assertEqual(app.session_state["page_idx_Cover_compressed.pdf"], 0)
            self.assertTrue(app.button(key="next_Cover_compressed.pdf").disabled)

            contents[0] = b"invalid PDF"
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(
                any("Error rendering document pages" in item.value for item in app.error)
            )


if __name__ == "__main__":
    unittest.main()
