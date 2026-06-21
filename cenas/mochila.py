import pygame
import random
import math
from cenas.cena_base import CenaBase

class Item:
    def __init__(self, nome, caminho_asset):
        self.nome = nome
        # Carregamos a imagem original para não perder qualidade ao dar scale
        try:
            self.img_original = pygame.image.load(caminho_asset).convert_alpha()
        except FileNotFoundError:
            # Placeholder caso a imagem não exista ainda
            self.img_original = pygame.Surface((100, 100))
            self.img_original.fill((0, 255, 0))

class CenaMochila(CenaBase):
    def __init__(self, tela):
        super().__init__(tela)
        self.tela = tela
        
        # Imagem de fundo
        try:
            img = pygame.image.load("assets/fundo_draft.png").convert()
            self.fundo = pygame.transform.scale(img, tela.get_size())
        except FileNotFoundError:
            self.fundo = pygame.Surface(tela.get_size())
            self.fundo.fill((30, 30, 40))
            
        self.fonte_dialogo = pygame.font.SysFont("Arial", 30)

        # Configurando os itens
        todos_itens = [
            Item("Peixeira", "assets/peixeira.png"),
            Item("Cantil", "assets/cantil.png"),
            Item("Abridor de Cerveja", "assets/cerveja.png")
        ]
        # Embaralha os 3 itens para virem em ordem aleatória
        self.itens_sorteados = random.sample(todos_itens, 3)
        self.itens_adquiridos = [] # O que vai ser passado pro jogador dps
        
        # Controle de fluxo da animação
        self.index_item_atual = 0
        # Estados: "descendo", "aguardando_clique", "indo_pro_canto", "finalizado"
        self.estado_animacao = "descendo" 
        
        largura, altura = self.tela.get_size()
        self.pos_centro = (largura // 2, altura // 2)
        self.y_inicial = -200
        
        # Posições finais para os 3 itens (lado a lado, um pouco pra direita)
        # Ajuste o X e o Y aqui conforme achar melhor no visual
        self.posicoes_finais = [
            (largura // 2 + 50, altura // 2),
            (largura // 2 + 150, altura // 2),
            (largura // 2 + 250, altura // 2)
        ]
        
        # Posição dinâmica do item atual sendo animado
        self.x_atual = self.pos_centro[0]
        self.y_atual = self.y_inicial
        
        self.progresso_movimento = 0.0
        self.tempo_animacao = 0.0 # Usado para o efeito contínuo (pulsar)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                
                # Clicou enquanto o item estava no meio da tela pulsando
                if self.estado_animacao == "aguardando_clique":
                    self.estado_animacao = "indo_pro_canto"
                    self.progresso_movimento = 0.0
                    
                # Clicou depois que os 3 itens já foram pra mochila
                elif self.estado_animacao == "finalizado":
                    self.itens_adquiridos = self.itens_sorteados
                    self.terminou = True
                    self.proxima_cena = "mapa"

    def atualizar(self, dt):
        self.tempo_animacao += dt * 0.005 # Velocidade do pulsar
        
        if self.index_item_atual < 3:
            if self.estado_animacao == "descendo":
                self.progresso_movimento += dt * 0.002
                if self.progresso_movimento >= 1.0:
                    self.progresso_movimento = 1.0
                    self.estado_animacao = "aguardando_clique"
                
                # Interpolação suave (Lerp) para a descida
                t = self.progresso_movimento
                fator_suave = 1 - pow(1 - t, 3)
                self.y_atual = self.y_inicial + (self.pos_centro[1] - self.y_inicial) * fator_suave
                self.x_atual = self.pos_centro[0]

            elif self.estado_animacao == "indo_pro_canto":
                self.progresso_movimento += dt * 0.003
                if self.progresso_movimento >= 1.0:
                    self.progresso_movimento = 1.0
                    # Prepara o próximo item
                    self.index_item_atual += 1
                    self.progresso_movimento = 0.0
                    
                    if self.index_item_atual >= 3:
                        self.estado_animacao = "finalizado"
                    else:
                        self.estado_animacao = "descendo"
                        self.y_atual = self.y_inicial
                        self.x_atual = self.pos_centro[0]
                else:
                    # Move do centro para a posição final na direita
                    t = self.progresso_movimento
                    fator_suave = 1 - pow(1 - t, 3)
                    pos_destino = self.posicoes_finais[self.index_item_atual]
                    
                    self.x_atual = self.pos_centro[0] + (pos_destino[0] - self.pos_centro[0]) * fator_suave
                    self.y_atual = self.pos_centro[1] + (pos_destino[1] - self.pos_centro[1]) * fator_suave

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        
        # 1. Desenha os itens que já foram pro canto e estão "guardados"
        for i in range(self.index_item_atual):
            item = self.itens_sorteados[i]
            img = pygame.transform.scale(item.img_original, (80, 80)) # Tamanho menor no canto
            pos = self.posicoes_finais[i]
            rect = img.get_rect(center=pos)
            self.tela.blit(img, rect)
            
        # 2. Desenha o item atual sendo animado (se ainda houver)
        if self.index_item_atual < 3:
            item_atual = self.itens_sorteados[self.index_item_atual]
            
            # Lógica para escalar a imagem
            tamanho_base = 150
            if self.estado_animacao == "aguardando_clique":
                # Efeito contínuo pulsando com seno
                escala = tamanho_base + math.sin(self.tempo_animacao) * 20
            elif self.estado_animacao == "indo_pro_canto":
                # Diminui de tamanho indo pro canto (de 150 para 80)
                escala = tamanho_base - (tamanho_base - 80) * self.progresso_movimento
            else:
                # Descendo com tamanho normal
                escala = tamanho_base
                
            escala = int(escala)
            img_animada = pygame.transform.scale(item_atual.img_original, (escala, escala))
            # O center é essencial para a imagem não tremer na hora do resize
            rect_animado = img_animada.get_rect(center=(int(self.x_atual), int(self.y_atual))) 
            
            self.tela.blit(img_animada, rect_animado)

        # 3. Caixa de diálogo (opcional, para guiar o jogador)
        dialogo = ""
        if self.estado_animacao in ["descendo", "aguardando_clique"]:
            dialogo = "Você encontrou um item! Clique para guardar."
        elif self.estado_animacao == "finalizado":
            dialogo = "Mochila cheia! Clique para voltar."
            
        if dialogo:
            largura, altura = self.tela.get_size()
            rect_caixa = pygame.Rect(100, altura - 180, largura - 200, 150)
            pygame.draw.rect(self.tela, (10, 10, 10), rect_caixa)
            pygame.draw.rect(self.tela, (200, 200, 200), rect_caixa, 4)
            
            img_texto = self.fonte_dialogo.render(dialogo, True, (255, 255, 255))
            self.tela.blit(img_texto, (rect_caixa.x + 30, rect_caixa.y + 50))