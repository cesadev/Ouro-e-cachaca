import pygame
from cena_base import CenaBase

class CenaIntroducao(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)

        self.dialogos = ["rapaiz"]
        self.indice_atual = 0

    
    def processar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.indice_atual += 1

                    if self.indice_atual >= len(self.dialogos):
                        self.terminou = True
                        self.proxima_cena = "tutorial"

    #aqui entra a animação. em standby enquanto não fiz
    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.tela.fill((30, 30, 30))
        
        if self.indice_atual < len(self.dialogos):
            largura, altura = self.tela.get_size()
            

            rect_caixa = pygame.Rect(100, altura - 180, largura - 200, 150)
            pygame.draw.rect(self.tela, (10, 10, 10), rect_caixa)
            pygame.draw.rect(self.tela, (200, 200, 200), rect_caixa, 4)

            texto = self.dialogos[self.indice_atual]
            fonte = pygame.font.SysFont("Arial", 40)
            img_texto = fonte.render(texto, True, (255, 255, 255))
            self.tela.blit(img_texto, (rect_caixa.x + 30, rect_caixa.y + 50))

            triangulo = [
                (rect_caixa.right - 40, rect_caixa.bottom - 40), 
                (rect_caixa.right - 20, rect_caixa.bottom - 40), 
                (rect_caixa.right - 30, rect_caixa.bottom - 20)
            ]
            pygame.draw.polygon(self.tela, (255, 255, 255), triangulo)
