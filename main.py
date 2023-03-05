from flask_login import login_user, login_required, logout_user
from cfg import *
from DB.Models import *
from forms import *
from flask import render_template, redirect, url_for, flash

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# создаем представление для логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # ищем пользователя в базе данных
        user = User.query.filter_by(email=form.email.data).first()
        # проверяем правильность пароля
        if user and user.check_password(form.password.data):
            # логиним пользователя
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))


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

        flash('You have successfully registered!', 'success')

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


if __name__ == '__main__':
    app.run(debug=True)
