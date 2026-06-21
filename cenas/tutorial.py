import pygame
import sys
import math
import random
from cenas.cena_base import CenaBase
from cenas.batalha import Carta

class CenaTutorial(CenaBase):
    def __init__(self, tela):
        super().__init__(tela) 

        tamanho_copo = (80, 96) 
        try:
            self.img_copo1 = pygame.transform.scale(pygame.image.load("assets/copo1.png").convert_alpha(), tamanho_copo)
            self.img_copo2 = pygame.transform.scale(pygame.image.load("assets/copo2.png").convert_alpha(), tamanho_copo)
        except FileNotFoundError:
            self.img_copo1 = None
            self.img_copo2 = None
        
        self.mao_jogador = [
            Carta("Perna Cabeluda", 0, 1, self._carregar_img("Perna"), 0, 1),
            Carta("Capelobo", 1, 3, self._carregar_img("Capelobo"), 1, 1),
            Carta("Curupira", 2, 2, self._carregar_img("curupira"), 2, 1),
            Carta("Capelobo", 1, 3, self._carregar_img("Capelobo"), 1, 1)
        ]
        self.deck_jogador = [
            Carta("Caboclo", 1, 1, self._carregar_img("caboclo"), 1, 1),
            Carta("Caboclo", 1, 1, self._carregar_img("caboclo"), 1, 1)
        ]
        
        self.slots_aliados = [None, None, None, None]
        self.slots_inimigos = [None, None, None, None]
        self.filas_espera_inimigas = [[], [], [], []]
        
        self.turno_atual = "jogador"
        self.turno_global = 1 
        self.ja_comprou_neste_turno = True
        self.estado_atual = "normal" 
        
        self.carta_selecionada = None
        self.index_carta_selecionada = None
        self.sangue_necessario = 0
        self.slots_sacrificados_pendentes = [] 
        #controle do tempo de sacrificio
        self.fade_sacrificio = [0.0, 0.0, 0.0, 0.0] 
        
        self.fase_resolucao = None       
        self.idx_atacante_atual = 0     
        self.progresso_ataque = 0.0     
        self.dano_aplicado = False      
        self.velocidade_ataque = 0.002  
        
        self.flash_aliado = [0, 0, 0, 0]
        self.flash_inimigo = [0, 0, 0, 0]
        self.animacoes = []
        
        self.pernas_disponiveis = 10 
        self.vida_player = 2 
        self.peso_balanca = 0 
        self.resultado = None
        self.terminou = False
        self.proxima_cena = None

        self.passo_tutorial = 0
        self.dialogos_pendentes = []
        self.dialogo_atual = ""
        self.ja_avisou_sacrificio = False
        
        def gerar_bagunca(quantidade):
            return [(random.randint(-2, 2), random.randint(-2, 2), random.uniform(-5, 5)) for _ in range(quantidade)]
        self.bagunca_pernas = gerar_bagunca(15)
        self.bagunca_deck = gerar_bagunca(40)
        
        largura_tela, altura_tela = tela.get_size()
        self.imagem_fundo = self._carregar_img("combate", scale=(largura_tela, altura_tela), convert=True) or pygame.Surface((largura_tela, altura_tela))
        self.img_perna = self._carregar_img("Perna")
        self.img_verso = self._carregar_img("carta_verso")
        
        self.campainha_rect = pygame.Rect(172, 50, 120, 120)
        self.comprar_pernas_rect = pygame.Rect(1190, 465, 144, 176)
        self.comprar_deck_rect = pygame.Rect(1350, 465, 144, 176)
        
        self.hitboxes_mao = [] 
        self.hitboxes_slots_aliados = [] 
        self.hitboxes_slots_inimigos = []
        self.hitboxes_slots_espera = [] 
        self.hitboxes_vida = [] 
        
        self.mensagem_debug = "Tutorial Iniciado"
        self.debug = pygame.font.SysFont("Arial", 36)
        self.fonte_cartas = pygame.font.SysFont("Arial", 20) 
        self.fonte_vida = pygame.font.SysFont("Arial", 30, bold=True)
        self.fonte_mini = pygame.font.SysFont("Arial", 14) 
        self.fonte_dialogo = pygame.font.SysFont("Arial", 40)
        self.index_foco = None 

        self.adicionar_dialogos(["Joga a Perna Cabeluda"])

    def _carregar_img(self, nome, scale=(144, 176), convert=False):
        try:
            img = pygame.image.load(f"assets/{nome}.png")
            img = img.convert() if convert else img.convert_alpha()
            return pygame.transform.scale(img, scale)
        except FileNotFoundError:
            return None

    def adicionar_dialogos(self, lista):
        self.dialogos_pendentes.extend(lista)
        if not self.dialogo_atual and self.dialogos_pendentes:
            self.dialogo_atual = self.dialogos_pendentes.pop(0)

    def processar_eventos(self, eventos):
        if self.dialogo_atual:
            for event in eventos:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.dialogos_pendentes:
                        self.dialogo_atual = self.dialogos_pendentes.pop(0)
                    else:
                        self.dialogo_atual = ""
            return

        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos_mouse = pygame.mouse.get_pos()
                
                # opção de cancelar com o botao direito
                if event.button == 3:
                    if self.estado_atual in ["sacrificio", "posicionamento"]:
                        self.estado_atual = "normal"
                        self.carta_selecionada = None
                        self.index_carta_selecionada = None
                        self.slots_sacrificados_pendentes.clear() 
                        self.fade_sacrificio = [0.0, 0.0, 0.0, 0.0] # reseta a animação se cancelar
                        continue

                if event.button == 1: 
                    if self.turno_atual == "jogador":
                        
                        # verificando os decks
                        if self.comprar_pernas_rect.collidepoint(pos_mouse):
                            if self.passo_tutorial < 6:
                                self.adicionar_dialogos(["Nada de comprar carta agora, jogue uma carta ou passe o turno!"])
                            elif self.ja_comprou_neste_turno:
                                self.adicionar_dialogos(["Só pode comprar uma carta por turno, nem invente de roubar no jogo!"])
                            elif self.pernas_disponiveis > 0:
                                self.mao_jogador.append(Carta("Perna Cabeluda", 0, 1, self.img_perna, 0, 1))
                                self.pernas_disponiveis -= 1
                                self.ja_comprou_neste_turno = True
                                self.estado_atual = "normal"
                            continue
                        
                        elif self.comprar_deck_rect.collidepoint(pos_mouse):
                            if self.passo_tutorial < 6:
                                self.adicionar_dialogos(["Nada de comprar carta agora, jogue uma carta ou passe o turno!"])
                            elif self.ja_comprou_neste_turno:
                                self.adicionar_dialogos(["Só pode comprar uma carta por turno, nem invente de roubar no jogo!"])
                            elif len(self.deck_jogador) > 0:
                                carta = self.deck_jogador.pop(0)
                                self.mao_jogador.append(carta)
                                self.ja_comprou_neste_turno = True
                                self.estado_atual = "normal"
                            continue
                        
                        # verificando a campainha
                        if self.campainha_rect.collidepoint(pos_mouse):
                            if self.passo_tutorial == 0:
                                self.adicionar_dialogos(["Jogue uma carta antes de passar a sua vez..."])
                            elif self.passo_tutorial == 1:
                                self.adicionar_dialogos(["Falei pra tu jogar um Capelobo, rapaz."])
                            elif self.estado_atual == "fase_compra":
                                self.adicionar_dialogos(["Compre uma carta pra continuar!"])
                            elif not self.ja_comprou_neste_turno and self.turno_global > 1:
                                self.adicionar_dialogos(["Nesse jogo, tu tem que comprar uma carta antes de fazer qualquer coisa!"])
                            elif self.passo_tutorial == 3 or (self.passo_tutorial >= 6 and self.ja_comprou_neste_turno):
                                self.turno_atual = "resolvendo_combate"
                                self.fase_resolucao = "aliados"
                                self.idx_atacante_atual = 0
                                self.progresso_ataque = 0.0
                                self.dano_aplicado = False
                            continue
                        

                        # Se chegou aqui, não clicou no deck nem na campainha
                        # Se estiver na fase de compra, bloqueia e dá a bronca no jogador
                        if self.estado_atual == "fase_compra":
                            self.adicionar_dialogos(["Compre uma carta pra continuar!"])
                            continue
                        
                        #logica das cartas
                        if self.estado_atual == "normal":

                            if not self.ja_comprou_neste_turno and self.turno_global > 1:
                                self.adicionar_dialogos(["Nesse jogo, tu tem que comprar uma carta antes de fazer qualquer coisa!"])
                                continue

                            if self.index_foco is not None and self.index_foco < len(self.mao_jogador):
                                carta_tentativa = self.mao_jogador[self.index_foco]
                                
                                if self.passo_tutorial == 0 and carta_tentativa.nome != "Perna Cabeluda":
                                    self.adicionar_dialogos(["Eu falei pra tu jogar a perna cabeluda, rapaz."])
                                    continue
                                if self.passo_tutorial == 1 and carta_tentativa.nome != "Capelobo":
                                    self.adicionar_dialogos(["Falei pra tu jogar um Capelobo, rapaz."])
                                    continue
                                if carta_tentativa.nome == "Curupira" and self.passo_tutorial < 6:
                                    continue
                                    
                                custo = carta_tentativa.custo_sangue

                                sangue_disponivel = sum(
                                    carta.valor_sacrificio
                                    for carta in self.slots_aliados
                                    if carta is not None
                                )
                                if custo > sangue_disponivel:
                                    self.adicionar_dialogos([
                                    f"Não tem sacrifícios suficiente para invocar essa carta de custo: {custo}"
                                    ])
                                    continue

                                if custo > 0:
                                    self.index_carta_selecionada = self.index_foco
                                    self.carta_selecionada = carta_tentativa
                                    self.estado_atual = "sacrificio"
                                    self.sangue_necessario = custo
                                    self.slots_sacrificados_pendentes.clear() 
                                    self.fade_sacrificio = [0.0, 0.0, 0.0, 0.0]
                                else:
                                    self.index_carta_selecionada = self.index_foco
                                    self.carta_selecionada = carta_tentativa
                                    self.estado_atual = "posicionamento"
                                
                        elif self.estado_atual == "sacrificio":
                            clicou_valido = False
                            for rect_slot, i in self.hitboxes_slots_aliados:
                                if rect_slot.collidepoint(pos_mouse):
                                    clicou_valido = True
                                    if self.slots_aliados[i] is not None and i not in self.slots_sacrificados_pendentes:
                                        self.slots_sacrificados_pendentes.append(i)
                                        sangue_acumulado = sum(self.slots_aliados[idx].valor_sacrificio for idx in self.slots_sacrificados_pendentes)
                                        
                                        if sangue_acumulado >= self.sangue_necessario:
                                            self.estado_atual = "posicionamento"
                                            if not self.ja_avisou_sacrificio:
                                                for idx_sac in self.slots_sacrificados_pendentes:
                                                    if self.slots_aliados[idx_sac].nome != "Perna Cabeluda":
                                                        self.adicionar_dialogos([
                                                            "Não se acanhe... o bicho foi sacrificado, mas não tirado do baralho.",
                                                            "A sofrencia é real. Mas tu ainda vai ver ele de novo."
                                                        ])
                                                        self.ja_avisou_sacrificio = True
                                                        break
                                    break
                            
                            # Se clicou em qualquer outro lugar da tela com o botão esquerdo, tira o foco da carta
                            if not clicou_valido:
                                self.estado_atual = "normal"
                                self.carta_selecionada = None
                                self.index_carta_selecionada = None
                                self.slots_sacrificados_pendentes.clear() 
                                self.fade_sacrificio = [0.0, 0.0, 0.0, 0.0]
                                    
                        elif self.estado_atual == "posicionamento":
                            clicou_valido = False
                            for rect_slot, i in self.hitboxes_slots_aliados:
                                if rect_slot.collidepoint(pos_mouse):
                                    clicou_valido = True
                                    slot_valido = (self.slots_aliados[i] is None or i in self.slots_sacrificados_pendentes)
                                    
                                    if slot_valido and not any(anim["slot_destino"] == i for anim in self.animacoes):
                                        rect_mao, _, _ = self.hitboxes_mao[self.index_carta_selecionada]
                                        
                                        # Apaga a carta da mesa e reseta o fade
                                        for idx in self.slots_sacrificados_pendentes:
                                            self.slots_aliados[idx] = None
                                            self.fade_sacrificio[idx] = 0.0
                                        self.slots_sacrificados_pendentes.clear() 
                                        
                                        self.animacoes.append({
                                            "carta": self.carta_selecionada.copy(),
                                            "pos_inicial": (rect_mao.x, rect_mao.y),
                                            "pos_final": (rect_slot.x, rect_slot.y),
                                            "pos_atual": [rect_mao.x, rect_mao.y],
                                            "progresso": 0.0,
                                            "slot_destino": i
                                        })
                                        
                                        self.mao_jogador.pop(self.index_carta_selecionada)
                                        self.estado_atual = "normal"
                                        self.carta_selecionada = None
                                        self.index_carta_selecionada = None
                                    break
                                    
                            # Se clicou em qualquer outro lugar da tela com o botão esquerdo, tira o foco da carta
                            if not clicou_valido:
                                self.estado_atual = "normal"
                                self.carta_selecionada = None
                                self.index_carta_selecionada = None
                                self.slots_sacrificados_pendentes.clear() 
                                self.fade_sacrificio = [0.0, 0.0, 0.0, 0.0]


    def atualizar(self, dt):
        if self.dialogo_atual:
            return 

        for idx in range(4):
            if self.flash_aliado[idx] > 0: self.flash_aliado[idx] -= dt
            if self.flash_inimigo[idx] > 0: self.flash_inimigo[idx] -= dt
            
            # Gerenciador do Fade Out para cartas sacrificadas (se quiser ajeitar, so ajeitar oq ta multiplicando)
            if idx in self.slots_sacrificados_pendentes:
                self.fade_sacrificio[idx] = min(255.0, self.fade_sacrificio[idx] + dt * 0.25)
            else:
                self.fade_sacrificio[idx] = 0.0

        for anim in self.animacoes[:]:
            anim["progresso"] += dt * 0.0035
            if anim["progresso"] >= 1.0:
                self.slots_aliados[anim["slot_destino"]] = anim["carta"]
                self.animacoes.remove(anim)
            else:
                t = anim["progresso"]
                fator_suave = 1 - pow(1 - t, 3)
                x0, y0 = anim["pos_inicial"]
                x1, y1 = anim["pos_final"]
                anim["pos_atual"][0] = x0 + (x1 - x0) * fator_suave
                anim["pos_atual"][1] = y0 + (y1 - y0) * fator_suave

        if self.passo_tutorial == 0:
            if any(c and c.nome == "Perna Cabeluda" for c in self.slots_aliados):
                self.passo_tutorial = 1
                self.adicionar_dialogos([
                    "Agora joga o capelobo",
                    "O capelobo custa 10 mirreis, ou 1 ouro pra facilitar.",
                    "Sacrifícios acontecem. Não vá ficar chorando sobre o leite derramado."
                ])

        elif self.passo_tutorial == 1:
            if self.estado_atual == "posicionamento" and self.carta_selecionada and self.carta_selecionada.nome == "Capelobo":
                self.passo_tutorial = 2
                self.adicionar_dialogos(["Foi pra terra dos pé junto. Agora joga o capelobo"])

        elif self.passo_tutorial == 2:
            if any(c and c.nome == "Capelobo" for c in self.slots_aliados):
                self.passo_tutorial = 3
                self.adicionar_dialogos([
                    "Os curupiras precisam de 2 ouros. Mas você tá liso.",
                    "Toca o sino pra terminar o teu turno... e a peleja começar."
                ])

        if self.turno_atual == "resolvendo_combate":
            if self.fase_resolucao == "aliados":
                while self.idx_atacante_atual < 4:
                    card = self.slots_aliados[self.idx_atacante_atual]
                    if card is not None and card.dano > 0:
                        break
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

                if self.idx_atacante_atual >= 4:
                    self.fase_resolucao = "pre_inimigo"
                    return

                card_atacante = self.slots_aliados[self.idx_atacante_atual]
                self.progresso_ataque += dt * self.velocidade_ataque
                
                if self.progresso_ataque >= 0.5 and not self.dano_aplicado:
                    tem_alvo = self.slots_inimigos[self.idx_atacante_atual] is not None
                    if tem_alvo:
                        self.slots_inimigos[self.idx_atacante_atual].vida -= card_atacante.dano
                        self.flash_inimigo[self.idx_atacante_atual] = 200 
                        if self.slots_inimigos[self.idx_atacante_atual].vida <= 0:
                            self.slots_inimigos[self.idx_atacante_atual] = None
                    else:
                        self.peso_balanca += card_atacante.dano
                    self.dano_aplicado = True

                if self.progresso_ataque >= 1.0:
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

            elif self.fase_resolucao == "pre_inimigo":
                if self.passo_tutorial == 3:
                    self.passo_tutorial = 4
                    self.adicionar_dialogos([
                        "Agora tem um Curupira na frente do seu capelobo",
                        "O numéro lá embaixo na esquerda da carta é o ataque do teu bixim: 1",
                        "Seu capelobo me da 1 de dano.",
                        "Quando eu tomo dano, eu desço um gole da minha breja.",
                        "O mesmo vale pra você.",
                        "O lacre da latinha vai pra balança.",
                        "Faça o meu lado descer pra ganhar."
                    ])
                    slot_capelobo = 0
                    for i, c in enumerate(self.slots_aliados):
                        if c and c.nome == "Capelobo": slot_capelobo = i
                    if len(self.slots_inimigos) < 4:
                        self.slots_inimigos = [None, None, None, None]
                    self.slots_inimigos[slot_capelobo] = Carta("Curupira", 3, 2, self._carregar_img("curupira"), 0, 1)
                    return

                elif self.passo_tutorial == 4:
                    self.passo_tutorial = 5
                    self.adicionar_dialogos([
                        "Teu capelobo tá no caminho do meu curupira",
                        "Meu curupira causará 3 de dano no teu capelobo",
                        "Ou seja, a vida do teu capelobo descerá",
                        "Os bixinhos morrem, se a vida descer pra 0."
                    ])
                    self.fase_resolucao = "inimigos"
                    self.idx_atacante_atual = 0
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False
                    return
                
                elif self.passo_tutorial == 6:
                    self.passo_tutorial = 7
                    self.adicionar_dialogos([
                        "Como tu ainda é leigo, eu passo a minha vez.",
                        "Escolha de novo..."
                    ])
                    self.turno_global += 1
                    self.turno_atual = "jogador"
                    self.fase_resolucao = None
                    self.ja_comprou_neste_turno = False
                    return
                    
                elif self.passo_tutorial >= 7:
                    self.fase_resolucao = "inimigos"
                    self.idx_atacante_atual = 0
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False
                    return

            elif self.fase_resolucao == "inimigos":
                while self.idx_atacante_atual < 4:
                    card = self.slots_inimigos[self.idx_atacante_atual]
                    if card is not None and card.dano > 0:
                        break
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

                if self.idx_atacante_atual >= 4:
                    self.turno_global += 1
                    self.turno_atual = "jogador"
                    self.fase_resolucao = None
                    self.ja_comprou_neste_turno = False
                    
                    if self.passo_tutorial == 5:
                        self.passo_tutorial = 6
                        self.estado_atual = "fase_compra"
                        
                        # atualizei alguns diálogos pois estava confuso para o jogador.
                        self.adicionar_dialogos([
                            "Agora é a tua vez...",
                            "Aqui tu compra uma perna cabeluda.",
                            "Aqui tu compra uma carta do teu baralho."
                        ])
                    return
                
                card_atacante = self.slots_inimigos[self.idx_atacante_atual]
                self.progresso_ataque += dt * self.velocidade_ataque
                
                if self.progresso_ataque >= 0.5 and not self.dano_aplicado:
                    tem_alvo = self.slots_aliados[self.idx_atacante_atual] is not None
                    if tem_alvo:
                        self.slots_aliados[self.idx_atacante_atual].vida -= card_atacante.dano
                        
                        if self.slots_aliados[self.idx_atacante_atual].nome.lower() == "timbu":
                            card_atacante.vida -= 1
                            if card_atacante.vida <= 0: self.slots_inimigos[self.idx_atacante_atual] = None
                            
                        self.flash_aliado[self.idx_atacante_atual] = 200
                        if self.slots_aliados[self.idx_atacante_atual] and self.slots_aliados[self.idx_atacante_atual].vida <= 0:
                            self.slots_aliados[self.idx_atacante_atual] = None
                    else:
                        self.peso_balanca -= card_atacante.dano
                    self.dano_aplicado = True

                if self.progresso_ataque >= 1.0:
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

        if self.peso_balanca >= 8: 
            if self.passo_tutorial < 99:
                self.passo_tutorial = 99
                self.adicionar_dialogos([
                    "Ganhasse essa partida.",
                    "Mas as próximas não vão ser moleza…"
                ])
            elif not self.dialogo_atual and not self.dialogos_pendentes:
                self.terminou = True
                self.proxima_cena = "mapa"

        self.hitboxes_vida.clear()
        for i in range(self.vida_player):
            self.hitboxes_vida.append(pygame.Rect(145 + (i * 100), 505, 80, 80))

        self.hitboxes_slots_aliados.clear()
        self.hitboxes_slots_inimigos.clear()
        self.hitboxes_slots_espera.clear()
        pos_x_slot = 458
        for i in range(4):
            self.hitboxes_slots_espera.append((pygame.Rect(pos_x_slot, 32, 144, 101), i))
            self.hitboxes_slots_inimigos.append((pygame.Rect(pos_x_slot, 158, 144, 176), i))
            self.hitboxes_slots_aliados.append((pygame.Rect(pos_x_slot, 408, 144, 176), i))
            pos_x_slot += 160

        self.hitboxes_mao.clear() 
        qtd_cartas = len(self.mao_jogador)
        if qtd_cartas > 0:
            largura_tela, margem_tela = self.tela.get_width(), 400 
            espacamento = 0 if qtd_cartas == 1 else max(30, min(80, (largura_tela - margem_tela - 144) // (qtd_cartas - 1)))
            largura_total_mao = (qtd_cartas - 1) * espacamento + 144
            pos_x_inicial_mao = (largura_tela - largura_total_mao) // 2 
            
            pos_mouse = pygame.mouse.get_pos()
            self.index_foco = None
            rects_virtuais = [pygame.Rect(pos_x_inicial_mao + (i * espacamento), 650, 144, 176) for i in range(qtd_cartas)]
            
            if self.turno_atual == "jogador" and self.estado_atual == "normal":
                for i in reversed(range(qtd_cartas)):
                    if rects_virtuais[i].collidepoint(pos_mouse):
                        self.index_foco = i
                        break 
            
            for i, carta in enumerate(self.mao_jogador):
                rect = rects_virtuais[i].copy()
                # A carta selecionada também fica levantada
                if i == self.index_foco or i == self.index_carta_selecionada: 
                    rect.y -= 60 
                self.hitboxes_mao.append((rect, carta, i))

    def desenhar(self):
        self.tela.blit(self.imagem_fundo, (0, 0))

        # desenho da balança
        centro_x, centro_y, raio = 240, 350, 128
        angulo_rad = math.radians(self.peso_balanca * 2.5)
        dx, dy = math.cos(angulo_rad) * raio, math.sin(angulo_rad) * raio
        esq_x, esq_y = centro_x - dx, centro_y + dy  
        dir_x, dir_y = centro_x + dx, centro_y - dy  

        pygame.draw.rect(self.tela, (90, 60, 30), (centro_x - 10, centro_y, 20, 80)) 
        pygame.draw.polygon(self.tela, (70, 40, 20), [(centro_x-30, centro_y+80), (centro_x+30, centro_y+80), (centro_x+15, centro_y+50), (centro_x-15, centro_y+50)]) 
        pygame.draw.line(self.tela, (200, 180, 50), (esq_x, esq_y), (dir_x, dir_y), 8) 
        pygame.draw.circle(self.tela, (255, 215, 0), (centro_x, centro_y), 10) 

        comp_corda = 40
        pygame.draw.line(self.tela, (200, 200, 200), (esq_x, esq_y), (esq_x, esq_y + comp_corda), 2)
        pygame.draw.polygon(self.tela, (180, 180, 180), [(esq_x-40, esq_y+comp_corda), (esq_x+40, esq_y+comp_corda), (esq_x+25, esq_y+comp_corda+15), (esq_x-25, esq_y+comp_corda+15)])
        pygame.draw.line(self.tela, (200, 200, 200), (dir_x, dir_y), (dir_x, dir_y + comp_corda), 2)
        pygame.draw.polygon(self.tela, (180, 180, 180), [(dir_x-40, dir_y+comp_corda), (dir_x+40, dir_y+comp_corda), (dir_x+25, dir_y+comp_corda+15), (dir_x-25, dir_y+comp_corda+15)])

        txt_balanca = self.debug.render(f"{self.peso_balanca}", True, (255, 255, 255))
        self.tela.blit(txt_balanca, (centro_x - txt_balanca.get_width()//2, centro_y - 30))

        # campainha
        pygame.draw.rect(self.tela, (200, 50, 50), self.campainha_rect)
        
        def desenhar_pilha(pos_rect, qtd, cor, img_verso=None):
            for i in range(qtd):
                if img_verso:
                    self.tela.blit(img_verso, (pos_rect.x, pos_rect.y - (i * 2)))
                else:
                    surf = pygame.Surface((144, 176))
                    surf.fill(cor)
                    self.tela.blit(surf, (pos_rect.x, pos_rect.y - (i * 2)))

        if self.pernas_disponiveis > 0: 
            desenhar_pilha(self.comprar_pernas_rect, self.pernas_disponiveis, (255, 105, 97), self.img_verso)
            
        if len(self.deck_jogador) > 0: 
            desenhar_pilha(self.comprar_deck_rect, len(self.deck_jogador), (174, 198, 207), self.img_verso)

        #efeito de piscar o deck na parte do tutorial q pede pra tu comprar uma carta (Estava muito confuso antes, vc nem sabia onde deveria comprar)
        if self.dialogo_atual == "Aqui tu compra uma perna cabeluda.":
            pisca_alpha = int(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255)
            s_pisca = pygame.Surface(self.comprar_pernas_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(s_pisca, (255, 215, 0, pisca_alpha), s_pisca.get_rect(), 6, border_radius=5)
            self.tela.blit(s_pisca, (self.comprar_pernas_rect.x, self.comprar_pernas_rect.y - 20))
            
        elif self.dialogo_atual == "Aqui tu compra uma carta do teu baralho.":
            pisca_alpha = int(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255)
            s_pisca = pygame.Surface(self.comprar_deck_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(s_pisca, (255, 215, 0, pisca_alpha), s_pisca.get_rect(), 6, border_radius=5)
            self.tela.blit(s_pisca, (self.comprar_deck_rect.x, self.comprar_deck_rect.y))

        for rect_slot, i in self.hitboxes_slots_inimigos:
            rect_desenho = rect_slot.copy()
            if self.turno_atual == "resolvendo_combate" and self.fase_resolucao == "inimigos" and self.idx_atacante_atual == i:
                rect_desenho.y += int(170 * math.sin(self.progresso_ataque * math.pi))
            if self.slots_inimigos[i]:
                if self.slots_inimigos[i].imagem: self.tela.blit(self.slots_inimigos[i].imagem, rect_desenho)
                else: pygame.draw.rect(self.tela, (200, 100, 100), rect_desenho)
                txt_vida = self.fonte_vida.render(f"{self.slots_inimigos[i].vida}", True, (54, 32, 10))
                self.tela.blit(txt_vida, (rect_desenho.x + 112, rect_desenho.y + 142))

        
        for rect_slot, i in self.hitboxes_slots_aliados:
            rect_desenho = rect_slot.copy()
            
            # A carta treme de medo se for a hora do sacrifício e AINDA NÃO tiver sido escolhida
            if self.estado_atual == "sacrificio" and self.slots_aliados[i] is not None and i not in self.slots_sacrificados_pendentes:
                rect_desenho.x += random.randint(-3, 3)
                rect_desenho.y += random.randint(-3, 3)
                
            if self.turno_atual == "resolvendo_combate" and self.fase_resolucao == "aliados" and self.idx_atacante_atual == i:
                rect_desenho.y -= int(170 * math.sin(self.progresso_ataque * math.pi))

            if self.slots_aliados[i]:
                foi_sacrificada = (i in self.slots_sacrificados_pendentes)
                
                alpha_imagem = 255
                if foi_sacrificada:
                    alpha_imagem = max(0, 255 - int(self.fade_sacrificio[i]))
                
                if alpha_imagem > 0:
                    if self.slots_aliados[i].imagem: 
                        img_render = self.slots_aliados[i].imagem.copy()
                        
                        if foi_sacrificada:
                           
                            escurecimento = min(200, int(self.fade_sacrificio[i] * 1.5))
                            surf_preta = pygame.Surface((144, 176), pygame.SRCALPHA)
                            surf_preta.fill((0, 0, 0, escurecimento))
                            img_render.blit(surf_preta, (0, 0))
                            
                            img_render.set_alpha(alpha_imagem)
                            
                        self.tela.blit(img_render, rect_desenho)
                    else: 
                        surf_fallback = pygame.Surface((144, 176), pygame.SRCALPHA)
                        surf_fallback.fill((100, 200, 100, alpha_imagem))
                        if foi_sacrificada:
                            pygame.draw.rect(surf_fallback, (0, 0, 0, min(200, int(self.fade_sacrificio[i] * 1.5))), (0,0,144,176))
                        self.tela.blit(surf_fallback, rect_desenho)
                    
                    cor_vida = (54, 32, 10)
                    txt_vida = self.fonte_vida.render(f"{self.slots_aliados[i].vida}", True, cor_vida)
                    
                    if foi_sacrificada:
                        txt_vida.set_alpha(alpha_imagem)
                        
                    self.tela.blit(txt_vida, (rect_desenho.x + 112, rect_desenho.y + 144))
        
        indice_destaque = self.index_carta_selecionada
        if indice_destaque is None:
            indice_destaque = self.index_foco

        # desenha todas as cartas normal menos a de destaque
        for rect_carta, carta, i in self.hitboxes_mao:
            if i == indice_destaque:
                continue

            if carta.imagem:
                self.tela.blit(carta.imagem, rect_carta)
            else:
                pygame.draw.rect(self.tela, (255, 255, 255), rect_carta)
                txt = self.fonte_cartas.render(carta.nome, True, (0,0,0))
                self.tela.blit(txt, (rect_carta.x + 5, rect_carta.y + 10))

            # vida
            txt_vida = self.fonte_vida.render(str(carta.vida), True, (54, 32, 10))
            self.tela.blit(txt_vida, (rect_carta.x + rect_carta.width - 30, rect_carta.y + rect_carta.height - 30))

        # desenha a carta destacada por cima
        if indice_destaque is not None and indice_destaque < len(self.hitboxes_mao):
            rect_carta, carta, i = self.hitboxes_mao[indice_destaque]

            if carta.imagem:
                self.tela.blit(carta.imagem, rect_carta)
            else:
                pygame.draw.rect(self.tela, (255, 255, 255), rect_carta)
                txt = self.fonte_cartas.render(carta.nome, True, (0,0,0))
                self.tela.blit(txt, (rect_carta.x + 5, rect_carta.y + 10))

            txt_vida = self.fonte_vida.render(str(carta.vida), True, (54, 32, 10))
            self.tela.blit(txt_vida, (rect_carta.x + rect_carta.width - 30, rect_carta.y + rect_carta.height - 30))

        if self.dialogo_atual:
            largura, altura = self.tela.get_size()
            rect_caixa = pygame.Rect(100, altura - 180, largura - 200, 150)
            pygame.draw.rect(self.tela, (10, 10, 10), rect_caixa)
            pygame.draw.rect(self.tela, (200, 200, 200), rect_caixa, 4)
            img_texto = self.fonte_dialogo.render(self.dialogo_atual, True, (255, 255, 255))
            self.tela.blit(img_texto, (rect_caixa.x + 30, rect_caixa.y + 50))
            triangulo = [(rect_caixa.right - 40, rect_caixa.bottom - 40), 
                         (rect_caixa.right - 20, rect_caixa.bottom - 40), 
                         (rect_caixa.right - 30, rect_caixa.bottom - 20)]
            pygame.draw.polygon(self.tela, (255, 255, 255), triangulo)

        for anim in self.animacoes:
            rect_render = pygame.Rect(anim["pos_atual"][0], anim["pos_atual"][1], 144, 176)
            if anim["carta"].imagem: self.tela.blit(anim["carta"].imagem, rect_render)