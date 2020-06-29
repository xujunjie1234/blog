import os

from flask import Flask
from flask_cors import CORS
from myblog.blueprints.main import main_bp
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.admin import admin_bp

from myblog.settings import config
from myblog.models import Admin, Post, Category, Comment #Sub_comment
from myblog.extensions import db, login_manager,migrate

import click

# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp


def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('myblog')
    CORS(app,resources=r'/*')
    app.config.from_object(config[config_name])
    # app.after_request(after_request)


    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    
    return app


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)



def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('此操作将会删除数据库，确认？', abort=True)
            click.echo('正在删除所有数据表')
            db.drop_all()
            click.echo('已删除所有数据表')
        click.echo('正在初始化数据库')
        db.create_all()
        click.echo('已初始化数据库')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building myblog, just for you."""

        click.echo('初始化数据库中...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('管理员已存在，更新管理员中...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('新建一个管理员账号...')
            admin = Admin(
                username=username,
                blog_title='myblog',
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('正在新建一个默认分类...')
            category = Category(name='默认')
            db.session.add(category)

        db.session.commit()
        click.echo('已完成')

    @app.cli.command()
    @click.option('--category', default=5, help='Quantity of categories, default is 10.')
    @click.option('--post', default=30, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=100, help='Quantity of comments, default is 500.')
    # @click.option('--sub_comment', default=300, help='Quantity of sub_comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from myblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('正在创建管理员...')
        fake_admin()

        click.echo('正在创建 %d 个分类...' % category)
        fake_categories(category)

        click.echo('正在创建 %d 篇文章...' % post)
        fake_posts(post)

        click.echo('正在创建 %d 条评论...' % comment)
        fake_comments(comment)

        # click.echo('正在创建 %d 条二级评论...' % comment)
        # comments = Comment.query.all()
        # for comment in comments:
        #     fake_sub_comments(comment)

        click.echo('已完成')
