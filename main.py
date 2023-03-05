from flask import render_template
from cfg import *
from DB.Models import *
from forms import CommentForm
from flask import render_template, redirect, url_for
from forms import RegistrationForm


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Create new user
        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


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


if __name__ == '__main__':
    app.run(debug=True)
