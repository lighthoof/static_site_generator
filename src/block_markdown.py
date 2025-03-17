import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(block):
    first_char = block[0]
    match first_char:
        case "#":
            if check_heading(block):
                return BlockType.HEADING
        case "`":
            if check_code_block(block):
                return BlockType.CODE
        case ">":
            if check_quote(block):
                return BlockType.QUOTE
        case "-":
            if check_unordered_list(block):
                return BlockType.UNORDERED
        case x if x.isnumeric():
            if check_ordered_list(block):
                return BlockType.ORDERED
            
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    split_text = markdown.split("\n\n")
    for i in range(len(split_text)-1, -1 , -1):
        split_text[i] = split_text[i].strip(" \n")
        if split_text[i] == "":
            del(split_text[i])

    return split_text

def check_heading(heading):
    return re.findall(r"#{1,7} ", heading[0:7]) != []

def check_code_block(code):
    return (code[0:3] == code[len(code)-3:len(code)])

def check_quote(quote):
    lines = quote.split("\n")
    for line in lines:
        if line[0] != ">":
            return False
    return True

def check_unordered_list(list):
    lines = list.split("\n")
    for line in lines:
        if line[0:2] != "- ":
            return False
    return True

def check_ordered_list(list):
    lines = list.split("\n")
    for line in lines:
        split_list_number = line.split(". ",1)[0]
        if not split_list_number.isnumeric():
            return False
    return True
