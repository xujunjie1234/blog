from flask import Flask, Blueprint,jsonify


from myblog.extensions import db
from myblog.models import Post,Category, Comment

import json

from datetime import datetime
from functools import reduce
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return 'hello'


@main_bp.route('/get_info')
def get_info():
    posts = Post.query.all()
    data = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        # d['body'] = post.body
        d['timestamp'] = datetime.timestamp(post.timestamp) * 1000
        # d['time'] = post.timestamp.strftime('%Y-%m-%d')
        d['view'] = post.view
        # d['can_comment'] = post.can_comment
        d['category'] = post.category.name
        d['like'] = post.like
        data.append(d)
    posts_length = len(posts)
    comments_length = reduce(lambda x,y: x+len(y.comments),posts,0)
    views = reduce(lambda x,y: x+y.view, posts,0)
    return jsonify(posts_length=posts_length,comments_length=comments_length,views=views,posts=data)
                    


@main_bp.route('/get_posts')
def get_posts():
    
    posts = Post.query.all()
    data = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['body'] = post.body
        d['html'] = post.html
        d['timestamp'] = datetime.timestamp(post.timestamp) * 1000
        d['time'] = post.timestamp.strftime('%Y-%m-%d')
        d['view'] = post.view
        d['can_comment'] = post.can_comment
        d['category'] = post.category.name
        d['like'] = post.like
        data.append(d)

    return jsonify({'posts':data})
    

@main_bp.route('/category/<int:category_id>',methods=['GET','POST'])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.with_parent(category).all()
    data = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['body'] = post.body
        d['timestamp'] = datetime.timestamp(post.timestamp) * 1000
        d['time'] = post.timestamp.strftime('%Y-%m-%d')
        d['view'] = post.view
        d['can_comment'] = post.can_comment
        d['category'] = post.category.name
        d['like'] = post.like
        data.append(d)

    return jsonify({'posts':data})



@main_bp.route('/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    d = {}
    d['id'] = post.id
    d['title'] = post.title
    d['body'] = post.body
    d['html'] = post.html
    d['timestamp'] = datetime.timestamp(post.timestamp) * 1000
    d['time'] = post.timestamp.strftime('%Y-%m-%d')
    d['view'] = post.view
    d['can_comment'] = post.can_comment
    d['category'] = post.category.name
    d['category_id'] = post.category_id
    d['comments'] = comment_to_list(post.comments)
    d['like'] = post.like

    return jsonify(post = d)


@main_bp.route('/get_categories')
def get_category():
    categories = Category.query.all()
    data = []
    for category in categories:
        item = {}
        item['id'] = category.id 
        item['name'] = category.name
        item['count'] = Post.query.with_parent(category).count()
        data.append(item)

    return jsonify({'categories': data})
    # return json.dumps({i.id:i.name for i in category},ensure_ascii=False) #content-type = utf-8


@main_bp.route('/get_comments')
def get_comments():
    comments = Comment.query.all()[:100]
    data = []
    for comment in comments:
        item = {}
        item['id'] = comment.id
        item['author'] = comment.author
        item['body'] = comment.body
        item['timestamp'] = datetime.timestamp(comment.timestamp) * 1000
        item['time'] = comment.timestamp.strftime('%Y-%m-%d')
        item['post_title'] = comment.post.title
        item['post_id'] = comment.post_id
        item['like'] = comment.like
        data.append(item)
    
    return jsonify(comments=data)


@main_bp.route('/post/<int:post_id>/comment')
def get_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comments = comment_to_list(post.comments)
    
    return jsonify({'comments': comments})


def get_sub_comment(comment):
    sub_comments = comment.replies
    data = []
    for sub_comment in sub_comments:
        item = {}
        item['id'] = sub_comment.id
        item['author'] = sub_comment.author
        item['email'] = sub_comment.email
        item['body'] = sub_comment.body
        item['timestamp'] = datetime.timestamp(sub_comment.timestamp) * 1000 #13为时间戳
        item['time'] = sub_comment.timestamp.strftime('%Y-%m-%d')
        item['replied'] = sub_comment.replied.author
        item['to'] = sub_comment.to
        item['show'] = sub_comment.show
        item['like'] = sub_comment.like
        item['post_id'] = sub_comment.post_id
        item['post_title'] = sub_comment.post.title
        data.append(item)

    return data


def comment_to_list(comments):
    data = []
    for comment in comments:
        item = {}
        item['id'] = comment.id
        item['author'] = comment.author
        # item['email'] = comment.email
        item['body'] = comment.body
        item['timestamp'] = datetime.timestamp(comment.timestamp) * 1000
        item['time'] = comment.timestamp.strftime('%Y-%m-%d')
        item['post_id'] = comment.post_id
        item['post_title'] = comment.post.title
        item['show'] = comment.show
        item['like'] = comment.like
        sub_comments = get_sub_comment(comment)
        item['sub_comments'] = sub_comments
        data.append(item)
    
    return data