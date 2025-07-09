# news_widget.py
from dash import html

def get_news_widget():
    # Örnek haber verisi – gerçek veriyle entegre edilebilir
    news_list = [
        {
            "title": "BIST 30 Endeksi Güne Yükselişle Başladı",
            "source": "BloombergHT",
            "time": "15 dk önce"
        },
        {
            "title": "Küresel Piyasalar Fed Kararına Odaklandı",
            "source": "Reuters",
            "time": "30 dk önce"
        },
        {
            "title": "Dolar/TL Geri Çekildi, Borsa Güçlü",
            "source": "NTV",
            "time": "1 saat önce"
        },
        {
            "title": "Havacılık Sektöründe Beklentiler Yükseldi",
            "source": "HaberTürk",
            "time": "2 saat önce"
        }
    ]

    news_items = []
    for news in news_list:
        news_items.append(
            html.Div([
                html.Strong(news["title"], className="text-white small"),
                html.Div(f"{news['source']} • {news['time']}", className="text-muted", style={"fontSize": "11px"}),
                html.Hr(style={"margin": "4px 0", "borderColor": "#333"})
            ], style={"marginBottom": "6px"})
        )

    return html.Div(news_items, style={
        "backgroundColor": "#1a1a1a",
        "padding": "10px",
        "borderRadius": "5px",
        "height": "100%",
        "overflowY": "auto"
    })
