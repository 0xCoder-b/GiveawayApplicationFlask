from flask import Flask, render_template, request, send_file, session, url_for, redirect
import instaloader
import requests
from io import BytesIO
import uuid
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = "KurdIcourse1.0"

giveaway = {
    
}
db = {
    
}

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        title = request.form['title']
        uid = str(uuid.uuid4())

        giveaway[uid] = {
            "winner":"",
            "joined":[],
            "title":title,
            "author":session['auth']
        }

        alert = '<div class="alert alert-success">  <a href="giveaway/'+uid+'">لینکی گیڤ ئەوەی</a> :  گیڤەوەی بە سەرکەوتووی دروستکرا</div>'
    else:
        alert = ''
    try:
        verify = request.args['verify']

        if verify=='true':
            badge = True
        elif verify=='false':
            badge = False
        else:
            badge = False
    except:
        badge = False

    try:
        prefix = request.args['prefix']
    except:
        prefix = 'Welcome'


    try:
        profile = session['auth']
    except:
        return redirect('/login')
    


    return render_template('home.html', profile=profile, badge=badge, prefix=prefix, alert=alert)


@app.route('/join')
def join():
    try:
        uid = request.args['id']
        user = session['auth']
    except:
        return redirect('/') 
    if user not in giveaway[uid]['joined']:
        giveaway[uid]['joined'].append(user)
    return redirect('/giveaway/'+uid)

@app.route('/gen')
def gen():
    try:
        uid = request.args['id']
        user = session['auth']
    except:
        return redirect('/') 
    
    if giveaway[uid]['author'] == user:
        winnerUser = random.choice(giveaway[uid]['joined'])
        giveaway[uid]['winner'] = winnerUser
        return redirect('/giveaway/'+uid)
    else:
        return redirect('/')
    


@app.route('/giveaway/<string:id>', methods=['GET', 'POST'])
def givaway_ret(id):

    try:
        verify = request.args['verify']

        if verify=='true':
            badge = True
        elif verify=='false':
            badge = False
        else:
            badge = False
    except:
        badge = False
    try:
        profile = session['auth']
    except:
        return redirect('/login')
    

    if id not in giveaway:
        return redirect('/')
    
    
    return render_template('giveaway.html',uid=id, infoGV=giveaway[id], profile=profile, badge=badge)



@app.route('/login', methods=['GET', 'POST'])
def login():

    alert = ''



    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username in db:
            if db[username] == password:
                session['auth'] = username
            else:
                alert = '<div class="alert alert-danger" role="alert">پاسۆرد هەڵەیە</div>'
        else:
            alert = '<div class="alert alert-danger" role="alert">یوزەرەکە بەردەست نیە !</div>'


    try:
        profile = session['auth']
        return redirect('/')
    except:
        pass
    

    return render_template('login.html', alert=alert)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    alert = ''


    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username not in db:
            db[username] = password
            session['auth'] = username
        else:
            alert = '<div class="alert alert-danger" role="alert">یوزەرەکە گیراوە </div>'
    try:
        profile = session['auth']
        return redirect('/')
    except:
        pass



    return render_template('signup.html', alert=alert)

@app.route('/logout', methods=['GET'])
def logout():

    try:

        profile = session['auth']
        session.pop('auth')

        return redirect('/login')
        
    except:
        return redirect('/login')
    


if __name__ == '__main__':
    app.run(debug=True)


