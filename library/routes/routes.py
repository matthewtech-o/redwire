from library.forms import BookForm, MemberForm
from library import app, db

import requests
import json

from datetime import date
from flask import render_template, redirect, url_for, flash, request
from library.models import Book, Member, BookBorrowed, Transaction
from sqlalchemy import desc
from sqlalchemy import func

@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home_page():
    books_to_borrow = Book.query.filter_by(returned=True).all()
    members_can_borrow = Member.query.all()  # Removed the filter condition
    books_to_return = Book.query.filter_by(returned=False).all()

    return render_template('home.html', member_form=MemberForm(), 
                           book_form=BookForm(), 
                           books_to_borrow=books_to_borrow, 
                           members_can_borrow=members_can_borrow, 
                           books_to_return=books_to_return, book=False)


@app.route('/reports', methods=['GET'])
def report_page():
    members_count = Member.query.count()
    books_count = Book.query.count()

    popular_books = db.session.query(Book, func.count(BookBorrowed.book).label('borrow_count')) \
                              .join(BookBorrowed, Book.id == BookBorrowed.book) \
                              .group_by(Book.id) \
                              .order_by(desc('borrow_count')) \
                              .limit(10).all()

    book_title = [book[0].title for book in popular_books]
    book_count = [book[1] for book in popular_books]

    # Get members' names from your database and put them in a list
    members_name = [member.member_name for member in Member.query.all()]

    return render_template("reports.html", members=members_count, books=books_count,
                           book_title=book_title, book_count=book_count, members_name=members_name)




                           
                           
                           
#@app.route('/reports', methods=['GET', 'POST'])
#def report_page():
 #   books = Book.query.all()
  #  members = Member.query.all()
    
   # popular_books = db.session.query(
    #    Book,
     #   func.count(BookBorrowed.book).label('borrow_count')
 #   ).join(BookBorrowed).group_by(Book).order_by(func.count(BookBorrowed.book).desc()).limit(10).all()
    
   # popular_books_title = [book.Book.title[:20] for book in popular_books]
  #  books_count = [book.borrow_count for book in popular_books]

 #   popular_books_title_json = json.dumps(popular_books_title)
#    books_count_json = json.dumps(books_count)

  #  return render_template("reports.html", members=members, 
 #                          books=books, book_title=popular_books_title_json, 
#                           book_count=books_count_json)

