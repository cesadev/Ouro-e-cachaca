import pygame, sys
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
    y_botoes = tela.get_height() * 0.75
    #botões do menu principal

    tamanho_icone = (150, 150)
    self.botoes = [
            {"texto": "INICIAR JOGO", "pos": (meio_x - 420, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaoiniciar.png"), tamanho_icone)},
            {"texto": "CONFIGURAÇÕES", "pos": (meio_x - 140, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaoconfig.png"), tamanho_icone)},
            {"texto": "EXTRA", "pos": (meio_x + 140, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaoextras.png"), tamanho_icone)},
            {"texto": "SAIR", "pos": (meio_x + 420, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaosair.png"), tamanho_icone)},
        ]

    for botao in self.botoes:
      botao["rect"] = pygame.Rect(0, 0, tamanho_icone[0], tamanho_icone[1])
      botao["rect"].center = botao["pos"]

    try:
      imagem_tela = pygame.image.load("cenarios/telaprincipal.png").convert()
      self.fundo = pygame.transform.scale(imagem_tela, tela.get_size())
    except FileNotFoundError:
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
            elif botao["texto"] == "EXTRA":
              self.terminou = True
              self.proxima_cena = "creditos"

  def atualizar(self, dt):
    pass

  def desenhar(self):
    if self.fundo:
      self.tela.blit(self.fundo, (0, 0))
    else:
      self.tela.fill("#1a1a2e") #cor de fundo azul

    posicaomouse = pygame.mouse.get_pos()

    #desenha os ícones dos botões
    for botao in self.botoes:
      iconeretangulo = botao["icone"].get_rect(center=botao["pos"])
      hover = iconeretangulo.collidepoint(posicaomouse)
      
      #aumenta o ícone se o mouse estiver em cima
      if hover:
        icone = pygame.transform.scale(botao["icone"], (180, 180))
      else:
        icone = botao["icone"]
      iconeretangulo = icone.get_rect(center=botao["pos"])
      self.tela.blit(icone, iconeretangulo)
      botao["rect"] = iconeretangulo
