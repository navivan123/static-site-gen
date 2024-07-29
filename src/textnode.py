from htmlnode import LeafNode

text_type_text   = "text"
text_type_bold   = "bold"
text_type_italic = "italic"
text_type_code   = "code"
text_type_link   = "link"
text_type_image  = "image"


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




class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

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
