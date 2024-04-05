import bdb
import random
from models import EmailCaptchaModel, UserModel
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# GET: 从服务器上获取数据
# POST: 将客户端的数据提交给服务器
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return redirect(url_for("auth.register"))
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET: 从服务器上获取数据
# POST: 将客户端的数据提交给服务器
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否正确
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))
            # error_message = form.errors
            # return render_template("register.html", errors=error_message)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@auth_bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject="邮箱验证码", recipients=[email], body=f"验证码是：{captcha}")
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "date": None})

# @auth_bp.route('/mail/test')
# def mail_test():
#     message = Message(subject="邮箱测试", recipients=["cshuming088@gmail.com"], body="这是一条测试邮件")
#     mail.send(message)
#     return "邮件发送成功！"