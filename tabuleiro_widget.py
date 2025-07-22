from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal

class TabuleiroWidget(QWidget):
    peca_clicada = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabuleiro = None
        self.tamanho_celula = 50
        self.peca_selecionada = None
        self.movimentos_possiveis = []
        self.setMinimumSize(400, 400)
        
    def set_tabuleiro(self, tabuleiro):
        self.tabuleiro = tabuleiro
        self.update()
        
    def set_movimentos_possiveis(self, movimentos):
        self.movimentos_possiveis = movimentos
        self.update()
        
    def set_peca_selecionada(self, linha, coluna):
        self.peca_selecionada = (linha, coluna) if linha is not None else None
        self.update()
        
    def paintEvent(self, event):
        if not self.tabuleiro:
            return
            
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        
        tamanho = min(self.width(), self.height()) // 8
        self.tamanho_celula = tamanho
        
        for linha in range(8):
            for coluna in range(8):
                if (linha + coluna) % 2 == 0:
                    cor = QColor(255, 206, 158)
                else:
                    cor = QColor(209, 139, 71)
                
                qp.fillRect(coluna * tamanho, linha * tamanho, tamanho, tamanho, cor)
                
                if self.peca_selecionada and self.peca_selecionada == (linha, coluna):
                    qp.setPen(QPen(QColor(255, 255, 0), 3))
                    qp.drawRect(coluna * tamanho + 2, linha * tamanho + 2, tamanho - 4, tamanho - 4)
                
                if (linha, coluna) in self.movimentos_possiveis:
                    qp.setPen(QPen(QColor(0, 255, 0), 2))
                    qp.drawRect(coluna * tamanho + 4, linha * tamanho + 4, tamanho - 8, tamanho - 8)
        
        for linha in range(8):
            for coluna in range(8):
                valor = self.tabuleiro[linha][coluna]
                if valor != 0:
                    if valor > 0:
                        cor = QColor(255, 255, 255)
                    else:
                        cor = QColor(0, 0, 0)
                    
                    centro_x = coluna * tamanho + tamanho // 2
                    centro_y = linha * tamanho + tamanho // 2
                    raio = tamanho // 2 - 5
                    
                    qp.setBrush(QBrush(cor))
                    qp.setPen(QPen(QColor(100, 100, 100), 2))
                    qp.drawEllipse(QPoint(centro_x, centro_y), raio, raio)
                    
                    if abs(valor) == 2:
                        qp.setPen(QPen(QColor(255, 215, 0), 2))
                        qp.drawEllipse(QPoint(centro_x, centro_y), raio - 5, raio - 5)
                        qp.drawText(QRect(centro_x - 5, centro_y - 8, 10, 16), Qt.AlignCenter, "R")
    
    def mousePressEvent(self, event):
        if not self.tabuleiro:
            return
            
        coluna = event.x() // self.tamanho_celula
        linha = event.y() // self.tamanho_celula
        
        if 0 <= linha < 8 and 0 <= coluna < 8:
            self.peca_clicada.emit(linha, coluna)
