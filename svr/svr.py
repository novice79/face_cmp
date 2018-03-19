#!/usr/bin/env python

import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

# import of

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/api/test', methods=['POST'])
def test():
    content = request.get_json(silent=True)
    print content
    ret = jsonify(
        username="david",
        email="david@cninone.com",
        age=39
    )
    return ret


@app.route('/api/cmp_imgs', methods=['POST'])
def cmp_imgs():
    content = request.get_json(silent=True)
    print content
    return jsonify(content)    

@socketio.on('filter_face')
def filter_face(data):
    # mat = of.cvMatFromDataUrl(data['dataURL'], data['w'], data['h'])
    # mat, bb = of.rectangle_face(mat)
    # if mat is None:
    #     return { "ret":-1}
    # mat = of.landmark_face(mat, bb)
    # if mat is None:
    #     return { "ret":-1}
    # data_url = of.cvMat2DataUrl(mat)
    # return { "ret":0, 'dataURL': data_url}
    pass

@socketio.on('cmp_face')
def cmp_face(data):
    # print('received json: ' + str(data))
    # or socketio.emit
    # emit('event_return', {'name': 'david', 'age':39})
    # return of.cmp_imgs(data['img1'], data['img2'])
    pass
    
if __name__ == '__main__':
    print('flask socket.io listen on port: 1979')
    socketio.run(app, host="0.0.0.0", port=1979)