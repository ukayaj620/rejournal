from app import db


class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  user = db.relationship('User', backref='role', lazy=True)

  def __repr__(self):
    return '<Role %r>' % self.name

  @staticmethod
  def create(name):
    role = Role(name=name)
    
    db.session.add(role)
    db.session.commit()

  @staticmethod
  def update(name, role_id):
    role = Role.query.filter_by(id=role_id).first()
    role.name = name
    db.session.commit()

  @staticmethod
  def delete(role_id):
    role = Role.query.filter_by(id=role_id).first()
    db.session.delete(role)
    db.session.commit()

