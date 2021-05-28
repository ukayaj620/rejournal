from app import db
from datetime import datetime


class JournalLog(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  journal_id = db.Column(db.Integer, db.ForeignKey('journal.id', ondelete='CASCADE'), unique=True, nullable=False)
  status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='SET NULL'), unique=False, nullable=True)
  reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id', ondelete='SET NULL'), unique=False, nullable=True)
  timestamp = db.Column(db.DateTime, unique=False, nullable=False)
  status = db.relationship('Status', back_populates='journal_log', lazy=True)

  def __repr__(self):
    return '<Journal Log %r>' % self.journal_id

  def create(self, journal_id, status_id):
    journal_log = JournalLog(
      journal_id=journal_id,
      status_id=status_id,
      timestamp=datetime.now()
    )

    db.session.add(journal_log)
    db.session.commit()

  def update(self, journal_id, status_id):
    journal_log = JournalLog.query.filter_by(journal_id=journal_id)
    journal_log.status_id = status_id
    journal_log.timestamp = datetime.now()

    db.session.commit()
