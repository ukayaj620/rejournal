import imghdr
import string
import random
from flask import abort
import os
from werkzeug.utils import secure_filename
from app.config import Config

def validate_image(stream):
  header = stream.read(512)
  stream.seek(0)
  format = imghdr.what(None, header)
  if not format:
    return None
  return '.' + (format if format != 'jpeg' else 'jpg')


def generate_filename(ext):
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)) + ext


def save_image(photo):
  filename = secure_filename(photo.filename)
  photo_filename = ''
  if filename != '':
    file_ext = os.path.splitext(filename)[1].lower()
    photo_filename = generate_filename(file_ext)
    if file_ext not in Config.UPLOAD_IMAGE_EXTENSIONS or \
        file_ext != validate_image(photo.stream):
      return False

    if not os.path.exists(Config.UPLOAD_IMAGE_PATH):
      os.mkdir(os.path.join(Config.UPLOAD_IMAGE_DIR, 'uploads'))
    photo.save(os.path.join(Config.UPLOAD_IMAGE_PATH, photo_filename))

  return photo_filename


def delete_image(filename):
  os.remove(os.path.join(Config.UPLOAD_IMAGE_PATH, filename))


def save_doc(doc):
  filename = secure_filename(doc.filename)
  doc_filename = ''
  if filename != '':
    file_ext = os.path.splitext(filename)[1].lower()
    doc_filename = generate_filename(file_ext)
    if file_ext not in Config.UPLOAD_DOC_EXTENSIONS:
      return False

    if not os.path.exists(Config.UPLOAD_DOC_PATH):
      os.mkdir(os.path.join(Config.UPLOAD_DOC_DIR, 'uploads'))
    doc.save(os.path.join(Config.UPLOAD_DOC_PATH, doc_filename))

  return doc_filename


def delete_doc(filename):
  os.remove(os.path.join(Config.UPLOAD_DOC_PATH, filename))