''' Command line interface for booksdatasource.py
'''
import booksdatasource
import sys
import argparse

class Books:
    def __init__(self):
        self.book_data = booksdatasource.BooksDataSource('books1.csv')
        self.args = sys.argv 

    def search_authors(self, search_text):
        return self.book_data.authors(search_text)

    def search_books(self, search_text, sort_type):
        return self.book_data.authors(search_text, sort_type)

    def search_years(self, start_year, end_year):
        return self.book_data.books_between_years(start_year, end_year)

    def print_usage(self):
        usage = open('usage.txt', 'r')
        usage_statement = usage.read()
        print(usage_statement)


def main():
    mySearch = Books()
    if len(mySearch.args) == 0:
        mySearch.print_usage()
    #switch for rest of the statements

if __name__ == "__main__":
    main()

