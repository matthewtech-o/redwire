from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from library.models import Member, Book, Transaction  # Make sure the import paths are correct

# Form for creating and updating members
class MemberForm(FlaskForm):
    def validate_member_name(self, member_name_to_check):
        member = Member.query.filter_by(member_name=member_name_to_check.data).first()
        if member:
            raise ValidationError('Username already exists! Please try a different Member Name')

    member_name = StringField(label='Member Name', validators=[Length(min=2, max=30), DataRequired()])
    submit = SubmitField(label='Submit')

# Form for creating and updating books
class BookForm(FlaskForm):
    def validate_title(self, title_to_check):
        book = Book.query.filter_by(title=title_to_check.data).first()
        if book:
            raise ValidationError('Book already exists')

    title = StringField(label='Title', validators=[DataRequired()])
    shelf_location = StringField(label='Shelf Location', validators=[DataRequired()])
    author = StringField(label='Author', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
