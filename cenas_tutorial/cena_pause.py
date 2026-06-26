import pygame
from cena_base import CenaBase

class CenaPause(CenaBase):
    def __init__(self, tela, cena_anterior):
        super().__init__(tela)
        self.tela = tela
        self.cena_anterior = cena_anterior

        self.fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
        self.fonte_texto = pygame.font.SysFont("Arial", 32)
        self.fonte_botao = pygame.font.SysFont("Arial", 30, bold=True)

        largura, altura = tela.get_size()
        self.rect_continuar = pygame.Rect(largura // 2 - 180, altura // 2 - 40, 360, 60)
        self.rect_menu = pygame.Rect(largura // 2 - 180, altura // 2 + 40, 360, 60)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_continuar.collidepoint(pos_mouse):
                    self.terminou = True
                    self.proxima_cena = self.cena_anterior
                if self.rect_menu.collidepoint(pos_mouse):
                    self.terminou = True
                    self.proxima_cena = "menu"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.terminou = True
                    self.proxima_cena = self.cena_anterior

    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.tela.fill((10, 10, 15))

        largura, altura = self.tela.get_size()
        titulo = self.fonte_titulo.render("PAUSADO", True, (255, 215, 0))
        self.tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 2 - 180))

        pygame.draw.rect(self.tela, (40, 40, 50), self.rect_continuar)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_continuar, 3)
        txt_continuar = self.fonte_botao.render("CONTINUAR", True, (255, 255, 255))
        self.tela.blit(txt_continuar, (self.rect_continuar.centerx - txt_continuar.get_width() // 2,
                                       self.rect_continuar.centery - txt_continuar.get_height() // 2))

        pygame.draw.rect(self.tela, (40, 40, 50), self.rect_menu)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_menu, 3)
        txt_menu = self.fonte_botao.render("MENU PRINCIPAL", True, (255, 255, 255))
        self.tela.blit(txt_menu, (self.rect_menu.centerx - txt_menu.get_width() // 2,
                                  self.rect_menu.centery - txt_menu.get_height() // 2))
