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
      {"texto": "INICIAR JOGO", "pos": (200, 525), "icone": pygame.transform.scale(pygame.image.load("assets/botaoiniciar.png"), (150, 150))},
      {"texto": "CONFIGURAÇÕES", "pos": (480, 525), "icone": pygame.transform.scale(pygame.image.load("assets/botaoconfig.png"), (150, 150))},
      {"texto": "EXTRA", "pos": (760, 525), "icone": pygame.transform.scale(pygame.image.load("assets/botaoextras.png"), (150, 150))},
      {"texto": "SAIR", "pos": (1040, 525), "icone": pygame.transform.scale(pygame.image.load("assets/botaosair.png"), (150, 150))},
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
    self.tela.fill("#1a1a2e") #cor de fundo azul
    posicaomouse = pygame.mouse.get_pos()

    #exibe o título
    titulo = fonte(80).render("OURO E CACHAÇA", True, "#f0c040")
    retangulotitulo = titulo.get_rect(center=(640, 120))
    self.tela.blit(titulo, retangulotitulo)

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