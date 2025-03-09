import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_text(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_link(self):
        html = "<a href=\"https://www.google.com\" target=\"_blank\">Hello, world!</a>"
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = LeafNode("a", "Hello, world!", props)
        self.assertEqual(node.to_html(), html)

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as error:
            node.to_html()
        self.assertEqual(str(error.exception), "Leaf must have a value")

if __name__ == "__main__":
    unittest.main()