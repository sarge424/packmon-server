from flask import Flask, render_template, send_file
from flask_socketio import SocketIO

import numpy as np
from PIL import Image
import io

from copy import deepcopy as dc

app = Flask(__name__)
socketio = SocketIO(app, max_http_buffer_size=50 * 1000 * 1000)
events = []
lastimg = []

@app.route('/')
def home():
    return render_template('index.html', events=events)


@socketio.on('event')
def add_data(data):
    data['url'] = data['startTime'].replace(':', '')
    events.append(data)
    socketio.emit('log', {'data': events})
    print('received an event', data['width'], data['height'])

    w = data['width']
    h = data['height']
    img = np.array(data['frame']).reshape([h, w, 3])

    for j, row in enumerate(img):
        for i, pixel in enumerate(row):
            img[j][i] = [pixel[2], pixel[1], pixel[0]]

    img = np.array(img)
    img = Image.fromarray(img.astype('uint8'))
    file_obj = io.BytesIO()
    img.save(file_obj, 'PNG')
    file_obj.seek(0)

    lastimg.append((data['startTime'], file_obj))

@app.route('/img/<url>', methods=['GET'])
def image_show(url):
    for img in lastimg:
        if img[0].replace(':', '') == url:
            return send_file(dc(img[1]), mimetype='image/PNG')

    return '404 - Not Found...'

if __name__ == '__main__':
    app.run(port=5007)
