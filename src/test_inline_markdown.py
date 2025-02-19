import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes,
)


class TestInLineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )


    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )


    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )



    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )



    def test_extract_markdown_image(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)")
        self.assertListEqual([
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )



    def test_extract_markdown_link_and_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        image_matches = extract_markdown_images(text)
        assert image_matches == [("image", "https://i.imgur.com/zjjcJKZ.png")]
        link_matches = extract_markdown_links(text)
        assert link_matches == [("link", "https://boot.dev")]



    def test_extract_markdown_with_no_matches(self):
        text = "This is plain text with no markdown links or images"
        assert extract_markdown_images(text) == []
        assert extract_markdown_links(text) == []



    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://www.example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                              TextNode("image", TextType.IMAGE, "https://www.example.com/image.png")], new_nodes)
        

    def test_single_image(self):
        node = TextNode("![image](https://www.example.com/image.png)", TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://www.example.com/image.png")], new_node)


    def test_split_multiple_images(self):
        node = TextNode("This is text with an ![image](https://www.example.com/image.png) and ![another image](https://www.example.com/another_image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                             TextNode("image", TextType.IMAGE, "https://www.example.com/image.png"),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("another image", TextType.IMAGE, "https://www.example.com/another_image.png")], new_nodes)
        

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT),
                              TextNode("link", TextType.LINK, "https://www.example.com")], new_nodes)
        

    def test_single_link(self):
        node = TextNode("[link](https://www.example.com)", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://www.example.com")], new_node)


    def test_split_multiple_links(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another link](https://www.example2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT),
                              TextNode("link", TextType.LINK, "https://www.example.com"),
                              TextNode(" and ", TextType.TEXT),
                              TextNode("another link", TextType.LINK, "https://www.example2.com")], new_nodes)
        

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),], nodes)




if __name__ == "__main__":
    unittest.main()