import io
from flask_login import login_user, login_required, logout_user, current_user
from forms import *
from flask_caching import Cache
from flask import render_template, redirect, url_for, flash, request, send_file
from utils import normal_data

login_manager = LoginManager()
login_manager.init_app(app)

cache = Cache(app)


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts.items, pagination=posts, title='Главная страница')


@app.context_processor
def inject_functions():
    return dict(normal_data=normal_data, count_user_posts=User.count_user_posts)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        # проверяем правильность пароля
        if user and user.check_password(form.password.data):
            # логиним пользователя
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('user_profile', user_id=current_user.id))
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
        new_user = User.add_user(name=form.name.data, email=form.email.data, password=form.password.data)
        login_user(new_user)

        flash('You have successfully registered!', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form, title="регистрация")


@app.route('/delete_posts/<slug>', methods=['POST'])
def delete_post(slug):
    # сделать так что бы когда удалял пост удалялись все комменты к посту
    Post.delete_post(slug)
    flash('You have successfully deleted your post!', 'success')

    return redirect(url_for('index'))


@app.route('/delete_comment/<int:id>/<path:slug>', methods=['POST'])
def delete_comment(id, slug):
    Comment.delete_comment_id(id)
    flash('You have successfully deleted your comment!', 'success')

    return redirect(url_for('show_post', slug=slug))

@app.route('/post/<slug>', methods=['GET', 'POST'])
def show_post(slug):
    post = Post.get_by_slug(slug)
    form = CommentForm()
    if form.validate_on_submit():
        Comment.add_comment(content=form.content.data, post_id=post.id, user_id=current_user.id)
        return redirect(url_for('show_post', slug=post.slug))
    return render_template('post_detail.html', title=f"Пост {post.title}", post=post, form=form,
                           user_id=current_user.id)


@app.route('/upload', methods=['POST'])
def upload():
    # Получаем файл из запроса
    file = request.files['file']

    # Читаем данные из файла в байтовый объект
    blob = file.read()

    # Сохраняем байтовый объект в базе данных для пользователя с id=1
    user = User.query.get(current_user.id)
    user.avatar = blob
    db.session.commit()

    # Возвращаем ответ об успешной загрузке
    return redirect(url_for('user_profile', user_id=current_user.id))


@app.route('/avatar/<int:user_id>')
def avatar(user_id):
    user = User.query.get(user_id)
    if user.avatar:
        return send_file(io.BytesIO(user.avatar), mimetype='image/jpeg')
    else:
        return send_file('static/images/default.png', mimetype='image/jpeg')


@app.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    if user_id != current_user.id:
        # Если пользователь пытается зайти на профиль другого пользователя,
        # перенаправляем его на страницу своего профиля
        flash('Вы были перенаправлены на эту страницу т.к пытались перейти на страницу другого пользователя', 'error')
        return redirect(url_for('user_profile', user_id=current_user.id))
    return render_template('profile.html', title=f'профиль {current_user.name}', user_id=user_id)


@app.route("/add", methods=['GET', 'POST'])
def add_page():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, title=form.title.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('show_post', slug=post.slug))
    return render_template('add_post.html', form=form, title = "Добавить пост")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
