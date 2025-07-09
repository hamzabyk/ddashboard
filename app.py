# app.py
from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import os
from data_utils import load_bist30_data, get_graphs, get_bist30_index_fig
from currency_widget import get_currency_widget
from news_widget import get_news_widget

external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

data = load_bist30_data()
bist30_fig = get_bist30_index_fig()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("BIST 30 Endeksi", className="text-white mb-2"),
            dcc.Graph(figure=bist30_fig, id="bist30-endeks-grafik", style={"marginBottom": "2rem"}),
            html.Div(id="bist30-index-summary", className="text-white")
        ], width=6),
        dbc.Col([
            html.H5("Grafikler", className="text-white mb-2"),
            dcc.Tabs([
                dcc.Tab(label="RSI", children=[dcc.Graph(id="rsi-graph")]),
                dcc.Tab(label="Hacim", children=[dcc.Graph(id="volume-graph")]),
            ])
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.H5("BIST 30 Hisseleri", className="text-white mb-2"),
            html.Div(id="stock-table", style={"maxHeight": "400px", "overflowY": "scroll"})
        ], width=8),
        dbc.Col([
            html.Div(get_news_widget(), style={"marginBottom": "2rem"}),
            html.Div(get_currency_widget())
        ], width=4)
    ]),

    html.Div(id="stock-detail-modal")
], fluid=True)

@app.callback(
    Output("stock-table", "children"),
    Input("bist30-endeks-grafik", "figure")
)
def update_stock_table(_):
    rows = []
    for _, row in data.iterrows():
        color = "#00cc00" if row["Değişim %"] >= 0 else "#cc0000"
        rows.append(
            html.Div([
                html.Div(f"{row['Sembol']} - {row['Şirket']}", className="text-white fw-bold"),
                html.Div([
                    html.Span(f"Fiyat: {row['Fiyat']} ₺", className="me-3"),
                    html.Span(f"%: {row['Değişim %']}", style={"color": color})
                ], className="text-muted small")
            ], style={"padding": "10px", "borderBottom": "1px solid #444", "cursor": "pointer"},
            id={"type": "stock-item", "index": row["Sembol"]})
        )
    return rows

@app.callback(
    Output("stock-detail-modal", "children"),
    Output("rsi-graph", "figure"),
    Output("volume-graph", "figure"),
    Input({"type": "stock-item", "index": ALL}, "n_clicks"),
    State({"type": "stock-item", "index": ALL}, "id")
)
def update_detail(n_clicks, ids):
    triggered = ctx.triggered_id
    if not triggered:
        return "", go.Figure(), go.Figure()
    selected_symbol = triggered["index"]
    info, rsi_fig, volume_fig = get_graphs(selected_symbol)

    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(f"{selected_symbol} - {info['name']}")),
        dbc.ModalBody([
            html.Div(f"Fiyat: {info['price']} ₺"),
            html.Div(f"Değişim: {info['change']}%"),
            html.Div(f"Hacim: {info['volume']:,}"),
            html.Div(f"RSI: {info['rsi']}")
        ])
    ], id="modal-centered", centered=True, is_open=True)

    return modal, rsi_fig, volume_fig

if __name__ == '__main__':
    app.run_server(debug=True)
