from app import mail
from flask_mail import Message
from app.config import Config

def send_email(to, subject, html):
  email = Message(subject, sender=Config.MAIL_USERNAME, recipients=to)
  email.html = html
  mail.send(email)


def send_signup_verification(to, link):

  verify_link = Config.VERIFY_URL + link

  message_body = f"""
    <div style="align-text: center;">
      <h4>Your Verification Link</h4>
      <p>Please click this link below to proceed</p>
      <a href="{verify_link}" target="_blank">{verify_link}</a>
    </div>
  """

  send_email(
    subject='ReJournal Registration Verification',
    to=[to],
    html=message_body
  )


def send_account_credential(to, password):
  message_body = f"""
    <div style="align-text: center;">
      <h4>Your Account has been created</h4>
      <p>Please use this code below as your password</p>
      <p>{password}</p>
    </div>
  """

  send_email(
    subject='ReJournal Account Creation',
    to=[to],
    html=message_body
  )


def send_review_notification(to, title):
  message_body = f"""
    <div style="align-text: center;">
      <h4>Your manuscript with Title</h4>
      <p><span style="font-weight: 700;">{title}</span> is being reviewed!</p>
      <p>Later information will be told the following day.</p>
    </div>
  """

  send_email(
    subject='Manuscript In Review',
    to=[to],
    html=message_body
  )


def send_acceptance_notification(to, title):
  message_body = f"""
    <div style="align-text: center;">
      <strong>Thank you for your submission.</strong>
      <p>Your manuscript with title <span style="font-weight: 700;">{title}</span> has been accepted and will be pusblish this year.</p>
      <p>We will soon inform to you after we publish your work.</p>
    </div>
  """

  send_email(
    subject='Manuscript Acceptance',
    to=[to],
    html=message_body
  )


def send_publication_notification(to, title, series):
  message_body = f"""
    <div style="align-text: center;">
      <strong>Hello, your manuscript has been published!</strong>
      <p>Your manuscript with <span style="font-weight: 700;">{title}</span> is published as {series} series</p>
      <p>Thank you for trusting us to publish your amazing work. Glad to see your another sophisticated works!</p>
    </div>
  """

  send_email(
    subject='Manuscript Publication',
    to=[to],
    html=message_body
  )


def send_application_notification(to, name):
  message_body = f"""
    <div style="align-text: center;">
      <p style="font-weight: 700;">Hello, {name}</p>
      <p>Thank you for your application. We will soon reach you out as soon as we can!</p>
    </div>
  """
  send_email(
    subject='Application Notification',
    to=[to],
    html=message_body
  )


def send_custom_mail(to, subject, content):
  message_body = f"""
    <div style="align-text: center;">
      <p>{content}</p>
    </div>
  """

  send_email(
    subject=subject,
    to=[to],
    html=message_body
  )
