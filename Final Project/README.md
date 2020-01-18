Setting up packages
===================

To run the application, Python 3 needs to be installed. The latest version as of December 4 2019 is Python 3.8 and that version is NOT supported. Instead, Python 3.7 should be used. Besides the standard packages, the following packages need to be installed as well:

* matplotlib
* numpy
* keras (version 2.3.1)
* tensorflow (version 1.13.1)
* sklearn
* joblib
* cs50
* flask-session
* requests

For keras and tensorflow, it is crucial to install the specified versions, as the newer versions are not supported. If you already have newer versions of these packages installed, it's probably the best idea to create a virtual environment through Anaconda and install the packages within that environment. More on that can be found here: https://anaconda.org/anaconda/virtualenv . Alternatively, you can use "pip uninstall [package]" to uninstall a package, and then "pip install [package]==[version]" to re-install the desired version.

If you don't have the packages already installed, you can simply use "pip install [package]==[version]".

For the packages that don't have the version specified, you can install the latest version.


Setting up the server
=====================

After you have finished installing the packages, open the Windows Command Prompt. Using the "cd" command, navigate to the directory where the "application.py" file is located. Execute the command "python application.py". After a few seconds, you should see notifications telling you that the Flask app is up and running. The last line should end with
"Running on http://[address] (press CTRL+C to quit)".
Copy the "http://[address]" part and paste it into your web browser. You should now see the login screen of the website.


Navigating the website
======================

Once you access the website, you will be directed to the homepage. To get to the predictor, you need to create an account, therefore head to the register page as by clicking the register button in the homepage or choose the option from the navigation pane.
In the register page, enter your creditentials, and create your own account. If you successful enter a username and password, you'll be directed to the page with a form. 
The form will ask questions that you need to answer in order to make the prediction based on your situation. Enter all of the fields with a valid input to get a better prediction. 
When you hit the predict button, you will be directed to a page that displays your result. Depending on the prediction, a page with recommendations will be displayed. 

