Open the live application on https://pairtradingdecisionengine.onrender.com/
How to use the application
-	Select Stock 1
-	Select Stock 2
-	Click on Analyze Pair
-	Review the generated dashboard output
You will see the following results displayed by the application
-	Cointegration status: if the pair is cointegrated or not based on the Augmented Dickey-Fuller test (ADF) p-value. 
-	Current Spread
-	Current Z-Score
-	Trading Signal: for the cointegrated pairs the application generates one of the three trading signals: long-, short spread, no signal. The signal is determined using predefined Z-score thresholds.
-	A visual Mean Reversion Indicator which higlights long, short, and neutral zone based on the generated trading signal.
There is a validation in place, which means if the user selects the same stock from the dropdown menu for stock 1 and stock 2 the application will give an invalid pair result and ask the user to select two different stocks.
The following technologies were used:
•  Python 
•  FastAPI 
•  Jinja2 
•  NumPy 
•  Pandas 
•  Statsmodels 
•  yfinance 
•  HTML 
•  CSS 
•  GitHub 
•  Render

Data and Methodology
Model development period: 01 January 2018 – 31 December 2025
Testing period: From 01 January 2026 to 01 August 2026.
Statistical techniques
In the application: 
•  Ordinary Least Squares (OLS) Regression 
•  Augmented Dickey-Fuller (ADF) Test 
•  Spread Calculation 
•  Standardized Z-score Calculation
The full project code which was developed in Python notebook contains the phase 5 machine learning for predicting spread as well. As it was not a requirement for the application to contain this phase the Financial Markets Final.html document will contain all the phases and the connected Financial Market Final python code.
Deployment Process
-	The code was uploaded to GitHub (The GitHub Repository is https://github.com/rekakollar/PairTradingDecisionEngine)
-	Connected the repository to Render
-	Python Web Service has been created
-	The build and start commands have been configured
-	The application has been deployed.
Known Limitations
-	The real time market data is not currently implemented, as the task was to use a fixed historical evaluation window.
-	Analysis is performed on a predefined set of S&P Technology stocks.
