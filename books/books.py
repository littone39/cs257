''' 
    books.py
    Emily Litton and Amir Al-Sheikh, September 30, 2021

    Command line interface for booksdatasource.py. Allows users to search a database of books. 
'''

import booksdatasource
import sys
import argparse

class Books:
    def __init__(self):
        self.book_data = booksdatasource.BooksDataSource('books1.csv')

    def search_authors(self, search_text=None):
        authors = self.book_data.authors(search_text)
        self.print_authors(authors)
        
    def search_books(self, search_text = None, sort_type=None):
        books = self.book_data.books(search_text, sort_type)
        self.print_books(books)

    def search_years(self, start_year=None, end_year=None):
        books = self.book_data.books_between_years(start_year, end_year)
        self.print_books(books)
               
    def print_usage(self):
        usage = open('usage.txt', 'r')
        usage_statement = usage.read()
        print(usage_statement)
        exit()
        
    def print_books(self, Books):
        for book in Books:
            author_string = ''
            for author in book.authors:
                author_string += author.given_name + ' ' + author.surname + ' and '
            author_string = author_string[:-5]
            print('Title: ' + book.title + ' Publication year:' + str(book.publication_year) + ' Author: ' + author_string)

    def print_authors(self, Authors):
        for author in Authors:
            print('Name: '+author.given_name + ' ' + author.surname + '(' + str(author.birth_year) + '-' +str(author.death_year) + ')')

def main():
    my_search = Books()
    
    if len(sys.argv) == 1:
        my_search.print_usage()
    elif sys.argv[1] == ('-a' or '--author'):
        if len(sys.argv) == 3:
            my_search.search_authors(sys.argv[2])
        elif len(sys.argv) == 2:
            my_search.search_authors()
        else:
            print("Wrong number of arguments given for author search, see usage statement below:")
            my_search.print_usage()
    elif sys.argv[1] == ('-b' or '--book'):
        if len(sys.argv) == 3:
            my_search.search_books(sys.argv[2])
        elif len(sys.argv) == 4:
            my_search.search_books(sys.argv[2],sys.argv[3])
        elif len(sys.argv) == 2:
            my_search.search_books()
        else:
            print("Wrong number of arguments given for book search, see usage statement below:")
            my_search.print_usage() 
    elif sys.argv[1] == ('-y' or '--year'):
        if len(sys.argv) == 4:
            my_search.search_years(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 3:
            my_search.search_years(sys.argv[2])
        elif len(sys.argv) == 2:
            my_search.search_years()
        else:
            print("Wrong number of arguments given for book search, see usage statement below:")
            my_search.print_usage() 
    elif sys.argv[1] == ('-h' or '--help'):
        print('help')
        my_search.print_usage() 
    else:
        my_search.print_usage() 


if __name__ == "__main__":
    main()

