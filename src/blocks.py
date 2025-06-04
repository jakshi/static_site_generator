from enum import Enum

from icecream import ic

from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for raw_block in raw_blocks:
        striped_block = raw_block.strip()
        if striped_block:
            blocks.append(striped_block)
    return blocks


def block_to_block_type(markdown_block):
    if markdown_block.startswith("#"):
        return BlockType.HEADING
    elif markdown_block.startswith("```"):
        return BlockType.CODE
    elif markdown_block.startswith(">"):
        return BlockType.QUOTE
    elif markdown_block.startswith("-"):
        return BlockType.UNORDERED_LIST
    elif markdown_block[0].isdigit() and markdown_block[1] == ".":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                block_strip_newlines = collapse_paragraph(block)
                html_blocks.append(
                    ParentNode("p", text_to_children(block_strip_newlines))
                )
            case BlockType.HEADING:
                block_strip_heading_sign, level = (
                    block.lstrip("#").strip(),
                    block.count("#"),
                )
                html_blocks.append(
                    ParentNode(f"h{level}", text_to_children(block_strip_heading_sign))
                )
            case BlockType.CODE:
                html_blocks.append(
                    ParentNode("pre", [LeafNode("code", strip_code_block(block))])
                )
            case BlockType.QUOTE:
                quotes = block.split("\n")
                block_strip_quote_sign = [
                    quote.lstrip(">").strip() for quote in quotes if quote.strip()
                ]
                block_strip_quote_sign = " ".join(
                    quote for quote in block_strip_quote_sign if quote.strip()
                )
                html_blocks.append(
                    ParentNode("blockquote", text_to_children(block_strip_quote_sign))
                )
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                items = [item.lstrip("-").strip() for item in items if item.strip()]
                list_items = [
                    ParentNode("li", text_to_children(item)) for item in items
                ]
                html_blocks.append(ParentNode("ul", list_items))
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                items = [
                    item.lstrip("0123456789.").strip() for item in items if item.strip()
                ]
                list_items = [
                    ParentNode("li", text_to_children(item)) for item in items
                ]
                html_blocks.append(ParentNode("ol", list_items))
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
    return ParentNode("div", html_blocks)


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in textnodes]
    return html_nodes


def strip_code_block(text):
    lines = text.splitlines(keepends=True)

    kept = [ln for ln in lines if ln.strip() != "```"]

    return "".join(kept)


def collapse_paragraph(paragraph):
    lines = paragraph.splitlines()
    return " ".join(line.strip() for line in lines if line.strip())
