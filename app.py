"""Flask app file containg view functions"""

from flask import Flask, render_template, redirect, request, flash, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import UserSignUpForm, UserLoginForm, GetStartedForm, NewTagForm
from models import connect_db, db, User, Tag, SearchItem
from datetime import datetime, timedelta
import json
from news import newsapi, get_articles

app = Flask(__name__)
app.config.from_object('config.Development')

connect_db(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def update_session():
    try:
        #attempt accessing data field only on logged in user
        if current_user.id:
            session['search_history'] = [{"item_id": item.id, "term": item.term} for item in current_user.searches()]
            session['active_tags'] = [{"tag_id": tag.id, "name": tag.name} for tag in current_user.active_tags()]

    except AttributeError:
        None

@login_manager.user_loader
def load_user(user_id):
    """return user object given passed user_id"""
    return User.query.get(user_id)

@app.route('/')
def homepage():
    """render homepage"""
    try:
        return redirect(f'/home?u={current_user.id}')
    except:
        form = GetStartedForm()
        get_started_form = GetStartedForm()
        return render_template('home/home.html', form=form)

@app.route('/get-started', methods=['POST'])
def get_started():
    """submit email for get started and redirect to sign-up page"""
    form = GetStartedForm()
    if form.validate_on_submit():
        user = User.get_started(form.email.data)
        return redirect(f'/sign-up?u={user.id}')
    return redirect('/')

@app.route('/home')
@login_required
def authenticated_homepage():
    """render homepage for logged in user, if user_id does not match 
    current_user.id redirect to proper page"""
    user_id = int(request.args['u'])
    if user_id == current_user.id:
        return render_template('dashboard/dashboard.html', user=current_user)
    return redirect(f'/login')

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    """handle form submission for new user registration"""
    user_id = request.args['u']
    user = User.query.get(user_id)
    form = UserSignUpForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        User.sign_up(user)
        login_user(user, remember=True)
        return redirect('/') #sending a logged in user to the root route should return the dashboard, not home nav
    return render_template('signup/sign-up.html', form=form, user=user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Render login-form or handle form submission"""
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data).first()
        if user:
            if User.authenticate(user, form.password.data):
                login_user(user, remember=True)
                return redirect('/')
    return render_template('login/login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/')

@app.route("/search")
@login_required
def search():
    """return json of news related to search term, a list of all recently searched terms, 
    and a list of all current tags for the logged-in user."""
    term = request.args['term']
    search_item = User.add_search(term, current_user.id)
    update_session()
    try:
        all_articles = get_articles(term)
        if all_articles['status'] == 'error':
            raise
        else:
            return jsonify(total_results=all_articles['totalResults'], articles=all_articles['articles'], item_id=search_item.id, search_history=session["search_history"])
    except:
        None


@app.route("/search/delete", methods=["POST"])
@login_required
def delete_search():
    """set SearchItem.display to False for selected term
    so that it no longer displays on the DOM"""
    item_id = int(request.json["item_id"])
    User.remove_search(item_id)
    update_session()
    return jsonify(session=session["search_history"])

@app.route("/tag/add", methods=['POST'])
@login_required
def add_tag():
    """add tag object using search item if tag does not already exist"""
    try:
        item_id = int(request.json["item_id"])
        selected_item = SearchItem.query.get(item_id)
        name = selected_item.term
        result = User.add_tag(name, current_user.id)
    except:
        result = False

    if result:
        all_articles = get_articles(name)
        if all_articles['status'] == 'error':
            return jsonify(result=False)
        else:
            return jsonify(articles=all_articles['articles'], result=True, tag_id=result.id, tag_name=result.name)
    else:
        return jsonify(result=False)
    
@app.route("/tag/delete", methods=['POST'])
@login_required
def delete_tag():
    """set display column to False for tag object associated with passed id"""
    tag_id = int(request.json["tag_id"])
    tag = Tag.remove_tag(tag_id)
    update_session()
    return jsonify(session=session["active_tags"])

@app.route("/tag/articles")
@login_required
def tag_articles():
    """set display column to False for tag object associated with passed id"""
    tag_id = int(request.args["tag_id"])
    tag_name = Tag.query.get(tag_id).name
    all_articles = get_articles(tag_name)
    if all_articles['status'] == 'error':
        return jsonify(result=False)
    else:
        return jsonify(articles=all_articles['articles'], result=True, tag_name=tag_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
