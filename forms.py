from wtforms import Form, StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from sql import session
from models import Author


def get_authors():
    return session.query(Author).all()


class BookForm(Form):
    title = StringField('Title', [validators.InputRequired()])
    authors = QuerySelectMultipleField(query_factory=get_authors)


class AuthorForm(Form):
    name = StringField('Name', [validators.InputRequired()])
