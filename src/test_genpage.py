from genpage import ( extract_title,
                    
                    )
import unittest

class TestGenPage(unittest.TestCase):
    
    def test_extract_title_start(self):
        self.assertEqual(
                extract_title("# I am very smart!"),
                "I am very smart!" )
    
    def test_extract_title_faulty(self):
        self.assertRaises(Exception, extract_title, " #\n##awefawef\n###asdfuawef\n#asdfasdf") 

    def test_extract_title_middle(self):
        self.assertEqual(
                extract_title("## I am very smart!\n### I be using improper heading usage\n # This isn't a title\n# But this is! \n bleh"),
                "But this is! " )







if __name__ == "__main__":
    unittest.main()
