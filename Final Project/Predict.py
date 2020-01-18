# This code performs the prediction on a given input, using the model saved in
# "model.h5" and scalers saved in "XScalers.save".

###############################################################################

import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras import optimizers
from sklearn.metrics import confusion_matrix, accuracy_score
from keras import regularizers
from ScaleData import ScaleData
import joblib

###############################################################################

# This function takes the input data, loads the model and the scalers, and returns
# the prediction.
def Predict(X):

    # Load the trained model.
    model = load_model('model.h5')

    # Convert X to a numpy array.
    X = np.asarray(X)
    
    # Reshape X into a row vector.
    X = np.reshape(X, (1, len(X)))

    # Load the scalers.
    XScalers = joblib.load("XScalers.save")

    # Scale the data using the saved scalers.
    X_scaled = ScaleData(X, XScalers)

    # Perform the prediction. The result will be a 2D array, so we want to take
    # its only entry.
    Y = model.predict(X_scaled)[0][0]

    # Return the prediction.
    return Y

###############################################################################