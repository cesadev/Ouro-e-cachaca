import pygame
class Carta:
    def __init__(self, nome, poder, vida, imagem=None, custo_sangue=0, valor_sacrificio=None, selos=None):
        self.nome = nome
        self.poder = poder
        self.dano = poder  
        self.vida = vida
        self.custo_sangue = custo_sangue
        self.valor_sacrificio = valor_sacrificio

        self.selos = selos if selos is not None else []
        self.selo_matinta = False
        
        self.imagem = imagem

        if self.imagem is not None:
            self.rect = self.imagem.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, 144, 176)

    def desenhar(self, tela, posicao_x, posicao_y):
        self.rect.topleft = (posicao_x, posicao_y)
        if self.imagem is not None:
            tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(tela, (255, 255, 255), self.rect) 
            pygame.draw.rect(tela, (0, 0, 0), self.rect, 3)
        
    def copy(self):
        """Retorna uma cópia real da instância da carta"""
        return Carta(self.nome, self.poder, self.vida, self.imagem, self.custo_sangue, self.valor_sacrificio, self.selos)