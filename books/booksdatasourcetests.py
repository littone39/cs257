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


    def test_book_search(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books("b")
        self.assertTrue(books[0].title == "Beloved")
        self.assertTrue(books[1].title == "Blackout")

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

    def test_no_start(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books_between_years(None, 2000)
        self.assertTrue(books[1].surname == "Christie")

    def test_same_book(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books()
        self.assertTrue(books[0].__eq__(books[0]))

    def test_one_book(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books()
        self.assertRaises(ValueError, books[0].__eq__())

    def test_diff_books(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books()
        self.assertFalse(books[0].__eq__(books[1]))

    def test_same_auth(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors()
        self.assertTrue(authors[0].__eq__(authors[0]))

    def test_one_auth(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors()
        self.assertRaises(ValueError, authors[0].__eq__())

    def test_diff_auths(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors()
        self.assertFalse(authors[0].__eq__(authors[1]))

if __name__ == '__main__':
    unittest.main()
