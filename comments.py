#!usr/bin/env python3
import calibre
import csv
import config
from calibre.library import db
from difflib import SequenceMatcher

def similar(a, b):
    #return a[:10].lower() == b[:10].lower()
    return SequenceMatcher(a=a[:15], b=b[:15]).ratio() > 0.7

def find_in_goodreads(books, title):
    ret = None
    for book in books:
        if similar(book['Title'], title):
            ret = book
            break
    return ret

def update_comments_in_calibre_books(goodreads_books):
    db = calibre.library.db(
        config.CALIBRE_LIBRARY_LOCATION
    ).new_api
    book_ids = db.books_in_virtual_library('Read')
    #print(list(mi.standard_field_keys()))
    #['#borrower', '#comments', '#pages', '#read', '#readdate', '#readorder', '#starteddate']
    #print(mi.metadata_for_field('#comments'))
    #['thumbnail', 'cover_data', 'comments', 'device_collections', 'timestamp', 'db_id', 'uuid', 'author_sort_map', 'rating', 'author_sort', 'authors', 'title', 'guide', 'size', 'user_categories', 'application_id', 'author_link_map', 'tags', 'manifest', 'cover', 'title_sort', 'languages', 'last_modified', 'identifiers', 'series_index', 'toc', 'formats', 'lpath', 'mime', 'publication_type', 'book_producer', 'pubdate', 'series', 'publisher', 'rights', 'spine']
    books = []
    matched = 0
    numbooks = 0
    numreviews = 0
    book_to_comment = dict()
    for id in [*book_ids, ][:300]:
        title       = db.field_for('title', id)
        rating      = db.field_for('rating', id)
        authors     = db.field_for('authors', id)
        identifiers = db.field_for('identifiers', id)
        pages       = db.field_for('#pages', id)
        comments    = db.field_for('#comments', id)
        #pages', '#read', '#readdate', '#readorder', '#starteddate
        #'timestamp', 'db_id', 'uuid', 'rating', 'authors',  'tags', 'languages', 'identifiers', 'toc', 'publication_type', 'book_producer', 'pubdate', 'series', 'publisher'
        calibre_txt = f"{id:<3} {str(title):<20.20} {str(authors[0]):20.20} *{str(rating):>4}* {str(pages):4} {len(str(comments)):4}|"
        book = find_in_goodreads(goodreads_books, title)
        numbooks += +1
        if book != None:
            # dict_keys(['Book Id', 'Title', 'Author', 'Author l-f', 'Additional Authors', 'ISBN', 'ISBN13', 'My Rating', 'Average Rating', 'Publisher', 'Binding', 'Number of Pages', 'Year Published', 'Original Publication Year', 'Date Read', 'Date Added', 'Bookshelves', 'Bookshelves with positions', 'Exclusive Shelf', 'My Review', 'Spoiler', 'Private Notes', 'Read Count', 'Recommended For', 'Recommended By', 'Owned Copies', 'Original Purchase Date', 'Original Purchase Location', 'Condition', 'Condition Description', 'BCID']
            gr_id     = book['Book Id']
            gr_title  = book['Title']
            gr_author = book['Author']
            gr_isbn   = book['ISBN']
            gr_rating = book['My Rating']
            gr_review = book['My Review']
            goodreads_txt = f" {gr_title:20.20} {gr_author:20.20} {gr_isbn:15.15} {gr_rating} {len(gr_review)}"
            if len(gr_review)>0:
                numreviews += 1
                print(calibre_txt, goodreads_txt)
                first_comments = '' if comments == None else comments
                book_to_comment[id] = first_comments + '\n\n' + gr_review
            matched += 1
    # The only line that updates Calibre        
    db.set_field('#comments', book_to_comment)
    print(f"Found {numbooks} books. Matched {matched}. New reviews {numreviews}. {(matched/numbooks)*100:2.4}%")

def read_goodreads_csv():
    filename = config.GOODREADS_FILE
    rows=[]
    with open(filename) as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            rows.append(row)
    return rows

goodread_books = read_goodreads_csv()
update_comments_in_calibre_books(goodread_books)
