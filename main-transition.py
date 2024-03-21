import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox, QMenu, QAction, QLineEdit, QSpinBox
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QFile, QTextStream, QSize
from Pacotes_Lutzer.convert import convert_to_numeric, convert_mes, converter_esporte
from Pacotes_Lutzer.validate import create_float_entry, create_combobox, float_error, gerar_mensagem, blank_error
from Pacotes_Lutzer.calc_apostas import calc_apostas
from Pacotes_Lutzer.classes_personalizadas import BetHistTreeview, preencher_treeview, import_df_filtrado, save_apostas, tabela_bethouses
from Pacotes_Lutzer.graficos import lucro_tempo, apostas_hora, calc_saldo_bethouse, apostas_bethouses, relacao_bethouses, relacao_esportes, eficiencia_bethouses, odds_x_resultado, participacao_lucros
from language import trans_config, trans_filtros, trans_graficos, trans_jogo, trans_tabelas, trans_dicas, trans_resultados
import sqlite3

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Minha Aplicação')

        # Criar layouts verticais para cada frame
        layout = QVBoxLayout()

        ############################## Frame Opções ##############################
        # Cria os frames
        frameOpcoes = QWidget()
        frameOpcoes.setObjectName("frameOpcoes")
        frameOpcoes.setStyleSheet("background-color: #CCCCCC; padding: 10px;")
        layout.addWidget(frameOpcoes)

        # Criar layout vertical para o frameOpcoes
        layout_opcoes = QHBoxLayout()

        # Define a variável de controle para o idioma
        selected_language = "English"

        # Dicionário de bandeiras
        flags = {
            'Português': '🇧🇷',
            'English': '🇺🇸',
            'Deutsch': '🇩🇪',
            'Italiano': '🇮🇹',
            'Français': '🇫🇷',
            'Ελληνικά': '🇬🇷',
            'Русский': '🇷🇺',
            'Español': '🇪🇸'
        }

        def save_language(language):
            with open('language.txt', 'w') as f:
                f.write(language)

        def load_language():
            if QFile.exists('language.txt'):
                with open('language.txt', 'r') as f:
                    language = f.read()
                    language = 'Português' if language == 'PortuguÃªs' else language
                    return language
            return 'English'

        def restart_program():
            python = sys.executable
            os.execl(python, python, *sys.argv)

        def update_language(language):
            global selected_language
            selected_language = language
            language_button.setText(flags[language])
            confirm = QMessageBox.question(self, trans_config['Confirmação'][language],
                                           f"{trans_config['Traduzir'][language]} {language}?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                save_language(language)
                restart_program()

        def open_language_menu():
            global language_frame
            language_frame = QWidget(self)
            language_frame.setGeometry(language_button.x() + 60, language_button.y() + language_button.height(), 200,
                                       200)

            for i, (language, flag) in enumerate(flags.items()):
                button = QPushButton(f"{language} {flag}", language_frame)
                button.clicked.connect(lambda lang=language: update_language(lang))
                button.move(10, 10 + i * 30)

            language_frame.show()

        selected_language = load_language()  # Define o idioma padrão aqui

        # Botão de idioma
        language_button = QPushButton(flags[selected_language])
        language_button.setFont(QFont('Arial', 21))
        language_button.clicked.connect(open_language_menu)
        layout_opcoes.addWidget(language_button)

        idioma = selected_language
        cambio = 'R$'
        self.setWindowTitle(trans_config['programa'][idioma])

        def alternar_tabelas():
            global tabela_visivel
            tabela_visivel = not tabela_visivel
            if tabela_visivel:
                frameTabela.show()
                frameSaldos.show()
                botao_tabelas.setText(trans_config['TabelaOff'][idioma])
            else:
                frameTabela.hide()
                frameSaldos.hide()
                botao_tabelas.setText(trans_config['TabelaOn'][idioma])

        tabela_visivel = True

        # Botão de tabelas
        botao_tabelas = QPushButton(trans_config['TabelaOn'][idioma])
        botao_tabelas.clicked.connect(alternar_tabelas)
        layout_opcoes.addWidget(botao_tabelas)

        def selecionar_opcao(opcao, popup, row):
            pass

        # Combobox de opções
        combo_opcoes = QComboBox()
        combo_opcoes.addItems([
            trans_graficos['lucro tempo'][idioma],
            trans_graficos['apostas hora'][idioma],
            trans_graficos['historico saldo'][idioma],
            trans_graficos['apostas tempo'][idioma],
            trans_graficos['apostas bethouse'][idioma],
            trans_graficos['esportes'][idioma],
            trans_graficos['resultado bethouse'][idioma],
            trans_graficos['odd resultado'][idioma],
            trans_graficos['Participação de lucros'][idioma]
        ])
        combo_opcoes.setCurrentIndex(-1)
        layout_opcoes.addWidget(combo_opcoes)

        def open_graficos_menu():
            global graficos_frame
            graficos_frame = QWidget(self)
            graficos_frame.setGeometry(graficos_button.x() + 50, graficos_button.y() + graficos_button.height(), 200,
                                       200)
            graficos_frame.setStyleSheet("background-color: white; border: 2px solid gray")

            popup = QWidget(self)

            for i, opcao in enumerate(combo_opcoes.currentText()):
                button = QPushButton(opcao, graficos_frame)
                button.clicked.connect(lambda opt=opcao, row=i: selecionar_opcao(opt, popup, row))
                button.move(10, 10 + i * 30)

            graficos_frame.show()

        # Botão de gráficos
        graficos_button = QPushButton(trans_graficos['graficos'][idioma])
        graficos_button.clicked.connect(open_graficos_menu)
        layout_opcoes.addWidget(graficos_button)

        # Rótulo em branco
        blank_label = QLabel('                                ')
        layout_opcoes.addWidget(blank_label)

        # Verifica se o arquivo SQLite já existe
        if not os.path.isfile("dados.db"):
            conn = sqlite3.connect("dados.db")
            c = conn.cursor()

            # Cria a tabela "apostas"
            c.execute('''CREATE TABLE apostas (
                            id INTEGER,
                            data_entrada TEXT,
                            data_jogo TEXT,
                            time_casa TEXT,
                            time_fora TEXT,
                            bethouse1 TEXT,
                            mercado1 TEXT,
                            valor1 REAL,
                            odd1 REAL,
                            aposta1 REAL,
                            resultado1 TEXT,
                            bethouse2 TEXT,
                            mercado2 TEXT,
                            valor2 REAL,
                            odd2 REAL,
                            aposta2 REAL,
                            resultado2 TEXT,
                            bethouse3 TEXT,
                            mercado3 TEXT,
                            valor3 REAL,
                            odd3 REAL,
                            aposta3 REAL,
                            resultado3 TEXT,
                            lucro_estimado REAL,
                            lucro_per_estimado REAL,
                            lucro_real REAL,
                            lucro_per_real REAL,
                            esporte TEXT
                        )''')

            conn.commit()
        else:
            conn = sqlite3.connect("dados.db")
            c = conn.cursor()


        frame_lucro = QLabel(self)
        frame_lucro.setGeometry(420, 5, 132, 57)
        frame_lucro.setStyleSheet("background-color: white; border: 2px solid gray")
        frame_lucro.setText(trans_config['Lucro Estimado Hoje'][idioma])
        frame_lucro.setAlignment(Qt.AlignCenter)
        frame_lucro.setFont(QFont("Arial", 12, QFont.Bold))

        # Cria um menu pop-up com as opções desejadas
        settings_menu = QMenu()
        settings_menu.addAction(trans_config['Configurações'][idioma]), #open_bethouses)
        settings_menu.addAction(trans_config['Personalizar'][idioma])#, open_customization_window)
        settings_menu.addSeparator()
        settings_menu.addAction(trans_config['Sair'][idioma], self.close)
        def show_settings_menu(event):
            settings_menu.exec_(event.globalPos())

        # Botão de configurações
        settings_icon = QIcon(QPixmap("./engrenagens.png").scaled(20, 20, Qt.KeepAspectRatio))
        settings_button = QPushButton()
        settings_button.setIcon(settings_icon)
        settings_button.setIconSize(settings_icon.actualSize(QSize(20, 20)))
        settings_button.clicked.connect(show_settings_menu)
        layout_opcoes.addWidget(settings_button)

        # Definir layout para o frameOpcoes
        frameOpcoes.setLayout(layout_opcoes)

        ############################## Frame Jogo ##############################
        # Criação dos widgets
        frameJogo = QWidget()
        frameJogo.setObjectName("frameJogo")
        frameJogo.setStyleSheet("background-color: #EEEEEE; padding: 10px;")
        layout.addWidget(frameJogo)

        # Criando os widgets
        label_jogo = QLabel("Jogo / Esporte:")
        label_data = QLabel("Data:")
        label_hora = QLabel("Hora:")

        entry_jogo = QLineEdit()
        entry_dia = QLineEdit()
        entry_mes = QLineEdit()
        entry_ano = QLineEdit()
        entry_hora = QLineEdit()
        entry_minuto = QLineEdit()

        entry_esporte = QLineEdit()
        label_arred = QLabel("Arred:")
        entry_arred = QLineEdit()
        botao_duplo = QPushButton("Duplo")

        # Organizando os widgets horizontalmente
        layout_horizontal1 = QHBoxLayout()
        layout_horizontal1.addWidget(label_jogo)
        layout_horizontal1.addWidget(label_data)
        layout_horizontal1.addWidget(label_hora)

        layout_horizontal2 = QHBoxLayout()
        layout_horizontal2.addWidget(entry_jogo)
        layout_horizontal2.addWidget(entry_dia)
        layout_horizontal2.addWidget(entry_mes)
        layout_horizontal2.addWidget(entry_ano)
        layout_horizontal2.addWidget(entry_hora)
        layout_horizontal2.addWidget(entry_minuto)

        layout_horizontal3 = QHBoxLayout()
        layout_horizontal3.addWidget(entry_esporte)
        layout_horizontal3.addWidget(label_arred)
        layout_horizontal3.addWidget(entry_arred)
        layout_horizontal3.addWidget(botao_duplo)

        # Organizando os layouts verticalmente
        layout_vertical = QVBoxLayout()
        layout_vertical.addLayout(layout_horizontal1)
        layout_vertical.addLayout(layout_horizontal2)
        layout_vertical.addLayout(layout_horizontal3)

        frameJogo.setLayout(layout_vertical)

        ############################## Frame SureBet ##############################
        frameSureBet = QLabel()
        frameSureBet.setObjectName("frameSureBet")
        frameSureBet.setStyleSheet("background-color: #AAAAAA; padding: 10px;")
        layout.addWidget(frameSureBet)

        ############################## Frame Apostas ##############################
        frameApostas = QWidget()
        frameApostas.setObjectName("frameApostas")
        frameApostas.setStyleSheet("background-color: #DDDDDD; padding: 10px;")
        layout.addWidget(frameApostas)

        ############################## Frame Gravar ##############################
        frameGravar = QWidget()
        frameGravar.setObjectName("frameGravar")
        frameGravar.setStyleSheet("background-color: #BBBBBB; padding: 10px;")
        layout.addWidget(frameGravar)

        ############################## Frame Tabela ##############################
        frameTabela = QWidget()
        frameTabela.setObjectName("frameTabela")
        frameTabela.setStyleSheet("background-color: #FFFFFF; padding: 10px;")
        layout.addWidget(frameTabela)

        ############################## Frame Saldos ##############################
        frameSaldos = QWidget()
        frameSaldos.setObjectName("frameSaldos")
        frameSaldos.setStyleSheet("background-color: #CCCCCC; padding: 10px;")
        layout.addWidget(frameSaldos)

        self.setLayout(layout)
        self.setWindowTitle(trans_config['programa'][idioma])  # Usando self.setWindowTitle()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
