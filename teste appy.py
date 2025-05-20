from pathlib import Path as pl
import pandas as pd
from shiny.express import input, render, ui
from shinywidgets import render_plotly
from shiny import render_plot, reactive
import plotly.express as px

@reactive.calc
def arquivo():
    arquivo_excel = pl(__file__).parent / 'sales.csv'
    df = pd.read_csv(arquivo_excel)
    return df

with ui.layout_columns():
    #@render.plot
   """ def gafrico_de_vendas():
        df = arquivo()
        df_grupo = df.groupby('product')['quantity_ordered'].sum().nlargest(10).reset_index()

        return px.bar(df_grupo, x = 'product', y = 'quantity_ordered', title= "Gráfico de Vendas por Produto")
    """
@render.data_frame
def planilha_dataFrame():
    df = arquivo()
    return df