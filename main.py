from flask import Flask, render_template, redirect, url_for, jsonify, request, Flask
from flask_bootstrap import Bootstrap, forms
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask_migrate import Migrate


app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(25))
    title = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(30), nullable=False)


class New(FlaskForm):
    __tablename__ = "New"
    author = StringField("author", validators=[DataRequired()])
    title = StringField("To Do Item", validators=[DataRequired()])
    date = StringField("To do By", validators=[DataRequired()])
    submit = SubmitField("add new ToDo Item")


# new_todo=New(id=1, author="callan", title="todo" , date="tomorrow")
# db.session.add(new_todo)
# db.session.commit()
db.create_all()


@app.route('/')
def home():
    return redirect(url_for('show_all'))


@app.route('/all', methods=["GET", "POST"])
def show_all():
    posts = ToDo.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/create", methods=["GET", "POST"])
def add_item():
    form = New()
    if form.validate_on_submit():
        new_todo = ToDo(
            author=form.author.data,
            title=form.title.data,
            date=form.date.data,
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("show_all"))
    return render_template("create.html", form=form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = ToDo.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('show_all', post_to_delete = post_id))


if __name__ == "__main__":
    app.run(debug=True)

#practice css and html by making my to do list site look pretty.
#create a footer and header html
