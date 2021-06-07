from app import db
from datetime import datetime


class Journal(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(255), unique=False, nullable=False)
  abstract = db.Column(db.Text, unique=False, nullable=False)
  journal_path = db.Column(db.String(255), unique=False, nullable=False)
  upload_time = db.Column(db.DateTime, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=False, nullable=False)
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='SET NULL'), unique=False, nullable=True)
  topic = db.relationship('Topic', uselist=False, back_populates='journal', lazy=True)
  author = db.relationship('Author', backref='journal', lazy=True, cascade='delete,delete-orphan')
  journal_log = db.relationship('JournalLog', uselist=False, backref='journal', lazy=True, cascade='delete,delete-orphan')

  def __repr__(self):
    return '<Journal %r>' % self.title

  def create(self, title, abstract, journal_path, user_id, topic_id):
    journal = Journal(
      title=title,
      abstract=abstract,
      journal_path=journal_path,
      upload_time=datetime.now(),
      user_id=user_id,
      topic_id=topic_id
    )

    db.session.add(journal)
    db.session.commit()
    db.session.flush()

    return journal

  def update(self, journal_id, title, abstract, journal_path, user_id, topic_id):
    journal = Journal.query.filter_by(id=journal_id).first()
    journal.title = title
    journal.abstract = abstract
    journal.user_id = user_id
    journal.topic_id = topic_id
    journal.upload_time = datetime.now()

    if journal_path is not None:
      journal.journal_path = journal_path

    db.session.commit()

  def delete(self, journal_id):
    journal = Journal.query.filter_by(id=journal_id).first()
    db.session.delete(journal)
    db.session.commit()

