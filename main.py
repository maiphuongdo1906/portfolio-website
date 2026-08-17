from flask import Flask, request, render_template, url_for, send_from_directory
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_ADDRESS_RECEIVER = os.getenv("GMAIL_ADDRESS_RECEIVER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/my-resume")
def resume():
    return render_template("resume.html")

@app.route("/download-resume")
def download():
    return send_from_directory("static", path="files/cv.pdf")
# @app.route("/my-projects")
# def projects():
#     return render_template("projects.html")

@app.route("/my-contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        with smtplib.SMTP(SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=GMAIL_ADDRESS,
                             password=GMAIL_PASSWORD)
            connection.sendmail(from_addr=GMAIL_ADDRESS,
                                to_addrs=GMAIL_ADDRESS_RECEIVER,
                                msg=f"Subject: New Offer!\n\nName: {name}\nEmail: {email}\nPhone number: {phone}\nMessage: {message}")
        return render_template("contact.html", submit=True)
    return render_template("contact.html", submit=False)

if __name__ == "__main__":
    app.run(port=8001, debug=True)