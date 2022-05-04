from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

class Form(FlaskForm):
    name = StringField("Word:", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    words = ["Hello", "Goodbye", "Happy", "Sad", "", "Red"]
    return render_template("index.html", words = words)

#@app.route('/user/<name>')
#def user(name):
#    return render_template("user.html", user_name = name)

@app.route('/form', methods=['GET', 'POST'])
def name():
    name = None
    form = Form()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Daily Challenge Completed!")
    return render_template("name.html", name = name, form = form)

