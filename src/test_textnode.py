from textnode import TextNode,                \
                     text_node_to_html_node,  \
                     split_nodes_delimiter,   \
                     extract_markdown_images, \
                     extract_markdown_links,  \
                     split_nodes_image,       \
                     split_nodes_link,        \
                     text_to_textnodes

import unittest


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

    def test_delim_split_bold(self):
        node = TextNode("**Bold!**", "text")
        n_t  = split_nodes_delimiter([node], "**", "bold")
        return self.assertEqual(text_node_to_html_node(n_t[0]).to_html(), "<b>Bold!</b>")

    def test_delim_split_unmatching(self):
        node = TextNode("**Bold!*", "text")
        return self.assertRaises(Exception, split_nodes_delimiter, [node], "**", "bold")
    
    def test_delim_split_italic(self):
        node = TextNode("*Brash!*", "text")
        n_t  = split_nodes_delimiter([node], "*", "italic")
        return self.assertEqual(text_node_to_html_node(n_t[0]).to_html(), "<i>Brash!</i>")

    def test_delim_split_code(self):
        node = TextNode("`Belongs!`", "text")
        n_t  = split_nodes_delimiter([node], "`", "code")
        return self.assertEqual(text_node_to_html_node(n_t[0]).to_html(), "<code>Belongs!</code>")

    def test_delim_split_all(self):
        n1 = TextNode("I have **Coders** and *maybe* **coders** and `possibly` **coders?** `possibly`", "text")
        pass1 = split_nodes_delimiter([n1], "**", "bold")
        pass2 = split_nodes_delimiter(pass1, "*", "italic")
        pass3 = split_nodes_delimiter(pass2, "`", "code")
        
        string = ""
        for node in pass3:
            string += text_node_to_html_node(node).to_html()

        return self.assertEqual(string, "I have <b>Coders</b> and <i>maybe</i> <b>coders</b> and <code>possibly</code> <b>coders?</b> <code>possibly</code>")

    def test_delim_split_mult(self):
        n1 = TextNode("**in**", "text")
        n2 = TextNode("**the**", "text")
        n3 = TextNode("**Trash!**", "text")

        n_all = split_nodes_delimiter([n1, n2, n3], "**", "bold")
        
        string = ""
        for node in n_all:
            string += text_node_to_html_node(node).to_html()

        return self.assertEqual(string, "<b>in</b><b>the</b><b>Trash!</b>")

    def test_ex_mark_img(self):
        return self.assertEqual(extract_markdown_images("a;lfgihawegfih ![shit](www.image.com/img.png) ![shit2](image.png)"), \
                                                      [("shit","www.image.com/img.png"), ("shit2","image.png")]) 
    
    def test_ex_mark_link(self):
        return self.assertEqual(extract_markdown_links("agwgwggfih  [googs](google.com)"), \
                                                     [("googs","google.com")])

    def test_split_node_img(self):
        n1 = TextNode("[shit](link.com) when i ![shoot](shot.com) let ![shit](chuck.com) [fork](book.com)![sting](stang.com)", "text")
        n2 = TextNode("more images: ![shoot](shot.com)", "text")
        n3 = TextNode("just link: [shoot](shot.com)", "text")
        n4 = TextNode("", "text")
        n5 = TextNode("just text: text", "text")


        n6 = split_nodes_image([n1, n2, n3, n4, n5])
        
        return self.assertEqual("[TextNode([shit](link.com) when i , text, None), TextNode(shoot, image, shot.com), TextNode( let , text, None), TextNode(shit, image, chuck.com), TextNode( [fork](book.com), text, None), TextNode(sting, image, stang.com), TextNode(more images: , text, None), TextNode(shoot, image, shot.com), TextNode(just link: [shoot](shot.com), text, None), TextNode(just text: text, text, None)]" , f'{n6}')
    
    def test_split_node_all(self):
        self.maxDiff = None
        n1 = TextNode("[shit](link.com) when i ![shoot](shot.com) let ![shit](chuck.com) [fork](book.com)![sting](stang.com)", "text")
        n2 = TextNode("more images: ![shoot](shot.com)", "text")
        n3 = TextNode("just link: [shoot](shot.com)", "text")
        n4 = TextNode("", "text")
        n5 = TextNode("just text: text", "text")

        n6 = split_nodes_image([n1, n2, n3, n4, n5])
        n7 = split_nodes_link(n6)
        
        return self.assertEqual("[TextNode(shit, link, link.com), TextNode( when i , text, None), TextNode(shoot, image, shot.com), TextNode( let , text, None), TextNode(shit, image, chuck.com), TextNode( , text, None), TextNode(fork, link, book.com), TextNode(sting, image, stang.com), TextNode(more images: , text, None), TextNode(shoot, image, shot.com), TextNode(just link: , text, None), TextNode(shoot, link, shot.com), TextNode(just text: text, text, None)]", f"{n7}")


    def test_text_to_node(self):
        n = text_to_textnodes("`I start with code` But continue ![fox](c.com) with the *never* **ending** ![relentless](frick.png) prrrsuit of the *maybe* `rich` individuals saying shit like [notimg](nimg.com) that really fricks up my **banana**")

        self.assertEqual("[TextNode(I start with code, code, None), TextNode( But continue , text, None), TextNode(fox, image, c.com), TextNode( with the , text, None), TextNode(never, italic, None), TextNode( , text, None), TextNode(ending, text, None), TextNode( , text, None), TextNode(relentless, image, frick.png), TextNode( prrrsuit of the , text, None), TextNode(maybe, italic, None), TextNode( , text, None), TextNode(rich, code, None), TextNode( individuals saying shit like , text, None), TextNode(notimg, link, nimg.com), TextNode( that really fricks up my , text, None), TextNode(banana, text, None)]",f"{n}")


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
