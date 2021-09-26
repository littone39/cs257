'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    #tests whether the tiebreak of first name works
    def test_author_tiebreak(self):
        # self.data_source = shorter source
        #self.assertEqual(self.data_source.authors("bronte"), )
        pass

    #tests with incorrect type for search_test
    def test_author_inttype(self):
        self.assertRaises(ValueError, self.data_source.authors, 1)

    def test_author_no_text(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        self.assertTrue(self.data_source.authors() == [])

    def test_author_search(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors("c")
        self.assertTrue(authors[0].surname == "Christie")
        self.assertTrue(authors[2].surname == "Willis")

    def test_years_start(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books_between_years(1987)
        self.assertTrue(books[0].title == "Beloved")
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[2].title == "Blackout")

    def test_no_years(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books_between_years()
        self.assertTrue(len(books) == 5)

if __name__ == '__main__':
    unittest.main()

