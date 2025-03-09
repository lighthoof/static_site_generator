import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a url node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a url node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a url node", TextType.LINK)
        node2 = TextNode("This is a url node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a node of text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a url node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a url node", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_repr_no_link(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(
            "TextNode(This is a text node, text, None)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()