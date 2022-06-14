import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, Response
from flask_bootstrap import Bootstrap
import smtplib
from datetime import datetime

SEND_EMAIL = os.getenv("SEND_EMAIL")
RECEIVE_EMAIL = os.getenv("RECEIVE_EMAIL")
EMAIL_PW = os.getenv("EMAIL_PW")

load_dotenv()

app = Flask(__name__)
Bootstrap(app)

current_year = datetime.now().year


def send_email(user_name, user_email, user_message):
    email = f"Subject: CONTACT FROM PERSONAL SITE\n\n" \
            f"Name: {user_name}\nEmail: {user_email}\nMessage: {user_message}"
    with smtplib.SMTP("smtp-mail.outlook.com") as connection:
        try:
            connection.starttls()
            connection.login(SEND_EMAIL, EMAIL_PW)
            connection.sendmail(SEND_EMAIL, RECEIVE_EMAIL, email)
        except Exception as e:
            print(e, "Send fail")


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method != "POST":
        return render_template("index.html", year=current_year, sent=False)
    else:
        name = request.form['name']
        email = request.form.get("email", False)
        message = request.form.get("message", False)
        send_email(name, email, message)
        return render_template("index.html", year=current_year, sent=True)


if __name__ == "__main__":
    app.run(debug=True)