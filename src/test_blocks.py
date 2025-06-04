import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
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


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("- Unordered list"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(block_to_block_type("1. Ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
# Heading

## Subheading

### Sub-subheading

# Heading with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><h2>Subheading</h2><h3>Sub-subheading</h3><h1>Heading with <b>bold</b> text</h1></div>",
        )

    def test_quote(self):
        md = """
> This is a quote

> This is another quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote><blockquote>This is another quote</blockquote></div>",
        )
        
    def test_multiple_quotes(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote></div>',
        )

    def test_unordered_list(self):
        md = """
- This is an unordered list item
- Another item

- Yet another item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list item</li><li>Another item</li></ul><ul><li>Yet another item</li></ul></div>",
        )
    
    def test_unordered_list_with_nested_items(self):
        md = """
- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><a href=\"/blog/glorfindel\">Why Glorfindel is More Impressive than Legolas</a></li><li><a href=\"/blog/tom\">Why Tom Bombadil Was a Mistake</a></li><li><a href=\"/blog/majesty\">The Unparalleled Majesty of \"The Lord of the Rings\"</a></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is an ordered list item
2. Another item
3. Yet another item

1. This is a new ordered list item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list item</li><li>Another item</li><li>Yet another item</li></ol><ol><li>This is a new ordered list item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
