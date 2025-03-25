import unittest
from build_doc import extract_title

class TestBuildDoc(unittest.TestCase):
    def test_extract_title(self):
        expected = "Hello"
        markdown_line = "# Hello"

        self.assertEqual(extract_title(markdown_line), expected)
        
    def test_extract_title_multiline(self):
        expected = "Hello"
        markdown_line = """Here come some text
        # Hello
        ## another heading
        and some more text
        """
        
        self.assertEqual(extract_title(markdown_line), expected)