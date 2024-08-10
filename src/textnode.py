from htmlnode import LeafNode
import re

######### Global "constant" definitions #########

text_type_text   = "text"   # Markdown: nothing, duh!
text_type_bold   = "bold"   # Markdown: **
text_type_italic = "italic" # Markdown: *
text_type_code   = "code"   # Markdown: `
text_type_link   = "link"   # Markdown: []()
text_type_image  = "image"  # Markdown: ![]()

tt_tag = { text_type_text   : None,   \
           text_type_bold   : "b",    \
           text_type_italic : "i",    \
           text_type_code   : "code", \
           text_type_link   : "a",    \
           text_type_image  : "img"
         }

tt_val = { text_type_text   : True,   \
           text_type_bold   : True,    \
           text_type_italic : True,    \
           text_type_code   : True, \
           text_type_link   : True,    \
           text_type_image  : False
         }

tt_pro = { text_type_text   : "",   \
           text_type_bold   : "",    \
           text_type_italic : "",    \
           text_type_code   : "", \
           text_type_link   : "href",    \
           text_type_image  : ["src", "alt"]
         }

######### Text Node Class to break down Markup #########

class TextNode:
    
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

######### Helper Functions #########

def text_node_to_html_node(text_node):
    if text_node.text_type not in tt_tag:
        raise Exception("Invalid text type!")

    if text_node.text_type != "image" and text_node.text == "":
        raise Exception(f"Cannot convert text to type {text_node.text_type}, text is empty and type is not self-closing!")
    
    v1 = tt_tag[text_node.text_type]
    v2 = text_node.text if tt_val[text_node.text_type] else ""

    if tt_pro[text_node.text_type] == "":
        v3 = None
    
    elif text_node.text_type == text_type_link:
        v3 = {tt_pro[text_type_link] : text_node.url}
    
    else:
        v3 = {tt_pro[text_type_image][0] : text_node.url, tt_pro[text_type_image][1] : text_node.text}  

    return LeafNode(v1, v2, v3) 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    for node in old_nodes:
        
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        
        a = node.text.split(delimiter)
        
        if len(a) % 2 == 0:
            raise Exception("Invalid Markdown Syntax! Section was not closed!")

        for i, section in enumerate(a):
            if section == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(a[i], "text"))

            else:
                new_nodes.append(TextNode(a[i], text_type))
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
            
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        if node.text == "":
            continue
        
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue

        split_strings = []
        
        for i, image in enumerate(images):
            if i == 0:
                temp = node.text.split(f"![{image[0]}]({image[1]})", 1)
            else:
                temp = rest.split(f"![{image[0]}]({image[1]})", 1)

            if len(temp) != 2:
                raise ValueError("Invalid Markdown Syntax! Section was not closed")
            
            if temp[0] != "":
                new_nodes.append(TextNode(temp[0], "text"))

            new_nodes.append(TextNode(image[0], "image", image[1]))

            rest = temp[1]

        if rest != "":
            new_nodes.append(TextNode(rest, "text"))

    return new_nodes 


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        if node.text == "":
            continue
        
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue

        split_strings = []
        
        for i, link in enumerate(links):
            if i == 0:
                temp = node.text.split(f"[{link[0]}]({link[1]})", 1)
            else:
                temp = rest.split(f"[{link[0]}]({link[1]})", 1)

            if len(temp) != 2:
                raise ValueError("Invalid Markdown Syntax! Section was not closed")
            
            if temp[0] != "":
                new_nodes.append(TextNode(temp[0], "text"))

            new_nodes.append(TextNode(link[0], "link", link[1]))

            rest = temp[1]

        if rest != "":
            new_nodes.append(TextNode(rest, "text"))

    return new_nodes

def text_to_textnodes(text):
    n = [TextNode(text, "text")]
    n = split_nodes_delimiter(n, "*", "italic")
    n = split_nodes_delimiter(n, "**", "bold")
    n = split_nodes_delimiter(n, "`", "code")
    n = split_nodes_image(n)
    return split_nodes_link(n)
