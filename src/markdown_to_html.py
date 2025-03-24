from htmlnode           import ParentNode, LeafNode
from textnode           import TextNode, TextType, text_node_to_html_node
from inline_markdown    import markdown_to_text_nodes
from block_markdown     import BlockType, markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):

    block_list = markdown_to_blocks(markdown)
    block_children = []
    for block in block_list:
        block_children.append(block_to_html_node(block.strip('"')))

    html_doc_node = ParentNode("div", block_children)
    return html_doc_node

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.CODE:
            return code_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.UNORDERED:
            return unordered_to_html(block)
        case BlockType.ORDERED:
            return ordered_to_html(block)
        case _:
            raise ValueError("Incorrect block type")

def text_to_children(text):
    html_nodes = []
    text_nodes = markdown_to_text_nodes(text)  
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def paragraph_to_html(text):
    return ParentNode("p", text_to_children(text))

def heading_to_html(text):
    heading_tag = text[0:6]
    tag = f"h{heading_tag.count("#")}"
    return ParentNode(tag, text_to_children(text.strip("# ")))

def code_to_html(text):
    child = [text_node_to_html_node(TextNode(text.strip("`\n"), TextType.CODE))]
    return ParentNode("pre", child)

def quote_to_html(text):
    split_by_lines = text.split("\n")
    for i in range(len(split_by_lines)):
        split_by_lines[i] = split_by_lines[i].lstrip("> ")
    return ParentNode("blockquote", text_to_children("\n".join(split_by_lines)))

def unordered_to_html(text):
    item_list = []
    for item in text.split("\n"):
        if not item.startswith("- "):
            raise Exception("Incorrectly formed list")
        item_children = text_to_children(item.strip("- "))
        item_list.append(ParentNode("li", item_children))
    return ParentNode("ul",item_list)

def ordered_to_html(text):
    item_list = []
    for item in text.split("\n"):
        split_number_string = item.split(". ")
        if not split_number_string[0].isnumeric():
            raise Exception("Incorrectly formed list")
        item_children = text_to_children(split_number_string[1])
        item_list.append(ParentNode("li", item_children))
    return ParentNode("ol",item_list)