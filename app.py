from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from data_utils import load_bist30_data, get_graphs, get_bist30_index_graph
from currency_widget import get_currency_component
from news_widget import get_news_component

external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

data = load_bist30_data()
bist30_fig, bist30_stats = get_bist30_index_graph(data)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("📊 BIST 30 Endeksi", className="text-white mb-3"),
            dcc.Graph(figure=bist30_fig, id="bist30-endeks-grafik", style={"marginBottom": "2rem"}),
            html.Div([
                html.P(f"Endeks Değeri: {bist30_stats['value']}", className="text-info"),
                html.P(f"Aylık Değişim: {bist30_stats['monthly_change']}", className="text-muted"),
                html.P(f"Yıllık Değişim: {bist30_stats['yearly_change']}", className="text-muted"),
                html.P(f"Hacim: {bist30_stats['volume']}", className="text-muted"),
            ])
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
            html.H5("📋 Hisseler", className="text-white"),
            html.Div(id="stock-list", style={"overflowY": "auto", "height": "60vh"})
        ], width=6),

        dbc.Col([
            dbc.Row([
                dbc.Col(get_news_component(), width=6),
                dbc.Col(get_currency_component(), width=6),
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
        filtered = filtered[filtered["Sembol"].str.contains(query.upper()) | filtered["Şirket"].str.contains(query, case=False)]
    items = []
    for _, row in filtered.iterrows():
        color = "green" if row['Değişim %'] >= 0 else "red"
        items.append(html.Div([
            html.Div(f"{row['Sembol']} – {row['Şirket']}", className="text-white fw-bold"),
            html.Div(f"Fiyat: {row['Fiyat']} | %: {row['Değişim %']}", className="text-muted small", style={"color": color}),
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
    info, rsi_fig, volume_fig = get_graphs(selected_symbol, data)
    detail = html.Div([
        html.H4(f"📈 {selected_symbol} – {info['name']}", className="text-info"),
        html.Div(f"Kapanış: {info['price']} ₺", className="text-white"),
        html.Div(f"Değişim: {info['change']}%", className="text-white"),
        html.Div(f"Hacim: {info['volume']:,}", className="text-white"),
        html.Div(f"RSI: {info['rsi']}", className="text-white"),
    ])
    rsi_expl = "RSI (Göreceli Güç Endeksi), hisse senedinin aşırı alım veya satım durumunu gösterir. 70 üzeri aşırı alım, 30 altı aşırı satım sinyali verebilir."
    volume_expl = "Hacim, belirli bir süre içinde alınıp satılan hisse miktarını ifade eder. Yüksek hacim yatırımcı ilgisini gösterebilir."
    return detail, {"display": "block"}, rsi_fig, volume_fig, rsi_expl, volume_expl


if __name__ == "__main__":
    app.run_server(debug=True)
