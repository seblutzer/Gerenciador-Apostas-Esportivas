import tkinter as tk
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

def plot_grafico():
    # Dados de exemplo
    x = ['A', 'B', 'C', 'D']
    y = [10, 20, 30, 40]

    # Criar o gráfico de barras
    fig = go.Figure(data=go.Bar(x=x, y=y))

    # Configurar o layout do gráfico
    fig.update_layout(title="Gráfico de Barras Interativo")

    # Criar a nova janela
    window = tk.Toplevel(root)

    # Converter o gráfico para HTML
    fig_html = pio.to_html(fig, full_html=False)

    # Exibir o gráfico no componente Plotly
    plotly_component = tk.Frame(window, width=800, height=600)
    plotly_component.grid(row=0, column=0, padx=10, pady=10)
    plotly_component.winfo_toplevel().title("Gráfico Interativo")

    # Carregar o HTML do gráfico no componente Plotly
    browser = pio.renderers._utils.Browser()
    browser.open("about:blank")
    browser.window.document.write(fig_html)
    plotly_component.bind("<Destroy>", lambda event: browser.close())

root = tk.Tk()

plot_button = tk.Button(root, text="Plotar Gráfico", command=plot_grafico)
plot_button.pack(pady=10)

root.mainloop()
