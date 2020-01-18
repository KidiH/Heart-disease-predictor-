# This function will accept the name of the CSV file and TrainEnd, read the data from the CSV file,
# split the data into X and Y. X are the characteristics of people, and Y is 0 or 1; 1 if they have
# the disease, 0 if they don't. TrainEnd is a number between 0 and 1 that essentially tells the function
# what percentage of data should be used as training, and what percentage should be used for testing.
# Based on TrainEnd, both X and Y are split into X_train and X_test (Y_train and Y_test). The function
# returns training and testing data, as well as the number of featurs (properties) and the total number of
# data points that we have.

###############################################################################

import numpy as np  # A library for dealing with arrays
from pandas import read_csv  # A library for data processing

###############################################################################

def SplitData(data, TrainPercent):
    # Take the name of the CSV file.
    read_data = read_csv(data)
    # Conver the data to a numpy array.
    read_data = np.array(read_data)
    # Randomly shuffle rows in the data array. This is very important. Note that
    # the CSV file lists all people with target 1 first, and then only people with
    # target 0. This was actually a bug that took significant time to debug, as
    # we were training the network only on the data with target 1, so the network
    # was essentially trained to always perform classification 1.
    np.random.shuffle(read_data)
    # Take the last column of data as Y.
    Y = read_data.T[-1]
    # Take all other columns as X.
    X = read_data.T[:-1]
    # Transpose X.
    X = X.T
    # Store the number of data points (rows) in the table.
    NumOfPoints = X.shape[0]
    # Store the number of features. These are age, sex, etc.
    NumOfFeatures = X.shape[1]
    # Reshape Y to be a column vector.
    Y = np.reshape(Y, (NumOfPoints, 1))
    
    # Define TrainEnd as the next lower integer of TrainPercent * NumOfPoints.
    # E.g. if we want to train the network on 80% of data, then we would have
    # 0.8 * NumOfPoints, so we would essentially select TrainEnd to be the index
    # which separates 80% and 20% of data.
    TrainEnd = int(np.floor(TrainPercent * NumOfPoints))
    # Take everything up until TrainEnd to be training data.
    # Take everything from TrainEnd onward to be test data.
    X_train = X[:TrainEnd, :]
    X_test = X[TrainEnd:, :]
    Y_train = Y[:TrainEnd, :]
    Y_test = Y[TrainEnd:, :]
    
    # Return training data, test data, number of features, and number of points.
    return X_train, X_test, Y_train, Y_test, NumOfFeatures, NumOfPoints

###############################################################################