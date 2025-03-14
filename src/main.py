from textnode import TextNode, TextType, extract_markdown_links
from htmlnode import ParentNode, LeafNode

def main():
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))

main()