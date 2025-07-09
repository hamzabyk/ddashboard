# app.py
from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import os
from data_utils import load_bist30_data, get_graphs, get_bist30_index_fig
from currency_widget import get_currency_widget

external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

data = load_bist30_data()
bist30_fig = get_bist30_index_fig()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("📊 BIST 30 Endeksi", className="text-white mb-3"),
            dcc.Graph(figure=bist30_fig, id="bist30-endeks-grafik", style={"marginBottom": "2rem"}),
            html.Div(id="bist30-ozet", className="text-white")
        ], width=6),

        dbc.Col([
            html.H4("📈 RSI ve Hacim Grafikleri", className="text-white mb-3"),
            dcc.Tabs([
                dcc.Tab(label="RSI", children=[dcc.Graph(id="rsi-graph")]),
                dcc.Tab(label="Hacim", children=[dcc.Graph(id="volume-graph")])
            ]),
            html.Div("RSI: Göreli Güç Endeksi, hisse fiyatındaki momentumu ölçer.", className="text-muted small mt-2"),
            html.Div("Hacim: İşlem gören hisse adedini ifade eder.", className="text-muted small")
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("📋 Hisseler", className="text-white mt-4 mb-2"),
            html.Div(id="stock-list", style={"maxHeight": "400px", "overflowY": "scroll"})
        ], width=6),

        dbc.Col([
            html.H4("🗞 Haberler ve Döviz", className="text-white mt-4 mb-2"),
            dbc.Row([
                dbc.Col([
                    html.Div("📢 Örnek Haber 1: Borsa İstanbul'da işlem hacmi rekor kırdı.", className="text-muted small mb-2"),
                    html.Div("📢 Örnek Haber 2: TCMB faiz kararını açıkladı.", className="text-muted small mb-2")
                ], width=6),
                dbc.Col([
                    get_currency_widget()
                ], width=6)
            ])
        ], width=6)
    ]),

    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
        dbc.ModalBody(id="modal-body")
    ], id="detail-modal", size="lg", is_open=False)
], fluid=True)

@app.callback(
    Output("stock-list", "children"),
    Input("bist30-endeks-grafik", "figure")
)
def update_stock_list(_):
    items = []
    for _, row in data.iterrows():
        renk = "lime" if row["Değişim %"] >= 0 else "red"
        items.append(html.Div([
            html.Div(f"{row['Sembol']} – {row['Şirket']}", className="text-white fw-bold"),
            html.Div(f"Fiyat: {row['Fiyat']} ₺ | %{row['Değişim %']:.2f}", style={"color": renk}, className="small")
        ], style={"padding": "10px", "borderBottom": "1px solid #333", "cursor": "pointer"},
        id={"type": "stock-item", "index": row["Sembol"]}))
    return items

@app.callback(
    Output("modal-title", "children"),
    Output("modal-body", "children"),
    Output("rsi-graph", "figure"),
    Output("volume-graph", "figure"),
    Output("detail-modal", "is_open"),
    Input({"type": "stock-item", "index": ALL}, "n_clicks"),
    State({"type": "stock-item", "index": ALL}, "id")
)
def show_stock_detail(n_clicks, ids):
    if not ctx.triggered_id:
        return "", "", go.Figure(), go.Figure(), False
    symbol = ctx.triggered_id["index"]
    info, rsi_fig, volume_fig = get_graphs(symbol)
    header = f"{symbol} – {info['name']}"
    body = html.Div([
        html.P(f"Kapanış: {info['price']} ₺"),
        html.P(f"Değişim: %{info['change']}"),
        html.P(f"Hacim: {info['volume']:,}"),
        html.P(f"RSI: {info['rsi']}")
    ])
    return header, body, rsi_fig, volume_fig, True

if __name__ == "__main__":
    app.run_server(debug=True)
