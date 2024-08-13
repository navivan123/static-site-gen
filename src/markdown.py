import re

from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import text_to_textnodes, text_node_to_html_node, TextNode

block_type_paragraph = "paragraph"
block_type_heading   = "heading"
block_type_code      = "code"
block_type_quote     = "quote"
block_type_olist     = "ordered_list"
block_type_ulist     = "unordered_list"

# Block types are defined above ^^ and this splits on \n\n.  
# It's a bit smarter than the naive method used in the project solution.
def markdown_to_blocks(markdown):
    blocks = []
    c_string = ""

    # I split each line early and strip the whitespace
    split_m = markdown.split("\n")

    for i, line in enumerate(split_m):
        split_m[i] = line.strip()
    
    # This function builds a string of each block, until it reaches the first double new line (new line is empty)
    b = True
    for i in range(len(split_m)):
        
        # When it reaches the first double new line, append the string to the block list, as it is a new block.
        # It strips the last \n if it exists (since we add them to every line), then a flag is set that indicates
        # there might be a string of newlines
        if split_m[i] == "" and b == False:
            b = True
            blocks.append(c_string)
            blocks[-1] = blocks[-1].strip("\n")
            c_string = ""
            continue

        # If the next lines are completely empty, and the last lines were empty, we simply continue and add nothing to the new c_string
        elif split_m[i] == "" and b == True:
            continue

        # We reached a line that is not empty, remove "empty lines" flag
        else:
            b = False
        
        # Add line to current string as well as the newline for the block
        c_string += split_m[i]
        c_string += "\n"
    
    # It's possible the last thing that was ran was the "block ending" detection.  
    # If so, c_string will be empty and nothing is needed to be added
    if c_string == "":
        return blocks

    # If not, append the block and strip the \n
    blocks.append(c_string)
    blocks[-1] = blocks[-1].strip("\n")

    return blocks

def block_to_block_type(block):
    if (len(block) >= 6) and (block[0:3] == block[-3:] == '```'):
        return "code"
    
    if (len(block) >= 3) and (reg_header(block)):
        return "heading"

    b_split = block.split("\n")
    
    # Check for remaining block types as they are nested.
    # This section looks at the first instance to determine which regex function to use in the loop.
    # This means there will not be a need for 3 different for loops. This might not be the best way to do it. (This line is a note for myself)
    type_m = "paragraph"
    if len(b_split[0]) >= 1 and reg_quote(b_split[0]):
        chk_func = reg_quote
        type_m = "quote"

    elif len(b_split[0]) >= 2 and reg_ul(b_split[0]):
        chk_func = reg_ul
        type_m = "unordered_list"

    elif len(b_split[0]) >= 3 and reg_l(b_split[0], 1):
        chk_func = reg_l
        type_m = "ordered_list"

    else:
        return "paragraph"

    # For each line in the list, check that it is of the correct type.  If not, it'll be automatically assumed it is a paragraph.  
    for i, line in enumerate(b_split):
        if i == 0:
            continue

        if type_m == "ordered_list":
            if not chk_func(line, i+1):
                return "paragraph"

        else:
            if not chk_func(line):
                return "paragraph"

    return type_m

def markdown_to_html_node(markdown):
    all_blocks = markdown_to_blocks(markdown)

    children = []
    for block in all_blocks:
        type_m = block_to_block_type(block)

        if type_m not in bpt_to_proc:
            raise ValueError("Invalid Block Type!")

        child = bpt_to_proc[type_m](block)

        children.append(child)

    return ParentNode("div", children, None)


# Helper functions for processing block types
def proc_quote(block):
    lines = block.split("\n")
    text = ""

    for line in lines:
        if line[0] != ">":
            raise ValueError("Block Quote aint it Chief")
        
        text = text + line[1:].strip() + " "

    text = text[:-1]
    
    children = conv_child(text)
    
    return ParentNode("blockquote", children)

def proc_ul(block):
    lines = block.split("\n")
    children = []
    
    for line in lines:
        text = line[2:]
        line_chldrn = conv_child(text)
        
        children.append(ParentNode("li", line_chldrn))

    return ParentNode("ul", children)

def proc_ol(block):
    lines = block.split("\n")
    children = []
    
    for line in lines:
        text = line[3:]
        line_chldrn = conv_child(text)
        
        children.append(ParentNode("li", line_chldrn))

    return ParentNode("ol", children)

def proc_code(block):
    if block[0:3] != "```" or block[-3:] != "```":
        raise ValueError("Invalid Code Block!  Make sure to use correct ``` delimiters at beginning and end.")

    
    text = block[3:-3]
    children = conv_child(text)

    code_c = ParentNode("code", children)
    return ParentNode("pre", [code_c])


def proc_head(block):
    i = 0
    char = block[i]

    if char != "#":
        raise ValueError("Warning, Header did not include header symbol!")

    while char == "#":
        if i >= 6:
            raise ValueError("Warning, Too many Pound Signs in Header!")
        i += 1
        char = block[i]

    if char != " ":
        raise ValueError("Warning, header requires space after pound symbol!")

    text = block[i + 1 : ]
    children = conv_child(text)
    

    return ParentNode(f"h{i}", children)

def proc_para(block):
    lines = block.split("\n")
    para = " ".join(lines)

    children = conv_child(para)
    #print(children)
    
    return ParentNode("p", children)
    
# Helper Hashmap for selecting block proccessing function
bpt_to_proc = { block_type_paragraph : proc_para,  \
                block_type_heading   : proc_head,  \
                block_type_code      : proc_code,  \
                block_type_quote     : proc_quote, \
                block_type_olist     : proc_ol,    \
                block_type_ulist     : proc_ul,    \
              }

# Helper function to convert text -> TextNode -> LeafNode
def conv_child(para):
    nodes = text_to_textnodes(para)
    children = []

    for node in nodes:
        leaf_node = text_node_to_html_node(node)
        children.append(leaf_node)

    #print(children)
    return children

# Helper functions for finding different block types.
def reg_header(text):
    return re.findall(r"^#{1,6} .", text)

def reg_quote(text):
    return re.findall(r"^>", text)

def reg_ul(text):
    return re.findall(r"^[*-] ", text)

def reg_l(text, num):
    return re.findall(r"^" + re.escape(str(num)) + r"\. ", text)
