import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_repr(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "greeting"})
        expected_repr = "HTMLNode(div, Hello, World!, [], {'class': 'greeting'})"

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "greeting", "id": "main"})
        expected_props_html = ' class="greeting" id="main"'
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_empty_props_to_html(self):
        node = HTMLNode("div", "Hello, World!", [], {})
        expected_props_html = ""
        self.assertEqual(node.props_to_html(), expected_props_html)


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("span", "Hello, World!", {"class": "greeting"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span_with_props(self):
        node = LeafNode("span", "Hello, world!", {"class": "greeting"})
        self.assertEqual(node.to_html(), '<span class="greeting">Hello, world!</span>')


class TestParentNode(unittest.TestCase):
    def test_init(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "World")
        node = ParentNode("div", [child1, child2], {"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_children(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "World")
        node = ParentNode("div", [child1, child2], {"class": "greeting"})
        expected_html = (
            '<div class="greeting"><span>Hello</span><span>World</span></div>'
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
