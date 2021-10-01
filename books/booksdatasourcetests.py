'''
   booksdatasourcetest.py
   Emily Litton, Amir Al-Sheikh, 27 September 2021

   This program runs tests on booksourcedata.py. 
'''

import booksdatasource
import unittest
from booksdatasource import Author
from booksdatasource import Book

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_author_search(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors()
        self.assertTrue(len(authors) == 4)
        self.assertTrue(authors[0] == Author('Christie', 'Agatha'))

    def test_author_tiebreak(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest2.csv')
        authors = self.data_source.authors('bront')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë', 'Ann'))
        self.assertTrue(authors[2]== Author('Brontë', 'Emily'))

    def test_author_text_search(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors("c")
        self.assertTrue(authors[0] == Author('Christie', 'Agatha'))
        self.assertTrue(authors[2] == Author('Willis', 'Connie'))

    def test_book_search(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books()
        self.assertTrue(len(books) == 5)
        self.assertTrue(books[3] == Book('Blackout'))

    def test_book_text_search(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books("b")
        self.assertTrue(books[0] == Book("Beloved"))
        self.assertTrue(books[1] == Book("Blackout"))

    def test_book_default_sort(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest2.csv')
        books = self.data_source.books("w", "table")
        self.assertTrue(books[0] == Book("A Wild Sheep Chase"))
        self.assertTrue(books[1] == Book("The Tenant of Wildfell Hall"))

    def test_book_year_sort(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest2.csv')
        books = self.data_source.books("th", "year")
        self.assertTrue(books[0] == Book('Wuthering Heights'))
        self.assertTrue(books[2] == Book('Thief of Time'))

    def test_years_inclusive(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest2.csv')
        books = books = self.data_source.books_between_years(1847, 1848)
        self.assertTrue(books[0] == Book('Wuthering Heights'))
        self.assertTrue(books[1] == Book('The Tenant of Wildfell Hall'))

    def test_years_start(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books_between_years(1987)
        self.assertTrue(books[0] == Book("Beloved"))
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[2] == Book("Blackout"))

    def test_no_years(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books_between_years()
        self.assertTrue(len(books) == 5)

    def test_no_start(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books_between_years(None, 2000)
        self.assertTrue(books[1] == Book("And Then There Were None"))
    
    def test_same_book(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books()
        self.assertTrue(books[0].__eq__(books[0]))

    def test_diff_books(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        books = self.data_source.books()
        self.assertFalse(books[0].__eq__(books[1]))
    
    def test_same_auth(self):
        self.data_source = booksdatasource.BooksDataSource('booksTest.csv')
        authors = self.data_source.authors()
        self.assertTrue(authors[0].__eq__(authors[0]))
    
if __name__ == '__main__':
    unittest.main()
