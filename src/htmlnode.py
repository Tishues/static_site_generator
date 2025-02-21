

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    
class LeafNode(HTMLNode):
    # List of self-closing tags
    SELF_CLOSING_TAGS = {"img", "br", "hr", "input", "meta", "link"}

    def __init__(self, tag, value, props=None):
        if props is None:
            props = {}
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value if self.value is not None else ""
        
        # Handle self-closing tags differently
        if self.tag in self.SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()}/>"
        
        # Regular tags
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self, visited=None):
        if visited is None:
            visited = set()
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("No children")
        # Prevent circular references
        if id(self) in visited:
            raise ValueError("Circular reference detected in ParentNode.")
        visited.add(id(self))  # Mark this node as visited
        # Start building the HTML string
        html = f"<{self.tag}>"
        # Handle each child node
        for child in self.children:
            if isinstance(child, ParentNode):  # Pass visited ONLY to ParentNode
                html += child.to_html(visited=visited)
            else:  # Assume it's a LeafNode
                html += child.to_html()
        # Close the tag
        html += f"</{self.tag}>"

        return html
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children} {self.props})"