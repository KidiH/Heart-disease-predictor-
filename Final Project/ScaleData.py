# In this file, we define functions whose purpose is to scale our training data. Neural networks
# can screw up fitting the model if the ranges of data wildly differ, for example one feature has values
# that go up to 100,000 and another has values that in the range [0, 1]. That is why we perform scaling of the data.
# In other words, for every feature we are going to rescale the range to be [0, 1]. For that, we use the function
# MinMaxScaler, that's defined in the sklearn library.
# Note that we are not scaling Y, because it's already in [0, 1] range. Even better, Y is discrete, so it can
# only take values 0 and 1.

###############################################################################

from sklearn.preprocessing import MinMaxScaler
import joblib
import numpy as np

###############################################################################

# This function takes the data as an input, and "fits" the scalers according to this data. In other words, the function
# sets the parameters of the scalers such that the maximum value gets scaled to 1, and the minimum value gets scaled to 0.
# We are performing separate scaling for each column of X. The function returns the array of fitted scalers.
# Also, the function saves the scalers into a file "XScalers.save" for later use.
def FitScalers(X):
    XScalers = []
    # Because we wanted to take columns instead of rows, we need to transpose X.
    for column in X.T:
        Scaler = MinMaxScaler()
        # MinMaxScaler takes column vectors as inputs, so we need to reshape a row vector into a column vector.
        # Then we fit the scaler.
        Scaler.fit(np.reshape(column, (len(column), 1)))
        # Finally, append the scaler to the list.
        XScalers.append(Scaler)
    
    # Save the array of scalers into "XScalers.save".
    joblib.dump(XScalers, "XScalers.save")
    # Return the array of scalers.
    return XScalers

###############################################################################

# This funcion takes the data and the array of scalers as an input. The array of scalers is the array of fitted
# scalers that we fit in FitScalers function. The function returns the scaled data.
def ScaleData(X, XScalers):
    XScaled = np.empty((X.shape[0], 0))  # Define an empty array of appropriate dimensions.
    for i in range(X.shape[1]): # Iterate over all columns in data.
        Scaler = XScalers[i]  # Choose the appropriate scaler from the array.
        # Append the scaled column to the array we defined.
        XScaled = np.append(XScaled, Scaler.transform(np.reshape(X[:, i], (X.shape[0], 1))), axis=1)
    
    # Return the scaled data.
    return XScaled

###############################################################################

# This function takes the data and the array of scalers as an input. The array of scalers is the array of fitted
# scalers that we fit in FitScalers functio. The function then reverts the scaled data back to the unscaled data.
def UnscaleData(X, XScalers):
    XUnscaled = np.empty((X.shape[0], 0))  # Define an empty array of appropriate dimensions.
    for i in range(X.shape[1]):  # Iterate over all columns in data.
        Scaler = XScalers[i]  # Choose the appropriate scaler from the array.
        # Appen the unscaled column to the empty array that we defined earlier.
        XUnscaled = np.append(XUnscaled, Scaler.inverse_transform(np.reshape(X[:, i], (X.shape[0], 1))), axis=1)
    
    # Return the array of unscaled data. Note that this function ended up not being used
    # in the final code, but it's very useful for debugging purposes, as we can unscale the
    # data at any point in the code and see what's going on.
    return XUnscaled

###############################################################################