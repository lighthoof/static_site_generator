from textnode import TextNode, TextType

def main():
    dummy_text = "This is it!"
    dummy_type = TextType.BOLD
    dummy_url = ""#"https://www.boot.dev"
    text_node = TextNode(dummy_text, dummy_type, dummy_url)
    print(text_node)

main()