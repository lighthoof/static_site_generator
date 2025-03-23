import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


#################################
#########HTMLNode test###########
#################################

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
            "HTMLNode(tag: <h1>, value: Nothing is happening, children: <p>, props: None)", repr(node)
        )

    def test_repr_props(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = HTMLNode("<a>", "Something is happening", None, props)
        self.assertEqual(
            f"HTMLNode(tag: <a>, value: Something is happening, children: None, props:  href=\"https://www.google.com\" target=\"_blank\")",
            repr(node)
        )

#################################
#########LeafNode test###########
#################################

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

#################################
########ParentNode test##########
#################################    

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_diff_level_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("span", [grandchild_node2])
        child_leaf = LeafNode("p", "child leaf")
        child_leaf2 = LeafNode("i", "child leaf2")
        child_leaf3 = LeafNode(None, "child leaf3")
        child_nodes = [child_node, child_leaf, child_leaf2, child_leaf3, child_node2]
        parent_node = ParentNode("div", child_nodes)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p>child leaf</p><i>child leaf2</i>child leaf3<span><b>grandchild2</b></span></div>",
        )

    def test_to_html_with_multiple_props(self):
        props = {
                "href": "404",
                "target": "none",
            }
        
        more_props = {
                "href": "https://www.boot.dev",
                "target": "_blank",
            }
        
        parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            LeafNode("a", "link", more_props),
        ],
        props,
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p href=\"404\" target=\"none\"><b>Bold text</b>Normal text<i>italic text</i>Normal text<a href=\"https://www.boot.dev\" target=\"_blank\">link</a></p>"
        )

    def test_to_html_no_children(self):
        child_node = ParentNode("span", None)
        child_node2 = ParentNode("span", None)
        parent_node = ParentNode("div", [child_node, child_node2])

        with self.assertRaises(ValueError) as error:
            parent_node.to_html()
        self.assertEqual(str(error.exception), "Parent node must have a child node")

    def test_to_html_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode(None, [grandchild_node2])
        child_leaf = LeafNode("p", "child leaf")
        child_leaf2 = LeafNode("i", "child leaf2")
        child_leaf3 = LeafNode(None, "child leaf3")
        child_nodes = [child_node, child_leaf, child_leaf2, child_leaf3, child_node2]
        parent_node = ParentNode("div", child_nodes)

        with self.assertRaises(ValueError) as error:
            parent_node.to_html()
        self.assertEqual(str(error.exception), "Parent node must have a tag")
    
if __name__ == "__main__":
    unittest.main()