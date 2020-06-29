from faker import Faker
import random

from myblog import db

from myblog.models import Admin, Post, Category, Comment
from sqlalchemy.exc import IntegrityError


fake = Faker('zh_CN')


def fake_admin():
    admin = Admin(
        username = "junjie",
        blog_title = "myblog"
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=5):
    default = Category(name = '默认')
    db.session.add(default)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title = fake.sentence(),
            body = fake.text(2000),
            timestamp = fake.date_time_this_year(),
            view = fake.random_int(),
            like = random.randint(1,30),
            category = Category.query.get(random.randint(1,Category.query.count()))
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=200):
    #一级评论
    for i in range(count):
        comment = Comment(
            author = fake.name(),
            body = fake.sentence(),
            email = fake.email(),
            show = True,
            like = random.randint(1,30),
            timestamp = fake.date_time_this_year(),
            post = Post.query.get(random.randint(1,Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    #二级评论
    salt = count * 2
    for i in range(salt):
        # replied = Comment.query.get(random.randint(1, Comment.query.count()))
        replied = random.choice(Comment.query.filter_by(show=True).all())
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            show=False,
            like = random.randint(1,30),
            # replied=Comment.query.get(random.randint(1, Comment.query.count())),
            replied = replied,
            to = random.choice(replied.replies + [replied]).author,
            # post=Post.query.get(random.randint(1, Post.query.count()))
            post = replied.post
        )
        db.session.add(comment)
    db.session.commit()


