import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout

class ApostasApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabela de Apostas")
        self.setGeometry(100, 100, 600, 300)

        # Criando a tabela
        table = QTableWidget(3, 9)  # 3 linhas e 9 colunas
        table.setHorizontalHeaderLabels(["", "", "time_casa", "bethouse1", "mercado1", "valor1", "odd1", "aposta1", "resultado1"])

        # Preenchendo os dados (substitua pelos seus dados reais)
        table.setItem(0, 0, QTableWidgetItem("data_entrada"))
        table.setItem(0, 1, QTableWidgetItem("data_jogo"))
        table.setItem(0, 2, QTableWidgetItem("VS"))
        table.setItem(0, 3, QTableWidgetItem("bethouse2"))
        table.setItem(0, 4, QTableWidgetItem("mercado2"))
        # ... preencha os outros dados ...

        # Organizando a tabela verticalmente
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApostasApp()
    window.show()
    sys.exit(app.exec_())