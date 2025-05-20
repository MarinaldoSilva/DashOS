from shiny import App, ui, render
import pandas as pd
import plotly.express as px
from pathlib import Path
import openpyxl

# Função para carregar os dados do Excel
def carregar_dados():
    arquivo_excel = Path(__file__).parent / "dados-tratados.xlsx"
    df = pd.read_excel(arquivo_excel, engine="openpyxl")
    return df

# Carrega os dados ao iniciar o app
df = carregar_dados()

# Interface do usuário
app_ui = ui.page_fluid(
    ui.tags.style("""
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .shiny-output-ui { max-width: 100%; overflow: auto; }
        .panel { padding: 15px; border-radius: 8px; background-color: #f8f9fa; }
    """),

    ui.panel_title("📊 Dashboard de OS"),

    ui.layout_columns(
        ui.panel_well(
            ui.input_select("executor", "Selecione um Executor", choices=df["executor"].dropna().unique().tolist())
        ),
        ui.panel_well(
            ui.output_text("total_os"),
            ui.output_ui("grafico_os")
        )
    )
)

def server(input, output, session):
    df = carregar_dados()

    @output
    @render.ui
    def grafico_os():
        if not input.executor():
            return ui.HTML("<p>Selecione um executor para ver o gráfico.</p>")

        df_filtrado = df[df["executor"] == input.executor()]
        df_agrupado = df_filtrado.groupby("tipo_os").size().reset_index(name="quantidade")

        fig = px.bar(
            df_agrupado,
            x="tipo_os",
            y="quantidade",
            title=f"Distribuição de OS - {input.executor()}",
        )

        fig.update_layout(bargap=0.4, autosize=True)

        return ui.HTML(fig.to_html())

    @output
    @render.text
    def total_os():
        if not input.executor():
            return "Selecione um Executor para ver o total de OS"
        total = df[df['executor'] == input.executor()].shape[0]
        return f"Total de OS para {input.executor()}: {total}"

# Criação e execução do app
app = App(app_ui, server)
app.run()
