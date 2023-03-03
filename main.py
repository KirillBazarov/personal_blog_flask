from flask import render_template
from cfg import *
from DB.Models import Post
from forms import CommentForm

@app.route('/post/<slug>')
def show_post(slug):
    # получить пост из базы данных по слагу
    post = Post.query.filter_by(slug=slug).first()

    # создать форму для комментария
    form = CommentForm()

    return render_template('post_detail.html', post=post, form=form)

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# @app.route('/post/<slug>')
# def post_detail(slug):
#     post = Post.get_by_slug(slug)
#     return render_template('post_detail.html', post=post)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# @app.route("/about")
# def about():
#     return render_template('base.html')
#
# @app.route("/blog")
# def blog():
#     return render_template('base.html')
#


# @app.route('/post/<slug>')
# def post_detail(slug):
#     post = Post.query.filter_by(slug=slug).first()
#     return render_template('post_detail.html', post=post)
#
#

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         user = User(username=username, email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return 'User created successfully!'
#     return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
