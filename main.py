# -*- coding: utf-8 -*-
"""
Pair Trading Decision Engine
Applied Computer Science Project

Author: T
"""

from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.tsa.stattools import adfuller

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Form

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Pair Trading Decision Engine",
    description="AI-Enhanced Pair Trading Strategy using S&P 500 Technology Stocks",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


class PairRequest(BaseModel):
    stock1: str
    stock2: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "latest_spread": 0.2935
        }
    )


@app.post("/analyze-pair")
def analyze_pair(pair: PairRequest):

    # Download data
    data = yf.download(
        [pair.stock1, pair.stock2],
        start="2018-01-01",
        end="2026-08-01",
        auto_adjust=True
    )

    # Closing prices
    prices = data["Close"][[pair.stock1, pair.stock2]]
    prices = prices.dropna()

    # Log prices
    pair_log_prices = np.log(prices)
    
    # Rename columns for OLS
    pair_log_prices.columns = [
        "stock1",
        "stock2"
    ]

    # Training period
    train_log_prices = pair_log_prices[
        pair_log_prices.index <= "2025-12-31"
    ]

    # Testing period
    test_log_prices = pair_log_prices[
        pair_log_prices.index >= "2026-01-01"
    ]



    # OLS regression
    model = ols(
       "stock1 ~ stock2",
       data=train_log_prices
    ).fit()

    # Training spread
    spread_train = model.resid

    
    # Spread last year
    spread_last_year = spread_train[
        spread_train.index >= "2025-01-01"
    ]

    spread_mean = spread_last_year.mean()
    spread_std = spread_last_year.std()
    
    
    # Apply the model to the testing period
    alpha = model.params["Intercept"]
    beta = model.params["stock2"]
    
    # Predicted values
    stock1_pred = (
        alpha
        + beta * test_log_prices["stock2"]
    )
    
    # Testing spread
    spread_test = (
        test_log_prices["stock1"]
        - stock1_pred
    )

    # Standardized Z-Score
    z_score = (
        spread_test - spread_mean
        ) / spread_std
    
    # Latest values
    latest_spread = spread_test.iloc[-1]
    latest_z_score = z_score.iloc[-1]
    
    # Trading thresholds from Phase 4
    long_threshold = -0.31
    short_threshold = 4.14

    if latest_z_score < long_threshold:

        signal = "LONG SPREAD"
        signal_icon = "🟢"

        signal_reason = (
            "Z-score is below the long threshold."
        )

    elif latest_z_score > short_threshold:

        signal = "SHORT SPREAD"
        signal_icon = "🔴"

        signal_reason = (
            "Z-score is above the short threshold."
        )

    else:

        signal = "NO SIGNAL"
        signal_icon = "🟡"

        signal_reason = (
            "Z-score is within the normal range."
    )

    # ADF test on spread
    adf_result = adfuller(spread_train)

    # ADF p-value
    p_value = adf_result[1]

    if p_value < 0.05:

        return {
            "pair": f"{pair.stock1}-{pair.stock2}",
            "p_value": round(float(p_value), 4),
            "cointegrated": True,
            "status": "COINTEGRATED",
            "status_icon": "✅",
            "status_colour": "green",
            "message": "Proceed with spread analysis",
            "latest_spread": round(float(latest_spread), 4),
            "latest_z_score": round(float(latest_z_score), 4),
            "long_threshold": -0.31,
            "short_threshold": 4.14,
            "signal": signal,
            "signal_icon": signal_icon,
            "signal_reason": signal_reason
        }

    else:

        return {
        "pair": f"{pair.stock1}-{pair.stock2}",
        "p_value": round(float(p_value), 4),
        "cointegrated": False,
        "status": "NOT COINTEGRATED",
        "status_icon": "❌",
        "status_colour": "red",

        "message": "Analysis stopped. Pair is unsuitable for pair trading.",

        "latest_spread": "N/A",
        "latest_z_score": "N/A",

        "long_threshold": "N/A",
        "short_threshold": "N/A",

        "signal": "NO SIGNAL",
        "signal_reason": "Pair is not cointegrated."
    }
    
@app.post("/dashboard")
def dashboard_analysis(
    request: Request,
    stock1: str = Form(...),
    stock2: str = Form(...)
):

    pair = PairRequest(
        stock1=stock1,
        stock2=stock2
    )

    results = analyze_pair(pair)

    results["stock1"] = stock1
    results["stock2"] = stock2

    results["request"] = request

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=results
)