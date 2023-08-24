from library import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String, nullable=False, unique=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    shelf_location = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String, nullable=False)
    returned = db.Column(db.Boolean, default=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('member.id'))
  

class BookBorrowed(db.Model):
    __tablename__ = 'book_borrowed'
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)
    book = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String)
    member_name = db.Column(db.String)
    type_of_transaction = db.Column(db.String(length=7), nullable=False)
    date = db.Column(db.Date)
