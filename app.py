from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from data_utils import load_bist100_data, get_graphs, get_bist30_index_graph
from currency_widget import get_currency_widget
from news_widget import get_news_widget

external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

data = load_bist100_data()
bist30_fig = get_bist30_index_graph()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("\ud83d\udcca BIST 30 Endeksi", className="text-white mb-3"),
            dcc.Graph(figure=bist30_fig, id="bist30-endeks-grafik", style={"marginBottom": "2rem"}),
        ], width=6),

        dbc.Col([
            dcc.Tabs([
                dcc.Tab(label="RSI", children=[dcc.Graph(id="rsi-graph")]),
                dcc.Tab(label="Hacim", children=[dcc.Graph(id="volume-graph")]),
            ]),
            html.Div(id="rsi-explanation", className="text-white small mt-2"),
            html.Div(id="volume-explanation", className="text-white small mt-2"),
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.H5("\ud83d\udccb Hisseler", className="text-white"),
            html.Div(id="stock-list", style={"overflowY": "auto", "height": "60vh"})
        ], width=6),

        dbc.Col([
            dbc.Row([
                dbc.Col(get_news_widget(), width=6),
                dbc.Col(get_currency_widget(), width=6),
            ])
        ], width=6)
    ]),

    html.Div(id="stock-detail", className="text-white", style={"position": "fixed", "top": "10%", "left": "30%", "zIndex": "9999", "backgroundColor": "#111", "padding": "20px", "borderRadius": "10px", "display": "none"})
], fluid=True)


@app.callback(
    Output("stock-list", "children"),
    Input("search-input", "value")
)
def update_stock_list(query):
    filtered = data.copy()
    if query:
        filtered = filtered[filtered["Sembol"].str.contains(query.upper()) | filtered["\u015eirket"].str.contains(query, case=False)]
    items = []
    for _, row in filtered.iterrows():
        items.append(html.Div([
            html.Div(f"{row['Sembol']} – {row['\u015eirket']}", className="text-white fw-bold"),
            html.Div(f"Fiyat: {row['Fiyat']} | %: {row['De\u011fi\u015fim %']}", className="text-muted small"),
        ], style={"padding": "10px", "borderBottom": "1px solid #333", "cursor": "pointer"},
        id={"type": "stock-item", "index": row["Sembol"]}))
    return items


@app.callback(
    Output("stock-detail", "children"),
    Output("stock-detail", "style"),
    Output("rsi-graph", "figure"),
    Output("volume-graph", "figure"),
    Output("rsi-explanation", "children"),
    Output("volume-explanation", "children"),
    Input({"type": "stock-item", "index": ALL}, "n_clicks"),
    State({"type": "stock-item", "index": ALL}, "id")
)
def update_detail(n_clicks, ids):
    triggered = ctx.triggered_id
    if not triggered:
        return "", {"display": "none"}, go.Figure(), go.Figure(), "", ""
    selected_symbol = triggered["index"]
    info, rsi_fig, volume_fig, _ = get_graphs(selected_symbol)
    detail = html.Div([
        html.H4(f"\ud83d\udccc {selected_symbol} – {info['name']}", className="text-info"),
        html.Div(f"Kapan\u0131\u015f: {info['price']} \u20ba", className="text-white"),
        html.Div(f"De\u011fi\u015fim: {info['change']}%", className="text-white"),
        html.Div(f"Hacim: {info['volume']:,}", className="text-white"),
        html.Div(f"RSI: {info['rsi']}", className="text-white"),
    ])
    rsi_expl = "RSI (G\u00f6receli G\u00fc\u00e7 Endeksi), hisse senedinin a\u015f\u0131r\u0131 al\u0131m veya sat\u0131m durumunu g\u00f6sterir. 70 \u00fczeri a\u015f\u0131r\u0131 al\u0131m, 30 alt\u0131 a\u015f\u0131r\u0131 sat\u0131m sinyali verebilir."
    volume_expl = "Hacim, belirli bir s\u00fcre i\u00e7inde al\u0131n\u0131p sat\u0131lan hisse miktar\u0131n\u0131 ifade eder. Y\u00fcksek hacim yat\u0131r\u0131mc\u0131 ilgisini g\u00f6sterebilir."
    return detail, {"display": "block"}, rsi_fig, volume_fig, rsi_expl, volume_expl


if __name__ == "__main__":
    app.run_server(debug=True)
