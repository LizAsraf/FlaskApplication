# render_template - option of adding HTML files externally by Jinja2 
# flash() function is a useful way to show a message to the user
# url_for function that enables developers to build and generate URLs on a Flask application
# request - asy way to convert Flask request form and args to route parameters
from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app
from app.forms import LoginForm
from app.forms import PostsForm
from app.forms import EditDeleteForm
from app import Users
from app import Posts
import logging
# import mylib
########################################################################################
#################################logger handler#########################################
########################################################################################

# create logger
logger = logging.getLogger('__name__')
level = logging.INFO
logger.setLevel(level)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(level)

# add ch to logger
logger.addHandler(console_handler)

########################################################################################
########################################################################################
########################################################################################
# logging.warning('And this, too')


########################################################################################
############################need login page#############################################
########################################################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def need_to_login():
    try:
        if request.method == 'POST':
            logger.info('Start: login into blog')
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
        else:
            return render_template('login.html', title='Sign In', form=form)    
    except Exception as error:
        logger.error("Oh no! you did not logged in, the error is: " + str(error))

########################################################################################
########################################################################################
########################################################################################

########################################################################################
#################################login page#############################################
########################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            logger.info('Start: login into blog')
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
        else:
            return render_template('login.html', title='Sign In', form=form)
    except Exception as error:
        logger.error("Oh no! you did not logged in, the error is: " + str(error))

#################################login page api########################################

@app.route('/api/login/<firstname>-<lastname>-<username>-<password>', methods=['GET', 'POST'])
def login_api(firstname, lastname, username, password):
    try:
        if request.method == 'POST':
            logger.info('Start: login into blog')
            Users.insert_one({'firstname': firstname, 'lastname': lastname, 'username': username, 'password': password})
            print('new user has been registerd') 
            return redirect(url_for('index', user=username))
        else:
            Users.find(username)
            return redirect(url_for('index', user=username))
    except Exception as error:
        logger.error("Oh no! you did not logged in, the error is: " + str(error))

########################################################################################
########################################################################################
########################################################################################

########################################################################################
################################welcom page#############################################
########################################################################################

@app.route('/index/<user>', methods=['GET'])
def index(user):
    try:
        logger.info('logged in: welcome page')
        print('Welcome') 
        return render_template('index.html', title='Home Page', user=user, posts=Posts.find())
    except Exception as error:
        logger.error("Oh no! you did not logged in, the error is: " + str(error))
########################################################################################
########################################################################################
########################################################################################

########################################################################################
#################################posts page#############################################
########################################################################################

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    try:
        if request.method == 'POST':
            logger.info('posts: new posts page')
            form = PostsForm()
            if form.validate_on_submit():
                flash('your post is {}'.format(
                    form.body.data))
                body = request.form['body']
                Posts.insert_one({'body': body})
                print('new post has been added')
                return render_template('posts.html', title='Posts', form=form, posts=Posts.find())
            return render_template('posts.html', title='Posts', form=form, posts=Posts.find())
        else:
            return render_template('posts.html', title='Posts', form=form, posts=Posts.find())
    except Exception as error:
        logger.error("Oh no! somthing went worng with the posts page, the error is: " + str(error))

#################################posts api#############################################

@app.route('/api/posts/<body>', methods=['GET', 'POST'])
def posts_api(body):
    try:
        if request.method == 'POST':
            logger.info('posts: new posts page')
            Posts.insert_one({'body': body})
            print('new post has been added')
            return render_template('posts.html', title='Posts', posts=Posts.find())
        else:
            return render_template('posts.html', title='Posts', posts=Posts.find(body))
    except Exception as error:
        logger.error("Oh no! somthing went worng with the posts page, the error is: " + str(error))
########################################################################################
########################################################################################
########################################################################################

########################################################################################
#################################edit/delete posts page#################################
########################################################################################

@app.route('/delete_edit', methods=['GET', 'POST'])
def delete_edit():
    try:
        if request.method == 'POST':
            logger.info('delete/edit: posts page')
            form = EditDeleteForm()
            print(request.args.get('body'))
            if "delete" in request.args: 
                print('You have requested to delete some posts')
                return redirect(url_for('delete', name=request.args.get('body')))
            elif "submitedit" in request.args: 
                print('You have requested to edit some posts')
                return redirect(url_for('update', name=request.args.get('body'), replacment=request.args.get('textedit')))
            else:
                return render_template('delete_edit.html', title='Delete or Edit', form=form, posts=Posts.find())
        else:
            return render_template('delete_edit.html', title='Delete or Edit', form=form, posts=Posts.find())
    except Exception as error:
        logger.error("Oh no! somthing went worng with the delete_edit page, the error is: " + str(error))

########################################################################################
########################################################################################
########################################################################################

########################################################################################
#################################delete posts page######################################
########################################################################################
@app.route('/api/delete/<name>', methods=['DELETE'])
@app.route('/delete/<name>', methods=['GET' , 'DELETE'])
def delete(name):
    try:
        if request.method == 'DELETE':
            logger.info('delete: posts page')
            Posts.delete_many({ "body" : name})
            print('instances that contains ',name,' were deleted' )
            return redirect(url_for('delete_edit'))
        else:
            return redirect(url_for('delete_edit'))       
    except Exception as error:
        logger.error("Oh no! somthing went worng with the deletion, the error is: " + str(error))

########################################################################################
########################################################################################
########################################################################################

########################################################################################
#################################edit posts page########################################
########################################################################################
@app.route('/api/update/<name>/<replacment>', methods=['PUT'])
@app.route('/update/<name>/<replacment>', methods=['GET' , 'PUT'])
def update(name,replacment):
    try:
        if request.method == 'PUT':
            logger.info('edit: posts page')
            Posts.update_many(
                {"body": name },
                    {
                        "$set": { "body" : replacment }
                    }
            )
            print('instances that contains ',name,' were updated to ',replacment )
            return redirect(url_for('delete_edit'))
        else:
            return redirect(url_for('delete_edit'))
    except Exception as error:
        logger.error("Oh no! somthing went worng with the edit page, the error is: " + str(error))