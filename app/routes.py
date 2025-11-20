from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
    current_app,
)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import date
from functools import wraps
from urllib.parse import urlparse, urljoin
import bleach

from .extensions import db, cache, limiter
from .models import User, BlogPost, Comment
from .forms import RegistrationForm, LoginForm, CommentForm, CreatePostForm, ContactForm
from .utils import save_contact_to_database, send_contact_email

main_bp = Blueprint("main", __name__)

ALLOWED_TAGS = [
    "p",
    "b",
    "i",
    "u",
    "em",
    "strong",
    "a",
    "h1",
    "h2",
    "h3",
    "ul",
    "ol",
    "li",
    "blockquote",
    "code",
    "pre",
    "img",
]
ALLOWED_ATTRS = {
    "*": ["class", "style"],
    "a": ["href", "rel", "target"],
    "img": ["src", "alt", "style", "width", "height"],
}


def is_safe_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            flash("Admin access required", "error")
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)

    return decorated_function


# Error Handlers
@main_bp.app_errorhandler(404)
def not_found(error):
    return render_template("error/404.html", error=error), 404


@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("error/500.html", error=error), 500


# Routes
@main_bp.route("/")
def home():
    try:
        page = request.args.get("page", 1, type=int)
        posts = db.paginate(
            select(BlogPost).order_by(BlogPost.date.desc()), page=page, per_page=5
        )
        return render_template("index.html", posts=posts)
    except Exception as e:
        current_app.logger.error(f"Home error: {e}")
        return render_template("error/500.html"), 500


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User()
            user.name = form.data["name"].strip().title()
            user.email = form.data["email"]
            user.password = generate_password_hash(
                form.data["password"], "pbkdf2:sha256:600000"
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Registration successful! Welcome!", "success")
            return redirect(url_for("main.home"))
        except IntegrityError:
            db.session.rollback()
            flash("Email already exists.", "error")
    return render_template("register.html", form=form)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.data["email"]))
        if user and check_password_hash(user.password, form.data["password"]):
            login_user(user, remember=form.data["remember"])
            next_page = request.args.get("next")
            if next_page and not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for("main.home"))
        flash("Invalid email or password", "error")
    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))


@main_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    post = db.get_or_404(BlogPost, post_id)
    comments = post.comments

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please login to comment", "error")
            return redirect(
                url_for("main.login", next=url_for("main.show_post", post_id=post_id))
            )

        clean_text = bleach.clean(
            form.data["text"], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS
        )
        comment = Comment(
            text=clean_text, # type: ignore
            author_id=current_user.id, # type: ignore
            post_id=post_id, # type: ignore
            date=date.today().strftime("%B %d, %Y"), # type: ignore
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added!", "success")
        return redirect(url_for("main.show_post", post_id=post_id))

    return render_template("post.html", post=post, comments=comments, form=form)


@main_bp.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        clean_body = bleach.clean(
            form.data["body"], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS
        )
        post = BlogPost(
            title=form.data["title"], # type: ignore
            subtitle=form.data["subtitle"], # type: ignore
            body=clean_body, # type: ignore
            img_url=form.data["img_url"], # type: ignore
            author_id=current_user.id, # type: ignore
            date=date.today().strftime("%B %d, %Y"), # type: ignore
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("make-post.html", form=form)


@main_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    form = CreatePostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.data["title"]
        post.subtitle = form.data["subtitle"]
        post.img_url = form.data["img_url"]
        post.body = bleach.clean(
            form.data["body"], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS
        )
        db.session.commit()
        return redirect(url_for("main.show_post", post_id=post.id))
    return render_template("make-post.html", form=form, is_edit=True)


@main_bp.route("/delete/<int:post_id>", methods=["POST"])
@login_required
@admin_only
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted", "success")
    return redirect(url_for("main.home"))


@main_bp.route("/about")
@cache.cached(timeout=300)
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if form.data.get("honeypot"):
            return redirect(url_for("main.home"))
        save_contact_to_database(form)
        send_contact_email(form, current_app)
        flash("Message sent!", "success")
        return redirect(url_for("main.home"))
    return render_template("contact.html", form=form)


@main_bp.route("/health")
def health_check():
    return {"status": "healthy"}, 200


@main_bp.route("/robots.txt")
def robots_txt():
    return current_app.send_static_file("robots.txt")
