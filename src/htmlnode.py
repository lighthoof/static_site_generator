class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        output = ""
        for key, value in self.props.items():
            output += f" {key}=\"{value}\""
        return output
    
    def __eq__(self, other):
        if (self.tag == other.tag 
            and self.value == other.value 
            and self.children == other.children 
            and self.props == other.props):
            return True
        return False
    
    def __repr__(self):
        props_to_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                props_to_string += f" {key}=\"{value}\""
        else:
            props_to_string = "None"
        return(f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {props_to_string})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf must have a value")
        
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have a child node")
        
        children_string = ""
        for child in self.children:
            children_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"    