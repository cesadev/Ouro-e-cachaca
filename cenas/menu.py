import pygame, sys
from cena_base import CenaBase

#define a fonte
def fonte(tamanho):
  return pygame.font.SysFont("arial", tamanho)

class Menu(CenaBase):
  def __init__(self, tela):
    super().__init__(tela)
    #botões do menu principal
    self.botoes = [
      {"texto": "INICIAR JOGO", "pos": (640, 280)},
      {"texto": "CONFIGURAÇÕES", "pos": (640, 380)},
      {"texto": "EXTRA", "pos": (640, 480)},
      {"texto": "SAIR", "pos": (640, 580)},
    ]

  def processar_eventos(self, eventos):
    posicaomouse = pygame.mouse.get_pos()
    for evento in eventos:
      #fecha o jogo se clicar x
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == pygame.MOUSEBUTTONDOWN:
        for botao in self.botoes:
          #verifica se o clique foi dentro do botão
          if botao["rect"].collidepoint(posicaomouse):
            if botao["texto"] == "SAIR":
              pygame.quit()
              sys.exit()

  def atualizar(self, dt):
    pass

  def desenhar(self):
    self.tela.fill("#1a1a2e")#cor de fundo azul
    posicaomouse = pygame.mouse.get_pos()

    #exibe o título
    titulo = fonte(80).render("CARTAS E CACHAÇA", True, "#f0c040")
    retangulotitulo = titulo.get_rect(center=(640, 120))
    self.tela.blit(titulo, retangulotitulo)

    for botao in self.botoes:
      fonteatual = fonte(55)
      #muda a cor ao passar o mouse por cima
      hover = botao["rect"].collidepoint(posicaomouse) if "rect" in botao else False
      cor = "#f0c040" if hover else "White"
      textobotao = fonteatual.render(botao["texto"], True, cor)
      botao["rect"] = textobotao.get_rect(center=botao["pos"])
      self.tela.blit(textobotao, botao["rect"])

if __name__ == "__main__":
  pygame.init()
  tela = pygame.display.set_mode((1280, 720))
  pygame.display.set_caption("Cartas e Cachaça")
  relogio = pygame.time.Clock()

  cena = Menu(tela)

  #loop do jogo
  while True:
    deltatempo = relogio.tick(60) / 1000
    eventos = pygame.event.get()
    cena.processar_eventos(eventos)
    cena.atualizar(deltatempo)
    cena.desenhar()
    pygame.display.update()