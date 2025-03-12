from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Incorrect text node type")

def split_text_node_by_delimiter(old_node, delimiter, text_type):
    nodes_so_far = []
    old_node_string = old_node.text
    first_postion = old_node_string.find(delimiter)

    if old_node_string.count(delimiter) % 2 != 0:
        raise Exception(f"Delimiter not closed correctly in ({old_node})" )
    if old_node.text_type != TextType.TEXT: 
        nodes_so_far.append(old_node)
        return nodes_so_far
    if first_postion == -1: 
        nodes_so_far.append(old_node)
        return nodes_so_far
    
    #Should I rewrite this as a recursion?
    while old_node_string.find(delimiter) != -1:
        split_leading_text = old_node_string.split(delimiter,1)
        split_delimited_node = split_leading_text[1].split(delimiter,1)
        
        if split_leading_text[0] != "":
            nodes_so_far.append(TextNode(split_leading_text[0], TextType.TEXT))
        nodes_so_far.append(TextNode(split_delimited_node[0], text_type))
        old_node_string = split_delimited_node[1]

    if old_node_string != "":    
        nodes_so_far.append(TextNode(old_node_string, TextType.TEXT))
    return nodes_so_far

def split_text_node_list(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.append(split_text_node_by_delimiter(old_node, delimiter, text_type))
    return new_nodes