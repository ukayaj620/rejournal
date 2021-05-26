from app import db


class Author(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  email = db.Column(db.String(255), unique=False, nullable=False)
  institution = db.Column(db.String(255), unique=False, nullable=False)
  journal_id = db.Column(db.Integer, db.ForeignKey('journal.id', ondelete='CASCADE'), unique=False, nullable=False)

  def __repr__(self):
    return '<Author %r>' % self.name

  def create(self, name, email, institution, journal_id):
    author = Author(
      name=name,
      email=email,
      institution=institution,
      journal_id=journal_id
    )

    db.session.add(author)
    db.session.commit()

  def update(self, author_id, name, email, institution, journal_id):
    author = Author.query.filter_by(id=author_id).first()
    author.name = name
    author.email = email
    author.institution = institution
    author.journal_id = journal_id

    db.session.commit()

  def delete(self, author_id):
    author = Author.query.filter_by(id=author_id).first()

    db.session.delete(author)
    db.session.commit()
