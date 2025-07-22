class JogoDamas:
    def __init__(self):
        self.tabuleiro = [[0 for _ in range(8)] for _ in range(8)]
        self.jogador_atual = 1
        self.inicializar_tabuleiro()
        
    def inicializar_tabuleiro(self):
        for linha in range(8):
            for coluna in range(8):
                if (linha + coluna) % 2 != 0:
                    if linha < 3:
                        self.tabuleiro[linha][coluna] = -1
                    elif linha > 4:
                        self.tabuleiro[linha][coluna] = 1
                    else:
                        self.tabuleiro[linha][coluna] = 0
                else:
                    self.tabuleiro[linha][coluna] = 0
    
    def obter_movimentos_possiveis(self, linha, coluna):
        if not self.eh_peca_valida(linha, coluna):
            return []
            
        movimentos = []
        peca = self.tabuleiro[linha][coluna]
        
        if (peca > 0 and self.jogador_atual == 1) or (peca < 0 and self.jogador_atual == -1):
            direcoes = []
            
            if abs(peca) == 2:
                direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            elif peca > 0:
                direcoes = [(-1, -1), (-1, 1)]
            else:
                direcoes = [(1, -1), (1, 1)]
            
            for dir_linha, dir_coluna in direcoes:
                nova_linha = linha + dir_linha
                nova_coluna = coluna + dir_coluna
                
                if self.eh_posicao_valida(nova_linha, nova_coluna) and self.tabuleiro[nova_linha][nova_coluna] == 0:
                    movimentos.append((nova_linha, nova_coluna))
            
            capturas = self.obter_capturas(linha, coluna)
            movimentos.extend(capturas)
        
        return movimentos
    
    def obter_capturas(self, linha, coluna):
        if not self.eh_peca_valida(linha, coluna):
            return []
            
        capturas = []
        peca = self.tabuleiro[linha][coluna]
        
        direcoes = []
        if abs(peca) == 2:
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif peca > 0:
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_linha, dir_coluna in direcoes:
            nova_linha = linha + dir_linha
            nova_coluna = coluna + dir_coluna
            
            if (self.eh_posicao_valida(nova_linha, nova_coluna) and 
                self.tabuleiro[nova_linha][nova_coluna] * peca < 0):
                
                linha_apos = nova_linha + dir_linha
                coluna_apos = nova_coluna + dir_coluna
                
                if (self.eh_posicao_valida(linha_apos, coluna_apos) and 
                    self.tabuleiro[linha_apos][coluna_apos] == 0):
                    capturas.append((linha_apos, coluna_apos))
        
        return capturas
    
    def mover_peca(self, linha_origem, coluna_origem, linha_destino, coluna_destino):
        if not self.eh_movimento_valido(linha_origem, coluna_origem, linha_destino, coluna_destino):
            return False
        
        peca = self.tabuleiro[linha_origem][coluna_origem]
        
        self.tabuleiro[linha_origem][coluna_origem] = 0
        self.tabuleiro[linha_destino][coluna_destino] = peca
        
        if abs(linha_destino - linha_origem) == 2:
            linha_meio = (linha_origem + linha_destino) // 2
            coluna_meio = (coluna_origem + coluna_destino) // 2
            self.tabuleiro[linha_meio][coluna_meio] = 0
            
            capturas = self.obter_capturas(linha_destino, coluna_destino)
            if capturas:
                return True
        
        if (peca == 1 and linha_destino == 0) or (peca == -1 and linha_destino == 7):
            self.tabuleiro[linha_destino][coluna_destino] = peca * 2
        
        self.jogador_atual *= -1
        return True
    
    def eh_movimento_valido(self, linha_origem, coluna_origem, linha_destino, coluna_destino):
        if not (self.eh_posicao_valida(linha_origem, coluna_origem) and 
                self.eh_posicao_valida(linha_destino, coluna_destino)):
            return False
        
        peca = self.tabuleiro[linha_origem][coluna_origem]
        if (peca > 0 and self.jogador_atual != 1) or (peca < 0 and self.jogador_atual != -1) or peca == 0:
            return False
        
        if self.tabuleiro[linha_destino][coluna_destino] != 0:
            return False
        
        movimentos = self.obter_movimentos_possiveis(linha_origem, coluna_origem)
        
        return (linha_destino, coluna_destino) in movimentos
    
    def eh_posicao_valida(self, linha, coluna):
        return 0 <= linha < 8 and 0 <= coluna < 8
    
    def eh_peca_valida(self, linha, coluna):
        return (self.eh_posicao_valida(linha, coluna) and 
                self.tabuleiro[linha][coluna] != 0)
    
    def verificar_vencedor(self):
        pecas_brancas = 0
        pecas_pretas = 0
        
        for linha in range(8):
            for coluna in range(8):
                peca = self.tabuleiro[linha][coluna]
                if peca > 0:
                    pecas_brancas += 1
                elif peca < 0:
                    pecas_pretas += 1
        
        if pecas_brancas == 0:
            return -1
        elif pecas_pretas == 0:
            return 1
        
        tem_movimento = False
        for linha in range(8):
            for coluna in range(8):
                peca = self.tabuleiro[linha][coluna]
                if (peca > 0 and self.jogador_atual == 1) or (peca < 0 and self.jogador_atual == -1):
                    if self.obter_movimentos_possiveis(linha, coluna):
                        tem_movimento = True
                        break
            if tem_movimento:
                break
        
        if not tem_movimento:
            return -self.jogador_atual
        
        return 0
