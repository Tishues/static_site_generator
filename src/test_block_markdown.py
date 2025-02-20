import unittest
from textnode import TextNode, TextType
from block_markdown import (
    markdown_to_blocks, 
    markdown_to_html_node,
    block_to_block_type,
    extract_title,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_my_markdown_to_blocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        test = markdown_to_blocks(text)
        self.assertListEqual(["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"], test)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


    def test_block_to_block_type(self):
        assert block_to_block_type("just some normal text") == block_type_paragraph
        assert block_to_block_type("```some text that is code````") == block_type_code
        assert block_to_block_type("#### this is a heading") == block_type_heading
        md =  """1. This
2. Is
3. An
4. Ordered
5. List"""
        assert block_to_block_type(md) == block_type_ordered_list
        md2 = """* This
* is an
* unordered list"""
        assert block_to_block_type(md) == block_type_ordered_list
        md2 = """- This
- is another
- unordered list"""
        assert block_to_block_type(md2) == block_type_unordered_list
        assert block_to_block_type("> this is a quote\n> so is this") == block_type_quote


    def test_paragraphs(self):
        md = """
This is a **bolded** paragraph
text inside of a p
tag"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                        "<div><p>This is a <b>bolded</b> paragraph text inside of a p tag</p></div>")
        

    def test_paragraphs(self):
        md = """
This is a **bolded** paragraph
text inside of a p
tag


This is a second paragraph with some `code` and *italic*

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                        "<div><p>This is a <b>bolded</b> paragraph text inside of a p tag</p><p>This is a second paragraph with some <code>code</code> and <i>italic</i></p></div>")
        

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. this is an **ordered** list
2. with items
3. and more `items`

* This is a second unordered list
* with two items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                        "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>this is an <b>ordered</b> list</li><li>with items</li><li>and more <code>items</code></li></ol><ul><li>This is a second unordered list</li><li>with two items</li></ul></div>")
        

    def test_headings(self):
        md = """
# This is a h1 heading

this is paragraph text

## this is a h2

###### this is a h6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><h1>This is a h1 heading</h1><p>this is paragraph text</p><h2>this is a h2</h2><h6>this is a h6</h6></div>")
        

    def test_blockquote(self):
        md = """
> This is a blockquote
> block

this is paragraph text

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>")
        

    def test_extract_title(self):
        md = """
# This is a header to be extracted

this is some paragraph text
"""
        node = extract_title(md)
        self.assertEqual(node,
                         "This is a header to be extracted")
        

    def test_extract_no_title(self):
        md = """
This is a header without a leading # to be extracted

this is some paragraph text
"""
        node = extract_title(md)
        self.assertRaises(Exception)


    def test_markdown_to_html_with_link(self):
        markdown_text = "Read my [first post here](/majesty) now!"
        html_node = markdown_to_html_node(markdown_text)
        html = html_node.to_html()
        #print("Generated HTML:", html)  # Add this line
        assert '<a href="/majesty">first post here</a>' in html




if __name__ == "__main__":
    unittest.main()