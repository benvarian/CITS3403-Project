from audioop import avg
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from sqlalchemy import Numeric
from app.models import Statistics
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Post
from werkzeug.urls import url_parse
import json
from sqlalchemy.sql.expression import func
from app.game import scrambledLetters, checkWordExists, adminOverwrite
import re
from datetime import date


@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html', title='Welcome')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title='Normal Scrambled')


@app.route('/speed', methods=['GET', 'POST'])
def speed():
    return render_template("speed.html", title='Speed Scrambled')


@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    todayGamesPlayedNormal = Statistics.query.filter(Statistics.game_completed==date.today()).filter(Statistics.gameMode=="normal").count()
    todayGamesPlayedSpeed = Statistics.query.filter(Statistics.game_completed==date.today()).filter(Statistics.gameMode=="speed").count()
    todayAvgNormalScore = db.session.query(db.func.round(db.func.avg(Statistics.score),0)).filter(Statistics.gameMode == 'normal').filter(Statistics.game_completed==date.today()).first()
    todayAvgSpeedScore = db.session.query(db.func.round(db.func.avg(Statistics.score),0)).filter(Statistics.gameMode == 'speed').filter(Statistics.game_completed==date.today()).first()

    if todayAvgSpeedScore[0] == None:
        todayAvgSpeedScore = list(filter(None, todayAvgSpeedScore))
        todayAvgSpeedScore = 0
    else:
        todayAvgSpeedScore = int(todayAvgSpeedScore[0])
    if todayAvgNormalScore[0] == None:
        todayAvgNormalScore = list(filter(None,avgNormalScore))
        todayAvgNormalScore = 0
    else:
        todayAvgNormalScore = int(todayAvgNormalScore[0])
    top10 = Statistics.query.order_by(Statistics.score.desc()).limit(10).all()
    return render_template('leaderboard.html', stats=top10, todayAvgNormalScore=todayAvgNormalScore,
            todayAvgSpeedScore=todayAvgSpeedScore, todayGamesPlayedNormal=todayGamesPlayedNormal, todayGamesPlayedSpeed=todayGamesPlayedSpeed)


@login_required
@app.route('/statistics/<username>', methods=['GET', 'POST'])
def stats(username):
    stats = Statistics.query.filter_by(
        userId=username).order_by(Statistics.score).all()
    averagegameScore = db.session.query(db.func.round(db.func.avg(Statistics.score)),0).outerjoin(
        User, User.username == Statistics.userId).group_by(Statistics.userId).filter(Statistics.userId == username).first()
    scoresforNormalData = db.session.query(Statistics.score, Statistics.game_completed).outerjoin(
        User, User.username == Statistics.userId).filter(Statistics.userId == username).filter(Statistics.gameMode == "normal").all()
    scoresforSpeedData = db.session.query(Statistics.score, Statistics.game_completed).outerjoin(
        User, User.username == Statistics.userId).filter(Statistics.userId == username).filter(Statistics.gameMode == "speed").all()
    datesofSubmissions = db.session.query(Statistics.game_completed, Statistics.score).outerjoin(
        User, User.username == Statistics.userId).filter(Statistics.userId == username).order_by(Statistics.game_completed.asc()).limit(10).all()

    gamesPlayedNormal = Statistics.query.filter(Statistics.userId==username).filter(Statistics.gameMode=='normal').count()
    gamesPlayedSpeed = Statistics.query.filter(Statistics.userId==username).filter(Statistics.gameMode=='speed').count()
    avgNormalScore = db.session.query(db.func.round(db.func.avg(Statistics.score),0)).filter(Statistics.userId==username).filter(Statistics.gameMode == 'normal').first()
    avgSpeedScore = db.session.query(db.func.round(db.func.avg(Statistics.score),0)).filter(Statistics.userId==username).filter(Statistics.gameMode == 'speed').first()
    
    user = User.query.filter_by(username=username).first_or_404()
   
    next_url = redirect(url_for('index'))
   
    if avgSpeedScore[0] == None:
        avgSpeedScore = list(filter(None, avgSpeedScore))
        speedModeAverage = 0
    else:
        speedModeAverage = int(avgSpeedScore[0])
    if avgNormalScore[0] == None:
        avgNormalScore = list(filter(None,avgNormalScore))
        avgNormalScore = 0
    else:
        avgNormalScore = int(avgNormalScore[0])
    
    scoresforNormal = []
    for amounts, _ in scoresforNormalData:
        scoresforNormal.append(amounts)
    scoresforSpeed = []
    for amounts, _ in scoresforSpeedData:
        scoresforSpeed.append(amounts)
    dates = []
    for amounts2, _ in datesofSubmissions:
        dates.append(amounts2)
    form = EmptyForm()
    return render_template('statistics.html', next_url=next_url, stats=stats, averagegameScore=json.dumps(averagegameScore, indent=0, sort_keys=True, default=str), datesScore=json.dumps(scoresforNormal), datesofSubmissions=json.dumps(dates, indent=4, sort_keys=True, default=str), speedScores=json.dumps(scoresforSpeed, indent=4, sort_keys=True, default=str), user=user, 
    form=form,gamesPlayedNormal=gamesPlayedNormal,gamesPlayedSpeed=gamesPlayedSpeed,speedModeAverage=speedModeAverage,avgNormalScore=avgNormalScore)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user = str(current_user)
        user = re.sub('User', '', user)
        user = re.sub('<', '', user)
        user = re.sub('>', '', user)
        username = user.strip()
        return redirect(url_for('stats', username=username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('stats', username=user.username))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = date.today()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        user = str(current_user)
        user = re.sub('User', '', user)
        user = re.sub('<', '', user)
        user = re.sub('>', '', user)
        username = user.strip()
        return redirect(url_for('stats',username=username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('stats', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('stats', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/checkword', methods=["GET", "POST"])
def checkWord():
    word = request.args['word']
    checkResponse = jsonify({'outcome': checkWordExists(word)})
    return checkResponse


@app.route('/letters/normal')
def lettersNormal():
    scrambledResponse = scrambledLetters("normal")
    letters = scrambledResponse[0]
    overwrite = scrambledResponse[1]
    lettersResponse = jsonify({'letters': letters, "overwrite":overwrite})
    return lettersResponse


@app.route("/letters/speed")
def lettersSpeed():
    scrambledResponse = scrambledLetters("speed")
    letters = scrambledResponse[0]
    overwrite = scrambledResponse[1]
    lettersResponse = jsonify({'letters': letters, "overwrite":overwrite})
    return lettersResponse

@app.route("/submitscore/normal", methods=["POST"])
def submitNormalScore():
    if current_user.is_authenticated:
        gameStat = json.loads(request.data)
        user = str(current_user)
        user = re.sub('User', '', user)
        user = re.sub('<', '', user)
        user = re.sub('>', '', user)
        username = user.strip()
        stats = Statistics(score=gameStat['score'], gameMode="normal", timeTaken=gameStat['timeTaken'], userId=username)
        print(stats)
        db.session.add(stats)
        db.session.commit()
    return make_response('True', 200)


@app.route("/submitscore/speed", methods=["POST", "GET"])
def submitSpeedScore():
    if current_user.is_authenticated:
        gameStat = json.loads(request.data)
        user = str(current_user)
        user = re.sub('User', '', user)
        user = re.sub('<', '', user)
        user = re.sub('>', '', user)
        username = user.strip()
        stats = Statistics(score=gameStat['speedScore'], gameMode="speed", timeTaken="2:00", userId=username)
        db.session.add(stats)
        db.session.commit()
    return make_response('True', 200)


@app.route("/changeletters/normal", methods=["GET", "POST"])
def changeLettersNormal():
    letters = json.loads(request.data)['letters']
    adminOverwrite(letters, "normal")
    response = make_response('True', 200)
    return response

@app.route("/changeletters/speed", methods=["GET", "POST"])
def changeLettersSpeed():
    letters = json.loads(request.data)['letters']
    adminOverwrite(letters, "speed")
    response = make_response('True', 200)
    return response

@app.route("/alter", methods=["GET", "POST"])
@login_required
def admin():
    gamesPlayedNormal = Statistics.query.filter(Statistics.gameMode=='normal').count()
    gamesPlayedSpeed = Statistics.query.filter(Statistics.gameMode=='speed').count()
    avgNormalScore = db.session.query(db.func.round(db.func.avg(Statistics.score),0)).filter(Statistics.gameMode == 'normal').first()
    avgSpeedScore = db.session.query(db.func.round(db.func.avg(Statistics.score),0)).filter(Statistics.gameMode == 'speed').first()
    if avgSpeedScore[0] == None:
        avgSpeedScore = list(filter(None, avgSpeedScore))
        avgSpeedScore = 0
    else:
        avgSpeedScore = int(avgSpeedScore[0])
    if avgNormalScore[0] == None:
        avgNormalScore = list(filter(None,avgNormalScore))
        avgNormalScore = 0
    else:
        avgNormalScore = int(avgNormalScore[0])
    
    if current_user.is_authenticated:
        user = str(current_user)
        user = re.sub('User', '', user)
        user = re.sub('<', '', user)
        user = re.sub('>', '', user)
        username = user.strip()
        if username == 'admin':
            return render_template("admin.html", gamesPlayedNormal=gamesPlayedNormal, gamesPlayedSpeed=gamesPlayedSpeed, avgNormalScore=avgNormalScore, avgSpeedScore=avgSpeedScore)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
