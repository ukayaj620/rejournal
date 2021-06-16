from app import db

class Applicant(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), unique=False, nullable=False)
  email = db.Column(db.String(255), unique=False, nullable=False)
  telephone = db.Column(db.String(255), unique=False, nullable=False)
  topic = db.Column(db.String(255), unique=False, nullable=False)
  cv_path = db.Column(db.String(255), unique=False, nullable=False)
  is_viewed = db.Column(db.Boolean, nullable=False)


  def __repr__(self):
    return '<Applicant %r>' % self.name

  def create(self, name, email, telephone, cv_path, topic):
    applicant = Applicant(
      name=name,
      email=email,
      telephone=telephone,
      topic=topic,
      cv_path=cv_path,
      is_viewed=False
    )

    db.session.add(applicant)
    db.session.commit()

  def has_viewed(self, applicant_id):
    applicant = Applicant.query.filter_by(id=applicant_id).first()
    applicant.is_viewed = True

    db.session.commit()

  def delete(self, applicant_id):
    applicant = Applicant.query.filter_by(id=applicant_id).first()

    db.session.delete(applicant)
    db.session.commit()
