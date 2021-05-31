from flask import redirect, url_for, flash, send_file
from flask_login import current_user
import os
from app.models.journal import Journal
from app.models.journal_log import JournalLog
from app.models.author import Author
from app.models.status import Status
from app.utils.file import save_doc, delete_doc
from app.config import Config


class JournalController:
  
  def __init__(self):
    self.journal = Journal()
    self.author = Author()
    self.status = Status()
    self.journal_log = JournalLog()

  def fetch_by_id(self, journal_id):
    return self.journal.query.filter_by(id=journal_id).first()

  def fetch_all(self):
    return self.journal.query.filter_by(user_id=current_user.id).all()

  def create(self, request, doc):
    doc_path = save_doc(doc)

    if doc_path is False:
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
      status_id=self.status.query.filter_by(name='Submitted').first().id
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
  
  def update(self, request, doc):
    doc_path = save_doc(doc) if doc else None

    if doc_path is False:
      flash('Wrong file type. Allowed file type is .pdf, .doc, and .docx', 'warning')
      return redirect(url_for('home.journal_create'))
    
    journal = self.fetch_by_id(journal_id=request['id'])

    delete_doc(journal.journal_path) if doc_path is not None else None
      
    self.journal.update(
      journal_id=request['id'],
      title=request['title'],
      abstract=request['abstract'],
      journal_path=doc_path,
      user_id=current_user.id,
      topic_id=request['topic'],
    )

    old_author_ids = [author.id for author in journal.author]

    updated_author_ids = [int(id) for id in request.getlist('ids[]')]
    authors_name = request.getlist('names[]')
    authors_email = request.getlist('emails[]')
    authors_institution = request.getlist('institutions[]')

    n_old_author = len(updated_author_ids)
    n_submitted_author = len(authors_name)

    ids_to_update = list(set(updated_author_ids) & set(old_author_ids))
    ids_to_delete = list(set(old_author_ids) - set(updated_author_ids))

    print('current_author_ids')
    print(old_author_ids)
    print('updated_author_ids')
    print(updated_author_ids)

    print('update')
    print(ids_to_update)
    print('delete')
    print(ids_to_delete)

    for index in range(0, n_old_author):
      if updated_author_ids[index] in ids_to_update:
        self.author.update(
          author_id=updated_author_ids[index],
          name=authors_name[index],
          email=authors_email[index],
          institution=authors_institution[index],
          journal_id=journal.id
        )

    for index in range(n_old_author, n_submitted_author):
      self.author.create(
        name=authors_name[index],
        email=authors_email[index],
        institution=authors_institution[index],
        journal_id=journal.id
      )

    for id_to_delete in ids_to_delete:
      self.author.delete(author_id=id_to_delete)

    return redirect(url_for('home.journal_view_detail', id=journal.id))

  def download(self, filename):
    directory = os.path.join('static/docs/uploads', filename)
    print(directory)
    return send_file(directory, as_attachment=True)
