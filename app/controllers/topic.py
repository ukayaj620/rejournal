from flask import redirect, url_for
from app.models.topic import Topic

class TopicController:

  def __init__(self):
    self.topic = Topic()

  def fetch_by_id(self, topic_id):
    return self.topic.query.filter_by(id=topic_id).first()

  def fetch_all(self):
    return self.topic.query.all()

  def create(self, request):
    self.topic.create(name=request['name'])

  def update(self, request, topic_id):
    self.topic.update(name=request['name'], topic_id=topic_id)

  def delete(self, topic_id):
    self.topic.delete(topic_id=topic_id)
