from flask import redirect, url_for, flash
from flask_login import current_user
from app.models.journal import Journal
from app.models.journal_log import JournalLog
from app.models.author import Author
from app.models.status import Status
from app.utils.file import save_doc


class JournalController:
  
  def __init__(self):
    self.journal = Journal()
    self.author = Author()
    self.status = Status()
    self.journal_log = JournalLog()

  def create(self, request, doc):

    doc_path = save_doc(doc)

    if doc_path is None:
      flash('Wrong file type. Allowed file type is .pdf, .doc, and .docx', 'warning')
      return redirect(url_for('home.journal_create'))

    journal = self.journal.create(
      title=request['title'],
      abstract=request['abstract'],
      journal_path=doc_path,
      user_id=current_user.id,
      topic_id=request['topic'],
    )

    self.journal_log.create(
      journal_id=journal.id,
      status_id=self.status.query.filter_by(name='In Review').first().id
    )

    authors_name = request.getlist('names[]')
    authors_email = request.getlist('emails[]')
    authors_institution = request.getlist('institutions[]')
    n_author = len(authors_name)

    for index in range(0, n_author):
      self.author.create(
        name=authors_name[index],
        email=authors_email[index],
        institution=authors_institution[index],
        journal_id=journal.id
      )

    return redirect(url_for('home.journal_create'))