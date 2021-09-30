#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.allAuthors = []
        self.allBooks = []
        with open(books_csv_file_name, 'r') as csvfile:
            readdata = csv.reader(csvfile)
            for row in readdata:
                newAuthors = []
                authorNames = row[-1].split(' and ')
                for name in authorNames:
                    name = name.split(' ')
                    surname = name[-2]
                    givenName = name[:-2]
                    firstName = ''
                    for i in givenName:
                        firstName += i+ ' '
                    firstName = firstName[:-1]
                    years = name[-1].split('-')
                    startYear = years[0][1:]
                    if startYear == '':
                        startYear = None
                    else:
                        startYear = int(startYear)
                    endYear = years[1][:-1]
                    if endYear == '':
                        endYear = None
                    else:
                        endYear = int(endYear)
                    newAuthor = Author(surname, firstName, startYear, endYear)
                    
                    if newAuthor not in self.allAuthors:
                        self.allAuthors.append(newAuthor)
    
                
                newBook = Book(row[0], int(row[1]), newAuthors)
                self.allBooks.append(newBook)
  

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        if search_text == None:
            return sorted(self.allAuthors, key = lambda x: (x.surname, x.given_name))
        
        results = []
        for author in self.allAuthors:
            fullName = author.given_name + author.surname
            if search_text in fullName:
                results.append(author)
            
        results.sort(key = lambda x: (x.surname, x.given_name))
        return results

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
  
        if search_text != None:
            bookList = []
            for book in self.allBooks:
                if search_text in book.title:
                    bookList.append(book)
        else:
            bookList = self.allBooks
        
        if sort_by == 'year':
            bookList.sort(key = lambda x: (x.year, x.title))
        else:
            bookList.sort(key = lambda x: x.title)
        
        return bookList

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        if start_year == None:
            start_year = 0

        if end_year == None:
            end_year = 3000

        results = []
        for book in self.allBooks:
            if book.publication_year >= start_year and book.publication_year <= end_year:
                results.append(book)
        

        return results.sort(key = lambda x: (x.publication_year, x.title))


test = BooksDataSource('books1.csv')