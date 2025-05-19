from shiny import App, ui, render
import pandas as pd
import plotly.express as px
from pathlib import Path

def carregar_dados():
    arquivo_excel = Path(__file__).parent / "dados-tratados.xlsx"

    if not arquivo_excel.exists():
        raise FileNotFoundError(f"Erro: Arquivo não encontrado em {arquivo_excel}")

    df = pd.read_excel(arquivo_excel)

    if not {"executor", "tipo_os"}.issubset(df.columns):
        raise ValueError("Erro: A planilha deve conter as colunas 'executor' e 'tipo_os'.")

    return df

df = carregar_dados()

app_ui = ui.page_fluid(
    ui.panel_title("Dashboard de OS"),
    ui.input_select("executor", "Selecione um Executor", choices=df["executor"].dropna().unique().tolist()),
    ui.output_ui("grafico_os") 
)

def server(input, output, session):
    df = carregar_dados()

    @output
    @render.ui 
    def grafico_os():
        if not input.executor():
            return None  

        df_filtrado = df[df["executor"] == input.executor()]
        df_agrupado = df_filtrado.groupby("tipo_os").size().reset_index(name="quantidade")

        fig = px.bar(
            df_agrupado,
            x="tipo_os",
            y="quantidade",
            title=f"Distribuição de OS - {input.executor()}",
            width=800,
            height=500,
        )

        fig.update_traces(width=0.3)  

        return ui.HTML(fig.to_html()) 

app = App(app_ui, server)
app.run()
