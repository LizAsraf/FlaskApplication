from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app
from app.forms import LoginForm
from app.forms import PostsForm
from app.forms import TestForm
from app import Users
from app import Posts
import logging
# import mylib

# render_template - option of adding HTML files externally by Jinja2 
# flash() function is a useful way to show a message to the user
# url_for function that enables developers to build and generate URLs on a Flask application
# request - asy way to convert Flask request form and args to route parameters
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('this is a debug massage')
# logging.info('App started')

# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def need_to_login():
    # logging.info('first enterence need to loggin into the app')
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for firstname {}, lastname {}, user {}'.format(
            form.firstname.data, form.lastname.data, form.username.data))
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        Users.insert_one({'firstname': firstname, 'lastname': lastname, 'username': username, 'password': password})
        print('new user has been registerd') 
        return redirect(url_for('index', user=username))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # logging.info('new registeration accured')
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for firstname {}, lastname {}, user {}'.format(
            form.firstname.data, form.lastname.data, form.username.data))
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        Users.insert_one({'firstname': firstname, 'lastname': lastname, 'username': username, 'password': password})
        print('new user has been registerd') 
        return redirect(url_for('index', user=username))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/index/<user>')
def index(user):
    # logging.info('Home page')
    print('Welcome') 
    return render_template('index.html', title='Home Page', user=user, posts=Posts.find())

@app.route('/posts', methods=('GET', 'POST'))
def posts():
    # logging.info('add a new post')
    form = PostsForm()
    if form.validate_on_submit():
        flash('your post is {}'.format(
            form.body.data))
        body = request.form['body']
        Posts.insert_one({'body': body})
        print('new post has been added')
        return render_template('posts.html', title='Posts', form=form, posts=Posts.find())
    return render_template('posts.html', title='Posts', form=form, posts=Posts.find())

@app.route('/test', methods=('GET', 'POST', 'DELETE', 'PUT'))
def test():
    # logging.info('posts edit and delete page')
    form = TestForm()
    print(request.args.get('body'))
    if "delete" in request.args: 
        print('You have requested to delete some posts')
        return redirect(url_for('delete', name=request.args.get('body')))
    elif "submitedit" in request.args: 
        print('You have requested to edit some posts')
        return redirect(url_for('update', name=request.args.get('body'), replacment=request.args.get('textedit')))
    else:
        return render_template('test.html', title='test', form=form, posts=Posts.find())

@app.route('/delete/<name>', methods=['DELETE'])
def delete(name):
    # logging.info('deleting post')
    Posts.delete_many({ "body" : name})
    print('instances that contains ',name,' were deleted' )
    return redirect(url_for('test'))


@app.route('/update/<name>/<replacment>')
def update(name,replacment):
    # logging.info('updating post')
    Posts.update_many(
        {"body": name },
            {
                "$set": { "body" : replacment }
            }
    )
    print('instances that contains ',name,' were updated to ',replacment )
    return redirect(url_for('test'))