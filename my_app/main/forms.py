from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from my_app import photos


class ProfileForm(FlaskForm):
    """ Class for the profile form """
    username = StringField(label='Username',
                           validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    gender = SelectField('Gender', choices=[('Female', 'Female'), ('Male', 'Male')])


class UpdateProfileForm(FlaskForm):
    """ Class for the profile form """
    username = StringField(label='Username',
                           validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    gender = SelectField('Gender', choices=[('Female','Female'),('Male','Male')])


class UpdatePhotoForm(FlaskForm):
    """ Class for the profile form """
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
