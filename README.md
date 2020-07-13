# Stock Prediction App

Simple stock predictionapplication to demonstrate prediction using fbprophet and integrating dash core components and http requests. 


# Demo Link 

click <a href="https://youtu.be/Bs1v7tfq-2Q" target="_blank">**Stock Market Prediction**</a> to see the demo.

**quick demo**

![Recordit GIF](http://g.recordit.co/SBvuRoucD5.gif)


# Contents

* ```app.py``` - Front and back end portion of the web application excluding css and static data
* ```Assets Folder```  - css files and static images
* ```models``` - it contains script for extarcting data from yahoo finannce and fbprophet prediction.
* ```src```- conatins stock file extracted from yahoo finance
* ```out```- contains final predicton file.

# Installation

* Download the entire repository as a folder and open ```app.py``` and run it with IDE . That's it!
   http://127.0.0.1:5001/
   
 ```
stock_prediction-Directory Tree

├─ app.py
├─ assets
│  ├─ images.jpg
│  └─ stylesheet.css
├─ LICENSE
├─ models
│  ├─ prophet.py
│  └─ __pycache__
│     └─ prophet.cpython-36.pyc
├─ out
│  ├─ pred_prophet_IOC.NS.csv
├─ README.md
├─ src
│  ├─ stock_price_IOC.NS.csv
└─ __pycache__
   └─ test.cpython-36.pyc

```
   
# Source: 
 *  https://dash.plotly.com/basic-callbacks
 *  https://finance.yahoo.com/lookup/
 *  https://pypi.org/project/fbprophet/


