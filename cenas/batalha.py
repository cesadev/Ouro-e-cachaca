import pygame
import math
import random
from cena_base import CenaBase

class Carta:
    def __init__(self, nome, poder, vida, imagem=None, custo_sangue=0, valor_sacrificio=1):
        self.nome = nome
        self.poder = poder
        self.dano = poder  
        self.vida = vida
        self.custo_sangue = custo_sangue
        self.valor_sacrificio = valor_sacrificio
        
        self.imagem = imagem

        if self.imagem is not None:
            self.rect = self.imagem.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, 140, 190)

    def desenhar(self, tela, posicao_x, posicao_y):
        self.rect.topleft = (posicao_x, posicao_y)
        if self.imagem is not None:
            tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(tela, (255, 255, 255), self.rect) 
            pygame.draw.rect(tela, (0, 0, 0), self.rect, 3)
        
        
    def copy(self):
        """Retorna uma cópia real da instância da carta (essencial para invocações)"""
        return Carta(self.nome, self.poder, self.vida, self.imagem, self.custo_sangue, self.valor_sacrificio)


# cena de combate
class CenaCombate(CenaBase):
    def __init__(self, tela, deck_jogador, dados_da_fase):
        super().__init__(tela) 
        
        # Transforma o deck inicial em objetos da classe Carta caso venham como dicionários
        self.deck_jogador = [
            Carta(c["nome"], c.get("dano", c.get("poder", 0)), c["vida"], c.get("imagem"), c.get("custo_sangue", 0), c.get("valor_sacrificio", 1))
            if isinstance(c, dict) else c
            for c in deck_jogador
        ]
        self.mao_jogador = [] 
        
        # dados fase
        self.id_combate = dados_da_fase.get("nome", "Combate Desconhecido")
        self.script_inimigo = dados_da_fase.get("script_inimigo", {})
        
        # gerenciador de turnos
        self.turno_atual = "jogador"
        self.turno_global = 1 
        self.ja_comprou_neste_turno = False 
        
        self.estado_atual = "fase_compra" 
        
        self.carta_selecionada = None
        self.index_carta_selecionada = None
        self.sangue_necessario = 0
        
        # sist sacrificio
        self.slots_sacrificados_pendentes = [] 
        
        # --- SISTEMA DE SEQUENCIAMENTO E COOLDOWN DE ATAQUES ---
        self.fase_resolucao = None       
        self.idx_atacante_atual = 0     
        self.progresso_ataque = 0.0     
        self.dano_aplicado = False      
        self.tempo_espera_fase = 0.0 
        
        # --- VELOCIDADE DO ATAQUE ---
        self.velocidade_ataque = 0.002  
        
        self.flash_aliado = [0, 0, 0, 0]
        self.flash_inimigo = [0, 0, 0, 0]
        
        self.animacoes = []
        
        # --- TABULEIRO (4 SLOTS) ---
        self.slots_aliados = [None, None, None, None]
        self.slots_inimigos = [None, None, None, None]
        
        # --- FILA DE MEMÓRIA/ANTECIPAÇÃO DO INIMIGO ---
        self.filas_espera_inimigas = [[], [], [], []]
        
        # Puxa os obstáculos iniciais convertendo-os em objetos Carta
        for obstaculo in dados_da_fase.get("obstaculos_iniciais", []):
            carta_obs = Carta(
                obstaculo["nome"], 
                obstaculo.get("dano", 0), 
                obstaculo["vida"], 
                obstaculo.get("imagem"), 
                obstaculo.get("custo_sangue", 0), 
                obstaculo.get("valor_sacrificio", 0)
            )
            self.slots_inimigos[obstaculo["slot"]] = carta_obs
            
        self._carregar_intencoes_inimigas_do_turno(1)
        
        # --- RECURSOS AND BALANÇA ---
        self.pernas_disponiveis = 10 
        self.vida_player = 2 
        self.peso_balanca = 0 
        self.resultado = None
        
        # decks
        def gerar_bagunca_cumulativa(quantidade):
            desvios = []
            x_atual, y_atual = 0.0, 0.0
            tendencia_x = random.uniform(-0.6, 0.6) 
            tendencia_y = random.uniform(-0.2, 0.2)
            for _ in range(quantidade):
                x_atual += tendencia_x + random.uniform(-0.4, 0.4)
                y_atual += tendencia_y + random.uniform(-0.4, 0.4)
                angulo = random.uniform(-6.0, 6.0) 
                desvios.append((int(x_atual), int(y_atual), angulo))
            return desvios
        
        self.bagunca_pernas = gerar_bagunca_cumulativa(15)
        self.bagunca_deck = gerar_bagunca_cumulativa(40)
        
        largura_tela, altura_tela = tela.get_size()
        
        try:
            imagem_original = pygame.image.load("assets/combate.png").convert()
            self.imagem_fundo = pygame.transform.scale(imagem_original, (largura_tela, altura_tela))
        except FileNotFoundError:
            self.imagem_fundo = pygame.Surface((largura_tela, altura_tela))
            self.imagem_fundo.fill((30, 30, 30))

        try:
            img_perna_original = pygame.image.load("assets/Perna.png").convert_alpha()
            self.img_perna = pygame.transform.scale(img_perna_original, (140, 190))
        except FileNotFoundError:
            self.img_perna = None

        # --- HITBOXES FIXAS ---
        self.campainha_rect = pygame.Rect(172, 50, 120, 120)
        self.comprar_pernas_rect = pygame.Rect(1190, 465, 140, 190)
        self.comprar_deck_rect = pygame.Rect(1350, 465, 140, 190)
        
        self.descricao_left_rect = pygame.Rect(1150, 130, 40, 40) 
        self.descricao_right_rect = pygame.Rect(1450, 130, 40, 40)

        self.hitboxes_mao = [] 
        self.hitboxes_slots_aliados = [] 
        self.hitboxes_slots_inimigos = []
        self.hitboxes_slots_espera = [] 
        self.hitboxes_vida = [] 
        self.hitboxes_itens = []
        
        self.itens_jogador = [{"nome": "Abridor de Lata"}, {"nome": "Peixeira"}]

        self.mensagem_debug = "Início do Turno: Compre uma carta!"
        self.debug = pygame.font.SysFont("Arial", 36)
        self.fonte_cartas = pygame.font.SysFont("Arial", 20) 
        self.fonte_mini = pygame.font.SysFont("Arial", 14) 
        self.index_foco = None 
        
    def _carregar_intencoes_inimigas_do_turno(self, turno):
        """Varre o script do turno e adiciona spawns de objetos Carta na fila correspondente"""
        acoes = self.script_inimigo.get(turno, [])
        for comando in acoes:
            if comando["acao"] == "jogar_carta":
                slot = comando["slot"]
                c = comando["carta"]
                if isinstance(c, dict):
                    carta_obj = Carta(c["nome"], c.get("dano", c.get("poder", 0)), c["vida"], c.get("imagem"), c.get("custo_sangue", 0), c.get("valor_sacrificio", 1))
                else:
                    carta_obj = c.copy()
                self.filas_espera_inimigas[slot].append(carta_obj)

    def processar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos_mouse = pygame.mouse.get_pos()
                
                if event.button == 3: 
                    if self.estado_atual in ["sacrificio", "posicionamento"]:
                        self.estado_atual = "normal"
                        self.carta_selecionada = None
                        self.index_carta_selecionada = None
                        self.slots_sacrificados_pendentes.clear() 
                        self.mensagem_debug = "Invocação cancelada. Suas criaturas foram salvas!"
                        continue

                if event.button == 1: 
                    if self.turno_atual == "jogador":
                        comprou_agora = False
                        
                        if self.comprar_pernas_rect.collidepoint(pos_mouse):
                            if not self.ja_comprou_neste_turno and self.pernas_disponiveis > 0:
                                # a parte do sacrificio da perna
                                self.mao_jogador.append(Carta("Perna", 0, 1, self.img_perna, 0, 1))
                                self.pernas_disponiveis -= 1
                                self.ja_comprou_neste_turno = True
                                comprou_agora = True
                                self.mensagem_debug = "Perna na mão!"
                        
                        elif self.comprar_deck_rect.collidepoint(pos_mouse):
                            if not self.ja_comprou_neste_turno and len(self.deck_jogador) > 0:
                                carta = self.deck_jogador.pop(0)
                                self.mao_jogador.append(carta)
                                self.ja_comprou_neste_turno = True
                                comprou_agora = True
                                self.mensagem_debug = f"Comprou: {carta.nome}"
                        
                        if comprou_agora:
                            self.estado_atual = "normal"
                            continue 
                        
                        if self.estado_atual == "fase_compra":
                            if self.campainha_rect.collidepoint(pos_mouse):
                                self.mensagem_debug = "Compre uma carta antes de passar a vez."
                        
                        else:
                            if self.campainha_rect.collidepoint(pos_mouse):
                                self.turno_atual = "resolvendo_combate"
                                self.fase_resolucao = "aliados"
                                self.idx_atacante_atual = 0
                                self.progresso_ataque = 0.0
                                self.dano_aplicado = False
                                self.mensagem_debug = "Seu ataque começou..."
                                
                            else:
                                if self.estado_atual == "normal":
                                    if self.index_foco is not None and self.index_foco < len(self.mao_jogador):
                                        carta_tentativa = self.mao_jogador[self.index_foco]
                                        custo = carta_tentativa.custo_sangue
                                        sangue_disponivel = sum(slot.valor_sacrificio for slot in self.slots_aliados if slot is not None)
                                        
                                        if custo > 0:
                                            if sangue_disponivel < custo:
                                                self.mensagem_debug = "Sangue insuficiente no tabuleiro!"
                                            else:
                                                self.index_carta_selecionada = self.index_foco
                                                self.carta_selecionada = carta_tentativa
                                                self.estado_atual = "sacrificio"
                                                self.sangue_necessario = custo
                                                self.slots_sacrificados_pendentes.clear() 
                                                self.mensagem_debug = f"SACRIFÍCIO: Escolha {custo} criatura(s) para abater!"
                                        else:
                                            self.index_carta_selecionada = self.index_foco
                                            self.carta_selecionada = carta_tentativa
                                            self.estado_atual = "posicionamento"
                                            self.mensagem_debug = "POSICIONAMENTO: Escolha um slot aliado vazio."
                                
                                elif self.estado_atual == "sacrificio":
                                    for rect_slot, i in self.hitboxes_slots_aliados:
                                        if rect_slot.collidepoint(pos_mouse):
                                            if self.slots_aliados[i] is not None and i not in self.slots_sacrificados_pendentes:
                                                self.slots_sacrificados_pendentes.append(i)
                                                
                                                sangue_acumulado = sum(self.slots_aliados[idx].valor_sacrificio for idx in self.slots_sacrificados_pendentes)
                                                
                                                if sangue_acumulado >= self.sangue_necessario:
                                                    self.estado_atual = "posicionamento"
                                                    self.mensagem_debug = f"Sacrifício pronto! Escolha onde baixar o {self.carta_selecionada.nome}."
                                                else:
                                                    restante = self.sangue_necessario - sangue_acumulado
                                                    self.mensagem_debug = f"Marcado! Faltam mais {restante} de sangue."
                                            break
                                            
                                elif self.estado_atual == "posicionamento":
                                    for rect_slot, i in self.hitboxes_slots_aliados:
                                        if rect_slot.collidepoint(pos_mouse):
                                            slot_valido = (self.slots_aliados[i] is None or i in self.slots_sacrificados_pendentes)
                                            
                                            if slot_valido and not any(anim["slot_destino"] == i for anim in self.animacoes):
                                                rect_mao, _, _ = self.hitboxes_mao[self.index_carta_selecionada]
                                                
                                                for idx in self.slots_sacrificados_pendentes:
                                                    self.slots_aliados[idx] = None
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

    def atualizar(self, dt):
        if self.resultado is not None:
            return

        for idx in range(4):
            if self.flash_aliado[idx] > 0: self.flash_aliado[idx] -= dt
            if self.flash_inimigo[idx] > 0: self.flash_inimigo[idx] -= dt

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

        if self.turno_atual == "resolvendo_combate":
            
            # FASE 1: SEUS CARDS ATACAM
            if self.fase_resolucao == "aliados":
                while self.idx_atacante_atual < 4:
                    card = self.slots_aliados[self.idx_atacante_atual]
                    if card is not None and card.dano > 0:
                        break
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

                if self.idx_atacante_atual >= 4:
                    self.mensagem_debug = "Turno Aliado encerrado. Inimigo preparando jogadas..."
                    self.fase_resolucao = "pre_inimigo"
                    self.tempo_espera_fase = 1000.0 
                    
                    for i in range(4):
                        if self.slots_inimigos[i] is None and len(self.filas_espera_inimigas[i]) > 0:
                            self.slots_inimigos[i] = self.filas_espera_inimigas[i].pop(0)
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
                        if self.peso_balanca >= 8:
                            self.resultado = "vitoria"
                            self.mensagem_debug = "VITÓRIA! A balança tombou totalmente."
                            return
                    self.dano_aplicado = True

                if self.progresso_ataque >= 1.0:
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

            # FASE 2: COOLDOWN E EVENTOS ESPECIAIS DO CHEFE
            elif self.fase_resolucao == "pre_inimigo":
                self.tempo_espera_fase -= dt
                if self.tempo_espera_fase <= 0:
                    acoes_do_turno = self.script_inimigo.get(self.turno_global, [])
                    for comando in acoes_do_turno:
                        if comando["acao"] == "ataque_especial":
                            self.peso_balanca -= comando.get("dano_direto", 1)
                            self.mensagem_debug = f"Chefe usou: {comando.get('nome')}!"
                    
                    self.fase_resolucao = "inimigos"
                    self.idx_atacante_atual = 0
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False
                    self.mensagem_debug = "Inimigos avançam para atacar!"

            # FASE 3: ATAQUE DOS CARDS INIMIGOS
            elif self.fase_resolucao == "inimigos":
                while self.idx_atacante_atual < 4:
                    card = self.slots_inimigos[self.idx_atacante_atual]
                    if card is not None and card.dano > 0:
                        break
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

                if self.idx_atacante_atual >= 4:
                    if self.peso_balanca <= -8:
                        self.vida_player -= 1
                        self.resultado = "derrota"
                        self.mensagem_debug = "Você perdeu."
                        if self.vida_player <= 0:
                            self.mensagem_debug = "Você sucumbiu..."
                            return

                    self.turno_global += 1
                    self.turno_atual = "jogador"
                    self.ja_comprou_neste_turno = False 
                    self.estado_atual = "fase_compra"
                    self.fase_resolucao = None
                    if self.resultado != "derrota":
                        self._carregar_intencoes_inimigas_do_turno(self.turno_global)
                        self.mensagem_debug = "Seu Turno! Compre 1 carta para agir."
                    return

                card_atacante = self.slots_inimigos[self.idx_atacante_atual]
                self.progresso_ataque += dt * self.velocidade_ataque
                
                if self.progresso_ataque >= 0.5 and not self.dano_aplicado:
                    tem_alvo = self.slots_aliados[self.idx_atacante_atual] is not None
                    if tem_alvo:
                        self.slots_aliados[self.idx_atacante_atual].vida -= card_atacante.dano
                        self.flash_aliado[self.idx_atacante_atual] = 200
                        if self.slots_aliados[self.idx_atacante_atual].vida <= 0:
                            self.slots_aliados[self.idx_atacante_atual] = None
                    else:
                        self.peso_balanca -= card_atacante.dano
                        
                    self.dano_aplicado = True

                if self.progresso_ataque >= 1.0:
                    self.idx_atacante_atual += 1
                    self.progresso_ataque = 0.0
                    self.dano_aplicado = False

        # Construção dos retangulos
        self.hitboxes_vida.clear()
        pos_x_vida, pos_y_vida, tamanho_vida, espacamento_vida = 145, 505, 80, 20
        for i in range(self.vida_player):
            rect = pygame.Rect(pos_x_vida + (i * (tamanho_vida + espacamento_vida)), pos_y_vida, tamanho_vida, tamanho_vida)
            self.hitboxes_vida.append(rect)

        self.hitboxes_slots_aliados.clear()
        self.hitboxes_slots_inimigos.clear()
        self.hitboxes_slots_espera.clear()
        
        pos_x_slot = 458
        y_espera = 62
        y_inimigos = 158
        y_aliados = 408
        
        espacamento_horizontal = 160
        largura_padrao, altura_padrao = 144, 176 
        altura_mini = 81
        for i in range(4):
            self.hitboxes_slots_espera.append((pygame.Rect(pos_x_slot, y_espera, largura_padrao, altura_mini), i))
            self.hitboxes_slots_inimigos.append((pygame.Rect(pos_x_slot, y_inimigos, largura_padrao, altura_padrao), i))
            self.hitboxes_slots_aliados.append((pygame.Rect(pos_x_slot, y_aliados, largura_padrao, altura_padrao), i))
            pos_x_slot += espacamento_horizontal
            
        self.hitboxes_itens.clear()
        pos_x_inicial_item = 1190
        for item in self.itens_jogador[:2]:
            self.hitboxes_itens.append((pygame.Rect(pos_x_inicial_item, 330, 120, 120), item))
            pos_x_inicial_item += 140

        # --- GERENCIADOR DA MÃO ---
        self.hitboxes_mao.clear() 
        qtd_cartas = len(self.mao_jogador)
        if qtd_cartas > 0:
            largura_tela, margem_tela = self.tela.get_width(), 400 
            espacamento = 0 if qtd_cartas == 1 else max(30, min(80, (largura_tela - margem_tela - largura_padrao) // (qtd_cartas - 1)))
            largura_total_mao = (qtd_cartas - 1) * espacamento + largura_padrao
            pos_x_inicial_mao = (largura_tela - largura_total_mao) // 2 
            
            pos_mouse = pygame.mouse.get_pos()
            self.index_foco = None
            
            rects_virtuais = []
            for i in range(qtd_cartas):
                rect = pygame.Rect(pos_x_inicial_mao + (i * espacamento), 650, largura_padrao, altura_padrao)
                rects_virtuais.append(rect)
                
            if self.turno_atual == "jogador" and self.estado_atual == "normal":
                for i in reversed(range(qtd_cartas)):
                    if rects_virtuais[i].collidepoint(pos_mouse):
                        self.index_foco = i
                        break 
            
            for i, carta in enumerate(self.mao_jogador):
                rect = rects_virtuais[i].copy()
                if i == self.index_foco:
                    rect.y -= 40 
                self.hitboxes_mao.append((rect, carta, i))

    def desenhar(self):
        self.tela.blit(self.imagem_fundo, (0, 0))

        # --- BALANÇA ---
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

        # --- CAMPAINHA ---
        pygame.draw.rect(self.tela, (200, 50, 50), self.campainha_rect)
        
        # --- DECKS ---
        piscar = self.estado_atual == "fase_compra" and (pygame.time.get_ticks() % 1000 < 500)
        cor_pernas_base = (200, 50, 50) if piscar else (255, 105, 97)
        cor_deck_base = (120, 150, 160) if piscar else (174, 198, 207)

        def desenhar_pilha(pos_rect, qtd_itens, lista_bagunca, cor_base, bloqueado):
            for i in range(qtd_itens):
                off_x, off_y, angulo = lista_bagunca[i % len(lista_bagunca)]
                surf_carta = pygame.Surface((140, 190), pygame.SRCALPHA)
                cor = (100, 100, 100) if bloqueado else cor_base
                surf_carta.fill(cor)
                pygame.draw.rect(surf_carta, (0, 0, 0), (0, 0, 140, 190), 6)
                
                carta_rot = pygame.transform.rotate(surf_carta, angulo)
                rect_final = carta_rot.get_rect(center=pos_rect.center)
                rect_final.x += off_x
                rect_final.y += (off_y - (i * 2)) 
                self.tela.blit(carta_rot, rect_final)

        if self.pernas_disponiveis > 0:
            desenhar_pilha(self.comprar_pernas_rect, self.pernas_disponiveis, self.bagunca_pernas, cor_pernas_base, self.ja_comprou_neste_turno)
        else:
            pygame.draw.rect(self.tela, (50, 50, 50), self.comprar_pernas_rect)

        if len(self.deck_jogador) > 0:
            desenhar_pilha(self.comprar_deck_rect, len(self.deck_jogador), self.bagunca_deck, cor_deck_base, self.ja_comprou_neste_turno)
        else:
            pygame.draw.rect(self.tela, (50, 50, 50), self.comprar_deck_rect) 

        # --- PERIFÉRICOS ---
        pygame.draw.rect(self.tela, (75, 0, 130), self.descricao_left_rect)   
        pygame.draw.rect(self.tela, (200, 162, 200), self.descricao_right_rect) 
        for rect_vida in self.hitboxes_vida:
            pygame.draw.rect(self.tela, (255, 182, 193), rect_vida) 
            pygame.draw.rect(self.tela, (255, 255, 255), rect_vida, 3) 
        for rect_item, item in self.hitboxes_itens:
            pygame.draw.rect(self.tela, (46, 111, 64), rect_item)
            pygame.draw.rect(self.tela, (255, 255, 255), rect_item, 2) 
            
        # --- EXIBIÇÃO DO CAMPO DE CIMA (MINI CARTAS DE MEMÓRIA) ---
        for rect_mini, i in self.hitboxes_slots_espera:
            pygame.draw.rect(self.tela, (60, 45, 45), rect_mini, 1)
            
            fila = self.filas_espera_inimigas[i]
            if len(fila) > 0:
                proxima_carta = fila[0] 
                
                pygame.draw.rect(self.tela, (45, 45, 50), rect_mini.inflate(-4, -4))
                pygame.draw.rect(self.tela, (100, 80, 80), rect_mini.inflate(-4, -4), 2)
                
                txt_nome = self.fonte_mini.render(proxima_carta.nome, True, (200, 200, 200))
                self.tela.blit(txt_nome, (rect_mini.x + 8, rect_mini.y + 8))
                
                txt_status = self.fonte_mini.render(f"ATK:{proxima_carta.dano}  HP:{proxima_carta.vida}", True, (160, 140, 140))
                self.tela.blit(txt_status, (rect_mini.x + 8, rect_mini.y + 45))

        # Coisas dos inimigos
        for rect_slot, i in self.hitboxes_slots_inimigos:
            rect_desenho = rect_slot.copy()
            
            if self.turno_atual == "resolvendo_combate" and self.fase_resolucao == "inimigos" and self.idx_atacante_atual == i:
                fator_onda = math.sin(self.progresso_ataque * math.pi)
                alvo_vazio = self.slots_aliados[i] is None
                dist_max = 240 if alvo_vazio else 170
                rect_desenho.y += int(dist_max * fator_onda) 
            
            pygame.draw.rect(self.tela, (150, 50, 50), rect_desenho, 2) 
            if self.slots_inimigos[i]:
                cor_corpo = (255, 30, 30) if self.flash_inimigo[i] > 0 else (200, 100, 100)
                
                pygame.draw.rect(self.tela, cor_corpo, rect_desenho.inflate(-10, -10))
                txt = self.fonte_cartas.render(self.slots_inimigos[i].nome, True, (255,255,255))
                self.tela.blit(txt, (rect_desenho.x + 10, rect_desenho.y + 20))
                txt_atk = self.fonte_cartas.render(f"ATK: {self.slots_inimigos[i].dano}", True, (255, 255, 255))
                self.tela.blit(txt_atk, (rect_desenho.x + 10, rect_desenho.y + 100))

                txt_vida = self.fonte_cartas.render(f"{self.slots_inimigos[i].vida}", True, (54, 32, 10))
                self.tela.blit(txt_vida, (rect_desenho.x + 112, rect_desenho.y + 144))
                
        # slots cartas player
        for rect_slot, i in self.hitboxes_slots_aliados:
            cor_borda = (50, 150, 50) 
            rect_desenho = rect_slot.copy()
            esta_em_panico = False
            prometida_ao_abate = i in self.slots_sacrificados_pendentes

            if self.turno_atual == "resolvendo_combate" and self.fase_resolucao == "aliados" and self.idx_atacante_atual == i:
                fator_onda = math.sin(self.progresso_ataque * math.pi)
                alvo_vazio = self.slots_inimigos[i] is None
                dist_max = 240 if alvo_vazio else 170
                rect_desenho.y -= int(dist_max * fator_onda) 

            if prometida_ao_abate:
                cor_borda = (0, 0, 0) 
                
            elif self.estado_atual == "sacrificio" and self.slots_aliados[i] is not None:
                esta_em_panico = True
                tempo_ticks = pygame.time.get_ticks()
                rect_desenho.x += int(math.sin(tempo_ticks * 0.03 + i * 12) * 3)
                rect_desenho.y += int(math.cos(tempo_ticks * 0.03 + i * 7) * 3)
                
                pulso_alfa = int(140 + 115 * math.sin(tempo_ticks * 0.015))
                cor_borda = (pulso_alfa, 0, 0) 
                
            elif self.estado_atual == "posicionamento" and (self.slots_aliados[i] is None or prometida_ao_abate):
                cor_borda = (0, 255, 0) 

            if prometida_ao_abate or esta_em_panico:
                pygame.draw.rect(self.tela, cor_borda, rect_desenho, 8)
            
            if self.slots_aliados[i] and not prometida_ao_abate:
                cor_texto = (0,0,0) if not esta_em_panico else (255,255,255)

                if self.slots_aliados[i].imagem is not None:
                    self.tela.blit(self.slots_aliados[i].imagem, (rect_desenho.x, rect_desenho.y-4))                
                else:
                    cor_corpo = (255, 30, 30) if self.flash_aliado[i] > 0 else ((100, 200, 100) if not esta_em_panico else (160, 80, 80))
                    
                    pygame.draw.rect(self.tela, cor_corpo, rect_desenho.inflate(-12, -12))
                    txt = self.fonte_cartas.render(self.slots_aliados[i].nome, True, cor_texto)
                    self.tela.blit(txt, (rect_desenho.x + 10, rect_desenho.y + 20))
                
                    
                cor_vida = (200, 0, 0) if prometida_ao_abate or esta_em_panico else (54, 32, 10)    
                txt_vida = self.fonte_cartas.render(f"{self.slots_aliados[i].vida}", True, cor_vida)
                self.tela.blit(txt_vida, (rect_desenho.x + 85, rect_desenho.y + 160))
    
        # MÃO DO JOGADOR
        for rect_carta, carta, i in self.hitboxes_mao:
            if i != self.index_foco:
                if carta.imagem is not None:
                    self.tela.blit(carta.imagem, rect_carta)
                else:
                    cor_fundo = (255, 255, 200) if (self.estado_atual != "normal" and self.estado_atual != "fase_compra" and i == self.index_carta_selecionada) else (255, 255, 255)
                    pygame.draw.rect(self.tela, cor_fundo, rect_carta) 
                    
                    txt_nome = self.fonte_cartas.render(carta.nome, True, (0,0,0))
                    txt_custo = self.fonte_cartas.render(f"Custo: {carta.custo_sangue}", True, (200,0,0))
                    self.tela.blit(txt_nome, (rect_carta.x + 5, rect_carta.y + 10))
                    self.tela.blit(txt_custo, (rect_carta.x + 5, rect_carta.y + 40))
                

                # isso aqui vai ser somente pra fazer o texto aparecer quando estiver na mão
                txt_vida_mao = self.fonte_cartas.render(f"{carta.vida}", True, (54, 32, 10))
                self.tela.blit(txt_vida_mao, (rect_carta.x + 112, rect_carta.y + 144))
                
        if self.index_foco is not None and self.index_foco < len(self.hitboxes_mao):
            rect_foco, carta_foco, _ = self.hitboxes_mao[self.index_foco]
            
            if carta_foco.imagem is not None:
                self.tela.blit(carta_foco.imagem, rect_foco)
            else:
                pygame.draw.rect(self.tela, (255, 255, 220), rect_foco) 
                
                txt_nome = self.fonte_cartas.render(carta_foco.nome, True, (0,0,0))
                txt_custo = self.fonte_cartas.render(f"Custo: {carta_foco.custo_sangue}", True, (200,0,0))
                self.tela.blit(txt_nome, (rect_foco.x + 5, rect_foco.y + 10))
                self.tela.blit(txt_custo, (rect_foco.x + 5, rect_foco.y + 40))
            
            # esse daqui é quando o mouse tá em cima  
            txt_vida_foco = self.fonte_cartas.render(f"{carta_foco.vida}", True, (54, 32, 10))
            self.tela.blit(txt_vida_foco, (rect_foco.x + 112, rect_foco.y + 144))
            
        #Trajetoria de entrada
        for anim in self.animacoes:
            x_anim, y_anim = anim["pos_atual"]
            rect_render_anim = pygame.Rect(x_anim, y_anim, 140, 190)
            carta_anim = anim["carta"]
            
            if carta_anim.imagem is not None:
                self.tela.blit(carta_anim.imagem, rect_render_anim)
            else:
                # Se não tiver imagem, faz o quadrado branco padrão
                pygame.draw.rect(self.tela, (240, 240, 240), rect_render_anim)
                pygame.draw.rect(self.tela, (0, 0, 0), rect_render_anim, 6)
                txt_nome = self.fonte_cartas.render(carta_anim.nome, True, (0,0,0))
                self.tela.blit(txt_nome, (rect_render_anim.x + 5, rect_render_anim.y + 10))

        # --- BANNER DE AVISOS ---
        texto_surface = self.debug.render(self.mensagem_debug, True, (255, 255, 255))
        rect_texto = texto_surface.get_rect(center=(self.tela.get_width() // 2, 825))
        pygame.draw.rect(self.tela, (0, 0, 0), rect_texto.inflate(20, 10)) 
        self.tela.blit(texto_surface, rect_texto)



# SEÇÃO PRINCIPAL DE TESTE

if __name__ == "__main__":
    pygame.init()
    
    LARGURA, ALTURA = 1536, 864
    tela_teste = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Inscryption Engine - Sistema de Antecipação de Turnos")
    relogio = pygame.time.Clock()

    try:
        from fases import fases_do_jogo
        mock_dados_fase = fases_do_jogo["boss_1"]
    except ModuleNotFoundError:
        try:
            img_capelobo = pygame.image.load("assets/Capelobo.png").convert_alpha()
            img_la_ursa = pygame.image.load("assets/LaUrsa.png").convert_alpha()
            img_anhanga = pygame.image.load("assets/Anhanga.png").convert_alpha()
            img_cobra_coral = pygame.image.load("assets/cobra_coral.png").convert_alpha()
            img_leao = pygame.image.load("assets/leao.png").convert_alpha()
            img_timbu = pygame.image.load("assets/timbu.png").convert_alpha()
        except FileNotFoundError:
            img_capelobo = None
            img_la_ursa = None
            img_anhanga = None
            img_leao = None
            img_cobra_coral = None
            img_timbu = None
        print("fases.py não encontrado. Rodando em modo de segurança com dados locais.")
        mock_dados_fase = {
            "nome": "o lenhador brabo (Failsafe)",
            "obstaculos_iniciais": [{"slot": 2, "nome": "Tronco", "vida": 5, "dano": 0, "valor_sacrificio": 0}],
            "script_inimigo": {
                1: [{"acao": "jogar_carta", "carta": {"nome": "Capelobo", "vida": 3, "dano": 1, "imagem": img_capelobo}, "slot": 0}],
                2: [{"acao": "jogar_carta", "carta": {"nome": "timbu", "vida": 1, "dano": 1, "imagem": img_timbu}, "slot": 3}],
                4: [{"acao": "ataque_especial", "nome": "Puxão master das trevas", "dano_direto": 1}]
            }
        }
    try:

        img_capelobo = pygame.image.load("assets/Capelobo.png").convert_alpha()
        img_la_ursa = pygame.image.load("assets/LaUrsa.png").convert_alpha()
        img_anhanga = pygame.image.load("assets/Anhanga.png").convert_alpha()
        img_cobra_coral = pygame.image.load("assets/cobra_coral.png").convert_alpha()
        img_leao = pygame.image.load("assets/leao.png").convert_alpha()
        img_timbu = pygame.image.load("assets/timbu.png").convert_alpha()
    except FileNotFoundError:
        img_capelobo = None
        img_la_ursa = None
        img_anhanga = None
        img_leao = None
        img_cobra_coral = None
        img_timbu = None

    mock_deck_jogador = [
        Carta(nome="Capelobo", poder = 1, vida=3, imagem= img_capelobo, custo_sangue=1, valor_sacrificio=1),
        Carta(nome="La Ursa", poder=4, vida=6, imagem=img_la_ursa, custo_sangue=3, valor_sacrificio=1),
    ]
    

    cena_teste = CenaCombate(tela_teste, mock_deck_jogador, mock_dados_fase)
    
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