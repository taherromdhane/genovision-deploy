import numpy as np
import math
import os
import cv2
from model import get_model_classif_nasnet
from predict_utils import get_windows, get_predictions, CCL, get_labeled_boxes, get_labeled_image, get_filled_image

def load_model(modelpath="model/model.h5") :
    model = get_model_classif_nasnet()    
    # First thing to do is to load the model
    model.load_weights(modelpath)
    model._make_predict_function()          # Necessary
    print('Model loaded. Start serving...')
    return model

def predict(model, image) :
    # We define variables we'll need in the functions
    w_size = 32

    height = image.shape[0]
    width = image.shape[1]
    windows_x = math.ceil(image.shape[0]/w_size)
    windows_y = math.ceil(image.shape[1]/w_size)    

    # We first get our predictions matrix, where each element is a prediction for a window of the image
    preds = get_predictions(model, image, windows_x, windows_y, w_size, height, width)

    # We then compute the labels of each region as well as groups for bounding boxes        
    labels = CCL(preds)
    groups = get_labeled_boxes(labels)

    # Creating the labeled image with bouding boxes
    labeled_img = get_labeled_image(image, groups, w_size, height, width, alpha=0.2)

    # Creating the filled image with positive regions filled
    filled_img =  get_filled_image(image, groups, windows_x, windows_y, w_size, labels, height, width, alpha=0.2)

    return labeled_img, filled_img