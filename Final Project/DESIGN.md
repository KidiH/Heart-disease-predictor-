Machine learning
================

The technical core of the project consists of four Python files: Train.py, ScaleData.py, SplitData.py, and Predict.py. The web application itself uses only two of these, Predict.py and ScaleData.py, whereas the others are meant for updating the model when maintaining the website.

The raw data is stored in ./Data/heart.csv file. This file contains around 300 data points. Each data point has 13 features (age, sex, maximum heart rate, etc.) and 1 target label (1 -- a person has the disease, 0 -- a person doesn't have the disease).

The files SplitData and ScaleData process the raw data, and the output is an array of scaled data, scaled to the range (0, 1). The reason why this is being done is because it need to be ensured that all features and labels have the same order of magnitude. This helps the neural network converge faster, and minimizes chances of a round-off error that blows up. In the process of scaling the data, an array of scalers is also saved to a file "XScalers.save". These scalers are later used for prediction, which will be explained later.

The file Train takes the scaled data from SplitData and ScaleData, builds and compiles a neural network, and trains it on the train data. We chose the neural network that had two hidden layers, one with 3 nodes and the other with 2 nodes. We tried several different network structures, and this one performed best, in the sense that it had the best accuracy score and minimal test loss. After training the network, Train then saves it into the file called "model.h5". This file is later used for prediction, which will be explained later. The web application itself doesn't use Train.py. The reason for this is that we don't want to train the network every time a user want to perform a prediction, as it takes a lot of time and is completely unnecessary. Instead, the idea is that the team who maintains the website train the network as necessary (for example, new data is added, a better model is found, a different network stucture performs better, etc.). The "model.h5" and "Xscalers.save" files will then get replaced, and the website will be able to keep running with updated data, without affecting the performance delivered to the end user.

The exact design of the web application is described below. As for the machine learning part, the website prompts the user for certain data. Once the data is received, the data is then scaled using the saved scalers in "XScalers.save". The scaled data is then passed to the file "Predict.py". This file then loads the saved model from "model.h5", and then performs the prediction using the (scaled) data from the user and the saved parameters of the network. The prediction is then passed back to the application and displayed to the user.


Web
===

As you access the website you will be directed to the homepage.The page hold statistics of how many people suffer from heart disease and shows the severity of the problem. 

Register : On the register page, the user will be prompted to input a username, a password and a confirmation of that password. Error handelers check if the any of the input fields are empty, if the username is already in use by another person, and if the passwords match. If the user fails to properly input the required text, an error message will be displayed telling them so.

Login: Once registered, the user will be taken to the login page. The page prompts the user to input the correct username and password combination. Similar to register, error handlers check if any of the fields are empty and if the username and password combination is invalid. 

When the user successfully logs in, they will be taken to a page with a form they need to fill out. Each field in the form correlates to a characteristic that is used by the machine learning code to predict the chance of a person in having a heart disease. 

Field 1: Age – Prompts the user to input a valid age of above 15. If the user fails to do so, an error message will be displayed telling them.
Field 2 – Sex : Offers a dropdown list from which the user chooses which sex they are. 
Field 3 – Weight: Takes in input from the user of number up to a precision of 0.1
Field 4 -  Chest pain: Displays a 4 choices from the user chooses which type of chest pain they have. If they don’t know, they may mark the check box that says so. Marking this check box assigns the user a chest pain of normal. 
Field 5 – Resting blood pressure: Prompts the user to input their resting blood pressure results. The number should be within the bounds of 70 to 250. If the user does not know about their result, they will be assigned a resting blood pressure result of 140(the average of an adult).
Field 6  - Cholestrol: The user is asked to input the test result for the level of cholesterol in their blood. The input should be with the range of 50 to 500(a high test result from the database). If the user does not know about their cholesterol level, they may mark the check box assigning them a result of 200.
Field 7 – Fasting blood sugar: The user is asked if they have elevated blood sugar level, meaning higher than 120. If the user does not know, theu will be assigned a result of NO.
Field 8 – Resting Electorcardiographic results: A drop down list that asks the user to choose from the 4 options available. If the user does not know, they will be assigned a result of NORMAL.
Field 9 – Maximum heart rate achieved: Asks the user to input their highest heart rate. 
Field 10 – Endused Angina: Asks the user whether they have indused angina or not. They may choose to say YES, NO or I DON’T KNOW. If they choose I DON’T KNOW, they will be assigned a result of NO.
Field 11 – ST depression result: Prompts the user to input result of an ST depression test. The field accepts result from 0 to 6 with a precision of 0.1.
Field 12 – Peak of ST segement : A dropdown list  that asks the user  what their ST segment looks like. There are 3 options to choose from and one that allows the user to say they don’t know. If chosen, they will be assigned a value of 0.
Field 13 – Number of major vessels colored in fluoroscopy: Offers a dropdown list of the possible number of major blood vessels that is colored by the test. If the user does not know, they may specify so to be assigned a result of 0.
Field 14 – Thal: Similarly offers a dropdown list of the possible result. If the user does not know, they will be assigned a result of 0.

In all of the fields, error handlers check if an entry has been made, a valid value is inputted, and if not display an error message notifying the user of the problem. In some of the fields, there are buttons next to the text box informing the user what it is they are expected to input. Furthermore, the “I don’t know” check box assigns a user with a value that is a normal result for an adult. 

Finally after inputting valid results, the user is able to see their result, as by clicking the predict button. If the result of the user is below 50%, as it is not as concerning, they will see a page with a green alert banner and links to tips on how to remain healthy. On the other hand, if the user has more than a 50% chance, the page displays a red alert banner telling them so. And also links directing them to make an appointment with a doctor. 
