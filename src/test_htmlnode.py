import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


# Unit tests
class TestHTMLNode(unittest.TestCase):
        #HTMLNode
    def test_props_to_html(self):
        # Create a node with some props
        node = HTMLNode(props={"href": "https://boot.dev"})
        # Test that the props_to_html method returns what we expect
        assert node.props_to_html() == ' href="https://boot.dev"'

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


        #LeafNode
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


        #ParentNode
    def test_empty_children(self):
        empty_parent = ParentNode("p", [])
        self.assertEqual(empty_parent.to_html(), "<p></p>")

    def test_mixed_nodes(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        nested_parent = ParentNode("i", [LeafNode(None, "italic text")])
        parent = ParentNode("p", [leaf1, leaf2, nested_parent])

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_deep_nested_nodes(self):
            # Create nested ParentNodes
        child = LeafNode(None, "Deep content")
        deep_parent = ParentNode("div", [child])

        for i in range(9):  # 9 additional levels of nesting (plus initial 1 = 10 total)
            deep_parent = ParentNode("div", [deep_parent])

        # Generate the HTML
        result = deep_parent.to_html()

        # Construct the expected HTML
        expected = "<div>" * 10 + "Deep content" + "</div>" * 10

        # Assert that the generated HTML matches the expectation
        self.assertEqual(result, expected)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            invalid_node = ParentNode(None, [])
            invalid_node.to_html()


if __name__ == "__main__":
    unittest.main()


    

    