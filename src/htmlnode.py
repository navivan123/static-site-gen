class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("HTMLNode base class should not be calling to_html")

    def props_to_html(self):
        if self.props is None:
            return ""

        ps = ""
        for key, value in self.props.items():
            ps += f' {key}="{value}"'
        
        return ps

    def __repr__(self):
        return f'Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes MUST have a value!")
        
        if not self.tag:
            return self.value

        if self.value == "":
            return "<" + self.tag + self.props_to_html() + ">"

        return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"
    def __repr__(self):
        return f"LeafNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("All Parent nodes MUST have a tag!")
        
        if self.children is None or self.children == []:
            raise ValueError("All Parent nodes MUST have children!")
        inner = ""        
        for node in self.children:
            inner += node.to_html()

        return "<" + self.tag + "" + self.props_to_html() + ">" + inner + "</" + self.tag + ">"

    def __repr__(self):
        return f"ParentNode(Tag: {self.tag}, Children: {self.children}, Props: {self.props})"
