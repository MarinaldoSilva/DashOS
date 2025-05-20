import pandas as pd
from pathlib import Path as pl
from shiny import App, reactive, render, ui        
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Dashboard", fillable=True)

ui.input_numeric("n", "Atendimentos", 10, min=1, max=100)

@reactive.calc

#base de dados que será usada nos exemplos
def arquivo():
    #caminho absoluto do arquivo
    arquivo = pl(__file__).parent / "/dados-tratados.xlsx"
    return pd.read_csv(arquivo)
    #retorna um dataFrame que ser executado pelo shiny

#tudo dentro desse bloco 'with' é parte do layout de colunas
with ui.layout_columns():
    # Esse bloco renderiza o DataFrame para ser exibido na interface web
    # Ele converte os dados para uma tabela interativa, permitindo rolagem, filtros e ordenação


    @render_plotly
    def grafico_top_vendas():
        #responsável por gerar o gráfico de barras.
        df = arquivo()
        
        top_vendas = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
        px.bar 
        return px.bar(top_vendas, x='product', y= 'quantity_ordered')
        #fig = px.pie(df, names='product', values='quantity_ordered', title="Distribuição das Vendas por Produto")
        #return fig

    #@render.data_frame
    #def dados_csv():
    #    return arquivo()

