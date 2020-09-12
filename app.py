  # ./app.py
from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import uuid

    # create flask app
app = Flask(__name__)

    # configure pusher object
pusher = Pusher(
  app_id="1071879",
  key="01fded8f3854f3384d82",
  secret="14176c52ca7cc1ba5fba",
  cluster="us2",
  ssl=True
)

   # ./app.py

  # index route, shows index.html view
@app.route('/')
def index():
  return render_template('index.html')

  # feed route, shows feed.html view
@app.route('/feed')
def feed():
  return render_template('feed.html')

     # ./app.py

  # store post
@app.route('/post', methods=['POST'])
def addPost():
  data = {
    'id': "post-{}".format(uuid.uuid4().hex),
    'title': request.form.get('title'),
    'content': request.form.get('content'),
    'status': 'active',
    'event_name': 'created'
  }
  pusher.trigger("blog", "post-added", data)
  return jsonify(data)

  # deactivate or delete post
@app.route('/post/<id>', methods=['PUT','DELETE'])
def updatePost(id):
  data = { 'id': id }
  if request.method == 'DELETE':
    data['event_name'] = 'deleted'
    pusher.trigger("blog", "post-deleted", data)
  else:
    data['event_name'] = 'deactivated'
    pusher.trigger("blog", "post-deactivated", data)
  return jsonify(data)

  pusher.trigger('a_channel', 'an_event', {'some': 'data'})

       # ./app.py

      # run Flask app in debug mode
app.run(debug=True)