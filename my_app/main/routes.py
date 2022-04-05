from datetime import datetime, timedelta

import requests as requests
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from my_app import photos, db
from my_app.main.forms import ProfileForm, UpdatePhotoForm
from my_app.models import Profile
from my_app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        flash('Welcome back, ' + current_user.first_name + '!')
    #return render_template('index.html', title="Home")

    api_key = '424dec4cf6034b2d8f81225fd670d72d'  # place your API key here
    search = 'air quality'
    newest = datetime.today().strftime('%Y-%m-%d')
    oldest = (datetime.today() - timedelta(hours=1)).strftime('%Y-%m-%d')
    sort_by = 'publishedAt'
    url = f'https://newsapi.org/v2/everything?q={search}&from={oldest}&to={newest}&sortBy={sort_by}'

    response = requests.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(api_key)
    })
    news = response.json()

    return render_template('index.html', title='Home page', news=news)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('main.display_profiles',id = profile.user_id))
    else:
        return redirect(url_for('main.create_profile'))


@main_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Set the filename for the photo to None,
        # this is the default if the user hasn't chosen to add a profile photo
        filename = None
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                # Save the photo using the global variable photos to get the location to save
                filename = photos.save(request.files['photo'])
        p = Profile(username=form.username.data, photo=filename,
                    bio=form.bio.data, gender=form.gender.data,
                    user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.display_profiles', id=p.user_id))
    return render_template('profile.html', form=form)


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)
    if request.method == 'POST'and form.validate_on_submit():
        profile.bio = request.form['bio']
        profile.username = request.form['username']
        profile.gender = request.form['gender']
        profile.bio = form.bio.data
        profile.username = form.username.data
        profile.gender = form.gender.data
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('main.update_profile'))
    return render_template('updateprofile.html', form=form, filename=profile.photo)

@main_bp.route('/update_photo', methods=['GET', 'POST'])
@login_required
def update_photo():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter_by(id=current_user.id).first()
    form = UpdatePhotoForm(obj=profile)
    if request.method == 'POST'and form.validate_on_submit():
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            profile.photo = filename
        db.session.commit()
        flash('Your profile photo has been updated!')
        return redirect(url_for('main.update_photo'))
    return render_template('updatephoto.html', form=form, filename=profile.photo)


@main_bp.route('/display_profiles/<id>', methods=['POST', 'GET'])
@login_required
def display_profiles(id):
    results = None
    if id is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.id.contains(term)).all()
    else:
        results = Profile.query.filter_by(id=id).all()
    if not results:
        flash("Id not found.")
        return redirect(url_for("main.index"))
    urls = []
    for result in results:
        if result.photo:
            url = url_for('static', filename='img/'+result.photo)
            urls.append(url)
    return render_template('display_profile.html',id=id, profiles=zip(results, urls))


