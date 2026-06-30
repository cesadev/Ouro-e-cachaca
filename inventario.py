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

        self.deck = deck_jogador
        self.indice_destaque = None
        self.hitboxes_mao = []
        self.y_base_itens = 0
        
        #Parte de agrupar os itens dinamicamente (antes tava 100% fixo, ficava zoado)
        self.itens_agrupados = {}
        if itens:
            for item in itens:
                #Caso o item seja um objeto com atributo .nome, ou apenas uma string
                nome = item.nome if hasattr(item, 'nome') else str(item)
                self.itens_agrupados[nome] = self.itens_agrupados.get(nome, 0) + 1
                
        self.totens_agrupados = {}
        if partes_totem:
            for totem in partes_totem:
                nome = totem.nome if hasattr(totem, 'nome') else str(totem)
                self.totens_agrupados[nome] = self.totens_agrupados.get(nome, 0) + 1

        self._organizar_deck()

        #Botão de voltar pro mapa
        largura, altura = tela.get_size()
        self.rect_voltar = pygame.Rect(largura // 2 - 100, altura - 100, 200, 60)

    def _organizar_deck(self):
        self.hitboxes_mao.clear()
        largura_tela = self.tela.get_width()
        
        card_width = 144
        card_height = 176
        espaco_x = 160
        
        #Limita a 8 cartas por linha para não sair da tela
        colunas = min(8, len(self.deck)) if self.deck else 1
        linhas = (len(self.deck) + colunas - 1) // colunas
        largura_total = colunas * card_width + (colunas - 1) * (espaco_x - card_width)
        
        inicio_x = largura_tela // 2 - largura_total // 2
        inicio_y = 160

        for i, carta in enumerate(self.deck):
            x = inicio_x + (i % colunas) * espaco_x
            y = inicio_y + (i // colunas) * (card_height + 40)
            rect_base = pygame.Rect(x, y, card_width, card_height)
            self.hitboxes_mao.append((rect_base, carta, i))
            
        #Salva o Y onde a seção de itens tem que começar, dependendo de quantas linhas de cartas nos temos
        self.y_base_itens = inicio_y + linhas * (card_height + 40) + 30

    def processar_eventos(self, eventos):
        pos_mouse = pygame.mouse.get_pos()
        
        #Logica do hover
        self.indice_destaque = None
        #Iterar de trás pra frente para selecionar a carta da frente caso elas venham a sobrepor ou algo assim
        for rect_carta, carta, i in reversed(self.hitboxes_mao):
            if rect_carta.collidepoint(pos_mouse):
                self.indice_destaque = i
                break

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect_voltar.collidepoint(pos_mouse):
                    self.terminou = True
                    self.proxima_cena = "mapa" 

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.terminou = True
                    self.proxima_cena = "mapa"

    def atualizar(self, dt):
        pass

    def _desenhar_carta(self, carta, rect):
        #Função auxiliar para desenhar uma carta na posição informada.
        if carta.imagem:
            img_redimensionada = pygame.transform.scale(carta.imagem, (rect.width, rect.height))
            self.tela.blit(img_redimensionada, rect)
        else:
            pygame.draw.rect(self.tela, (200, 200, 200), rect)
            pygame.draw.rect(self.tela, (255, 255, 255), rect, 3)
            txt_nome = self.fonte_cartas.render(carta.nome, True, (0,0,0))
            self.tela.blit(txt_nome, (rect.x + 10, rect.y + 10))
        
        #Vida da carta
        txt_vida = self.fonte_vida.render(str(carta.vida), True, (54, 32, 10))
        self.tela.blit(txt_vida, (rect.x + rect.width - 30, rect.y + rect.height - 30))

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        
        txt_titulo = self.fonte_titulo.render("INVENTÁRIO", True, (255, 255, 255))
        self.tela.blit(txt_titulo, (self.tela.get_width()//2 - txt_titulo.get_width()//2, 30))

        txt_cartas = self.fonte_subtitulo.render("Suas Cartas", True, (218, 165, 32))
        self.tela.blit(txt_cartas, (self.tela.get_width()//2 - txt_cartas.get_width()//2, 100))

        #Desenhar cartas não selecionadas
        for rect_base, carta, i in self.hitboxes_mao:
            if i == self.indice_destaque: 
                continue # uso do continue pra pular a destacada pra desenhar por cima depois
            self._desenhar_carta(carta, rect_base)

        # desenhar a carta em destaque com a animaçao subindo
        if self.indice_destaque is not None and self.indice_destaque < len(self.hitboxes_mao):
            rect_original, carta, i = self.hitboxes_mao[self.indice_destaque]
            rect_hover = rect_original.copy()
            rect_hover.y -= 20 #levanta a carta aqui
            self._desenhar_carta(carta, rect_hover)

        # ============Seção dos itens e dos totens+========================
        if self.itens_agrupados or self.totens_agrupados:
            itens_textos = [self.fonte_cartas.render(f"- {nome}: x{qtd}", True, (255, 255, 255)) for nome, qtd in self.itens_agrupados.items()]
            totens_textos = [self.fonte_cartas.render(f"- {nome}: x{qtd}", True, (255, 255, 255)) for nome, qtd in self.totens_agrupados.items()]

            txt_itens = self.fonte_subtitulo.render("Itens na Mochila", True, (218, 165, 32))
            txt_totens = self.fonte_subtitulo.render("Partes do Totem", True, (218, 165, 32))

            # Lógica de centralização das duas colunas
            larguras_itens = [txt.get_width() for txt in itens_textos] + [txt_itens.get_width()]
            larguras_totens = [txt.get_width() for txt in totens_textos] + [txt_totens.get_width()]
            
            largura_coluna_itens = max(larguras_itens) if larguras_itens else txt_itens.get_width()
            largura_coluna_totens = max(larguras_totens) if larguras_totens else txt_totens.get_width()
            
            espacamento = 120
            largura_total_itens = largura_coluna_itens + largura_coluna_totens + espacamento
            inicio_x_coluna = self.tela.get_width() // 2 - largura_total_itens // 2

            itens_x = inicio_x_coluna
            totens_x = inicio_x_coluna + largura_coluna_itens + espacamento

            self.tela.blit(txt_itens, (itens_x + largura_coluna_itens // 2 - txt_itens.get_width() // 2, self.y_base_itens))
            self.tela.blit(txt_totens, (totens_x + largura_coluna_totens // 2 - txt_totens.get_width() // 2, self.y_base_itens))

            y_item = self.y_base_itens + txt_itens.get_height() + 15
            for txt in itens_textos:
                self.tela.blit(txt, (itens_x + largura_coluna_itens // 2 - txt.get_width() // 2, y_item))
                y_item += 30

            y_totem = self.y_base_itens + txt_totens.get_height() + 15
            for txt in totens_textos:
                self.tela.blit(txt, (totens_x + largura_coluna_totens // 2 - txt.get_width() // 2, y_totem))
                y_totem += 30
        else:
            txt_vazio = self.fonte_cartas.render("Sua mochila está vazia.", True, (200, 200, 200))
            self.tela.blit(txt_vazio, (self.tela.get_width()//2 - txt_vazio.get_width()//2, self.y_base_itens))

        #Botão de voltar
        pygame.draw.rect(self.tela, (90, 50, 20), self.rect_voltar)
        pygame.draw.rect(self.tela, (218, 165, 32), self.rect_voltar, 3)
        txt_voltar = self.fonte_subtitulo.render("VOLTAR", True, (255, 255, 255))
        self.tela.blit(txt_voltar, (self.rect_voltar.centerx - txt_voltar.get_width()//2, self.rect_voltar.centery - txt_voltar.get_height()//2))