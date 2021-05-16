from flask import render_template, redirect, url_for
from app.models.topic import Topic

class TopicController:

  def __init__(self):
    self.topic = Topic()

  def fetch_by_id(self, topic_id):
    return self.topic.query.filter_by(id=topic_id).first()

  def fetch_all(self):
    topics = self.topic.query.all()
    return render_template('pages/admin/topic/view.html', topics=topics, role='Admin')

  def create(self, request):
    self.topic.create(name=request['name'])
    return redirect(url_for('admin.topic'))

  def update(self, request, topic_id):
    self.topic.update(name=request['name'], topic_id=topic_id)
    return redirect(url_for('admin.topic'))

  def delete(self, topic_id):
    self.topic.delete(topic_id=topic_id)
    return redirect(url_for('admin.topic'))
