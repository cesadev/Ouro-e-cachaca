import pygame

class Carta:
    def __init__(self, nome, poder, vida, imagem=None, custo_sangue=0, valor_sacrificio=None, selos=None):
        self.nome = nome
        self.poder = poder
        self.dano = poder  
        self.vida = vida
        self.custo_sangue = custo_sangue
        self.valor_sacrificio = valor_sacrificio

        self.selos = selos.copy() if selos is not None else []
        
        self.imagem = imagem

        if self.imagem is not None:
            self.rect = self.imagem.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, 144, 176)

    def adicionar_novo_selo(self, nome_selo_logica, nome_arquivo_imagem):
        """
        Carimba QUALQUER selo novo diretamente na arte da carta e adiciona ele na lógica/back-end.
        """
        try:
            # Puxa o selo baseado no nome do arquivo do caminho
            caminho = f"selos/{nome_arquivo_imagem}"
            img_temp = pygame.image.load(caminho).convert_alpha()
            img_selo = pygame.transform.scale(img_temp, (45, 45))
            
            if self.imagem is not None:
                # Copia a imagem só para essa carta
                self.imagem = self.imagem.copy()
                
                pos_selo_x = 8
                pos_selo_y = 25
                
                pos_selo_x += 35 * len(self.selos)
                # Coloca o Selo na Carta
                self.imagem.blit(img_selo, (pos_selo_x, pos_selo_y))
            
            self.selos.append(nome_selo_logica)
            
            
        except FileNotFoundError:
            pass

    def desenhar(self, tela, posicao_x, posicao_y):
        self.rect.topleft = (posicao_x, posicao_y)
        
        if self.imagem is not None:
            tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(tela, (255, 255, 255), self.rect) 
            pygame.draw.rect(tela, (0, 0, 0), self.rect, 3)
        
    def copy(self):
        """Retorna uma cópia real da instância da carta"""
        return Carta(
            self.nome, self.poder, self.vida, self.imagem, 
            self.custo_sangue, self.valor_sacrificio, self.selos
        )