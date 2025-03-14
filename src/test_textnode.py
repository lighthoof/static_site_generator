import unittest

from textnode import (TextNode, TextType, text_node_to_html_node, 
                      split_text_node_by_delimiter, split_text_node_list, 
                      extract_markdown_images, extract_markdown_links)


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

#################################
######Node conversion tests######
################################# 

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_html(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic_to_html(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code_to_html(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link_to_html(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_link_to_html(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image node"})

#################################
#######Text parsing tests########
#################################

class TestTextToNodes(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("`This` is text with _no_ expected delimiters", TextType.TEXT)
        new_nodes = split_text_node_by_delimiter(node, "**", TextType.CODE)
        expected = [TextNode("`This` is text with _no_ expected delimiters", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
                ]
        new_nodes = split_text_node_by_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
                ]
        new_nodes = split_text_node_by_delimiter(node, "**", TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_italic_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
                ]
        new_nodes = split_text_node_by_delimiter(node, "_", TextType.CODE)
        self.assertEqual(new_nodes, expected)
    
    def test_leading_and_trailing_blocks(self):
        node = TextNode("`This is text` with 3 `code blocks` in `it`", TextType.TEXT)
        expected = [
            TextNode("This is text", TextType.CODE),
            TextNode(" with 3 ", TextType.TEXT),
            TextNode("code blocks", TextType.CODE),
            TextNode(" in ", TextType.TEXT),
            TextNode("it", TextType.CODE),
        ]
        new_nodes = split_text_node_by_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("`This is text` with 3 `code blocks` in `it`", TextType.TEXT),
            TextNode("This is text with a `code block` word", TextType.TEXT),
        ]
        new_nodes = split_text_node_list(nodes, "`", TextType.CODE)
        expected = [
            [
                TextNode("This is text", TextType.CODE),
                TextNode(" with 3 ", TextType.TEXT),
                TextNode("code blocks", TextType.CODE),
                TextNode(" in ", TextType.TEXT),
                TextNode("it", TextType.CODE),
            ],
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        ]
        self.assertEqual(new_nodes, expected)

    def test_not_text_type(self):
        node = TextNode("code block", TextType.CODE)
        expected =  [TextNode("code block", TextType.CODE)]
        new_nodes = split_text_node_by_delimiter(node, "**", TextType.CODE)
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("This is text with an unclosed `code block` word `here", TextType.TEXT)
        with self.assertRaises(Exception) as error:
            split_text_node_by_delimiter(node, "`", TextType.CODE)
        self.assertTrue("Delimiter not closed correctly in" in str(error.exception)) 

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()