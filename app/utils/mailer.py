from app import mail
from flask_mail import Message
import os

def send_email(sender, to, subject, html):
  email = Message(subject, sender=sender, recipients=to)
  email.html = html
  mail.send(email)

def send_signup_verification(to, link):

  verify_link = str(os.environ.get('VERIFY_URL')) + link

  message_body = f"""
    <div style="align-text: center;">
      <h4>Your Verification Link</h4>
      <p>Please click this link below to proceed</p>
      <p>{verify_link}</p>
    </div>
  """

  send_email(
    subject='Itevenz Registration Verification',
    sender=str(os.environ.get('MAIL_USERNAME')),
    to=[to],
    html=message_body
  )
  