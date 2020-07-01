from flask import Flask, Blueprint, request, jsonify,send_from_directory


from myblog.extensions import db
from myblog.models import Post,Category, Comment,News,Admin
from myblog.utils import allowed_file

from datetime import datetime

admin_bp = Blueprint('admin',__name__)



@admin_bp.route('/get_about')
def get_about():
    admin = Admin.query.first()
    title = admin.blog_title
    body = admin.body
    html = admin.html
    timestamp = datetime.timestamp(admin.timestamp)*1000

    return jsonify(title=title,body=body,html=html,timestamp=timestamp)


@admin_bp.route('/edit_about',methods=['POST'])
def edit_about():
    admin = Admin.query.first()
    admin.blog_title = request.json.get('title')
    admin.body = request.json.get('body')
    admin.html = request.json.get('html')
    admin.timestamp = datetime.fromtimestamp(request.json.get('timestamp')/1000)
    db.session.commit()

    return jsonify(type='edit about success')



@admin_bp.route('/api/add_comment',methods=['POST'])
def add_comment():
    author = request.json.get('author')
    body = request.json.get('body')
    email = request.json.get('email')
    timestamp = datetime.fromtimestamp(request.json.get('timestamp')/1000)
    post_id = request.json.get('post_id')
    replied_id = request.json.get('replied_id')
    to = request.json.get('to')
    show = request.json.get('show')
    like = request.json.get('like')
    comment = Comment(author=author,
                    body=body,
                    timestamp=timestamp,
                    post_id=post_id,
                    replied_id=replied_id,
                    to=to,
                    show=show,
                    like=like,
                    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'type':'success'})


@admin_bp.route('/api/delete_comments',methods=['POST'])
def delete_comments():
    comments = request.json.get('comments',[])
    for item in comments:
        comment = Comment.query.get_or_404(item['id'])
        db.session.delete(comment)
    db.session.commit()
    
    return jsonify(type='delete success')


@admin_bp.route('/api/delete_categories',methods=['POST'])
def delete_categories():
    categories = request.json.get('categories',[])
    for item in categories:
        category = Category.query.get_or_404(item['id'])
        db.session.delete(category)
    db.session.commit()
    
    return jsonify(type='delete categories success')


@admin_bp.route('/api/delete_posts',methods=['POST'])
def delete_posts():
    posts = request.json.get('posts',[])
    for item in posts:
        post = Post.query.get_or_404(item['id'])
        db.session.delete(post)
    db.session.commit()

    return jsonify(type="delete post success")


@admin_bp.route('/api/post/<int:post_id>/can_comment',methods=["POST"])
def can_or_not(post_id):
    # post_id = request.json.get('post_id')
    post = Post.query.get_or_404(post_id)
    post.can_comment = not post.can_comment
    db.session.commit()

    return jsonify(type="update success")


@admin_bp.route('/api/add_category',methods=['POST'])
def add_category():
    category_id = request.json.get('id')
    name = request.json.get('name')
    category = Category(id=category_id,name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(type="add category success")


@admin_bp.route('/post/<int:post_id>/add_like',methods=['POST'])
def post_add_like(post_id):
    post = Post.query.get_or_404(post_id)
    post.like += 1
    db.session.commit()

    return jsonify(type="post add like success")


@admin_bp.route('/comment/<int:comment_id>/add_like',methods=['POST'])
def comment_add_like(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.like += 1
    db.session.commit()

    return jsonify(type="comment add like success")


@admin_bp.route('/category/<int:category_id>/rename',methods=["POST"])
def rename_category(category_id):
    new_name = request.json.get('name')
    category = Category.query.get_or_404(category_id)
    category.name = new_name
    db.session.commit()

    return jsonify(type="category rename success")



@admin_bp.route('/get_news',methods=['GET','POST'])
def get_news():
    news = News.query.all()
    data = []
    for new in news:
        item = {}
        item['id'] = new.id
        item['author'] = new.author
        item['body'] = new.body
        item['timestamp'] = datetime.timestamp(new.timestamp) * 1000
        post = Post.query.get_or_404(new.post_id)
        item['post_title'] = post.title
        item['reviewed'] = new.reviewed
        data.append(item)
        
    return jsonify(news=data)


@admin_bp.route('/api/read_news',methods=['POST'])
def read_news():
    ids = request.json.get('id')
    for i in ids:
        new = News.query.get_or_404(i)
        new.reviewed = True
    db.session.commit()
    return jsonify(type="reviewed success")



@admin_bp.route('/api/add_news',methods=['POST'])
def add_news():
    author = request.json.get('author')
    post_id = request.json.get('post_id')
    body = request.json.get('body')
    timestamp = datetime.fromtimestamp(request.json.get('timestamp')/1000)
    
    new = News(author=author,post_id=post_id,
                timestamp=timestamp,body=body)
    db.session.add(new)
    db.session.commit()
    return jsonify(author=author,post_id=post_id,body=body,timestamp=timestamp)


@admin_bp.route('/api/delete_news',methods=['POST'])
def delete_news():
    ids = request.json.get('id')
    for i in ids:
        new = News.query.get_or_404(i)
        db.session.delete(new)
    db.session.commit()
    return jsonify(type="news delete success")


@admin_bp.route('/add_post',methods=['POST'])
def add_post():
    title = request.json.get('title')
    body = request.json.get('body')
    html = request.json.get('html')
    timestamp = datetime.fromtimestamp(request.json.get('timestamp')/1000)
    category_id = request.json.get('category_id')
    post = Post(title=title,body=body,timestamp=timestamp,category_id=category_id,html=html)
    db.session.add(post)
    db.session.commit()
    return jsonify(title=title,body=body,post_id=post.id,category_id=category_id,timestamp=timestamp,html=html)
    # return jsonify(title=title,body=body,timestamp=timestamp)


@admin_bp.route('/edit_post/<int:post_id>',methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.json.get('title')
    post.body = request.json.get('body')
    post.html = request.json.get('html')
    # post.timestamp = datetime.fromtimestamp(request.json.get('timestamp')/1000)
    post.category_id = request.json.get('category_id')
    db.session.commit()
    return jsonify(post_id=post_id)



import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


@admin_bp.route('/upload_image',methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if not allowed_file(image.filename):
        return jsonify(type='error')
    url = os.path.join(basedir,"upload\img")
    image.save(os.path.join(url,image.filename))

    # url = 'http://127.0.0.1:5000/uploads/' + image.filename
    url = 'http://134.175.155.79/uploads/' + image.filename
    return jsonify(type="success",url=url)


@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    url = os.path.join(basedir,"upload\img")
    return send_from_directory(url, filename)


# @admin_bp.route('/test')
# def test():
#     post = Post.query.first()
#     res = post.to_dict()
#     return jsonify(data=res)