import pygame
from cenas.cena_base import CenaBase

class CenaIntroducao(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)

        self.dialogos = ["Outro atrevido. Já faz um tempo...", "Talvez tu não te lembre dessa história...", "Deixa eu refrescar a tua memória..."]
        self.indice_atual = 0
        self.hitbox_seta = pygame.Rect(1400, 750, 80, 80)
    
    def processar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    if self.hitbox_seta.collidepoint(pos_mouse):
                        self.indice_atual +=1

                        if self.indice_atual >= len(self.dialogos):
                            self.terminou = True
                            self.proxima_cena = "mapa"

    #aqui entra a animação. em standby enquanto não fiz
    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.tela.fill((30, 30, 30))
        
        
        rect_caixa = pygame.Rect(100, 650, 1336, 150)
        pygame.draw.rect(self.tela, (10, 10, 10), rect_caixa)        
        pygame.draw.rect(self.tela, (200, 200, 200), rect_caixa, 4)

        if self.indice_atual < len(self.dialogos):
            texto = self.dialogos[self.indice_atual]
            fonte = pygame.font.SysFont("Arial", 40)
            img_texto = fonte.render(texto, True, (255, 255, 255))
            self.tela.blit(img_texto, (rect_caixa.x + 30, rect_caixa.y + 50))

        pygame.draw.polygon(self.tela, (255, 100, 100), [
            (self.hitbox_seta.x, self.hitbox_seta.y),                                                    
            (self.hitbox_seta.x + self.hitbox_seta.width, self.hitbox_seta.y + (self.hitbox_seta.height // 2)), 
            (self.hitbox_seta.x, self.hitbox_seta.y + self.hitbox_seta.height)])