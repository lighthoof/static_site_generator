from textnode import TextNode, TextType, split_text_node_by_deilimiter
from htmlnode import ParentNode, LeafNode

def main():
    nodes = [
            TextNode("`This is text` with 3 `code blocks` in `it`", TextType.TEXT),
            TextNode("This is text with a `code block` word", TextType.TEXT),
        ]
    new_nodes = split_text_node_by_deilimiter(nodes, "`", TextType.CODE)
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
        
    print(new_nodes)
    print(expected)

main()