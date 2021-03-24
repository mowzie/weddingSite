import os.path
import json
from flask import Flask, send_from_directory, url_for, redirect, flash, make_response
from flask import render_template, request
from flask_mail import Mail, Message
import logging
from datetime import datetime



delta = datetime(2021, 8, 21, 13) - datetime.now()

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL'],
    "MAIL_PASSWORD": os.environ['PASSWRD']
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html', days=delta.days, email=app.config.get("MAIL_USERNAME"), passwrd=app.config.get("MAIL_PASSWORD"))

@app.route("/thankyou.html")
def thankyou():
    return render_template('/thankyou.html', days=delta.days)

@app.route("/travel.html")
def travel():
    return render_template('/travel.html', days=delta.days)

@app.route("/story.html")
def story():
    return render_template('/story.html', days=delta.days)

@app.route("/photos.html")
def photos():
    return render_template('/photos.html', days=delta.days)

@app.route("/registry.html")
def registry():
    return render_template('/registry.html', days=delta.days)

@app.route('/rsvp.html', methods=['GET', 'POST'])
def rsvp():
	error = None
	formfilled = request.cookies.get('rsvpstat')
	if formfilled == '1':
		return redirect(url_for('thankyou'))
	if request.method == 'POST':
		if 'inputName' in request.form:
			if request.form['inputName'] == '':
				error = "Name field cannot be blank."
				return render_template('rsvp.html', error=error)
			else:
				inputName = request.form['inputName']
		if 'inputGuest' in request.form:
			inputGuest = request.form['inputGuest']
		if 'inputEmail' in request.form:
			inputEmail = request.form['inputEmail']
		if 'decision' in request.form:
			inputDecision = request.form['decision']
		if 'inputComment' in request.form:
			inputComment = request.form['inputComment']

		with app.app_context():
			msg = Message(subject="Wedding RSVP",
			sender=app.config.get("MAIL_USERNAME"),
			recipients=["the.littkes@gmail.com"],
			body=(f"From:     {inputName}\n"
				  f"And:      {inputGuest}\n"
			      f"Email:    {inputEmail}\n"
				  f"Question: {inputComment}\n"
				  f"Response: {inputDecision}"))
		mail.send(msg)
		resp = make_response(redirect(url_for('thankyou')))
		resp.set_cookie('rsvpstat', '1')
		return resp
	return render_template('rsvp.html', days=delta.days, error=error)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', days=delta.days), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
