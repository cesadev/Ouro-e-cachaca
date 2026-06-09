import pygame
from cena_base import CenaBase

class CenaCombate(CenaBase):
    def __init__(self, tela, deck_jogador, id_combate, deck_inimigo):
        super().__init__(tela) 
        
        self.deck_jogador = deck_jogador
        self.mao_jogador = [] 
        
        self.id_combate = id_combate
        self.deck_inimigo = deck_inimigo
        self.turno_atual = "jogador"
        
        # --- LIMITE DE COELHOS E VIDA ---
        self.coelhos_disponiveis = 10 
        self.vida_player = 2 # Max de 2 vidas ("2 shots")
        self.vida_inimigo = 20
        self.resultado = None
        
        largura_tela, altura_tela = tela.get_size()
        
        try:
            imagem_original = pygame.image.load("assets/combate.png").convert()
            self.imagem_fundo = pygame.transform.scale(imagem_original, (largura_tela, altura_tela))
        except FileNotFoundError:
            self.imagem_fundo = pygame.Surface((largura_tela, altura_tela))
            self.imagem_fundo.fill((30, 30, 30))

        self.campainha_rect = pygame.Rect(100, 50, 120, 120)
        self.comprar_coelho_rect = pygame.Rect(1190, 465, 120, 120)
        self.comprar_deck_rect = pygame.Rect(1330, 465, 120, 120)
        self.descricao_left_rect = pygame.Rect(1150, 130, 40, 40) 
        self.descricao_right_rect = pygame.Rect(1450, 130, 40, 40)

        self.hitboxes_mao = [] 
        self.hitboxes_itens = [] 
        self.hitboxes_vida = [] # Lista dinâmica das vidas
        
        self.itens_jogador = [{"nome": "Abridor de Lata"}, {"nome": "Peixeira"}]

        self.mensagem_debug = "Pronto para comprar cartas!"
        self.debug = pygame.font.SysFont("Arial", 36)
        self.fonte_cartas = pygame.font.SysFont("Arial", 20) 

        self.index_foco = None 
        
    def processar_eventos(self, eventos):
        for event in eventos:
            # --- TESTE DE DANO NO PLAYER (APERTE ESPAÇO) ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.vida_player > 0:
                        self.vida_player -= 1
                        self.mensagem_debug = f"Tomou Dano! Vida restante: {self.vida_player}"
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    pos_mouse = pygame.mouse.get_pos()

                    if self.campainha_rect.collidepoint(pos_mouse):
                        self.mensagem_debug = "Clicou na campainha"
                        
                    elif self.comprar_coelho_rect.collidepoint(pos_mouse):
                        if self.coelhos_disponiveis > 0:
                            self.mao_jogador.append({"nome": "coelho", "dano": 0})
                            self.coelhos_disponiveis -= 1
                            self.mensagem_debug = f"Gerou Coelho ({self.coelhos_disponiveis} restantes)"
                        else:
                            self.mensagem_debug = "Limite atingido! Não há mais coelhos."
                        
                    elif self.comprar_deck_rect.collidepoint(pos_mouse):
                        if len(self.deck_jogador) > 0:
                            carta_comprada = self.deck_jogador.pop(0)
                            self.mao_jogador.append(carta_comprada)
                            self.mensagem_debug = f"Comprou do deck: {carta_comprada['nome']}"
                        else:
                            self.mensagem_debug = "O deck está vazio!"
                        
                    elif self.descricao_left_rect.collidepoint(pos_mouse):
                        self.mensagem_debug = "Clicou na descrição ESQUERDA"
                        
                    elif self.descricao_right_rect.collidepoint(pos_mouse):
                        self.mensagem_debug = "Clicou na descrição DIREITA"

                    else:
                        if self.index_foco is not None and self.index_foco < len(self.mao_jogador):
                            carta = self.mao_jogador[self.index_foco]
                            self.mensagem_debug = f"Usou a carta: {carta['nome']}"
                            print(f"Jogou a carta: {carta['nome']} (Dano: {carta['dano']})")
                            self.mao_jogador.pop(self.index_foco)
                            self.index_foco = None 

                    for rect_item, item in self.hitboxes_itens:
                        if rect_item.collidepoint(pos_mouse):
                            self.mensagem_debug = f"Usou o item: {item['nome']}"
                            break 

    def atualizar(self, dt):
        if self.resultado is not None:
            return

        # --- RECALCULAR A VIDA DO PLAYER (LISTA DINÂMICA) ---
        self.hitboxes_vida.clear()
        pos_x_vida = 250 # Fica ao lado da campainha
        pos_y_vida = 70
        tamanho_vida = 80
        espacamento_vida = 20
        
        # Cria um rect para cada ponto de vida que o player tem
        for i in range(self.vida_player):
            rect_vida = pygame.Rect(pos_x_vida + (i * (tamanho_vida + espacamento_vida)), pos_y_vida, tamanho_vida, tamanho_vida)
            self.hitboxes_vida.append(rect_vida)

        # --- RECALCULAR A MÃO ---
        self.hitboxes_mao.clear() 
        qtd_cartas = len(self.mao_jogador)
            
        if qtd_cartas > 0:
            largura_carta = 144
            altura_carta = 176
            largura_tela = self.tela.get_width()
            margem_tela = 400 
            
            if qtd_cartas == 1:
                espacamento = 0 
            else:
                espacamento_ideal = (largura_tela - margem_tela - largura_carta) // (qtd_cartas - 1)
                espacamento = max(30, min(80, espacamento_ideal))
                
            largura_total_mao = (qtd_cartas - 1) * espacamento + largura_carta
            pos_x_inicial_mao = (largura_tela - largura_total_mao) // 2 
            pos_y_base_mao = 670 
            
            pos_mouse = pygame.mouse.get_pos()
            self.index_foco = None
            
            rects_virtuais = []
            for i in range(qtd_cartas):
                rect = pygame.Rect(pos_x_inicial_mao + (i * espacamento), pos_y_base_mao, largura_carta, altura_carta)
                rects_virtuais.append(rect)
                
            for i in reversed(range(qtd_cartas)):
                if rects_virtuais[i].collidepoint(pos_mouse):
                    self.index_foco = i
                    break 
            
            for i, carta in enumerate(self.mao_jogador):
                rect = rects_virtuais[i].copy()
                if i == self.index_foco:
                    rect.y -= 40 
                    
                self.hitboxes_mao.append((rect, carta, i))
            
        self.hitboxes_itens.clear()
        pos_x_inicial_item = 1190
        pos_y_base_item = 330
        
        for item in self.itens_jogador[:2]:
            rect_item = pygame.Rect(pos_x_inicial_item, pos_y_base_item, 120, 120)
            self.hitboxes_itens.append((rect_item, item))
            pos_x_inicial_item += 140

        # Atualizando a lógica de derrota para a nova quantidade de vida
        if self.vida_player <= 0:
            self.resultado = "derrota"
            self.mensagem_debug = "Você Morreu!"
        elif self.vida_inimigo <= 0:
            self.resultado = "vitoria"

    def desenhar(self):
        self.tela.blit(self.imagem_fundo, (0, 0))

        pygame.draw.rect(self.tela, (200, 50, 50), self.campainha_rect)
        
        if self.coelhos_disponiveis > 0:
            pygame.draw.rect(self.tela, (255, 105, 97), self.comprar_coelho_rect) 
        else:
            pygame.draw.rect(self.tela, (100, 100, 100), self.comprar_coelho_rect) 
            
        pygame.draw.rect(self.tela, (174, 198, 207), self.comprar_deck_rect) 
        pygame.draw.rect(self.tela, (75, 0, 130), self.descricao_left_rect)   
        pygame.draw.rect(self.tela, (200, 162, 200), self.descricao_right_rect) 
        
        # --- DESENHAR A VIDA DO PLAYER ---
        for rect_vida in self.hitboxes_vida:
            pygame.draw.rect(self.tela, (255, 182, 193), rect_vida) # Rosa Pastel
            pygame.draw.rect(self.tela, (255, 255, 255), rect_vida, 3) # Borda Branca para destacar
        
        for rect_carta, carta, i in self.hitboxes_mao:
            if i != self.index_foco:
                pygame.draw.rect(self.tela, (255, 255, 255), rect_carta) 
                pygame.draw.rect(self.tela, (0, 0, 0), rect_carta, 3) 
                
                texto_carta = self.fonte_cartas.render(carta['nome'], True, (0,0,0))
                self.tela.blit(texto_carta, (rect_carta.x + 5, rect_carta.y + 10))
                
        if self.index_foco is not None and self.index_foco < len(self.hitboxes_mao):
            rect_foco, carta_foco, _ = self.hitboxes_mao[self.index_foco]
            pygame.draw.rect(self.tela, (255, 255, 220), rect_foco) 
            pygame.draw.rect(self.tela, (255, 50, 50), rect_foco, 4) 
            
            texto_carta = self.fonte_cartas.render(carta_foco['nome'], True, (0,0,0))
            self.tela.blit(texto_carta, (rect_foco.x + 5, rect_foco.y + 10))
            
        for rect_item, item in self.hitboxes_itens:
            pygame.draw.rect(self.tela, (46, 111, 64), rect_item)
            pygame.draw.rect(self.tela, (255, 255, 255), rect_item, 2) 
            
        texto_surface = self.debug.render(self.mensagem_debug, True, (255, 255, 255))
        rect_texto = texto_surface.get_rect(center=(self.tela.get_width() // 2, 30))
        pygame.draw.rect(self.tela, (0, 0, 0), rect_texto.inflate(20, 10)) 
        self.tela.blit(texto_surface, rect_texto)


if __name__ == "__main__":
    pygame.init()
    
    LARGURA, ALTURA = 1536, 864
    tela_teste = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Debug Isolado - Cena de Combate")
    relogio = pygame.time.Clock()

    mock_deck_jogador = [
        {"nome": "cobra", "dano": 5}, 
        {"nome": "mula", "dano": 8},
        {"nome": "lobo", "dano": 4},
        {"nome": "dragao", "dano": 15}
    ] 
    mock_id_combate = "boss_1" 
    mock_deck_inimigo = [{"nome": "Lobo", "posicao": 1}]

    cena_teste = CenaCombate(tela_teste, mock_deck_jogador, mock_id_combate, mock_deck_inimigo)

    rodando = True
    while rodando:
        dt = relogio.tick(60) 
        eventos = pygame.event.get() 
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        cena_teste.processar_eventos(eventos)
        cena_teste.atualizar(dt)
        cena_teste.desenhar()

        pygame.display.flip()

    pygame.quit()