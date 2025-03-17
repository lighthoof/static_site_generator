import unittest

from textnode import (TextNode, TextType) 
from inline_markdown import (split_text_node_by_delimiter, split_node_list, 
                            extract_markdown_images, extract_markdown_links,
                            split_image_node, split_link_node, markdown_to_text_nodes)


class TestTextToNodes(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("`This` is text with _no_ expected delimiters", TextType.TEXT)
        new_nodes = split_text_node_by_delimiter(node, TextType.CODE, "**")
        expected = [TextNode("`This` is text with _no_ expected delimiters", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
                ]
        new_nodes = split_text_node_by_delimiter(node, TextType.CODE, "`")
        self.assertEqual(new_nodes, expected)

    def test_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
                ]
        new_nodes = split_text_node_by_delimiter(node, TextType.CODE, "**")
        self.assertEqual(new_nodes, expected)

    def test_italic_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
                ]
        new_nodes = split_text_node_by_delimiter(node, TextType.CODE, "_")
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
        new_nodes = split_text_node_by_delimiter(node, TextType.CODE, "`")
        self.assertEqual(new_nodes, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("`This is text` with 3 `code blocks` in `it`", TextType.TEXT),
            TextNode("This is text with a `code block` word", TextType.TEXT),
        ]
        new_nodes = split_node_list(nodes, TextType.CODE,  "`")
        expected = [
                TextNode("This is text", TextType.CODE),
                TextNode(" with 3 ", TextType.TEXT),
                TextNode("code blocks", TextType.CODE),
                TextNode(" in ", TextType.TEXT),
                TextNode("it", TextType.CODE),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_not_text_type(self):
        node = TextNode("code block", TextType.CODE)
        expected =  [TextNode("code block", TextType.CODE)]
        new_nodes = split_text_node_by_delimiter(node, TextType.CODE, "**")
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("This is text with an unclosed `code block` word `here", TextType.TEXT)
        with self.assertRaises(Exception) as error:
            split_text_node_by_delimiter(node, TextType.CODE, "`")
        self.assertTrue("Delimiter not closed correctly in" in str(error.exception)) 

###images and links###

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_invalid(self):
        matches = extract_markdown_images(
        "This is text with an ![image]break(https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_invalid(self):
        matches = extract_markdown_links(
        "This is text with a [link]break(https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_image_node(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with an image(https://i.imgur.com/zjjcJKZ.png) and another second image(https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_image_node(node)
        expected = [TextNode("This is text with an image(https://i.imgur.com/zjjcJKZ.png) and another second image(https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        self.assertEqual(expected,
            new_nodes
            )

    def test_leading_and_trailing_Images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) between images ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_image_node(node)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" between images ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_multiple_image_nodes(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            TextNode("![image](https://i.imgur.com/zjjcJKZ.png) between images ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ]
        new_nodes = split_node_list(nodes, TextType.IMAGE)
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" between images ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_one_image(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            TextNode("[image]!(https://i.imgur.com/zjjcJKZ.png) between images [second image]!(https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ]
        new_nodes = split_node_list(nodes, TextType.IMAGE)
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("[image]!(https://i.imgur.com/zjjcJKZ.png) between images [second image]!(https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_link_node(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode(
            "This is text with a link(https://i.imgur.com/zjjcJKZ.png) and another second link(https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_link_node(node)
        expected = [TextNode("This is text with a link(https://i.imgur.com/zjjcJKZ.png) and another second link(https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        self.assertEqual(expected,
            new_nodes
            )
        
    def test_leading_and_trailing_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) between links [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_link_node(node)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" between links ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_multiple_link_nodes(self):
        nodes = [
            TextNode("This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            TextNode("[link](https://i.imgur.com/zjjcJKZ.png) between links [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ]
        new_nodes = split_node_list(nodes, TextType.LINK)
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" between links ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_full_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = markdown_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)

if __name__ == "__main__":
    unittest.main()