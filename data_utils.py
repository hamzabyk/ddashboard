import pandas as pd
import plotly.graph_objs as go

def load_bist30_data():
    df = pd.read_csv("data/bist30-3.csv")
    df["Değişim %"] = df["Değişim %"].astype(float)
    return df

def get_graphs(symbol, data):
    hist = data[data["Sembol"] == symbol]

    info = {
        "name": hist.iloc[0]["Şirket"],
        "price": hist.iloc[0]["Fiyat"],
        "change": hist.iloc[0]["Değişim %"],
        "volume": hist.iloc[0]["Hacim"],
        "rsi": hist.iloc[0]["RSI"]
    }

    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=[1], y=[info["rsi"]], mode='lines+markers', name='RSI'))
    rsi_fig.update_layout(template="plotly_dark", height=300, margin=dict(l=30, r=30, t=30, b=30))

    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(x=[symbol], y=[info["volume"]], name='Hacim'))
    vol_fig.update_layout(template="plotly_dark", height=300, margin=dict(l=30, r=30, t=30, b=30))

    return info, rsi_fig, vol_fig

def get_bist30_index_graph(data):
    semboller = data["Sembol"].unique()
    fiyatlar = [data[data["Sembol"] == s]["Fiyat"].mean() for s in semboller]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semboller, y=fiyatlar, mode='lines+markers'))
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=30, r=30, t=30, b=30))

    stats = {
        "value": round(sum(fiyatlar), 2),
        "monthly_change": "%+0.2f" % data["Değişim %"].mean(),
        "yearly_change": "%+0.2f" % (data["Değişim %"].mean() * 12),
        "volume": int(data["Hacim"].sum())
    }

    return fig, stats
