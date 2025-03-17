from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from block_markdown import check_heading


def main():
    print(check_heading("#Heading ## "))
    
main()