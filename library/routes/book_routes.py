from library import app, db
from library.models import Book, Member, BookBorrowed

import requests
from flask import render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import or_

from library.forms import BookForm  # Updated import to match naming conventions

                           
@app.route('/books', methods=['GET', 'POST'])
def books_page():
    books = Book.query.order_by(Book.id).all()
    form_book = BookForm()  # Updated class name to match naming conventions
    books_to_borrow = Book.query.filter_by(returned=True).all()
    members_can_borrow = Member.query.all()
    books_to_return = Book.query.filter_by(returned=False).all()
    
    if form_book.validate_on_submit():
        book_to_create = Book(
            title=form_book.title.data,
            shelf_location=form_book.shelf_location.data,
            author=form_book.author.data
        )
        db.session.add(book_to_create)
        db.session.commit()
        flash('Successfully created a book', category="success")
        return redirect(request.referrer)

    if form_book.errors:
        for err_msg in form_book.errors.values():
            flash(f'There was an error with creating a book: {err_msg}', category='danger')
    
    return render_template('books/books.html', book_form=form_book, 
                           books=books, length=len(books),
                           books_to_borrow=books_to_borrow, 
                           members_can_borrow=members_can_borrow, 
                           books_to_return=books_to_return)


@app.route('/delete-book/<book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash("Deleted Successfully", category="success")

    except:
        flash("Error in deletion", category="danger")

    return redirect(url_for('books_page'))

@app.route('/update-book/<book_id>', methods=['POST'])
def update_book(book_id):
    book = Book.query.get(book_id)
    new_title = request.form.get("title")
    new_author = request.form.get("author")
    new_shelf_location = request.form.get("shelf_location")  # Added shelf_location
    
    try:
        if new_title != book.title:
            book.title = new_title
        if new_author != book.author:
            book.author = new_author
        if new_shelf_location != book.shelf_location:
            book.shelf_location = new_shelf_location
        db.session.commit()
        flash("Updated successfully", category="success")

    except:
        flash("Nothing to update!", category="warning")

    return redirect(url_for('books_page'))

@app.route('/search', methods=['POST'])
def search_book():
    query = request.form.get("query")
    books = Book.query.filter(
        or_(Book.title.ilike(f'%{query}%'), Book.author.ilike(f'%{query}%'))
    ).all()

    return render_template('books/search_page.html', books=books, length=len(books))

@app.route('/import-from-frappe', methods=['POST'])
def import_books_from_frappe():
    title = request.form.get('title')
    url = f"https://frappe.io/api/method/frappe-library?page=1&title={title}"
    response = requests.get(url)
    if response.status_code == 200:
        books = response.json().get('message', [])
        existing_titles = {book.title for book in Book.query.all()}
        existing_authors = {book.author for book in Book.query.all()}

        for book in books:
            if book['title'] not in existing_titles and book['authors'] not in existing_authors:
                book_to_create = Book(
                    title=book['title'], 
                    shelf_location="",  # You can adjust this based on your needs
                    author=book['authors']
                )
                db.session.add(book_to_create)

        db.session.commit()
        flash("Successfully imported", category="success")
    else:
        flash("No response from the API", category="danger")

    return redirect(url_for('books_page'))

    
@app.route('/book/<int:id>')
def get_borrowing_members(id):
    book = Book.query.get(id)
    book_borrowings = BookBorrowed.query.filter_by(book=id).all()
    members = [{'id': borrowing.member, 'member_name': borrowing.member_name} for borrowing in book_borrowings]

    return jsonify({'members': members})

