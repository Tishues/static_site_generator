import unittest
from htmlnode import HTMLNode


# Unit tests

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Create a node with some props
        node = HTMLNode(props={"href": "https://boot.dev"})
        # Test that the props_to_html method returns what we expect
        assert node.props_to_html() == ' href="https://boot.dev"'

    def test_props_initialization(self):
        node = HTMLNode(props=None)
        node2 = HTMLNode(props={})
            # Check if `props` is correctly initialized
        self.assertEqual(node.props, {})  # `props=None` should be converted to {}
        self.assertEqual(node2.props, {})  # Explicit `props={}` should remain as {}

        # Check if the two nodes are equal
        self.assertEqual(node, node2)  # These nodes should be treated as equal



    

    