import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        if self.text == o.text and self.text_type == o.text_type and self.url == o.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        text = node.text
        node_type = node.text_type
        split_text = text.split(delimiter)
        for i, part in enumerate(split_text):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, node_type))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_links_and_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        old_node_text = old_node.text
        old_node_type = old_node.text_type

        pattern = re.compile(r"(!)?\[(.*?)\]\((.*?)\)")
        last_end = 0

        for m in pattern.finditer(old_node_text):
            if m.start() > last_end:
                text_chunk = old_node_text[last_end : m.start()]
                new_nodes.append(TextNode(text_chunk, old_node_type))
            kind = "image" if m.group(1) else "link"
            label = m.group(2)
            url = m.group(3)
            if kind == "image":
                new_nodes.append(TextNode(label, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(label, TextType.LINK, url))
            last_end = m.end()

        # Append any remaining text after the last match
        if last_end < len(old_node_text):
            text_chunk = old_node_text[last_end:]
            new_nodes.append(TextNode(text_chunk, old_node_type))

    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_links_and_images(old_nodes)


def split_nodes_link(old_nodes):
    return split_nodes_links_and_images(old_nodes)


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    pass1 = split_nodes_links_and_images([node])
    pass2 = []
    for text_chunk in pass1:
        if text_chunk.text_type == TextType.TEXT:
            pass2 += split_nodes_delimiter([text_chunk], "**", TextType.BOLD)
        else:
            pass2.append(text_chunk)
    pass3 = []
    for text_chunk in pass2:
        if text_chunk.text_type == TextType.TEXT:
            pass3 += split_nodes_delimiter([text_chunk], "_", TextType.ITALIC)
        else:
            pass3.append(text_chunk)
    pass4 = []
    for text_chunk in pass3:
        if text_chunk.text_type == TextType.TEXT:
            pass4 += split_nodes_delimiter([text_chunk], "`", TextType.CODE)
        else:
            pass4.append(text_chunk)

    return pass4
