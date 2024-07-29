import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        return self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "www.shit.com")
        node2 = TextNode("This is a text node", "bold", "www.shit.com")
        return self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text crime", "italic")
        return self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", "bold", "www.s.com")
        node2 = TextNode("This is a text node", "bold", "www.shit.com")
        return self.assertNotEqual(node, node2)

    def test_neq_def(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "www.notdefault.com")
        return self.assertNotEqual(node, node2)

    def test_neq_txt(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text crime", "italic")
        return self.assertNotEqual(node, node2)
    
    def test_neq_txt_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text crime", "italic")
        return self.assertNotEqual(node, node2)

    def test_neq_all_def(self):
        node = TextNode("This is a text node", "bold", "www.")
        node2 = TextNode("This is a text crime", "italic")
        return self.assertNotEqual(node, node2)

    def test_neq_all(self):
        node = TextNode("This is a text node", "bold", "www")
        node2 = TextNode("This is a text crime", "italic", "www.")
        return self.assertNotEqual(node, node2)
    
    def test_empty_str(self):
        node = TextNode("", "")
        return self.assertEqual(f"{node}", "TextNode(, , None)")
    
    def test_conv_text(self):
         node = TextNode("Hello!", "text")
         html_n = text_node_to_html_node(node)
         return self.assertEqual(html_n.to_html(), "Hello!")

    def test_conv_bold(self):
         node = TextNode("Hello!", "bold")
         html_n = text_node_to_html_node(node)
         return self.assertEqual(html_n.to_html(), "<b>Hello!</b>")

    def test_conv_italic(self):
         node = TextNode("Hello!", "italic")
         html_n = text_node_to_html_node(node)
         return self.assertEqual(html_n.to_html(), "<i>Hello!</i>")

    def test_conv_code(self):
         node = TextNode("Hello!", "code")
         html_n = text_node_to_html_node(node)
         return self.assertEqual(html_n.to_html(), "<code>Hello!</code>")

    def test_conv_link(self):
         node = TextNode("Click here to go to google", "link", "www.google.com")
         html_n = text_node_to_html_node(node)
         return self.assertEqual(html_n.to_html(), '<a href="www.google.com">Click here to go to google</a>')

    def test_conv_image(self):
         node = TextNode("img-alt", "image", "www.google.com/img.img")
         html_n = text_node_to_html_node(node)
         return self.assertEqual(html_n.to_html(), '<img src="www.google.com/img.img" alt="img-alt">')

    def test_conv_invalid_type(self):
         return self.assertRaises(Exception, text_node_to_html_node, TextNode("", "", ""))

    def test_conv_invalid_closure(self):
         node = TextNode("", "bold", None)
         return self.assertRaises(Exception, text_node_to_html_node, node)

    def test_print_all_convs(self):
        print()
        print()
        print("Printing all text to html conversions!")
        node = TextNode("Hello!", "text")
        html_n = text_node_to_html_node(node) # Text
        print(html_n.to_html())
        print()
        print()

        node = TextNode("Hello!", "bold")
        html_n = text_node_to_html_node(node) # Bold
        print(html_n.to_html())
        print()
        print()

        node = TextNode("Hello!", "italic")
        html_n = text_node_to_html_node(node)
        print(html_n.to_html())
        print()
        print()

        node = TextNode("Hello!", "code")
        html_n = text_node_to_html_node(node)
        print(html_n.to_html())
        print()
        print()

        node = TextNode("Click here to go to Google!", "link", "www.google.com")
        html_n = text_node_to_html_node(node)
        print(html_n.to_html())
        print()
        print()

        node = TextNode("Hello-img", "image", "www.google.com/img.img")
        html_n = text_node_to_html_node(node)
        print(html_n.to_html())
        print()
        print()
#
#    def test_text_conv_bold(self):
#        node = TextNode("Hello!", "bold")
#        html_n = text_node_to_html_node(node)
#        print()
#        print(html_n)
#        print()
#        print(html_n.to_html())
#        print()
#
#    def test_text_conv_italic(self):
#        node = TextNode("Hello!", "italic")
#        html_n = text_node_to_html_node(node)
#        print()
#        print(html_n)
#        print()
#        print(html_n.to_html())
#        print()
#
#    def test_text_conv_code(self):
#        node = TextNode("Hello!", "code")
#        html_n = text_node_to_html_node(node)
#        print()
#        print(html_n)
#        print()
#        print(html_n.to_html())
#        print()
#
#    def test_text_conv_link(self):
#        node = TextNode("Click here to go to Google!", "link", "www.google.com")
#        html_n = text_node_to_html_node(node)
#        print()
#        print(html_n)
#        print()
#        print(html_n.to_html())
#        print()
#
#    def test_text_conv_img(self):
#        node = TextNode("Hello-img", "image", "www.google.com/img.img")
#        html_n = text_node_to_html_node(node)
#        print()
#        print(html_n)
#        print()
#        print(html_n.to_html())
#        print()


if __name__ == "__main__":
    unittest.main()
