
import pygame
from cena_base import CenaBase

class CenaOpcoes(CenaBase):
    def __init__(self, tela, volume_musica=0.6, volume_efeitos=1.0):
        super().__init__(tela)
        self.tela = tela
        self.volume_musica = volume_musica
        self.volume_efeitos = volume_efeitos
        self.tela_cheia = False

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
        
        # --- AJUSTE DE COORDENADAS ---
        # Posicionando os botões à direita do centro para não sobrepor o texto
        tamanho_btn = 60
        self.rect_musica_minus = pygame.Rect(largura // 2 + 40, 165, tamanho_btn, tamanho_btn)
        self.rect_musica_plus = pygame.Rect(largura // 2 + 210, 165, tamanho_btn, tamanho_btn)
        self.rect_efeitos_minus = pygame.Rect(largura // 2 + 40, 245, tamanho_btn, tamanho_btn)
        self.rect_efeitos_plus = pygame.Rect(largura // 2 + 210, 245, tamanho_btn, tamanho_btn)

        self.opcoes = [
            ("Volume Música", f"{int(self.volume_musica * 100)}%"),
            ("Volume Efeitos", f"{int(self.volume_efeitos * 100)}%"),
            ("Resolução", f"{largura}x{altura}"),
        ]
        self.opcoes_centro_x = largura // 2

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = evento.pos
                if self.rect_voltar.collidepoint(pos_mouse):
                    self.terminou = True
                    self.proxima_cena = "menu"
                elif self.rect_musica_minus.collidepoint(pos_mouse):
                    self.volume_musica = max(0.0, round(self.volume_musica - 0.1, 1))
                    pygame.mixer.music.set_volume(self.volume_musica)
                elif self.rect_musica_plus.collidepoint(pos_mouse):
                    self.volume_musica = min(1.0, round(self.volume_musica + 0.1, 1))
                    pygame.mixer.music.set_volume(self.volume_musica)
                elif self.rect_efeitos_minus.collidepoint(pos_mouse):
                    self.volume_efeitos = max(0.0, round(self.volume_efeitos - 0.1, 1))
                elif self.rect_efeitos_plus.collidepoint(pos_mouse):
                    self.volume_efeitos = min(1.0, round(self.volume_efeitos + 0.1, 1))

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.terminou = True
                    self.proxima_cena = "menu"

    def atualizar(self, dt):
        self.opcoes[0] = ("Volume Música", f"{int(self.volume_musica * 100)}%")
        self.opcoes[1] = ("Volume Efeitos", f"{int(self.volume_efeitos * 100)}%")
        pygame.mixer.music.set_volume(self.volume_musica)

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))

        largura, _ = self.tela.get_size()
        titulo = self.fonte_titulo.render("OPÇÕES", True, (255, 215, 0))
        self.tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 40))

        inicio_y = 180
        max_nome_largura = max(self.fonte_texto.size(nome)[0] for nome, _ in self.opcoes)
        
        # Define um centro fixo para as porcentagens (ficarem entre os botões de - e +)
        valor_x = largura // 2 + 155 

        for i, (nome, valor) in enumerate(self.opcoes):
            texto_nome = self.fonte_texto.render(f"{nome}", True, (255, 255, 255))
            texto_valor = self.fonte_texto.render(f"{valor}", True, (218, 165, 32))
            y = inicio_y + i * 80
            
            nome_x = self.opcoes_centro_x - max_nome_largura
            self.tela.blit(texto_nome, (nome_x, y))
            
            # Centraliza o texto do valor para não "dançar" ao mudar de "100%" para "0%"
            rect_valor = texto_valor.get_rect(centerx=valor_x, top=y)
            self.tela.blit(texto_valor, rect_valor)

        pygame.draw.rect(self.tela, (40, 40, 40), self.rect_musica_minus)
        pygame.draw.rect(self.tela, (40, 40, 40), self.rect_musica_plus)
        pygame.draw.rect(self.tela, (40, 40, 40), self.rect_efeitos_minus)
        pygame.draw.rect(self.tela, (40, 40, 40), self.rect_efeitos_plus)

        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_musica_minus, 3)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_musica_plus, 3)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_efeitos_minus, 3)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_efeitos_plus, 3)

        txt_minus = self.fonte_texto.render("-", True, (255, 255, 255))
        txt_plus = self.fonte_texto.render("+", True, (255, 255, 255))
        
        self.tela.blit(txt_minus, (self.rect_musica_minus.centerx - txt_minus.get_width() // 2,
                                   self.rect_musica_minus.centery - txt_minus.get_height() // 2))
        self.tela.blit(txt_plus, (self.rect_musica_plus.centerx - txt_plus.get_width() // 2,
                                  self.rect_musica_plus.centery - txt_plus.get_height() // 2))
        self.tela.blit(txt_minus, (self.rect_efeitos_minus.centerx - txt_minus.get_width() // 2,
                                   self.rect_efeitos_minus.centery - txt_minus.get_height() // 2))
        self.tela.blit(txt_plus, (self.rect_efeitos_plus.centerx - txt_plus.get_width() // 2,
                                  self.rect_efeitos_plus.centery - txt_plus.get_height() // 2))

        # Os textos manuais redundantes que ficavam aqui foram deletados para limpar a tela

        pygame.draw.rect(self.tela, (30, 30, 30), self.rect_voltar)
        pygame.draw.rect(self.tela, (255, 215, 0), self.rect_voltar, 4)
        txt_voltar = self.fonte_botao.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(txt_voltar, (self.rect_voltar.centerx - txt_voltar.get_width() // 2,
                                    self.rect_voltar.centery - txt_voltar.get_height() // 2))