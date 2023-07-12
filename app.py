from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
events = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def form_fill():
    return render_template('formfill.html')


@app.route('/history')
def show_history():
    return render_template('history.html', events=events)


@app.route('/event', methods=['POST'])
def event():
    data = (request.values.get('time'), request.values.get('duration'))
    events.append(data)
    socketio.emit('event', {'data': events})
    print('emitted', data)
    return redirect('/generate')


last_post = []


@app.route('/ping', methods=['GET', 'POST'])
def ping_serv():
    if request.method == 'POST':
        last_post.append(request.values)

    return str(last_post)
