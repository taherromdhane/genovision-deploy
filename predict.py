import numpy as np
import math
import os
import cv2
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.keras.models import load_model
# from model import get_model_classif_nasnet
from predict_utils import get_windows, get_predictions, CCL, get_labeled_boxes, get_labeled_image, get_filled_image
import sys


# This is the old method, load nasnet model then load weights, changed into tensorflow loading

# def load_model(modelpath="model/model.h5") :
    
#     session = tf.Session()
#     graph = tf.get_default_graph()
#     set_session(session)

#     # initialize model
#     model = get_model_classif_nasnet()    
#     # First thing to do is to load the model
#     model.load_weights(modelpath)

#     model._make_predict_function()          # Necessary
#     print('Model loaded. Start serving...', file=sys.stderr)
#     return model, session, graph

def load_model_tf(modelpath = 'model/saved_model') :
    # Load model with tensorflow saved_model format

    session = tf.Session()
    graph = tf.get_default_graph()
    set_session(session)

    # Load with tensorflow
    model = load_model(modelpath)
    
    model._make_predict_function()          # Necessary
    print('Model loaded. Start serving...', file=sys.stderr)
    return model, session, graph

def predict(model, image, session, graph) :
    # We define variables we'll need in the functions
    w_size = 32

    height = image.shape[0]
    width = image.shape[1]
    windows_x = math.ceil(image.shape[0]/w_size)
    windows_y = math.ceil(image.shape[1]/w_size)    

    # We first get our predictions matrix, where each element is a prediction for a window of the images
    preds = get_predictions(model, image, windows_x, windows_y, w_size, height, width, session, graph)

    # We then compute the labels of each region as well as groups for bounding boxes        
    labels = CCL(preds)
    groups = get_labeled_boxes(labels)

    # Creating the labeled image with bouding boxes
    labeled_img = get_labeled_image(image, groups, w_size, height, width, alpha=0.2)

    # Creating the filled image with positive regions filled
    filled_img =  get_filled_image(image, groups, windows_x, windows_y, w_size, labels, height, width, alpha=0.2)

    return labeled_img, filled_img