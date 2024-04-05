from flask import *
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required

qa_bp = Blueprint("qa", __name__, url_prefix="/")

@qa_bp.route("/")
# 首页
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)

@qa_bp.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@qa_bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    # answers = AnswerModel.query.order_by(AnswerModel.create_time.desc()).all()
    # print("answers:",answers, type(answers))
    # for answer in answers:
    #     print(answer.content)
    return render_template("detail.html", question=question)

@qa_bp.route('/answer/public', methods=['POST'])
# @qa_bp.post('/answer/public')  第二种写法
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))

@qa_bp.route('/search')
def search():
    # 获得搜索框内容的三种方式
    # 1. /search?q=flask
    # 2. /search/<q>
    # 3. post, request.form
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    # for qu in questions:
    #     print(qu.content)
    return render_template("index.html", questions=questions)
