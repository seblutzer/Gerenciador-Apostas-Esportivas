from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidgetSelectionRange
import pandas as pd
from PyQt5 import QtCore, QtWidgets

class Table(QtWidgets.QWidget):
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file
        self.initUI()

    def initUI(self):
        df = pd.read_csv(self.csv_file)

        transformed_data = []

        for _, row in df.iterrows():
            for i in range(1, 4):
                bethouse_col = f'Bethouse {i}'
                mercado_col = f'Mercado {i}'
                valor_col = f'Valor {i}'
                odd_col = f'Odd {i}'
                aposta_col = f'Aposta {i}'

                if pd.notnull(row[bethouse_col]):
                    transformed_data.append({
                        'Jogo': f"{row['Time Casa']} - {row['Time Fora']}",
                        'Data': f"{row['Dia']}/{row['Mês']}/{row['Ano']} {row['Hora']}:{row['Minuto']}",
                        'Bethouse': row[bethouse_col],
                        'Mercado': row[mercado_col],
                        'Valor': row[valor_col],
                        'Odd': row[odd_col],
                        'Aposta': row[aposta_col],
                        'Lucro Esperado': row['Lucro Esperado'],
                        'Lucro Percentual': row['Lucro Percentual']
                    })
        transformed_df = pd.DataFrame(transformed_data)

        # Create a custom model to display the data
        model = CustomTableModel(transformed_df, [0, 1])

        # Create a QTableView and set the model
        self.table = QtWidgets.QTableView()
        self.table.setModel(model)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
class CustomTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, merge_columns):
        super().__init__()
        self.data = data
        self.merge_columns = merge_columns

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data.columns)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # Check if the cell should be merged
            if index.column() in self.merge_columns:
                current_value = self.data.iloc[index.row(), index.column()]
                previous_value = self.data.iloc[index.row() - 1, index.column()] if index.row() > 0 else None

                # Return an empty value for cells that should be merged
                if current_value == previous_value:
                    return ''

            return str(self.data.iloc[index.row(), index.column()])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    view = Table('Apostas.csv')
    transformed_df = pd.DataFrame({
        'Jogo': ['jogo 1', 'jogo 1', 'jogo 2', 'jogo 2'],
        'Data': ['01/01/2022', '01/01/2022', '02/01/2022', '02/01/2022'],
        'Bethouse': ['bethouse 1', 'bethouse 2', 'bethouse 1', 'bethouse 2']
    })
    model = CustomTableModel(transformed_df, [0, 1])
    view = QtWidgets.QTableView()
    view.setModel(model)
    view.show()
    app.exec_()