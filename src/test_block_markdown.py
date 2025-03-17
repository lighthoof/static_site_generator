import unittest

from block_markdown import (BlockType, markdown_to_blocks, check_heading, 
                            check_code_block, check_quote, check_unordered_list, 
                            check_ordered_list, block_to_block_type)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
 This is **bolded** paragraph 


 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 


 - This is a list
- with items 
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    ##############################
    def test_check_heading(self):
        heading1 = "# Heading1"
        heading2 = "## Heading2"
        heading3 = "### Heading3"
        heading4 = "#### Heading4"
        heading5 = "##### Heading5"
        heading6 = "###### Heading6"

        self.assertTrue(check_heading(heading1))
        self.assertTrue(check_heading(heading2))
        self.assertTrue(check_heading(heading3))
        self.assertTrue(check_heading(heading4))
        self.assertTrue(check_heading(heading5))
        self.assertTrue(check_heading(heading6))

    ##############################
    def test_check_malformed_heading(self):
        bad_heading = "###Heading3 # malformed"
        bad_heading2 = "#!Heading1 - malformed"

        self.assertFalse(check_heading(bad_heading))
        self.assertFalse(check_heading(bad_heading2))

    ##############################
    def test_block_to_block_type(self):
        heading = "# Heading"
        code = """```
some code
```"""
        quote = "> some quote"
        unordered = """- first item
- second item"""
        ordered = """1. First list item
2. Second list item
3. Third list item"""
        text = """just some
plain text
in a few lines"""

        self.assertEqual(BlockType.HEADING,block_to_block_type(heading))
        self.assertEqual(BlockType.CODE,block_to_block_type(code))
        self.assertEqual(BlockType.QUOTE,block_to_block_type(quote))
        self.assertEqual(BlockType.UNORDERED,block_to_block_type(unordered))
        self.assertEqual(BlockType.ORDERED,block_to_block_type(ordered))
        self.assertEqual(BlockType.PARAGRAPH,block_to_block_type(text))

    ##############################
    def test_check_code_block(self):
        code_block = """```
some code here
and some here
```"""
        code_block2 = """```
some code here
``` 
and some here
```"""
        self.assertTrue(check_code_block(code_block))
        self.assertTrue(check_code_block(code_block2))

    ##############################
    def test_check_malformed_code_block(self):
        bad_code_block = """```
some code here
and some here
``` but not here"""

        bad_code_block2 = """```
some code here
and some here
``` but not here``"""

        self.assertFalse(check_code_block(bad_code_block))
        self.assertFalse(check_code_block(bad_code_block2))

    ##############################
    def test_check_quote(self):
        quote = """> Some quoted line here
> and another one here
> and some more"""
        quote2 = "> One line quote"

        self.assertTrue(check_quote(quote))
        self.assertTrue(check_quote(quote2))

    ##############################
    def test_check_malformed_quote(self):
        bad_quote = """> Some quoted line here
but not another one here
> and some more"""
        bad_quote2 = "!> One line bad quote"

        self.assertFalse(check_quote(bad_quote))
        self.assertFalse(check_quote(bad_quote2))

    ##############################
    def test_check_unordered_list(self):
        list = """- First list item
- Second list item
- Third list item"""
        list2 = "- One line list"

        self.assertTrue(check_unordered_list(list))
        self.assertTrue(check_unordered_list(list2))

        ##############################
    def test_check_malformed_unordered_list(self):
        bad_list = """-First list item
- Second list item
- Third list item"""
        bad_list2 = """- First list item
-. Second list item
- Third list item"""

        self.assertFalse(check_unordered_list(bad_list))
        self.assertFalse(check_unordered_list(bad_list2))

    ##############################
    def test_check_ordered_list(self):
        list = """1. First list item
2. Second list item
3. Third list item"""
        list2 = "1. One line list"

        self.assertTrue(check_ordered_list(list))
        self.assertTrue(check_ordered_list(list2))

        ##############################
    def test_check_malformed_ordered_list(self):
        bad_list = """1.First list item
2. Second list item
3. Third list item"""
        bad_list2 = """1 First list item
2 Second list item
3 Third list item"""

        self.assertFalse(check_ordered_list(bad_list))
        self.assertFalse(check_ordered_list(bad_list2))