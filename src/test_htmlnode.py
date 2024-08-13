from htmlnode import HTMLNode, LeafNode, ParentNode

import unittest



class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        return self.assertEqual(f'{node}', 'Tag: None, Value: None, Children: None, Props: {}') 
    
    def test_props(self):
        self.maxDiff = None 
        e_node = HTMLNode()
        a_node = HTMLNode(tag = "a", props = { "href" : "http://www.google.com"})
        node = HTMLNode(tag = "h1", children = [e_node, a_node])
        return self.assertEqual(f'{node}', "Tag: h1, Value: None, Children: [Tag: None, Value: None, Children: None, Props: {}, Tag: a, Value: None, Children: None, Props: {'href': 'http://www.google.com'}], Props: {}") 

    def test_all_value(self):
        node = HTMLNode("p", "I came. I saw. I conquered ;)", props = { "id" : "1" })
        return self.assertEqual(f'{node}', 'Tag: p, Value: I came. I saw. I conquered ;), ' + "Children: None, Props: {'id': '1'}")

    def test_all_children_nest(self):
        a_node = HTMLNode()
        b_node = HTMLNode("p", "I came. I saw. I conquered ;)", props = { "id" : "2" })
        c_node = HTMLNode("p", "I came. I cawed. I cumquered ;)", props = { "id" : "3" })
        d_node = HTMLNode("h3", children = [b_node, c_node], props = { "id" : "1" })
        node = HTMLNode("h2", children = [a_node, d_node], props = { "id" : "0" })
        return self.assertEqual(f'{node}', "Tag: h2, Value: None, Children: [Tag: None, Value: None, Children: None, Props: {}, Tag: h3, Value: None, Children: [Tag: p, Value: I came. I saw. I conquered ;), Children: None, Props: {'id': '2'}, Tag: p, Value: I came. I cawed. I cumquered ;), Children: None, Props: {'id': '3'}], Props: {'id': '1'}], Props: {'id': '0'}")

    def test_LeafNode_basic(self):
        l_node = LeafNode(tag = None, value = "Stuff")
        return self.assertEqual("Stuff", l_node.to_html())

    def test_LeafNode_full(self):
        l_node = LeafNode(tag = "b", value = "Get me some bold zaza.", props = {"title" : "THE ZAZA-ING", "id" : "mytitle"})
        return self.assertEqual(l_node.to_html(), '<b title="THE ZAZA-ING" id="mytitle">Get me some bold zaza.</b>')

    def test_LeafNode_Error(self):
        l_node = LeafNode(tag = "i", value = None)
        return self.assertRaises(ValueError, l_node.to_html)

    def test_LeafNode_Empty(self):
        return self.assertRaises(TypeError, LeafNode)

    def test_ParentNode_All(self):
        c_1_1 = LeafNode(tag = "i", value = "fancy italics", props = {"id" : "myi", "title" : "thei"})
        c_1_2 = LeafNode(tag = None, value = "base man")
        c_2_1 = LeafNode(tag = "b", value = "fancy bold", props = {"id" : "myb", "title" : "theb"})
        p_1 = ParentNode(tag = "h2", children = [c_1_2, c_1_1], props = {"id" : "myh", "title" : "theh"})
        p_2 = ParentNode(tag = "h1", children = [p_1, c_2_1])
        return self.assertEqual('<h1><h2 id="myh" title="theh">base man<i id="myi" title="thei">fancy italics</i></h2><b id="myb" title="theb">fancy bold</b></h1>',p_2.to_html())

    def test_ParentNode_None(self):
        return self.assertRaises(ValueError, ParentNode(None, None, None).to_html)
    
    def test_ParentNode_empty_ch(self):
        return self.assertRaises(ValueError, ParentNode("p", [], None).to_html)
    
    #def test_ParentNode_empty_tag(self):
    #    c = LeafNode(tag = "", value = "stuff")
    #    return self.assertRaises(ValueError, ParentNode("", [c], None).to_html)

    def test_ParentNode_None(self):
        return self.assertRaises(ValueError, ParentNode("", [], None).to_html)

    def test_print_stuff(self):
        a = LeafNode(tag = None, value = "Stuff", props = None)
        b = ParentNode(tag = "p", children = [a], props = {"id" : "p1"})
#       print()
#       print()
#       print("Printing Example ParentNode")
#       print(b)
#       print()

if __name__ == "__main__":
    unittest.main()
