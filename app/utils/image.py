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


def generate_photoname(ext):
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)) + ext


def save_image(photo):
  filename = secure_filename(photo.filename)
  photo_filename = ''
  if filename != '':
    file_ext = os.path.splitext(filename)[1].lower()
    photo_filename = generate_photoname(file_ext)
    if file_ext not in Config.UPLOAD_EXTENSIONS or \
        file_ext != validate_image(photo.stream):
      abort(400)

    if not os.path.exists(Config.UPLOAD_PATH):
      os.mkdir(os.path.join(Config.UPLOAD_DIR, 'uploads'))
    photo.save(os.path.join(Config.UPLOAD_PATH, photo_filename))

  return photo_filename

def delete_image(filename):
  os.remove(os.path.join(Config.UPLOAD_PATH, filename))