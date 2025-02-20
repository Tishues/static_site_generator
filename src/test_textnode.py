import unittest
from textnode import TextNode, TextType, text_node_to_html_node

# Unit tests
    #TextNode
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("this is to test url=None", TextType.BOLD, url=None)
        node2 = TextNode("this is to test url=None", TextType.BOLD, url="http://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a test of url=SOME", TextType.ITALIC, url="http://example.com")
        node2 = TextNode("This is a test of url=SOME", TextType.ITALIC, url="http://example.com")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a test of = equal text", TextType.TEXT)
        node2 = TextNode("This is a test of not = text", TextType.TEXT)
        self.assertNotEqual(node, node2)

        #text_node_to_html_node.. test from boots
    def test_text_node_to_html_node(self):
            #Test case for plain text
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "Hello, world!"
        assert html_node.props == {}
            #Test bold text
        text_node = TextNode("Hello, world!", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "Hello, world!"
        assert html_node.props == {}
            #Test italic text
        text_node = TextNode("Hello, world!", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "i"
        assert html_node.value == "Hello, world!"
        assert html_node.props == {}
            #Test code text
        text_node = TextNode("Hello, world!", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "code"
        assert html_node.value == "Hello, world!"
        assert html_node.props == {}
            #Test link text
        text_node = TextNode("Example link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.value == "Example link"
        assert html_node.props == {"href": text_node.url}
            #Test image text
        text_node = TextNode("Example image", TextType.IMAGE, "example.jpg")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props == {"src": text_node.url, "alt": text_node.text}
            #Test exceptions
        text_node = TextNode("Hello, world!", "invalid_type")
        self.assertRaises(Exception, text_node_to_html_node, text_node)




if __name__ == "__main__":
    unittest.main()