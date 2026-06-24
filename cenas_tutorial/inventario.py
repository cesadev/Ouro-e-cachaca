import pygame
from cena_base import CenaBase

class CenaInventario(CenaBase):
    def __init__(self, tela, deck_jogador, itens=None, partes_totem=None):
        super().__init__(tela)
        self.tela = tela
        
        try:
            img = pygame.image.load("assets/fundo_draft.png").convert()
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
        self.tela.blit(txt_cartas, (50, 100))

        inicio_x = 50
        inicio_y = 160
        espaco_x = 160 #distancia do espaço entre as cartas
        
        for i, item in enumerate(self.cartas_agrupadas):
            carta = item['carta']
            qtd = item['qtd']
            
            x = inicio_x + (i % 8) * espaco_x
            y = inicio_y + (i // 8) * 200
            rect_base = pygame.Rect(x, y, 144, 176)

            rect_base = pygame.Rect(x, y, 144, 176)

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

        #desenhar os itens
        txt_itens = self.fonte_subtitulo.render("Itens na Mochila", True, (218, 165, 32))
        self.tela.blit(txt_itens, (50, 600))
        
        y_item = 650
        for nome, qtd in self.itens.items():
            txt = self.fonte_cartas.render(f"- {nome}: x{qtd}", True, (255, 255, 255))
            self.tela.blit(txt, (50, y_item))
            y_item += 30

        #desenhar totens
        txt_totens = self.fonte_subtitulo.render("Partes do Totem", True, (218, 165, 32))
        self.tela.blit(txt_totens, (400, 600))

        y_totem = 650
        for nome, qtd in self.partes_totem.items():
            txt = self.fonte_cartas.render(f"- {nome}: x{qtd}", True, (255, 255, 255))
            self.tela.blit(txt, (400, y_totem))
            y_totem += 30

        #botao de voltar
        pygame.draw.rect(self.tela, (90, 50, 20), self.rect_voltar)
        pygame.draw.rect(self.tela, (218, 165, 32), self.rect_voltar, 3)
        txt_voltar = self.fonte_subtitulo.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(txt_voltar, (self.rect_voltar.centerx - txt_voltar.get_width()//2, self.rect_voltar.centery - txt_voltar.get_height()//2))