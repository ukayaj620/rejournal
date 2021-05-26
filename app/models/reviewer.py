from app import db


class Reviewer(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), unique=False, nullable=False)
  journal_log = db.relationship('JournalLog', backref='reviewer', lazy=True)
  topic = db.relationship('Topic', back_populates='reviewer', lazy=True)

  def __repr__(self):
    return '<Reviewer %r>' % self.user_id
  
  def create(self, user_id, topic_id):
    reviewer = Reviewer(
      user_id=user_id,
      topic_id=topic_id
    )

    db.session.add(reviewer)
    db.session.commit()

  def update(self, user_id, topic_id):
    reviewer = Reviewer.query.filter_by(user_id=user_id).first()
    reviewer.topic_id = topic_id

    db.session.commit()
  