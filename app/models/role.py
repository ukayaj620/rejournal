from app import db


class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  user = db.relationship('User', backref='role', lazy=True)

  def __repr__(self):
    return '<Role %r>' % self.name

  def create(self, name):
    role = Role(name=name)
    db.session.add(role)
    db.session.commit()

  def update(self, name, role_id):
    role = Role.query.filter_by(id=role_id).first()
    role.name = name
    db.session.commit()

  def delete(self, role_id):
    role = Role.query.filter_by(id=role_id).first()
    db.session.delete(role)
    db.session.commit()

