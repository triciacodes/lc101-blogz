from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
# this gives you a view into what is happening in terminal
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# creating a class for the blog
class Blog(db.Model):

    # specify the data fields that should go into columns
    id = db.Column(db.Integer, primary_key=True)     # start with primary ID
    # these are both set as Text instead of String so there is not a character limit
    title = db.Column(db.Text)  # blog title
    post = db.Column(db.Text)   # blog post text
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post 
        self.owner = owner

# creating a class for the users
class User(db.Model):

    # specify the data fields that should go into columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


# DISPLAYS IND BLOG POSTS
@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        ind_post = Blog.query.get(post_id)
        return render_template('ind_post.html', ind_post=ind_post)
    else:
        # queries database for all existing blog entries
        # post_id = request.args.get('id')
        all_blog_posts = Blog.query.all()
        # first of the pair matches to {{}} in for loop in the .html template, second of the pair matches to variable declared above
        return render_template('blog.html', posts=all_blog_posts)


# VALIDATION FOR EMPTY FORM
def empty_val(x):
    if x:
        return True
    else:
        return False

# THIS HANDLES THE REDIRECT (SUCCESS) AND ERROR MESSAGES (FAILURE)

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':

        # THIS CREATES EMPTY STRINGS FOR THE ERROR MESSAGES
        title_error = ""
        blog_entry_error = ""

        # assigning variable to blog title from entry form
        post_title = request.form['blog_title']
        # assigning variable to blog post from entry form
        post_entry = request.form['blog_post']
        # assigning variable to blog post from user signup
        owner = User.query.filter_by(username=session['username']).first()
        # creating a new blog post variable from title and entry
        post_new = Blog(post_title, post_entry, owner)

        # if the title and post entry are not empty, the object will be added
        if empty_val(post_title) and empty_val(post_entry):
            # adding the new post (this matches variable created above) as object 
            db.session.add(post_new)
            # commits new objects to the database
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not empty_val(post_title) and not empty_val(post_entry):
                title_error = "Please enter text for blog title"
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, title_error=title_error)
            elif not empty_val(post_title):
                title_error = "Please enter text for blog title"
                return render_template('new_post.html', title_error=title_error, post_entry=post_entry)
            elif not empty_val(post_entry):
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, post_title=post_title)

    # DISPLAYS NEW BLOG ENTRY FORM
    else:
        return render_template('new_post.html')


@app.route('/signup', methods=['POST', 'GET'])
def add_user():

    if request.method == 'POST':

        # THIS CREATES EMPTY STRINGS FOR THE ERROR MESSAGES

        # assigning variable to username from signup form
        user_name = request.form['username']
        # assigning variable to user password from signup form
        user_password = request.form['password']
        # assigning variable to user password from signup form
        user_password_validate = request.form['password_validate']
        # creating a new blog post variable from title and entry
        user_new = User(user_name, user_password)

        # if the title and post entry are not empty, the object will be added
        #if empty_val(user_name) and empty_val(user_password):
            # adding the new post (this matches variable created above) as object 
        db.session.add(user_new)
            # commits new objects to the database
        db.session.commit()
        return redirect('/newpost')

    # DISPLAYS NEW BLOG ENTRY FORM
    else:
        return render_template('signup.html')
        

# only runs when the main.py file run directly
if __name__ == '__main__':
    app.run()