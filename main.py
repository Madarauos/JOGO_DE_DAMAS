import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from tabuleiro_widget import TabuleiroWidget
from jogo_damas import JogoDamas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        self.jogo = JogoDamas()
        self.peca_selecionada = None
        
        self.atualizar_interface()
    
    def setup_ui(self):
        self.setWindowTitle("Jogo de Damas")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        titulo = QLabel("JOGO DE DAMAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24pt; font-weight: bold; margin: 10px;")
        main_layout.addWidget(titulo)
        
        layout_jogo = QHBoxLayout()
        
        self.tabuleiro_widget = TabuleiroWidget()
        self.tabuleiro_widget.peca_clicada.connect(self.clicar_peca)
        layout_jogo.addWidget(self.tabuleiro_widget)
        
        info_panel = QFrame()
        info_panel.setFrameShape(QFrame.StyledPanel)
        info_panel.setMinimumWidth(200)
        info_layout = QVBoxLayout(info_panel)
        
        self.label_jogador = QLabel("Jogador: Brancas")
        self.label_jogador.setStyleSheet("font-size: 14pt; font-weight: bold;")
        info_layout.addWidget(self.label_jogador)
        
        self.label_status = QLabel("Selecione uma peça para mover")
        self.label_status.setWordWrap(True)
        info_layout.addWidget(self.label_status)
        
        self.btn_novo_jogo = QPushButton("Novo Jogo")
        self.btn_novo_jogo.clicked.connect(self.novo_jogo)
        info_layout.addWidget(self.btn_novo_jogo)
        
        self.btn_desistir = QPushButton("Desistir")
        self.btn_desistir.clicked.connect(self.desistir)
        info_layout.addWidget(self.btn_desistir)
        
        info_layout.addStretch()
        
        layout_jogo.addWidget(info_panel)
        main_layout.addLayout(layout_jogo)
        
        self.statusBar().showMessage("Bem-vindo ao Jogo de Damas!")
    
    def atualizar_interface(self):
        self.tabuleiro_widget.set_tabuleiro(self.jogo.tabuleiro)
        
        if self.jogo.jogador_atual == 1:
            self.label_jogador.setText("Jogador: Brancas")
        else:
            self.label_jogador.setText("Jogador: Pretas")
        
        vencedor = self.jogo.verificar_vencedor()
        if vencedor == 1:
            self.label_status.setText("Brancas venceram!")
            QMessageBox.information(self, "Fim de Jogo", "Brancas venceram!")
        elif vencedor == -1:
            self.label_status.setText("Pretas venceram!")
            QMessageBox.information(self, "Fim de Jogo", "Pretas venceram!")
    
    def clicar_peca(self, linha, coluna):
        if self.peca_selecionada is None:
            peca = self.jogo.tabuleiro[linha][coluna]
            
            if (peca > 0 and self.jogo.jogador_atual == 1) or (peca < 0 and self.jogo.jogador_atual == -1):
                movimentos = self.jogo.obter_movimentos_possiveis(linha, coluna)
                
                if movimentos:
                    self.peca_selecionada = (linha, coluna)
                    self.tabuleiro_widget.set_peca_selecionada(linha, coluna)
                    self.tabuleiro_widget.set_movimentos_possiveis(movimentos)
                    self.label_status.setText("Selecione o destino")
                else:
                    self.label_status.setText("Esta peça não tem movimentos possíveis")
            else:
                self.label_status.setText("Selecione uma peça sua")
        
        else:
            linha_origem, coluna_origem = self.peca_selecionada
            
            if linha == linha_origem and coluna == coluna_origem:
                self.peca_selecionada = None
                self.tabuleiro_widget.set_peca_selecionada(None, None)
                self.tabuleiro_widget.set_movimentos_possiveis([])
                self.label_status.setText("Selecione uma peça para mover")
                return
            
            if self.jogo.mover_peca(linha_origem, coluna_origem, linha, coluna):
                self.peca_selecionada = None
                self.tabuleiro_widget.set_peca_selecionada(None, None)
                self.tabuleiro_widget.set_movimentos_possiveis([])
                self.atualizar_interface()
                self.label_status.setText("Movimento realizado")
            else:
                self.label_status.setText("Movimento inválido")
    
    def novo_jogo(self):
        self.jogo = JogoDamas()
        self.peca_selecionada = None
        self.tabuleiro_widget.set_peca_selecionada(None, None)
        self.tabuleiro_widget.set_movimentos_possiveis([])
        self.atualizar_interface()
        self.label_status.setText("Novo jogo iniciado")
    
    def desistir(self):
        resposta = QMessageBox.question(
            self, 
            "Desistir", 
            f"O jogador {'Brancas' if self.jogo.jogador_atual == 1 else 'Pretas'} deseja desistir?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            vencedor = "Pretas" if self.jogo.jogador_atual == 1 else "Brancas"
            QMessageBox.information(self, "Fim de Jogo", f"{vencedor} venceram por desistência!")
            self.novo_jogo()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
