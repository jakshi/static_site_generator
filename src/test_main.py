import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_with_header(self):
        markdown = "# This is a title\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")

    def test_extract_title_without_header(self):
        markdown = "No header here."
        title = extract_title(markdown)
        self.assertEqual(title, "")

    def test_extract_title_with_multiple_headers(self):
        markdown = "# First Title\n## Second Title\nContent here."
        title = extract_title(markdown)
        self.assertEqual(title, "First Title")

    def test_extract_title_empty_markdown(self):
        markdown = ""
        title = extract_title(markdown)
        self.assertEqual(title, "")
