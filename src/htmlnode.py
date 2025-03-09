class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
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
        if self.props != None:
            for key, value in self.props.items():
                props_to_string += f" {key}=\"{value}\""
        else:
            props_to_string = "None"
        return(f"HTMLNode(tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {props_to_string})")