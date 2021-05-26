from app import db

class Status(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  journal_log = db.relationship('JournalLog', backref='status', lazy=True)

  def __repr__(self):
    return '<Status %r>' % self.name

  def create(self, name):
    status = Status(name=name)
    db.session.add(status)
    db.session.commit()

  def update(self, name, status_id):
    status = Status.query.filter_by(id=status_id).first()
    status.name = name
    db.session.commit()

  def delete(self, status_id):
    status = Status.query.filter_by(id=status_id).first()
    db.session.delete(status)
    db.session.commit()

