from flask import Flask, Blueprint, redirect, url_for, session,request,jsonify

from flask_login import login_user, logout_user, login_required, current_user

from myblog.models import Admin

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/api/login',methods=["POST"])
def login():
    username = request.json.get('username',None)
    password = request.json.get('password',None)
    admin = Admin.query.first()
    if admin:
        if admin.username == username and admin.validate_password_hash(password):
            login_user(admin)
            return jsonify({'status':'ok','info':'登录成功','session':username})
        return jsonify({'status':'no','info':'用户名或密码错误，登录失败'})
    return jsonify({'aaa':'dfsd'})


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))