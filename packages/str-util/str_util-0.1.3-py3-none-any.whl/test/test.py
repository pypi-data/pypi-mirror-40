import unittest
import doctest
import str_util


class TestStrUtil(unittest.TestCase):
    def test_side_effects(self):
        list = ['B', 'A', 'C', 'C', '']
        length = len(list)
        new_list = str_util.trim(list)
        new_list = str_util.sort(list)
        new_list = str_util.unique(list)
        new_list = str_util.unique(list, True)
        new_list = str_util.lowercase(list)
        new_list = str_util.replace(list, 'A', 'Abe')
        new_list = str_util.replace_substring(list, 'A', 'Abe')

        self.assertEqual(len(list), length)  # Original list has the same length
        self.assertEqual(['B', 'A', 'C', 'C', ''], list)

    def test_to_list(self):
        self.assertEqual(str_util.to_list("Hello"), ['Hello'])
        self.assertEqual(str_util.to_list([]), [])

    def test_to_string(self):
        self.assertEqual(str_util.to_string(1), "1")
        self.assertEqual(str_util.to_string("Hello"), "Hello")
        self.assertEqual(str_util.to_string(None), "None")
        self.assertEqual(str_util.to_string([1, 2, 3]), "[1, 2, 3]")

    def test_is_string(self):
        self.assertTrue(str_util.is_string("Hello"))
        self.assertFalse(str_util.is_string(6))
        self.assertFalse(str_util.is_string(None))
        self.assertFalse(str_util.is_string(["A"]))

    def test_is_list(self):
        self.assertTrue(str_util.is_list(["A"]))
        self.assertTrue(str_util.is_list([]))
        self.assertFalse(str_util.is_list("Hello"))
        self.assertFalse(str_util.is_list("Hello"))

    def test_trim(self):
        self.assertEqual(str_util.trim("A  B C   "), "A B C")
        self.assertEqual(str_util.trim(["A   B C   ", "", "E  "]), ["A B C", "E"])
        string_with_newlines = """   A  B 
            C   """
        self.assertEqual(str_util.trim(string_with_newlines), "A B C")

        self.assertRaises(BaseException, str_util.trim, None)
        self.assertRaises(BaseException, str_util.trim, 1)

    def test_is_empty(self):
        self.assertTrue(str_util.is_empty("      "))
        self.assertTrue(str_util.is_empty(""))
        self.assertTrue(str_util.is_empty(None))

    def test_contains(self):
        self.assertTrue(str_util.contains("Hello World", "Wo"))
        self.assertFalse(str_util.contains("Hello World", "wo"))
        self.assertTrue(str_util.contains("Hello World", "wo", True))

    def test_replace_substring(self):
        self.assertEqual(str_util.replace_substring('c:\\temp', '\\', '/'), "c:/temp")
        self.assertEqual(str_util.replace_substring('c:/temp/*.*', '/', '\\'), "c:\\temp\\*.*")

    def test_word(self):
        self.assertEqual(str_util.word('a b c', 4), '')

    def test_doctest(self):
        suite = unittest.TestSuite()
        suite.addTest(doctest.DocTestSuite("str_util"))
        result = unittest.TextTestRunner().run(suite)
        self.assertTrue(result.wasSuccessful())


if __name__ == '__main__':
    unittest.main()
