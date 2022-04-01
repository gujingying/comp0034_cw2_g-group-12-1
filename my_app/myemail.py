from flask_mail import Message
from flask import render_template, current_app
from werkzeug.exceptions import InternalServerError

from my_app import mail
from threading import Thread


def send_async_email(currrent_app, msg):
    with currrent_app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working")


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