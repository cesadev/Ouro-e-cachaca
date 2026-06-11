import pygame
import math
import random
from cena_base import CenaBase

class CenaCombate(CenaBase):
    def __init__(self, tela, deck_jogador, dados_da_fase):
        super().__init__(tela) 
        
        self.deck_jogador = deck_jogador
        self.mao_jogador = [] 
        
        # --- DADOS DA FASE ---
        self.id_combate = dados_da_fase.get("nome", "Combate Desconhecido")
        self.script_inimigo = dados_da_fase.get("script_inimigo", {})
        
        # --- GERENCIADOR DE TURNOS E ESTADOS ---
        self.turno_atual = "jogador"
        self.turno_global = 1 
        self.ja_comprou_neste_turno = False 
        
        self.estado_atual = "fase_compra" 
        self.erros_fase_compra = 0 
        
        self.carta_selecionada = None
        self.index_carta_selecionada = None
        self.sangue_necessario = 0
        
        # --- TABULEIRO (4 SLOTS) ---
        self.slots_aliados = [None, None, None, None]
        self.slots_inimigos = [None, None, None, None]
        
        for obstaculo in dados_da_fase.get("obstaculos_iniciais", []):
            self.slots_inimigos[obstaculo["slot"]] = obstaculo.copy()
        
        # --- RECURSOS E A BALANÇA ---
        self.coelhos_disponiveis = 10 
        self.vida_player = 2 
        self.peso_balanca = 0 
        self.resultado = None
        
        # --- BAGUNÇA VISUAL DOS DECKS (CUMULATIVA E ROTACIONADA) ---
        def gerar_bagunca_cumulativa(quantidade):
            desvios = []
            x_atual, y_atual = 0.0, 0.0
            
            # Sorteia uma tendência de inclinação para a pilha inteira tombar organicamente
            tendencia_x = random.uniform(-0.6, 0.6) 
            tendencia_y = random.uniform(-0.2, 0.2)
            
            for _ in range(quantidade):
                # Deslocamento gradual + micro variações de inclinação angular
                x_atual += tendencia_x + random.uniform(-0.4, 0.4)
                y_atual += tendencia_y + random.uniform(-0.4, 0.4)
                angulo = random.uniform(-6.0, 6.0) 
                desvios.append((int(x_atual), int(y_atual), angulo))
                
            return desvios
        
        self.bagunca_coelhos = gerar_bagunca_cumulativa(15)
        self.bagunca_deck = gerar_bagunca_cumulativa(40)
        
        largura_tela, altura_tela = tela.get_size()
        
        try:
            imagem_original = pygame.image.load("assets/combate.png").convert()
            self.imagem_fundo = pygame.transform.scale(imagem_original, (largura_tela, altura_tela))
        except FileNotFoundError:
            self.imagem_fundo = pygame.Surface((largura_tela, altura_tela))
            self.imagem_fundo.fill((30, 30, 30))

        # --- HITBOXES FIXAS COM PROPORÇÕES UNIFICADAS ---
        self.campainha_rect = pygame.Rect(172, 50, 120, 120)
        
        # Pilhas de compra agora com a proporção exata de uma carta (140x190)
        self.comprar_coelho_rect = pygame.Rect(1190, 465, 140, 190)
        self.comprar_deck_rect = pygame.Rect(1350, 465, 140, 190)
        
        self.descricao_left_rect = pygame.Rect(1150, 130, 40, 40) 
        self.descricao_right_rect = pygame.Rect(1450, 130, 40, 40)

        self.hitboxes_mao = [] 
        self.hitboxes_slots_aliados = [] 
        self.hitboxes_slots_inimigos = []
        self.hitboxes_vida = [] 
        self.hitboxes_itens = []
        
        self.itens_jogador = [{"nome": "Abridor de Lata"}, {"nome": "Peixeira"}]

        self.mensagem_debug = "Início do Turno: Compre uma carta!"
        self.debug = pygame.font.SysFont("Arial", 36)
        self.fonte_cartas = pygame.font.SysFont("Arial", 20) 

        self.index_foco = None 

    def executar_ataques(self, atacantes, defensores, multiplicador_balanca):
        for i in range(4):
            atacante = atacantes[i]
            if atacante is not None and atacante.get("dano", 0) > 0:
                dano = atacante["dano"]
                defensor = defensores[i]
                
                if defensor is not None:
                    defensor["vida"] -= dano
                    print(f"{atacante['nome']} atacou {defensor['nome']}! Causou {dano} de dano.")
                    if defensor["vida"] <= 0:
                        print(f"{defensor['nome']} morreu!")
                        defensores[i] = None
                else:
                    self.peso_balanca += (dano * multiplicador_balanca)
                    print(f"{atacante['nome']} atacou diretamente! Balança agora é {self.peso_balanca}")
        
    def processar_eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.vida_player > 0:
                        self.vida_player -= 1
                        self.mensagem_debug = f"Perdeu um shot! Vidas globais: {self.vida_player}"
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos_mouse = pygame.mouse.get_pos()
                
                if event.button == 3: 
                    if self.estado_atual in ["sacrificio", "posicionamento"]:
                        self.estado_atual = "normal"
                        self.carta_selecionada = None
                        self.index_carta_selecionada = None
                        self.mensagem_debug = "Ação cancelada."
                        continue

                if event.button == 1: 
                    if self.turno_atual == "jogador":
                        comprou_agora = False
                        
                        if self.comprar_coelho_rect.collidepoint(pos_mouse):
                            if not self.ja_comprou_neste_turno:
                                if self.coelhos_disponiveis > 0:
                                    self.mao_jogador.append({"nome": "Coelho", "dano": 0, "vida": 1, "custo_sangue": 0, "valor_sacrificio": 1})
                                    self.coelhos_disponiveis -= 1
                                    self.ja_comprou_neste_turno = True
                                    comprou_agora = True
                                    self.mensagem_debug = f"Coelho na mão! ({self.coelhos_disponiveis} restam)"
                                else:
                                    self.mensagem_debug = "Sem coelhos!"
                            else:
                                self.mensagem_debug = "Você já comprou neste turno!"
                                
                        elif self.comprar_deck_rect.collidepoint(pos_mouse):
                            if not self.ja_comprou_neste_turno:
                                if len(self.deck_jogador) > 0:
                                    carta = self.deck_jogador.pop(0)
                                    self.mao_jogador.append(carta)
                                    self.ja_comprou_neste_turno = True
                                    comprou_agora = True
                                    self.mensagem_debug = f"Comprou: {carta['nome']}"
                                else:
                                    self.mensagem_debug = "O deck está vazio!"
                            else:
                                self.mensagem_debug = "Você já comprou neste turno!"
                        
                        if comprou_agora:
                            self.estado_atual = "normal"
                            self.erros_fase_compra = 0
                            continue 
                        
                        if self.estado_atual == "fase_compra":
                            clicou_valido = False
                            msg_erro = "Você precisa comprar uma carta no início do turno."
                            
                            if self.campainha_rect.collidepoint(pos_mouse):
                                msg_erro = "Tá querendo pular a tua vez assim? Compre uma carta antes de pular."
                                clicou_valido = True
                            else:
                                for rect_item, _ in self.hitboxes_itens:
                                    if rect_item.collidepoint(pos_mouse):
                                        msg_erro = "Compre uma carta antes de usar um item, essas são as regras."
                                        clicou_valido = True
                                        break
                                
                                if not clicou_valido:
                                    areas_bloqueadas = [r[0] for r in self.hitboxes_mao] + [r[0] for r in self.hitboxes_slots_aliados] + [self.descricao_left_rect, self.descricao_right_rect]
                                    for rect in areas_bloqueadas:
                                        if rect.collidepoint(pos_mouse):
                                            clicou_valido = True
                                            break
                            
                            if clicou_valido:
                                self.erros_fase_compra += 1
                                if 3 <= self.erros_fase_compra <= 5:
                                    self.mensagem_debug = "Deixe de ser teimoso, siga as regras."
                                elif self.erros_fase_compra >= 6:
                                    self.mensagem_debug = "Compre uma carta para continuar a jogar."
                                else:
                                    self.mensagem_debug = msg_erro
                        
                        else:
                            if self.campainha_rect.collidepoint(pos_mouse):
                                self.turno_atual = "resolvendo_combate"
                                self.estado_atual = "normal" 
                                self.mensagem_debug = "Batalha acontecendo..."
                                print("--- RESOLUÇÃO DO TURNO ---")
                                
                            elif self.descricao_left_rect.collidepoint(pos_mouse):
                                self.mensagem_debug = "Descrição ESQUERDA"
                                
                            elif self.descricao_right_rect.collidepoint(pos_mouse):
                                self.mensagem_debug = "Descrição DIREITA"

                            else:
                                clicou_item = False
                                for rect_item, item in self.hitboxes_itens:
                                    if rect_item.collidepoint(pos_mouse):
                                        self.mensagem_debug = f"Usou o item: {item['nome']}"
                                        clicou_item = True
                                        break
                                
                                if not clicou_item:
                                    if self.estado_atual == "normal":
                                        if self.index_foco is not None and self.index_foco < len(self.mao_jogador):
                                            carta_tentativa = self.mao_jogador[self.index_foco]
                                            custo = carta_tentativa.get("custo_sangue", 0)
                                            
                                            sangue_disponivel = sum(slot.get("valor_sacrificio", 1) for slot in self.slots_aliados if slot is not None)
                                            
                                            if custo > 0:
                                                if sangue_disponivel < custo:
                                                    self.mensagem_debug = "Nem tente invocar essa carta, rapaz. Não tem sangue suficiente."
                                                else:
                                                    self.index_carta_selecionada = self.index_foco
                                                    self.carta_selecionada = carta_tentativa
                                                    self.estado_atual = "sacrificio"
                                                    self.sangue_necessario = custo
                                                    self.mensagem_debug = f"SACRIFÍCIO: Pague {custo} sangue(s) no campo!"
                                            else:
                                                self.index_carta_selecionada = self.index_foco
                                                self.carta_selecionada = carta_tentativa
                                                self.estado_atual = "posicionamento"
                                                self.mensagem_debug = "POSICIONAMENTO: Escolha um slot aliado vazio."
                                    
                                    elif self.estado_atual == "sacrificio":
                                        for rect_slot, i in self.hitboxes_slots_aliados:
                                            if rect_slot.collidepoint(pos_mouse):
                                                if self.slots_aliados[i] is not None:
                                                    valor_fornecido = self.slots_aliados[i].get("valor_sacrificio", 1)
                                                    nome_morta = self.slots_aliados[i]['nome']
                                                    
                                                    self.slots_aliados[i] = None
                                                    self.sangue_necessario -= valor_fornecido
                                                    
                                                    if self.sangue_necessario <= 0:
                                                        self.estado_atual = "posicionamento"
                                                        self.mensagem_debug = f"{nome_morta} sacrificada! Escolha onde jogar."
                                                    else:
                                                        self.mensagem_debug = f"{nome_morta} sacrificada (-{valor_fornecido}). Faltam {self.sangue_necessario}!"
                                                else:
                                                    self.mensagem_debug = "Este slot já está vazio!"
                                                break
                                                
                                    elif self.estado_atual == "posicionamento":
                                        for rect_slot, i in self.hitboxes_slots_aliados:
                                            if rect_slot.collidepoint(pos_mouse):
                                                if self.slots_aliados[i] is None:
                                                    self.slots_aliados[i] = self.carta_selecionada.copy()
                                                    self.mao_jogador.pop(self.index_carta_selecionada)
                                                    self.mensagem_debug = f"{self.carta_selecionada['nome']} em campo!"
                                                    self.estado_atual = "normal"
                                                    self.carta_selecionada = None
                                                    self.index_carta_selecionada = None
                                                else:
                                                    self.mensagem_debug = "Slot ocupado! Escolha um vazio."
                                                break

    def atualizar(self, dt):
        if self.resultado is not None:
            return

        if self.turno_atual == "resolvendo_combate":
            self.executar_ataques(self.slots_aliados, self.slots_inimigos, multiplicador_balanca=1)
            
            if self.peso_balanca >= 8:
                self.resultado = "vitoria"
                self.mensagem_debug = "VENCEU! A balança chegou em +8."
                return
            
            acoes_do_turno = self.script_inimigo.get(self.turno_global, [])
            for comando in acoes_do_turno:
                if comando["acao"] == "jogar_carta":
                    slot = comando["slot"]
                    if self.slots_inimigos[slot] is None:
                        self.slots_inimigos[slot] = comando["carta"].copy()
                        print(f"Inimigo jogou {comando['carta']['nome']} no slot {slot}")
                elif comando["acao"] == "ataque_especial":
                    dano_direto = comando.get("dano_direto", 1)
                    self.peso_balanca -= dano_direto 
                    print(f"Inimigo usou ataque especial! -{dano_direto} na balança.")
            
            self.executar_ataques(self.slots_inimigos, self.slots_aliados, multiplicador_balanca=-1)
            
            if self.peso_balanca <= -8:
                self.vida_player -= 1
                self.resultado = "derrota"
                self.mensagem_debug = f"Balança quebrou! Você perdeu 1 shot."
                return

            self.turno_global += 1
            self.turno_atual = "jogador"
            self.ja_comprou_neste_turno = False 
            self.estado_atual = "fase_compra"
            self.erros_fase_compra = 0
            self.mensagem_debug = "Seu Turno! Compre 1 carta do Deck ou Coelho."

        # --- VIDA ---
        self.hitboxes_vida.clear()
        pos_x_vida, pos_y_vida, tamanho_vida, espacamento_vida = 145, 505, 80, 20
        for i in range(self.vida_player):
            rect = pygame.Rect(pos_x_vida + (i * (tamanho_vida + espacamento_vida)), pos_y_vida, tamanho_vida, tamanho_vida)
            self.hitboxes_vida.append(rect)

        # --- SLOTS (Padronizados para 140x190) ---
        self.hitboxes_slots_aliados.clear()
        self.hitboxes_slots_inimigos.clear()
        
        pos_x_slot = 458
        for i in range(4):
            rect_inimigo = pygame.Rect(pos_x_slot, 158, 140, 190)
            self.hitboxes_slots_inimigos.append((rect_inimigo, i))
            
            rect_aliado = pygame.Rect(pos_x_slot, 386, 140, 190)
            self.hitboxes_slots_aliados.append((rect_aliado, i))
            
            pos_x_slot += 158
            
        # --- ITENS ---
        self.hitboxes_itens.clear()
        pos_x_inicial_item = 1190
        pos_y_base_item = 330
        for item in self.itens_jogador[:2]:
            rect_item = pygame.Rect(pos_x_inicial_item, pos_y_base_item, 120, 120)
            self.hitboxes_itens.append((rect_item, item))
            pos_x_inicial_item += 140

        # --- MÃO DO JOGADOR (Padronizada para 140x190) ---
        self.hitboxes_mao.clear() 
        qtd_cartas = len(self.mao_jogador)
            
        if qtd_cartas > 0:
            largura_carta, altura_carta = 140, 190
            largura_tela, margem_tela = self.tela.get_width(), 400 
            
            espacamento = 0 if qtd_cartas == 1 else max(30, min(80, (largura_tela - margem_tela - largura_carta) // (qtd_cartas - 1)))
            largura_total_mao = (qtd_cartas - 1) * espacamento + largura_carta
            pos_x_inicial_mao = (largura_tela - largura_total_mao) // 2 
            
            pos_mouse = pygame.mouse.get_pos()
            self.index_foco = None
            
            rects_virtuais = []
            for i in range(qtd_cartas):
                rect = pygame.Rect(pos_x_inicial_mao + (i * espacamento), 650, largura_carta, altura_carta)
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

        # --- A BALANÇA VISUAL ---
        centro_x = 240
        centro_y = 350 
        raio = 128 

        angulo_graus = self.peso_balanca * 2.5 
        angulo_rad = math.radians(angulo_graus)

        dx = math.cos(angulo_rad) * raio
        dy = math.sin(angulo_rad) * raio

        esq_x = centro_x - dx
        esq_y = centro_y + dy  
        
        dir_x = centro_x + dx
        dir_y = centro_y - dy  

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
        
        # --- PREPARAÇÃO DE CORES DAS PILHAS ---
        piscar = self.estado_atual == "fase_compra" and (pygame.time.get_ticks() % 1000 < 500)
        cor_coelho_base = (200, 50, 50) if piscar else (255, 105, 97)
        cor_deck_base = (120, 150, 160) if piscar else (174, 198, 207)

        # --- FUNÇÃO DE SUPORTE PARA DESENHO COM ROTAÇÃO ---
        def desenhar_pilha(pos_rect, qtd_itens, lista_bagunca, cor_base, bloqueado):
            for i in range(qtd_itens):
                off_x, off_y, angulo = lista_bagunca[i % len(lista_bagunca)]
                
                # Superfície alfa para evitar bordas pretas esquisitas ao girar
                surf_carta = pygame.Surface((140, 190), pygame.SRCALPHA)
                cor = (100, 100, 100) if bloqueado else cor_base
                surf_carta.fill(cor)
                pygame.draw.rect(surf_carta, (0, 0, 0), (0, 0, 140, 190), 2)
                
                # Rotaciona a superfície inteira
                carta_rot = pygame.transform.rotate(surf_carta, angulo)
                
                # Mantém o pivô no centro exato para evitar desvios bruscos fora da bagunça
                rect_final = carta_rot.get_rect(center=pos_rect.center)
                rect_final.x += off_x
                rect_final.y += (off_y - (i * 2)) 
                
                self.tela.blit(carta_rot, rect_final)

        # Desenho das Pilhas Rotacionadas Organicamente
        if self.coelhos_disponiveis > 0:
            desenhar_pilha(self.comprar_coelho_rect, self.coelhos_disponiveis, self.bagunca_coelhos, cor_coelho_base, self.ja_comprou_neste_turno)
        else:
            pygame.draw.rect(self.tela, (50, 50, 50), self.comprar_coelho_rect)

        qtd_deck = len(self.deck_jogador)
        if qtd_deck > 0:
            desenhar_pilha(self.comprar_deck_rect, qtd_deck, self.bagunca_deck, cor_deck_base, self.ja_comprou_neste_turno)
        else:
            pygame.draw.rect(self.tela, (50, 50, 50), self.comprar_deck_rect) 

        # --- OUTROS ELEMENTOS ---
        pygame.draw.rect(self.tela, (75, 0, 130), self.descricao_left_rect)   
        pygame.draw.rect(self.tela, (200, 162, 200), self.descricao_right_rect) 
        
        for rect_vida in self.hitboxes_vida:
            pygame.draw.rect(self.tela, (255, 182, 193), rect_vida) 
            pygame.draw.rect(self.tela, (255, 255, 255), rect_vida, 3) 
            
        for rect_item, item in self.hitboxes_itens:
            pygame.draw.rect(self.tela, (46, 111, 64), rect_item)
            pygame.draw.rect(self.tela, (255, 255, 255), rect_item, 2) 
            
        for rect_slot, i in self.hitboxes_slots_inimigos:
            pygame.draw.rect(self.tela, (150, 50, 50), rect_slot, 2) 
            if self.slots_inimigos[i]:
                pygame.draw.rect(self.tela, (200, 100, 100), rect_slot.inflate(-10, -10))
                txt = self.fonte_cartas.render(self.slots_inimigos[i]['nome'], True, (255,255,255))
                self.tela.blit(txt, (rect_slot.x + 10, rect_slot.y + 20))
                txt_atk = self.fonte_cartas.render(f"ATK: {self.slots_inimigos[i].get('dano', 0)}", True, (255, 50, 50))
                self.tela.blit(txt_atk, (rect_slot.x + 10, rect_slot.y + 100))
                txt_vida = self.fonte_cartas.render(f"HP: {self.slots_inimigos[i]['vida']}", True, (0,0,0))
                self.tela.blit(txt_vida, (rect_slot.x + 10, rect_slot.y + 120))
                
        for rect_slot, i in self.hitboxes_slots_aliados:
            cor_borda = (50, 150, 50) 
            if self.estado_atual == "sacrificio" and self.slots_aliados[i] is not None:
                cor_borda = (255, 0, 0) 
            elif self.estado_atual == "posicionamento" and self.slots_aliados[i] is None:
                cor_borda = (0, 255, 0) 

            pygame.draw.rect(self.tela, cor_borda, rect_slot, 3 if cor_borda != (50,150,50) else 2) 
            
            if self.slots_aliados[i]:
                pygame.draw.rect(self.tela, (100, 200, 100), rect_slot.inflate(-10, -10))
                txt = self.fonte_cartas.render(self.slots_aliados[i]['nome'], True, (0,0,0))
                self.tela.blit(txt, (rect_slot.x + 10, rect_slot.y + 20))
                txt_atk = self.fonte_cartas.render(f"ATK: {self.slots_aliados[i].get('dano', 0)}", True, (200, 0, 0))
                self.tela.blit(txt_atk, (rect_slot.x + 10, rect_slot.y + 100))
                txt_vida = self.fonte_cartas.render(f"HP: {self.slots_aliados[i]['vida']}", True, (0,0,0))
                self.tela.blit(txt_vida, (rect_slot.x + 10, rect_slot.y + 120))
        
        for rect_carta, carta, i in self.hitboxes_mao:
            if i != self.index_foco:
                cor_fundo = (255, 255, 200) if (self.estado_atual != "normal" and self.estado_atual != "fase_compra" and i == self.index_carta_selecionada) else (255, 255, 255)
                
                pygame.draw.rect(self.tela, cor_fundo, rect_carta) 
                pygame.draw.rect(self.tela, (0, 0, 0), rect_carta, 3) 
                
                txt_nome = self.fonte_cartas.render(carta['nome'], True, (0,0,0))
                txt_custo = self.fonte_cartas.render(f"Custo: {carta.get('custo_sangue', 0)}", True, (200,0,0))
                self.tela.blit(txt_nome, (rect_carta.x + 5, rect_carta.y + 10))
                self.tela.blit(txt_custo, (rect_carta.x + 5, rect_carta.y + 40))
                
        if self.index_foco is not None and self.index_foco < len(self.hitboxes_mao):
            rect_foco, carta_foco, _ = self.hitboxes_mao[self.index_foco]
            pygame.draw.rect(self.tela, (255, 255, 220), rect_foco) 
            pygame.draw.rect(self.tela, (255, 50, 50), rect_foco, 4) 
            
            txt_nome = self.fonte_cartas.render(carta_foco['nome'], True, (0,0,0))
            txt_custo = self.fonte_cartas.render(f"Custo: {carta_foco.get('custo_sangue', 0)}", True, (200,0,0))
            self.tela.blit(txt_nome, (rect_foco.x + 5, rect_foco.y + 10))
            self.tela.blit(txt_custo, (rect_foco.x + 5, rect_foco.y + 40))
            
        texto_surface = self.debug.render(self.mensagem_debug, True, (255, 255, 255))
        rect_texto = texto_surface.get_rect(center=(self.tela.get_width() // 2, 800))
        pygame.draw.rect(self.tela, (0, 0, 0), rect_texto.inflate(20, 10)) 
        self.tela.blit(texto_surface, rect_texto)

if __name__ == "__main__":
    pygame.init()
    
    LARGURA, ALTURA = 1536, 864
    tela_teste = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Debug Isolado - Cena de Combate")
    relogio = pygame.time.Clock()

    mock_deck_jogador = [
        {"nome": "Lobo", "dano": 3, "vida": 2, "custo_sangue": 2, "valor_sacrificio": 2}, 
        {"nome": "Urso", "dano": 4, "vida": 6, "custo_sangue": 3, "valor_sacrificio": 1},
        {"nome": "Sapo", "dano": 1, "vida": 2, "custo_sangue": 1, "valor_sacrificio": 1},
        {"nome": "Corvo", "dano": 2, "vida": 1, "custo_sangue": 1, "valor_sacrificio": 1},
        {"nome": "Marta", "dano": 1, "vida": 1, "custo_sangue": 1, "valor_sacrificio": 1},
        {"nome": "Cobra", "dano": 3, "vida": 1, "custo_sangue": 2, "valor_sacrificio": 1}
    ] 
    
    mock_dados_fase = {
        "nome": "O Lenhador Furioso",
        "obstaculos_iniciais": [
            {"slot": 2, "nome": "Pedra", "vida": 5, "dano": 0, "valor_sacrificio": 0}
        ],
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "Sapo", "vida": 2, "dano": 2}, "slot": 0}],
            2: [], 
            3: [{"acao": "ataque_especial", "nome": "Vento Gelado", "dano_direto": 2}]
        }
    }

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