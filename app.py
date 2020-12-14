from flask import Flask, request
from flask import render_template
from flask_bootstrap import Bootstrap
from db_manager.database import DBManager

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


@app.route('/')
def index():
    manager = DBManager()
    return render_template("index.html", tables=manager.get_table_names_from_db("nan_db"))


@app.route('/edit', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('edit_table.html', title='Sign In', form=form)


@app.route('/<my_table>', methods=['GET'])
def table(my_table):
    manager = DBManager()
    manager.path = ""
    m_table = manager.get_table("nan_db", my_table)
    return render_template("table.html", table=m_table, count=m_table.row_count())


if __name__ == '__main__':
    app.run()
