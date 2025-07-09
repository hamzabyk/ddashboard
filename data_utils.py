# data_utils.py
import pandas as pd
import plotly.graph_objs as go


def load_bist30_data():
    df = pd.read_csv("data/bist30.csv")
    return df


def get_graphs(symbol):
    df = pd.read_csv("data/bist30.csv")
    df_symbol = df[df["Sembol"] == symbol]

    if df_symbol.empty:
        return {"name": symbol, "price": 0, "change": 0, "volume": 0, "rsi": 0}, go.Figure(), go.Figure()

    name = df_symbol.iloc[0]["Şirket"]
    price = df_symbol.iloc[0]["Fiyat"]
    change = df_symbol.iloc[0]["Değişim %"]
    volume = df_symbol.iloc[0]["Hacim"]
    rsi = df_symbol.iloc[0]["RSI"]

    # RSI grafiği
    rsi_fig = go.Figure(data=go.Scatter(
        x=[symbol],
        y=[rsi],
        mode='markers+text',
        text=[f"RSI: {rsi}"],
        textposition="top center"
    ))
    rsi_fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} RSI"
    )

    # Hacim grafiği
    volume_fig = go.Figure(data=go.Bar(
        x=[symbol],
        y=[volume],
        marker_color='lightblue'
    ))
    volume_fig.update_layout(
        template="plotly_dark",
        title=f"{symbol} Hacim"
    )

    info = {
        "name": name,
        "price": price,
        "change": change,
        "volume": volume,
        "rsi": rsi
    }

    return info, rsi_fig, volume_fig


def get_bist30_index_fig():
    df = pd.read_csv("data/bist30.csv")
    df_sorted = df.sort_values("Tarih")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted["Tarih"],
        y=df_sorted["BIST30"],
        mode='lines',
        line=dict(color='royalblue')
    ))

    fig.update_layout(
        template="plotly_dark",
        title="BIST 30 Endeks Grafiği"
    )

    return fig
