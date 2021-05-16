from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  telephone = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), unique=False, nullable=False)
  gender = db.Column(db.String(2), unique=False, nullable=False)
  is_verified = db.Column(db.Integer, unique=False, nullable=False)
  registered_date = db.Column(db.DateTime, nullable=False)
  role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), unique=False, nullable=False)
  picture_path = db.Column(db.String(255), nullable=True)
  verification = db.relationship('Verification', backref='user', lazy=True)

  def __repr__(self):
    return '<User %r>' % self.name

  def create(self, name, email, telephone, password, gender, role_id):
    user = User(
      name=name,
      email=email,
      telephone=telephone,
      password=password,
      gender=gender,
      is_verified=0,
      registered_date=datetime.now(),
      role_id=role_id
    )
    
    db.session.add(user)
    db.session.commit()

  def update(self, name, email, telephone, gender, id):
    user = User.query.filter_by(id=id).first()
    user.name = name
    user.email = email
    user.telephone = telephone
    user.gender = gender

    db.session.commit()

  def update_image(self, filename, id):
    user = User.query.filter_by(id=id).first()
    user.picture_path = filename

    db.session.commit()

  def verified_user(self, id):
    user = User.query.filter_by(id=id).first()
    user.is_verified = 1

    db.session.commit()

