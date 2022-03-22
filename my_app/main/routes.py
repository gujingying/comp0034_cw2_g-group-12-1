import os
import pandas as pd

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from my_app import photos, db
from my_app.main.forms import ProfileForm
from my_app.models import Profile
from my_app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title="Home")


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('main.update_profile'))
    else:
        return redirect(url_for('main.create_profile'))


@main_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Set the filename for the photo to None, this is the default if the user hasn't chosen to add a profile photo
        filename = None
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                # Save the photo using the global variable photos to get the location to save to
                filename = photos.save(request.files['photo'])
        p = Profile(username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter_by(id=current_user.id).first()
    # https://wtforms.readthedocs.io/en/3.0.x/fields/#wtforms.fields.SelectField fields with dynamic choice
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            profile.photo = filename
        profile.bio = form.bio.data
        profile.username = form.username.data
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=profile.username))
    return render_template('profile.html', form=form)


@main_bp.route('/display_profiles', methods=['POST', 'GET'], defaults={'username': None})
@main_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("Username not found.")
        return redirect(url_for("main.index"))
    urls = []
    for result in results:
        if result.photo:
            url = photos.url(result.photo)
            urls.append(url)
    return render_template('display_profile.html', profiles=zip(results, urls))
