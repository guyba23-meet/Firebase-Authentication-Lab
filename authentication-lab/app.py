from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyC0R4nD4nKpgFc7Va_W3II4sNB9PphslM4",
  "authDomain": "test-c84ce.firebaseapp.com",
  "projectId": "test-c84ce",
  "storageBucket": "test-c84ce.appspot.com",
  "messagingSenderId": "9603805946",
  "appId": "1:9603805946:web:102d33534e94ee90228f43",
  "measurementId": "G-WD6ELP1MJJ",
  "databaseURL": "https://test-c84ce-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("tweets").get().val()

    return render_template('all_tweets.html', tweets = tweets)

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        tweettitle = request.form['tweettitle']
        tweetbody = request.form['tweetbody']
        tweets = {'tweettitle': tweettitle, 'tweetbody': tweetbody}
        db.child("tweets").push(tweets)

    return render_template('add_tweet.html')


@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        full_name = request.form['full_name']
        bio = request.form['bio']
        user = {"full_name": full_name, "username": username, "bio": bio}
        #db.child("Users").child(login_session['user'])
        #['localId'].set(user)
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")




if __name__ == '__main__':
    app.run(debug=True)

