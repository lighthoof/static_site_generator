from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from inline_markdown import markdown_to_text_nodes
from block_markdown import check_heading
from markdown_to_html import markdown_to_html_node, text_to_children, markdown_to_blocks


def main():
    text = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
    markdown_to_html_node(text)
    
main()