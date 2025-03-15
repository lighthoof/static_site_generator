from enum import Enum
from htmlnode import LeafNode
import re

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

def split_text_node_by_delimiter(old_node, text_type, delimiter):
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

def split_image_node(old_node):
    nodes_so_far = []
    old_node_string = old_node.text
    image_nodes_data = extract_markdown_images(old_node_string)

    if image_nodes_data == []:
        return old_node
    
    for image_data in image_nodes_data:
        alt_text = image_data[0]
        image_link = image_data[1]
        split_node_text = old_node_string.split(f"![{alt_text}]({image_link})",1)
        old_node_string = split_node_text[1]

        if split_node_text[0] != "":
            nodes_so_far.append(TextNode(split_node_text[0], TextType.TEXT))
        nodes_so_far.append(TextNode(alt_text, TextType.IMAGE, image_link))

    if old_node_string != "":    
        nodes_so_far.append(TextNode(old_node_string, TextType.TEXT))
    return nodes_so_far        

def split_link_node(old_node):
    nodes_so_far = []
    old_node_string = old_node.text
    link_nodes_data = extract_markdown_links(old_node.text)
    
    if link_nodes_data == []:
        return old_node
    
    for link_data in link_nodes_data:
        link_text = link_data[0]
        link = link_data[1]
        split_node_text = old_node_string.split(f"[{link_text}]({link})",1)
        old_node_string = split_node_text[1]

        if split_node_text[0] != "":
            nodes_so_far.append(TextNode(split_node_text[0], TextType.TEXT))
        nodes_so_far.append(TextNode(link_text, TextType.LINK, link))

    if old_node_string != "":    
        nodes_so_far.append(TextNode(old_node_string, TextType.TEXT))
    return nodes_so_far   

def split_node_list(old_nodes, text_type, delimiter=None):
    new_nodes = []
    for old_node in old_nodes:
        match text_type:
            case TextType.IMAGE:
                new_nodes.append(split_image_node(old_node))
            case TextType.LINK:
                new_nodes.append(split_link_node(old_node))
            case _:
                if delimiter is None :
                    raise ValueError("Text type node should have delimiter set")
                new_nodes.append(split_text_node_by_delimiter(old_node, text_type, delimiter))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)