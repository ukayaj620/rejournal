from flask import flash, redirect, url_for
from app.models.applicant import Applicant
from app.utils.file import save_doc
from app.utils.mailer import send_application_notification


class ApplicantController:

  def __init__(self):
    self.applicant = Applicant()

  def apply(self, request, cv):
    cv_path = save_doc(cv)

    if cv_path is False:
      flash('Wrong file type. Allowed file type is .pdf', 'warning')
      return redirect(url_for('base.application'))
    
    self.applicant.create(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      cv_path=cv_path,
      topic=request['topic']
    )

    flash('Thanks for your application. We will soon reach out you!', 'info')
    send_application_notification(to=request['email'], name=request['name'])
    