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
    y_botoes = tela.get_height() * 0.82
    #botões do menu principal

    tamanho_icone = (120, 120)

    def carregar_icone(nome_arquivo):
      try:
        return pygame.transform.scale(pygame.image.load(f"assets/{nome_arquivo}"), tamanho_icone)
      except FileNotFoundError:
        return None

    self.botoes = [
            {"texto": "INICIAR JOGO", "pos": (meio_x - 310, y_botoes), "icone": carregar_icone("botaojogar.png")},
            {"texto": "CONFIGURAÇÕES", "pos": (meio_x - 110, y_botoes), "icone": carregar_icone("botaoconfig.png")},
            {"texto": "EXTRA", "pos": (meio_x + 110, y_botoes), "icone": carregar_icone("botaocreditos.png")},
            {"texto": "SAIR", "pos": (meio_x + 310, y_botoes), "icone": carregar_icone("botaosair.png")}
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
            elif botao["texto"] == "CONFIGURAÇÕES":
              self.terminou = True
              self.proxima_cena = "opcoes"
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
        botao["rect"] = pygame.Rect(0, 0, tamanho_icone[0], tamanho_icone[1])
        botao["rect"].center = botao["pos"]
        texto = fonte(24).render(botao["texto"], True, (255, 255, 255))
        texto_rect = texto.get_rect(center=botao["pos"])
        self.tela.blit(texto, texto_rect)
