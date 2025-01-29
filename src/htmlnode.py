

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    def to_html(self):
        raise NotImplementedError()
        
    def props_to_html(self):
        empty_string = ""
        for key, value in self.props.items():
            empty_string += f' {key}="{value}"'
        return empty_string

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False  # Ensure we're only comparing HTMLNode objects
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
       )