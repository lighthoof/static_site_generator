import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_txt(self):
        node = HTMLNode(None, "Nothing is happening", None, None)
        node2 = HTMLNode(None, "Nothing is happening", None, None)
        self.assertEqual(node, node2)

    def test_eq_tag(self):
        node = HTMLNode("<h1>", "Nothing is happening", None, None)
        node2 = HTMLNode("<h1>", "Nothing is happening", None, None)
        self.assertEqual(node, node2)
    
    def test_eq_chld(self):
        node = HTMLNode("<h1>", "Nothing is happening", "<p>", None)
        node2 = HTMLNode("<h1>", "Nothing is happening", "<p>", None)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = HTMLNode("<a>", "Something is happening", None, props)
        node2 = HTMLNode("<a>", "Something is happening", None, props)
        self.assertEqual(node, node2)

    def test_neq_txt(self):
        node = HTMLNode(None, "Nothing is happening", None, None)
        node2 = HTMLNode(None, "Something is happening", None, None)
        self.assertNotEqual(node, node2)

    def test_neq_tag(self):
        node = HTMLNode("<h1>", "Nothing is happening", None, None)
        node2 = HTMLNode("<h2>", "Nothing is happening", None, None)
        self.assertNotEqual(node, node2)
    
    def test_neq_chld(self):
        node = HTMLNode("<h1>", "Nothing is happening", "<p>", None)
        node2 = HTMLNode("<h1>", "Nothing is happening", "<li>", None)
        self.assertNotEqual(node, node2)

    def test_neq_link(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        
        props2 = {
                    "href": "https://www.boot.dev",
                    "target": "_main",
                }
        node = HTMLNode("<a>", "Something is happening", None, props)
        node2 = HTMLNode("<a>", "Something is happening", None, props2)
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        html = " href=\"https://www.google.com\" target=\"_blank\""
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        
        node = HTMLNode("<a>", None, None, props)
        self.assertEqual(html, node.props_to_html())

    def test_repr_chld(self):
        node = HTMLNode("<h1>", "Nothing is happening", "<p>", None)
        self.assertEqual(
            "HTMLNode(tag: <h1>\nvalue: Nothing is happening\nchildren: <p>\nprops: None)", repr(node)
        )

    def test_repr_props(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = HTMLNode("<a>", "Something is happening", None, props)
        self.assertEqual(
            f"HTMLNode(tag: <a>\nvalue: Something is happening\nchildren: None\nprops:  href=\"https://www.google.com\" target=\"_blank\")",
            repr(node)
        )
    

if __name__ == "__main__":
    unittest.main()