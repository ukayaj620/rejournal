from datetime import datetime


def is_expire(expire):
  now = datetime.now()
  return now > expire

  