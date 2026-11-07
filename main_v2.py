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

app = FastAPI(
    title="Pair Trading Decision Engine",
    description="AI-Enhanced Pair Trading Strategy using S&P 500 Technology Stocks",
    version="1.0"
)


class PairRequest(BaseModel):
    stock1: str
    stock2: str


@app.get("/")
def home():
    return {
        "message": "Welcome to the Pair Trading Decision Engine",
        "available_stocks": [
            "MSFT",
            "GOOGL",
            "NVDA",
            "AAPL",
            "AMZN",
            "META"
        ]
    }


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

    # OLS regression
    model = ols(
        "stock1 ~ stock2",
        data=pair_log_prices
    ).fit()

    # Spread (residuals)
    spread = model.resid
    
    # Spread statistics
    spread_mean = spread.mean()
    spread_std = spread.std()

    # Standardized Z-Score
    z_score = (
        spread - spread_mean
        ) / spread_std
    
    # Latest values
    latest_spread = spread.iloc[-1]
    latest_z_score = z_score.iloc[-1]

    # ADF test on spread
    adf_result = adfuller(spread)

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
            "latest_z_score": round(float(latest_z_score), 4)
        }

    else:

        return {
            "pair": f"{pair.stock1}-{pair.stock2}",
            "p_value": round(float(p_value), 4),
            "cointegrated": False,
            "status": "NOT COINTEGRATED",
            "status_icon": "❌",
            "status_colour": "red",
            "message": "Analysis stopped. Pair is unsuitable for pair trading."
        }
    
