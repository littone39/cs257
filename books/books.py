''' 
    books.py
    Emily Litton and Amir Al-Sheikh, September 30, 2021

    Command line interface for booksdatasource.py. Allows users to search a database of books using 
    functionality described in usage.txt. 
'''

import booksdatasource
import argparse

class BookSearchDispatcher:
    def __init__(self):
        #Initialize book class by parsing csv data into Books and Authors
        self.book_data = booksdatasource.BooksDataSource('books1.csv')

    def search_authors(self, search_text=None):
        #searches for authors using given parameteres and prints results
        authors = self.book_data.authors(search_text)
        print("Result of Author search:".upper())
        self.print_authors(authors)
        print('\n')
        
    def search_books(self, search_text = None, sort_type=None):
        #searches for books using given parameters and prints results
        books = self.book_data.books(search_text, sort_type)
        print("Result of Book search:".upper())
        self.print_books(books)
        print('\n')

    def search_years(self, start_year=None, end_year=None):
        #passes parametes book_between_years method and prints results
        books = self.book_data.books_between_years(start_year, end_year)
        print("Result of Books Between Years search:".upper())
        self.print_books(books)
        print('\n')
      
    def print_usage(self):
        #prints usage statement 
        usage = open('usage.txt', 'r')
        usage_statement = usage.read()
        print(usage_statement)
        exit()
        
    def print_books(self, Books):
        #prints list of books formatted '[title] ([year]) by Author(s): [name]'
        for book in Books:
            author_string = ''
            for author in book.authors:
                author_string += author.given_name + ' ' + author.surname + ' and '
            author_string = author_string[:-5]
            print( book.title + ' (' + str(book.publication_year) + ') by ' + author_string)

    def print_authors(self, Authors):
        #prints list of authors formatted '[name] (birth year - death year)'
        for author in Authors:
            print(author.given_name + ' ' + author.surname + ' (' + str(author.birth_year) + '-' +str(author.death_year) + ')')

    def get_parsed_arguments(self):
        parser = argparse.ArgumentParser(description='Searches book database', add_help=False)
        parser.add_argument('-a', '--author', nargs='*', help='tag for searching authors')
        parser.add_argument('-b', '--book', nargs='*', help='tag for searching books')
        parser.add_argument('-y', '--year', nargs='*', help='tag for searching books')
        parser.add_argument('-h', '--help', action='store_true', help='tag for usage')
        parsed_args = parser.parse_args()
        return parsed_args

def main():
    dispatcher = BookSearchDispatcher() #creates instance of BookSearchDispatcher class that will be used to query command line arguments
    
    arguments = dispatcher.get_parsed_arguments()
    printed = False #printed boolean flips to true if any of the command line flags have been triggered
    
    # searches authors if -a or --author is present in command line
    if arguments.author is not None:
        args = arguments.author
        printed = True 
        if len(args) > 1:
            print("Wrong number of arguments given for author search, see usage statement below:")
            dispatcher.print_usage()
        args.append(None) # adds None to the list to avoid indexing into an empty list
        dispatcher.search_authors(args[0])

    if arguments.book is not None:
        printed = True
        args = arguments.book 
        if len(args) > 2:
            print("Wrong number of arguments given for book search, see usage statement below:")
            dispatcher.print_usage()
        args = args + [None,None]
        dispatcher.search_books(args[0], args[1])

    if arguments.year is not None:
        printed = True
        args = arguments.year
        if len(args) > 2:
            print("Wrong number of arguments given for book between year search, see usage statement below:")
            dispatcher.print_usage()
        args = args + [None,None]
        dispatcher.search_years(args[0], args[1])

    if arguments.help or not printed: #print usage statement if help flag indicated or if command line empty
        dispatcher.print_usage()


if __name__ == "__main__":
    main()

