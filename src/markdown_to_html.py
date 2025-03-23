from htmlnode           import HTMLNode
from textnode           import TextNode, TextType, text_node_to_html_node
from inline_markdown    import markdown_to_text_nodes
from block_markdown     import BlockType, markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):

    block_list = markdown_to_blocks(markdown)

    print(block_list)

    for block in block_list:
        tag = ""
        block_type = block_to_block_type(block)
        #print(block_type)
        if block_type == BlockType.CODE:
            block_html_node = text_node_to_html_node(TextNode(block, TextType.CODE))
        else:
            children = text_to_children(block)
        #print(f"textnode_children - {children}")
        match block_type:
            case BlockType.PARAGRAPH:
                tag = "p"
            case BlockType.HEADING:
                pass
            case BlockType.CODE:
                tag = "code"
            case BlockType.QUOTE:
                tag = "blockquote"
            case BlockType.UNORDERED:
                tag = "ul"
            case BlockType.ORDERED:
                tag = "li"
        #html_node = HTMLNode(tag, value, children, props)

    htmlDoc = []
    return htmlDoc

def text_to_children(text):
    #text_node = TextNode(text, TextType.TEXT)
    text_nodes = markdown_to_text_nodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
