from flask import flash, redirect, url_for, send_file
import os
from app.models.applicant import Applicant
from app.utils.file import save_doc, delete_doc
from app.utils.mailer import send_application_notification, send_custom_mail


class ApplicantController:

  def __init__(self):
    self.applicant = Applicant()

  def fetch_all(self):
    return self.applicant.query.all()

  def fetch_by_id(self, applicant_id):
    return self.applicant.query.filter_by(id=applicant_id).first()

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

  def cv_download(self, filename):
    directory = os.path.join('static/docs/uploads', filename)
    return send_file(directory, as_attachment=True)
  
  def receive(self, request):
    applicant = self.fetch_by_id(applicant_id=request['id'])

    self.applicant.has_viewed(applicant_id=request['id'])

    send_custom_mail(
      to=applicant.email,
      subject=request['subject'],
      content=request['messages']
    )

    flash('Message has been sent to ' + applicant.name, 'info')
  
  def reject(self, request):
    applicant = self.fetch_by_id(applicant_id=request['id'])

    send_custom_mail(
      to=applicant.email,
      subject=request['subject'],
      content=request['messages']
    )

    delete_doc(applicant.cv_path)

    self.applicant.delete(applicant_id=request['id'])

    flash('Message has been sent to ' + applicant.name, 'info')
