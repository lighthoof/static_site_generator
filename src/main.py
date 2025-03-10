from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode

def main():
    props = {
                "href": "404",
                "target": "none",
            }
        
    parent_node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
    props,
)

    print(parent_node.to_html())

    print("-----------------------------------------------------------")

    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node2 = ParentNode("div", [child_node])

    print(parent_node2.to_html())

main()