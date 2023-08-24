from library import app, db

import requests

from datetime import date
from flask import render_template, redirect, url_for, flash, request
from library.models import Book, Member, Transaction, BookBorrowed

@app.route('/transactions')
def transactions_page():
    transaction = Transaction.query.order_by('id').all()
    books_to_borrow = Book.query.filter_by(returned=True).all()
    members_can_borrow = Member.query.all()  # Removed the filter condition
    books_to_return = Book.query.filter_by(returned=False).all()
    return render_template('transactions/transactions.html', 
                            transactions=transaction, length=len(transaction), 
                            books_to_borrow=books_to_borrow, 
                            members_can_borrow=members_can_borrow, 
                            books_to_return=books_to_return)

@app.route('/borrow-book', methods=['POST'])
def borrow_book():
    member_requested = request.form.get("member_name")
    book_requested = request.form.get("book_name")
    member = Member.query.get(int(member_requested))
    book = Book.query.get(int(book_requested))

    if book and member:
        borrow = BookBorrowed(book=book.id, member=member.id)
        borrow_book = Transaction(book_name=book.title, 
                                  member_name=member.member_name, 
                                  type_of_transaction="borrow", 
                                  date=date.today())
        db.session.add(borrow_book)
        db.session.add(borrow)
        db.session.commit()
        flash(f"Issued book", category='success')
    else:
        flash(f'Error in borrowing the book', category='danger')

    return redirect(request.referrer)
    
    
@app.route('/return-book', methods=['POST'])
def return_book():
    member_id = request.form.get("member_name")
    book_requested = request.form.get("book_name")
    
    member = Member.query.get(int(member_id))
    book = Book.query.get(int(book_requested))

    if member and book and not book.returned and book.borrower_id == member.id:
        book.returned = True
        book.borrower_id = None
        
        return_transaction = Transaction(
            book_name=book.title,
            member_name=member.member_name,
            type_of_transaction="return",
            date=date.today()
        )
        
        db.session.add(return_transaction)
        db.session.commit()
        
        flash(f"Returned book from {member.member_name}", category='success')
    else:
        flash(f'Error in returning the book', category='danger')

    return redirect(request.referrer)


 


