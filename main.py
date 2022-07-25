from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditor
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField
import smtplib
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['FLASK_APP_KEY']
Bootstrap(app)
ckeditor = CKEditor(app)
date = datetime.now()
year = date.year

MY_EMAIL = "my-email"
APP_PASSWORD = "my-app-password"


class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = EmailField("Your Email", validators=[DataRequired(), Email()])
    body = CKEditorField("Your Message", validators=[DataRequired()])
    submit = SubmitField("Send Email")


@app.route("/")
def home():
    return render_template('index.html', year=year)


@app.route("/about")
def about_page():
    return render_template('about.html', year=year)


@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    form = ContactForm()
    if request.method == "POST":
        print(form.name.data)
        print(form.email.data)
        print(form.body.data)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg=f"Subject:Contact from {form.name.data}\n\n{form.body.data}{form.email.data}")
    return render_template('contact.html', year=year, form=form)


if __name__ == "__main__":
    app.run(debug=True)
