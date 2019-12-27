from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):

    name = StringField('Name of Cat: ')
    submit = SubmitField('Add Cat')


class AdOwnerForm(FlaskForm):
    name = StringField('Name of Owner:')
    cat_id = IntegerField("Id of Cats: ")
    submit = SubmitField("Add Owner")


class DelForm(FlaskForm):

    id = IntegerField('Id Number of Cat to Remove: ')
    submit = SubmitField('Remove Cat')
