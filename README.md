[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7124964&assignment_repo_type=AssignmentRepo)
# COMP0034 Coursework 2
## Techinical information
### Repository URL
[Repository](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1.git)     
[Dash App video](https://www.youtube.com/watch?v=774rWQp11oo)

## Additional features implementation
Our group has tried to implement 2 additional features to the app, one is the user profiles with moore extensive details with photos, which has been succesfully implemented, and another is the password reset with email integration which failed to work. And below is the explanation of the password reset feature:

### <li> Brief explain what you were tring to achieve
I was trying to implement a feature to reset the password via the email. By clicking the 'Forgot Your Password? Click to Reset It' link on the login page, it will redirect the user to the reset_password_request page to ask for the user's email address and send a password reset email to that address. In the email it contains the url link to the reset_password page for entering the new password to submit. </li>

### <li> Explain what isn't working and if you know it, the reason and what you did try and resolve it:
The issue is after entering the email address on the reset_password_request page the email fails to send to the user. The functions of sending email in my code are:
```
def send_async_email(current_app, msg):
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[OpenAirQuality] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

```

After run the code a RuntimeError is raised:  
```
RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
to interface with the current application object in some way. To solve
this, set up an application context with app.app_context().  See the
documentation for more information.
```

In the above text, it mentioned to add "with app.app_context()" to solve the error, so I added that in the send_async_email function in myemail.py, the function therefore becomes:
```
def send_async_email(current_app, msg):
    with app.app_context():
        mail.send(msg)  
```

However, after runing the code again, it raises an import error:
```
ImportError: cannot import name 'auth_bp' from partially initialized module 'my_app.auth.routes' (most likely due to a circular import)
```

Then, I searched online and imported current_app to solve the import error, the code now becomes:
```
def send_async_email(current_app, msg):
    with current_app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working") 
```

This modified code succesfully solved the import error but still encountered the same RuntimeError. I am sure the bug is in "with current_app.app_context():" "mail.send(msg)" these two lines but have no idea about how to solve it.
</li> 

### <li> State what code is in your repo that can be reviewed
The code for the config can be seen in [config.py](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/config.py). 
```
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    ADMINS = ['zcecjp0@gmail.com']
```
  
Mail is imported from flask_mail in [init.py](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/__init__.py):
```
mail = Mail()
```

The code for the forms can be seen in [auth/forms.py](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/auth/forms.py) as the ResetPasswordRequestForm and the ResetPasswordForm:
```
class ResetPasswordRequestForm(FlaskForm):
  ...
class ResetPasswordForm(FlaskForm):
  ...
```
  
The code for the routes can be seen in [auth/routes.py](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/auth/routes.py):
```
@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
  ...

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  ...
```

The functions of sending email is wrapped in a separate file [myemail.py](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/myemail.py):
```
def send_async_email(current_app, msg):
  ...
  
def send_email(subject, sender, recipients, text_body, html_body):
  ...
  
def send_password_reset_email(user):
  ...
  
```

The template pages are in [template/reset_password_request.html](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/templates/reset_password_request.html) and [template/reset_password.html](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/templates/reset_password.html).
  
The email content is in [template/email/reset_password.html](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/templates/email/reset_password.html) in html format and in [template/email/reset_password.txt](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/b1bb0c03879f78297c971e949a972ec029c9ed24/my_app/templates/email/reset_password.txt) in text format.
</li> 


## Evidence of the appropriate use of software engineering and data science tools
### Linter
Code quality issues have been checked and addressed by [Linter](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/main/.github/workflows/pylint.yml). 
    
### Requirements
Install [required python packages](https://github.com/ucl-comp0035/comp0034_cw2_g-group-12-1/blob/203f9688724a23972d00dd80c4bc0d2e73a7a03c/requirements.txt) from the library before running the code.
    
### User stories
The user stories that have been met in this visulization are listed below:
| No. | Persona | User Stories | Priority |
| :---: | :---: | --- | :---: |
| 1 | Commutor | As a website user, I want to be able to run the web app on all versions of Internet Explorer and Netscape browsers so that I can click on any web page to search and use it. | Must have | 
| 2 | Commutor | As a website user, I want to see a icon or background image (e.g. foggy sky, fresh breeze) related to the air qulity. | Could have |  
| 3 | Commutor | As a website user, I want to change the avatar in my profile. | Could have |  
| 4 | Commutor | As a website user, I want to change my password if I accidently forget it. | should have | 
| 5 | Environmentalist | As a website user, I hope that the content of this app can explain the hazards of having poor air quality to call for everyone to protect the environment. | Could have |    
| 6 | Environmentalist | As a website user, I want to see the data of different pollutants so that I can find which contributed most to the air pollution. | Must have |      
| 7 | Developer | As a developer, I want to use a web browser as its user interface. | Must have |   
| 8 | Developer | As a developer, I want the web design program shall be written using standard python to run on different operation system. | Must have |

