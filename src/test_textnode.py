import unittest
from textnode import TextNode, TextType

# Unit tests

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
        node = TextNode("This is a test of = equal text", TextType.NORMAL)
        node2 = TextNode("This is a test of not = text", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    



if __name__ == "__main__":
    unittest.main()