from __future__ import print_function
from flask import Flask, request, jsonify, render_template, make_response, send_file, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import numpy as np
import cv2
import json
import base64
from predict import load_model_tf, predict
import sys
import os

model, session, graph = load_model_tf()

app = Flask(__name__)

"""
Routes
"""

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/index')
def index2() :
    return redirect('/')

@app.route('/upload', methods=["GET", "POST"])
def upload() :    
    return render_template('upload.html')


#Utility functions for prediction
def json2im(filestr) :
    npimg = np.fromstring(filestr, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    return image

def im2json(image) :
    _, imdata = cv2.imencode('.PNG', image)
    jstr = base64.b64encode(imdata).decode('ascii')
    return jstr

@app.route('/predict', methods=["POST"])
def prediction() :
    if request.method == 'POST':
        filestr = request.files['image'].read()
        image = json2im(filestr)

        labeled_img, filled_img = predict(model, image, session, graph)

        print("got predictions", file=sys.stderr)

        labeled_jstr = im2json(labeled_img)
        filled_jstr = im2json(filled_img)
        result = {
            "prediction": {
                "labeled_img": labeled_jstr,
                "filled_img": filled_jstr
            }
        }
        response = jsonify(result)
        return make_response(response, 201)
    return None 


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000, debug=True)
    
    http_server = WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), app)
    print(int(os.environ.get("PORT", 5000)), file=sys.stderr)
    http_server.serve_forever()
    