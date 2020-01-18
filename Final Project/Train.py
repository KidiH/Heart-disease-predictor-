# This part of the code trains the neural network and saves the trained model
# to be used for later prediction.

###############################################################################

from SplitData import SplitData
from ScaleData import FitScalers, ScaleData, UnscaleData
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
from sklearn.metrics import confusion_matrix, accuracy_score
from keras import regularizers
import matplotlib.pyplot as plt

###############################################################################

# Pass the path to CSV file and TrainPercent to SplitData. The reason why we're passing
# 0.99 is that in the final product we want to train our network on all available data.
# When testing the network and debugging, we need to train on less, to see how it performs
# on the test data. The reason why it's not exactly 1 is that passing 1 would make the code
# more complicated, as we would constantly need to check if the passed array is None.
# This way, the code remains simple, and the amount of data we're discarding is next to nothing.
X_train, X_test, Y_train, Y_test, NumOfFeatures, NumOfPoints = SplitData("./Data/heart.csv", 0.99)

# Fit the scalers on the train data.
XScalers = FitScalers(X_train)

# Scale the data, both train and test. The reason why we're not fitting the scalers on the
# test data as well is that it would defeat the purpose of having test data; it is assumed
# that the test data is not a priori known when training the network.
X_train_scaled = ScaleData(X_train, XScalers)
X_test_scaled = ScaleData(X_test, XScalers)

###############################################################################

# Instantiate the model. We are using the Sequential model, which is a neural network
# with sequences of layers.
model = Sequential()

# Define all layers. Here, we have an input layer, two hidden layers, and an output layer.
# The activation function we are using is sigmoid. It is convenient as its domain is
# the set of all real numbers, and range is (0, 1), which is exactly the output that
# we need.
layer1 = Dense(3, activation='sigmoid', input_shape=(NumOfFeatures, ), activity_regularizer=regularizers.l2(0.01))
layer2 = Dense(2, activation='sigmoid', activity_regularizer=regularizers.l2(0.01))
layer_out = Dense(1, activation='sigmoid')

# Add the defined layers to the model.
model.add(layer1)
model.add(layer2)
model.add(layer_out)

# Compile the model. Here, we are using the Adam optimizer, which is one of the best
# optimizers for neural networks like this. The loss function is binary cross-entropy,
# which is very good for classification (which we are essentially doing), as opposed to
# MSE (mean squared error), which is optimal for reggression problems.
model.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')

# Fit the model. Here we are passing the train data (scaled), and validating on the test data.
# We choose to train for 2000 epochs (we determined that this is optimal to minimize the loss
# function), and the batch size is 32, which is pretty standard. Also, the values of loss
# during epochs are being stored in history, which can be used for analysis.
history = model.fit(X_train_scaled, Y_train, validation_data = (X_test_scaled, Y_test), epochs=2000, batch_size=32, verbose=0)

# Save the model into a file "model.h5" for later use.
model.save('model.h5')

###############################################################################

# Compute both the predictions on the training data and test data using the trained
# network. Note that a better match is expected for training data.
Y_train_output = model.predict(X_train_scaled)
Y_test_output = model.predict(X_test_scaled)

# We already said that the range of sigmoid function is (0, 1). This function sets
# everything higher than 0.5 to 1 (disease), and everything lower than 0.5 to 0 (no disease).
Y_train_output = (Y_train_output > 0.5)
Y_test_output = (Y_test_output > 0.5)

# Print the confusion matrix, both for training set and test set. The confusion
# matrix is a 2x2 matrix which tells us how many true positives and negatives we have,
# as well as how many false positives and negatives we have.
print('Confusion matrix for the training set:', confusion_matrix(Y_train, Y_train_output))
print('Confusion matrix for the test set: ', confusion_matrix(Y_test, Y_test_output))

# Print the accuracy score, both for training set and test set. The accuracy score
# is a percentage that tells us simply what fraction of our guesses were correct.
# We managed to hit an average accuracy score of about 80% on the test set.
print('Accuracy score for the training set:', accuracy_score(Y_train, Y_train_output))
print('Accuracy score for the test set:', accuracy_score(Y_test, Y_test_output))

# Plot the loss function as a function of the number of epochs, both for training
# and test set. This can be used for debugging purposes, to determine the optimal
# number of epochs, regularization, etc.
f = plt.figure(1)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Train','Test'],loc='best')
plt.xlabel('Epoch')
plt.ylabel('Loss')
f.show()

###############################################################################