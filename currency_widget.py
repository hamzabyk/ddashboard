# currency_widget.py
import yfinance as yf
import plotly.graph_objs as go
from dash import html

def get_currency_widget():
    currencies = {
        "USD/TRY": "USDTRY=X",
        "EUR/TRY": "EURTRY=X",
        "GBP/TRY": "GBPTRY=X",
        "GA (Altın)": "GC=F"  # XAUUSD çalışmıyor, yerine altın vadeli işlemler kullanıldı
    }

    items = []
    for name, ticker in currencies.items():
        try:
            data = yf.Ticker(ticker).history(period="1d")
            price = round(data["Close"].iloc[-1], 2)
        except Exception:
            price = "—"
        items.append(html.Div(f"{name}: {price}", className="text-white small mb-1"))

    return html.Div(items, style={"backgroundColor": "#1a1a1a", "padding": "10px", "borderRadius": "5px"})
