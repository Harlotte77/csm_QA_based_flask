import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired

from exts import db
from models import UserModel, EmailCaptchaModel

# Form: 主要用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码错误")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    # 自定义验证
    # 1.验证邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或者验证码错误")
        # else:
        #     """
        #     todo: 验证成功后可以删掉captcha_model，也就是数据库中的验证码
        #         但是每次都删除一条验证码数据会影响性能
        #         可以每隔一段时间将已经过期的验证码删除（used=True的验证码表示已经过期）
        #     """
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱还没有注册")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码错误")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误")])
    content = wtforms.StringField(validators=[Length(min=1, message="内容不能为空")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="内容不能为空")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="问题不能为空")])