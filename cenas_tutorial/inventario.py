import os
import pygame
from cena_base import CenaBase

class CenaInventario(CenaBase):
    def __init__(self, tela, deck_jogador, itens=None, partes_totem=None):
        super().__init__(tela)
        self.tela = tela
        
        try:
            path_fundo = os.path.join("cenarios", "4k_tela_de_opcoes.png")
            img = pygame.image.load(path_fundo).convert()
            self.fundo = pygame.transform.scale(img, tela.get_size())
        except FileNotFoundError:
            self.fundo = pygame.Surface(tela.get_size())
            self.fundo.fill((30, 30, 40))
            
        self.fonte_titulo = pygame.font.SysFont("Arial", 50, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 35, bold=True)
        self.fonte_cartas = pygame.font.SysFont("Arial", 20)
        self.fonte_vida = pygame.font.SysFont("Arial", 25, bold=True)
        self.fonte_qtd = pygame.font.SysFont("Arial", 22, bold=True)

        #agrupar as cartas iguais pra melhorar a visualização
        self.cartas_agrupadas = []
        contagem = {}
        for carta in deck_jogador:
            if carta.nome in contagem:
                contagem[carta.nome]['qtd'] += 1
            else:
                contagem[carta.nome] = {'carta': carta, 'qtd': 1}
        
        self.cartas_agrupadas = list(contagem.values())

        #mock dos itens e totens
        self.itens = itens if itens else {"Cachaça": 2, "Pote de Barro": 1}
        self.partes_totem = partes_totem if partes_totem else {"Pedaço de Madeira": 1, "Corda Velha": 3}

        #botao de voltar pro mapa
        largura, altura = tela.get_size()
        self.rect_voltar = pygame.Rect(largura // 2 - 100, altura - 100, 200, 60)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                if self.rect_voltar.collidepoint(pos_mouse):
                    self.terminou = True
                    self.proxima_cena = "mapa" 
            

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.terminou = True
                    self.proxima_cena = "mapa"

    def atualizar(self, dt):
        pass

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        
        #titulo
        txt_titulo = self.fonte_titulo.render("INVENTÁRIO", True, (255, 255, 255))
        self.tela.blit(txt_titulo, (self.tela.get_width()//2 - txt_titulo.get_width()//2, 30))

        #desenhar cartas
        txt_cartas = self.fonte_subtitulo.render("Suas Cartas", True, (218, 165, 32))
        self.tela.blit(txt_cartas, (self.tela.get_width()//2 - txt_cartas.get_width()//2, 100))

        card_width = 144
        card_height = 176
        espaco_x = 160
        colunas = min(8, len(self.cartas_agrupadas)) if self.cartas_agrupadas else 1
        linhas = (len(self.cartas_agrupadas) + colunas - 1) // colunas
        largura_total = colunas * card_width + (colunas - 1) * (espaco_x - card_width)
        inicio_x = self.tela.get_width() // 2 - largura_total // 2
        inicio_y = 160

        for i, item in enumerate(self.cartas_agrupadas):
            carta = item['carta']
            qtd = item['qtd']
            
            x = inicio_x + (i % colunas) * espaco_x
            y = inicio_y + (i // colunas) * (card_height + 40)
            rect_base = pygame.Rect(x, y, card_width, card_height)

            if carta.imagem:
                img_redimensionada = pygame.transform.scale(carta.imagem, (rect_base.width, rect_base.height))
                self.tela.blit(img_redimensionada, rect_base)

            else:
                pygame.draw.rect(self.tela, (200, 200, 200), rect_base)
                pygame.draw.rect(self.tela, (255, 255, 255), rect_base, 3)
                txt_nome = self.fonte_cartas.render(carta.nome, True, (0,0,0))
                self.tela.blit(txt_nome, (rect_base.x + 10, rect_base.y + 10))
            
            #vida da carta
            txt_vida = self.fonte_vida.render(str(carta.vida), True, (54, 32, 10))
            self.tela.blit(txt_vida, (rect_base.x + rect_base.width - 30, rect_base.y + rect_base.height - 30))

            #quantidade
            if qtd > 0:
                centro_bolinha = (rect_base.right - 10, rect_base.top + 10)
                pygame.draw.circle(self.tela, (200, 30, 30), centro_bolinha, 18)
                pygame.draw.circle(self.tela, (255, 255, 255), centro_bolinha, 18, 2) # Borda
                txt_qtd = self.fonte_qtd.render(f"x{qtd}", True, (255, 255, 255))
                self.tela.blit(txt_qtd, (centro_bolinha[0] - txt_qtd.get_width()//2, centro_bolinha[1] - txt_qtd.get_height()//2))

        # desenhar os itens e totens lado a lado
        y_base = inicio_y + linhas * (card_height + 40) + 30
        itens_textos = [self.fonte_cartas.render(f"- {nome}: x{qtd}", True, (255, 255, 255)) for nome, qtd in self.itens.items()]
        totens_textos = [self.fonte_cartas.render(f"- {nome}: x{qtd}", True, (255, 255, 255)) for nome, qtd in self.partes_totem.items()]

        txt_itens = self.fonte_subtitulo.render("Itens na Mochila", True, (218, 165, 32))
        txt_totens = self.fonte_subtitulo.render("Partes do Totem", True, (218, 165, 32))

        largura_coluna_itens = max([txt.get_width() for txt in itens_textos] + [txt_itens.get_width()])
        largura_coluna_totens = max([txt.get_width() for txt in totens_textos] + [txt_totens.get_width()])
        espacamento = 120
        largura_total = largura_coluna_itens + largura_coluna_totens + espacamento
        inicio_x_coluna = self.tela.get_width() // 2 - largura_total // 2

        itens_x = inicio_x_coluna
        totens_x = inicio_x_coluna + largura_coluna_itens + espacamento

        self.tela.blit(txt_itens, (itens_x + largura_coluna_itens // 2 - txt_itens.get_width() // 2, y_base))
        self.tela.blit(txt_totens, (totens_x + largura_coluna_totens // 2 - txt_totens.get_width() // 2, y_base))

        y_item = y_base + txt_itens.get_height() + 15
        for txt in itens_textos:
            self.tela.blit(txt, (itens_x + largura_coluna_itens // 2 - txt.get_width() // 2, y_item))
            y_item += 30

        y_totem = y_base + txt_totens.get_height() + 15
        for txt in totens_textos:
            self.tela.blit(txt, (totens_x + largura_coluna_totens // 2 - txt.get_width() // 2, y_totem))
            y_totem += 30

        #botao de voltar
        pygame.draw.rect(self.tela, (90, 50, 20), self.rect_voltar)
        pygame.draw.rect(self.tela, (218, 165, 32), self.rect_voltar, 3)
        txt_voltar = self.fonte_subtitulo.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(txt_voltar, (self.rect_voltar.centerx - txt_voltar.get_width()//2, self.rect_voltar.centery - txt_voltar.get_height()//2))