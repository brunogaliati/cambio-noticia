import pandas as pd
import yfinance as yf
import plotly.express as px

# Carregar o arquivo CSV com os eventos (ajustado para usar ; como separador e converter data)
eventos_df = pd.read_csv('cambio-noticia.csv', 
                        sep=';',
                        parse_dates=['Data'],
                        dayfirst=True)  # Formato brasileiro dd/mm/yyyy

# Obter as cotações históricas do dólar (USD/BRL) utilizando o Yahoo Finance
ticker = 'BRL=X'
inicio = '2014-01-01'
fim = '2024-12-31'

# Baixar os dados de cotação
cotacao_df = yf.download(ticker, start=inicio, end=fim)

# Resetar o índice para transformar a coluna de datas em uma coluna regular
cotacao_df = cotacao_df.reset_index()

# Renomear a coluna 'Date' para 'Data' para coincidir com o DataFrame de eventos
cotacao_df = cotacao_df.rename(columns={'Date': 'Data'})

# Mesclar os dados de cotação com os eventos
df = pd.merge(cotacao_df, eventos_df, on='Data', how='left')

# Criar o gráfico interativo com a linha de cotação
fig = px.line(df, x='Data', y='Close', 
              title='Cotação Histórica USD/BRL',
              template='plotly_white')  # Tema mais limpo e profissional

# Customizar a linha principal
fig.update_traces(
    line=dict(color='#1f77b4', width=1.5),
    name='Cotação USD/BRL'
)

# Adicionar os pontos de eventos
eventos = df.dropna(subset=['Noticia'])
fig.add_trace(
    px.scatter(
        eventos, 
        x='Data', 
        y='Close',
        hover_data={'Data': True, 'Close': ':.4f', 'Noticia': True},
        hover_name='Noticia'
    ).data[0].update(
        marker=dict(
            size=12,
            symbol='circle',
            color='#e74c3c',  # Vermelho para destaque
            line=dict(color='white', width=2)
        ),
        name='Eventos Importantes'
    )
)

# Configurar o layout para melhor visualização
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title={
        'text': 'Cotação Histórica USD/BRL<br><span style="font-size: 14px;">Com Eventos Relevantes</span>',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis=dict(
        title='Data',
        gridcolor='#f0f0f0',
        showline=True,
        linewidth=1,
        linecolor='#d3d3d3'
    ),
    yaxis=dict(
        title='Cotação (BRL)',
        gridcolor='#f0f0f0',
        showline=True,
        linewidth=1,
        linecolor='#d3d3d3',
        tickprefix='R$ '
    ),
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor='white',
        font_size=14,
        font_family='Arial'
    ),
    showlegend=True,
    legend=dict(
        yanchor='top',
        y=0.99,
        xanchor='left',
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)'
    )
)

# Exibir o gráfico
fig.show()
