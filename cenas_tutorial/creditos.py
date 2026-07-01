import os
import pygame
from cena_base import CenaBase

class CenaCreditos(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.tela = tela
        self.terminou = False
        self.proxima_cena = None

        try:
            path_fundo = os.path.join("cenarios", "Creditos1.png")
            img = pygame.image.load(path_fundo).convert()
            self.fundo = pygame.transform.scale(img, tela.get_size())
        except FileNotFoundError:
            self.fundo = pygame.Surface(tela.get_size())
            self.fundo.fill((18, 18, 30))

        self.fonte_botao = pygame.font.SysFont("Arial", 28, bold=True)
        largura, altura = tela.get_size()
        self.rect_voltar = pygame.Rect(largura // 2 - 100, altura - 110, 200, 60)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_voltar.collidepoint(pos_mouse):
                    self.terminou = True
                    self.proxima_cena = "menu"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.terminou = True
                    self.proxima_cena = "menu"

    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))

        pygame.draw.rect(self.tela, (90, 50, 20), self.rect_voltar)
        pygame.draw.rect(self.tela, (218, 165, 32), self.rect_voltar, 3)
        txt_voltar = self.fonte_botao.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(txt_voltar, (self.rect_voltar.centerx - txt_voltar.get_width() // 2, self.rect_voltar.centery - txt_voltar.get_height() // 2))
