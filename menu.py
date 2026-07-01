import pygame, sys
import cv2
import numpy as np
from cena_base import CenaBase

#define a fonte
def fonte(tamanho):
  return pygame.font.SysFont("arial", tamanho)

class Menu(CenaBase):
  def __init__(self, tela):
    super().__init__(tela)
    self.terminou = False
    self.proxima_cena = None

    meio_x = tela.get_width() // 2
    y_botoes = tela.get_height() * 0.82
    #botões do menu principal

    self.tamanho_icone = (120, 120)

    def carregar_icone(nome_arquivo):
      try:
        return pygame.transform.scale(pygame.image.load(f"assets/{nome_arquivo}"), self.tamanho_icone)
      except FileNotFoundError:
        return None

    self.botoes = [
            {"texto": "INICIAR JOGO", "pos": (meio_x - 310, y_botoes), "icone": carregar_icone("botaojogar.png")},
            {"texto": "CONFIGURAÇÕES", "pos": (meio_x - 110, y_botoes), "icone": carregar_icone("botaoconfig.png")},
            {"texto": "EXTRA", "pos": (meio_x + 110, y_botoes), "icone": carregar_icone("botaocreditos.png")},
            {"texto": "SAIR", "pos": (meio_x + 310, y_botoes), "icone": carregar_icone("botaosair.png")}
        ]

    for botao in self.botoes:
      botao["rect"] = pygame.Rect(0, 0, self.tamanho_icone[0], self.tamanho_icone[1])
      botao["rect"].center = botao["pos"]

    # Tenta carregar o vídeo como fundo
    self.video = None
    self.frame_atual = None
    self.fundo = None
    self.velocidade_video = 1.0  # 1.0 = velocidade normal
    self.frame_counter = 0
    
    try:
      self.video = cv2.VideoCapture("cenarios/video tela inicial (corrigido).mp4")
      if self.video.isOpened():
        self.fps_video = self.video.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"✓ Vídeo carregado com sucesso!")
        print(f"  FPS: {self.fps_video:.1f}")
        print(f"  Frames totais: {total_frames}")
        print(f"  Velocidade: {self.velocidade_video}x (normal=1.0)")
      else:
        raise Exception("Não conseguiu abrir o vídeo")
    except Exception as e:
      print(f"⚠ Não foi possível carregar vídeo: {e}")
      print("  Usando imagem estática como fallback...")
      self.video = None
      
      # Fallback para imagem
      try:
        imagem_tela = pygame.image.load("cenarios/telaprincipal.png").convert()
        self.fundo = pygame.transform.scale(imagem_tela, tela.get_size())
        print("✓ Imagem estática carregada com sucesso!")
      except FileNotFoundError:
        print("✗ Nenhuma imagem de fundo encontrada!")
        self.fundo = None

  def processar_eventos(self, eventos):
    posicaomouse = pygame.mouse.get_pos()
    for evento in eventos:
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        for botao in self.botoes:
          if botao["rect"].collidepoint(posicaomouse):
            if botao["texto"] == "SAIR":
              pygame.quit()
              sys.exit()
            elif botao["texto"] == "INICIAR JOGO":
              self.terminou = True
              self.proxima_cena = "introducao"
            elif botao["texto"] == "CONFIGURAÇÕES":
              self.terminou = True
              self.proxima_cena = "opcoes"
            elif botao["texto"] == "EXTRA":
              self.terminou = True
              self.proxima_cena = "creditos"

  def atualizar(self, dt):
    # Atualiza o frame do vídeo sincronizado com tempo real
    if self.video and self.video.isOpened():
      # Incrementa contador de frames
      self.frame_counter += 1
      
      # Calcula quantas atualizações cada frame de vídeo deve ser mostrado
      fps_game = 60
      atualizacoes_por_frame_video = fps_game / (self.fps_video * self.velocidade_video)
      
      # Só lê novo frame quando atingir o número correto de atualizações
      if self.frame_counter >= atualizacoes_por_frame_video:
        ret, frame = self.video.read()
        
        if ret:
          # Converte BGR para RGB
          frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          
          # Redimensiona diretamente para a resolução da tela com interpolação de alta qualidade
          frame_resized = cv2.resize(frame_rgb, (self.tela.get_width(), self.tela.get_height()), interpolation=cv2.INTER_LANCZOS4)
          
          # Converte para surface do Pygame
          frame_surface = pygame.image.fromstring(
            frame_resized.tobytes(),
            (self.tela.get_width(), self.tela.get_height()),
            "RGB"
          )
          
          self.frame_atual = frame_surface
        else:
          # Reinicia o vídeo quando chega ao fim (loop)
          self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Reseta contador
        self.frame_counter = 0

  def desenhar(self):
    # Desenha o vídeo ou a imagem de fundo
    if self.frame_atual:
      self.tela.blit(self.frame_atual, (0, 0))
    elif self.fundo:
      self.tela.blit(self.fundo, (0, 0))
    else:
      self.tela.fill("#1a1a2e") #cor de fundo azul

    posicaomouse = pygame.mouse.get_pos()

    #desenha os ícones dos botões
    for botao in self.botoes:
      if botao["icone"] is not None:
        iconeretangulo = botao["icone"].get_rect(center=botao["pos"])
        hover = iconeretangulo.collidepoint(posicaomouse)

        #aumenta o ícone se o mouse estiver em cima
        if hover:
          icone = pygame.transform.scale(botao["icone"], (150, 150))
        else:
          icone = botao["icone"]
        iconeretangulo = icone.get_rect(center=botao["pos"])
        self.tela.blit(icone, iconeretangulo)
        botao["rect"] = iconeretangulo

        if hover:
          label = fonte(22).render(botao["texto"], True, (255, 255, 255))
          label_rect = label.get_rect(midtop=(botao["pos"][0], iconeretangulo.bottom + 8))
          self.tela.blit(label, label_rect)
      else:
        botao["rect"] = pygame.Rect(0, 0, self.tamanho_icone[0], self.tamanho_icone[1])
        botao["rect"].center = botao["pos"]
        texto = fonte(24).render(botao["texto"], True, (255, 255, 255))
        texto_rect = texto.get_rect(center=botao["pos"])
        self.tela.blit(texto, texto_rect)
