from htmlnode           import ParentNode, LeafNode
from textnode           import TextNode, TextType, text_node_to_html_node
from inline_markdown    import markdown_to_text_nodes
from block_markdown     import BlockType, markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):

    block_list = markdown_to_blocks(markdown)
    block_children = []
    for block in block_list:
        block_children.append(block(block))

    html_doc_node = ParentNode("div", block_children)
    return html_doc_node

def block_to_html_node(block):
    tag = ""
    children = []
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            tag = "p"
        case BlockType.HEADING:
            heading_tag = block[0:6]
            tag = f"h{heading_tag.count("#")}"
        case BlockType.CODE:
            tag = "pre"
        case BlockType.QUOTE:
            tag = "blockquote"
        case BlockType.UNORDERED:
            tag = "ul"
        case BlockType.ORDERED:
            tag = "li"
        case _:
            raise ValueError("Incorrect block type")
    if block_type == BlockType.CODE:
        children = [text_node_to_html_node(TextNode(block.strip("`\n"), TextType.CODE))]
    else:
        children = text_to_children(block.replace("\n"," "))
    return ParentNode(tag, children)

def text_to_children(text):
    html_nodes = []
    text_nodes = markdown_to_text_nodes(text)  
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
