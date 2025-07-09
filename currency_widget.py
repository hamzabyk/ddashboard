# currency_widget.py
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import dash_html_components as html

def get_currency_widget():
    symbols = {
        "USD/TRY": "USDTRY=X",
        "EUR/TRY": "EURTRY=X",
        "GBP/TRY": "GBPTRY=X",
        "RUB/TRY": "RUBTRY=X"
    }

    prices = {}
    for label, ticker in symbols.items():
        try:
            data = yf.download(ticker, period="1d", interval="1h")
            price = round(data["Close"].iloc[-1], 2)
            prices[label] = price
        except:
            prices[label] = "-"

    table = html.Table([
        html.Tr([html.Th("Kur", style={"color": "white"}), html.Th("Fiyat", style={"color": "white"})])
    ] + [
        html.Tr([
            html.Td(k, style={"color": "white"}),
            html.Td(str(v), style={"color": "white"})
        ]) for k, v in prices.items()
    ], style={"border": "1px solid white", "padding": "10px"})

    return table
