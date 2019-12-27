import os
from forms import AddForm, DelForm, AdOwnerForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Cats(db.Model):

    __tablename__ = 'kittens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref='cats', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Cats name is {self.name} and owner is {self.owner.name}"
        else:
            return f"Cat name: {self.name} and no owner assigned yet"


class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cats_id = db.Column(db.Integer, db.ForeignKey('kittens.id'))

    def __init__(self, name, cats_id):
        self.name = name
        self.cats_id = cats_id

    def __repr__(self):
        return f"Owner Name : {self.name}"


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():

    form = AdOwnerForm()

    if form.validate_on_submit():
        name = form.name.data
        cat_id = form.cat_id.data

        new_owner = Owner(name, cat_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for('list_cat'))

    return render_template('add_owner.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add_cat():

    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        new_cat = Cats(name)
        db.session.add(new_cat)
        db.session.commit()

        return redirect(url_for('list_cat'))

    return render_template('add.html', form=form)


@app.route('/list')
def list_cat():
    kittens = Cats.query.all()
    return render_template('list.html', kittens=kittens)


@app.route('/delete', methods=['GET', 'POST'])
def del_cat():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        cat = Cats.query.get(id)
        db.session.delete(cat)
        db.session.commit()

        return redirect(url_for('list_cat'))

    return render_template('delete.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
