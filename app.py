from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sql import session, engine
from sqlalchemy import or_

from models import Book, Author
from forms import BookForm, AuthorForm


@app.route("/")
def index():
    authors = session.query(Author).all()
    books = session.query(Book).all()
    return render_template('index.html', authors=authors, books=books)


@app.route("/book/add", methods=['GET', 'POST'])
def add_book():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        book = Book(form.title.data, form.authors.data)
        session.add(book)
        session.commit()
        return redirect(url_for('index'))
    return render_template('book_form.html', form=form, action="/book/add")


@app.route("/book/<int:book_id>/edit", methods=['GET', 'POST'])
def edit_book(book_id):
    form = BookForm(request.form)
    if request.method == 'GET':
        form = BookForm(request.form, session.query(Book).get(book_id))
    if request.method == 'POST' and form.validate():
        book_edited = Book(form.title.data, form.authors.data)
        book_db = session.query(Book).get(book_id)
        book_db.title = book_edited.title
        book_db.authors = book_edited.authors
        session.commit()
        return redirect(url_for('index'))
    return render_template('book_form.html', form=form, action="/book/%s/edit" % book_id, submit_text="Save")


@app.route("/book/<int:book_id>/delete")
def delete_book(book_id):
    book = session.query(Book).get(book_id)
    session.delete(book)
    session.commit()
    return redirect(url_for('index'))


@app.route("/author/add", methods=['GET', 'POST'])
def add_author():
    form = AuthorForm(request.form)
    if request.method == 'POST' and form.validate():
        author = Author(form.name.data)
        session.add(author)
        session.commit()
        return redirect(url_for('index'))
    return render_template('author_form.html', form=form, action="/author/add")


@app.route("/author/<int:author_id>/edit", methods=['GET', 'POST'])
def edit_author(author_id):
    form = AuthorForm(request.form)
    if request.method == 'GET':
        form = AuthorForm(request.form, session.query(Author).get(author_id))
    if request.method == 'POST' and form.validate():
        author_edited = Author(form.name.data)
        author_db = session.query(Author).get(author_id)
        author_db.name = author_edited.name
        session.commit()
        return redirect(url_for('index'))
    return render_template('author_form.html', form=form, action="/author/%s/edit" % author_id, submit_text="Save")


@app.route("/author/<int:author_id>/delete")
def delete_author(author_id):
    author = session.query(Author).get(author_id)
    session.delete(author)
    session.commit()
    return redirect(url_for('index'))


@app.route("/search_results")
def search_results():
    q = request.values['q']
    books = session.query(Book).filter(
        or_(Book.title.like("%" + q + "%"), Book.authors.any(Author.name.like("%" + q + "%"))))
    return render_template('search_results.html', books=books)


Book.metadata.create_all(engine)
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8888, )
