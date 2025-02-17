import unittest
from block_markdown import (
    markdown_to_blocks, 
    block_to_block_type,
)


class TestBlockMarkdown(unittest.TestCase):
    def my_test_markdown_to_blocks(self):
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


    def test_paragraph(self):
        assert block_to_block_type("just some normal text") == "paragraph"


    def test_code(self):
        assert block_to_block_type("```some text that is code````") == "code"


    def test_heading(self):
        assert block_to_block_type("#### this is a heading") == "heading"

    
    def test_ordered_list(self):
        md =  """1. This
2. Is
3. An
4. Ordered
5. List"""
        assert block_to_block_type(md) == "ordered list"


    def test_unordered_list(self):
        md = """* This
* is
* an unordered list"""
        assert block_to_block_type(md) == "unordered list"

    def test_quote(self):
        assert block_to_block_type("> this is a quote\n> so is this") == "quote"




if __name__ == "__main__":
    unittest.main()