from app import db
from datetime import datetime, timedelta


class Verification(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=False, nullable=False)
  token = db.Column(db.String(255), unique=False, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False)
  valid = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return '<Verification %r>' % self.token

  def create(self, token, user_id):
    now = datetime.now()
    verification = Verification(
      token=token,
      user_id=user_id,
      created_at=now,
      valid=(now + timedelta(hours=24))
    )
    db.session.add(verification)
    db.session.commit()

  def update(self, token, user_id):
    now = datetime.now()
    verification = Verification.query.filter_by(user_id=user_id).first()
    verification.token = token
    verification.created_at = now
    verification.valid = now + timedelta(hours=24)
    db.session.commit()

  def delete(self, token_id):
    verification = Verification.query.filter_by(id=token_id).first()
    db.session.delete(verification)
    db.session.commit()

