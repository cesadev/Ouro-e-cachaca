import pygame
from cena_base import CenaBase

class CenaOpcoes(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.tela = tela

        try:
            img = pygame.image.load("cenarios/4k tela de opções.png").convert()
            self.fundo = pygame.transform.scale(img, tela.get_size())
        except FileNotFoundError:
            self.fundo = pygame.Surface(tela.get_size())
            self.fundo.fill((20, 20, 30))

        self.fonte_titulo = pygame.font.SysFont("Arial", 56, bold=True)
        self.fonte_texto = pygame.font.SysFont("Arial", 28)
        self.fonte_botao = pygame.font.SysFont("Arial", 32, bold=True)

        largura, altura = tela.get_size()
        self.rect_voltar = pygame.Rect(largura // 2 - 120, altura - 120, 240, 70)

        self.opcoes = [
            ("Volume Música", "100%"),
            ("Volume Efeitos", "100%"),
            ("Resolução", f"{largura}x{altura}"),
            ("Tela Cheia", "Ligado"),
        ]
        self.opcoes_centro_x = largura // 2

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

        largura, _ = self.tela.get_size()
        titulo = self.fonte_titulo.render("OPÇÕES", True, (255, 215, 0))
        self.tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 40))

        inicio_y = 180
        max_nome_largura = max(self.fonte_texto.size(nome)[0] for nome, _ in self.opcoes)
        valor_x = self.opcoes_centro_x + max_nome_largura // 2 + 40
        for i, (nome, valor) in enumerate(self.opcoes):
            texto_nome = self.fonte_texto.render(f"{nome}", True, (255, 255, 255))
            texto_valor = self.fonte_texto.render(f"{valor}", True, (218, 165, 32))
            y = inicio_y + i * 60
            nome_x = self.opcoes_centro_x - max_nome_largura - 20
            self.tela.blit(texto_nome, (nome_x, y))
            self.tela.blit(texto_valor, (valor_x, y))

        pygame.draw.rect(self.tela, (30, 30, 30), self.rect_voltar)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_voltar, 4)
        txt_voltar = self.fonte_botao.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(txt_voltar, (self.rect_voltar.centerx - txt_voltar.get_width() // 2,
                                    self.rect_voltar.centery - txt_voltar.get_height() // 2))
