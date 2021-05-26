from app import db

class Topic(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  journal = db.relationship('Journal', backref='topic', lazy=True)
  reviewer = db.relationship('Reviewer', back_populates='topic', lazy=True)

  def __repr__(self):
    return '<Topic %r>' % self.name

  def create(self, name):
    topic = Topic(name=name)
    db.session.add(topic)
    db.session.commit()

  def update(self, name, topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    topic.name = name
    db.session.commit()

  def delete(self, topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    db.session.delete(topic)
    db.session.commit()

