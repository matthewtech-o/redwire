from library.forms import MemberForm
from library import app, db
from library.models import Book, Member

import requests
from flask import render_template, redirect, url_for, flash, request

@app.route('/members', methods=['GET', 'POST'])
def members_page():
    members = Member.query.order_by(Member.id).all()
    form_member = MemberForm() 
    books_to_borrow = Book.query.filter_by(returned=True).all()
    members_can_borrow = Member.query.all()  # Removed the filter condition
    books_to_return = Book.query.filter_by(returned=False).all()
    
    if form_member.validate_on_submit():
        member_to_create = Member(
            member_name=form_member.member_name.data
        )
        db.session.add(member_to_create)
        db.session.commit()
        flash('Successfully created a member', category="success")
        return redirect(request.referrer)
    
    if form_member.errors:
        for err_msg in form_member.errors.values():
            flash(f'There was an error with creating a Member: {err_msg}', category='danger')
    
    return render_template('members/members.html', member_form=form_member,
                            members=members, length=len(members),
                            books_to_borrow=books_to_borrow, 
                            members_can_borrow=members_can_borrow, 
                            books_to_return=books_to_return)

@app.route('/delete-member/<member_id>', methods=['POST'])
def delete_member(member_id):
    try:
        member = Member.query.get(member_id)
        db.session.delete(member)
        db.session.commit()
        flash("Deleted Successfully", category="success")

    except:
        flash("Error in deletion", category="danger")

    return redirect(url_for('members_page'))

@app.route('/update-member/<member_id>', methods=['POST'])
def update_member(member_id):
    member = Member.query.get(member_id)
    new_member_name = request.form.get("member_name")

    try:
        if new_member_name != member.member_name:
            member.member_name = new_member_name
        db.session.commit()
        flash("Updated Successfully!", category="success")

    except:
        flash("Failed to update", category="danger")

    return redirect(url_for('members_page'))
