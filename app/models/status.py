from app import db

class Status(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  color = db.Column(db.String(255), unique=False, nullable=True)
  journal_log = db.relationship('JournalLog', back_populates='status', lazy=True)

  def __repr__(self):
    return '<Status %r>' % self.name

  def create(self, name, color):
    status = Status(name=name, color=color)
    db.session.add(status)
    db.session.commit()

  def update(self, name, color, status_id):
    status = Status.query.filter_by(id=status_id).first()
    status.name = name
    status.color = color
    db.session.commit()

  def delete(self, status_id):
    status = Status.query.filter_by(id=status_id).first()
    db.session.delete(status)
    db.session.commit()

