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

    #carrega o fundo uma vez só
    self.fundo = pygame.transform.scale(pygame.image.load("cenarios/telaprincipal.png"), (tela.get_width(), tela.get_height()))

    #botões do menu principal
    self.botoes = [
      {"texto": "INICIAR JOGO", "pos": (meio_x - 220, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaoiniciar.png"), (100, 100))},
      {"texto": "CONFIGURAÇÕES", "pos": (meio_x - 70, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaoconfig.png"), (100, 100))},
      {"texto": "EXTRA", "pos": (meio_x + 70, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaoextras.png"), (100, 100))},
      {"texto": "SAIR", "pos": (meio_x + 220, y_botoes), "icone": pygame.transform.scale(pygame.image.load("assets/botaosair.png"), (100, 100))},
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
            if botao["texto"] == "INICIAR JOGO":
              self.terminou = True
              self.proxima_cena = "introducao"
            if botao["texto"] == "CONFIGURAÇÕES":
              self.terminou = True
              self.proxima_cena = "opcoes"
            if botao["texto"] == "EXTRA":
              self.terminou = True
              self.proxima_cena = "extra"

  def atualizar(self, dt):
    pass

  def desenhar(self):
    #desenha o fundo
    self.tela.blit(self.fundo, (0, 0))
    posicaomouse = pygame.mouse.get_pos()

    #desenha os ícones dos botões
    for botao in self.botoes:
      iconeretangulo = botao["icone"].get_rect(center=botao["pos"])
      hover = iconeretangulo.collidepoint(posicaomouse)

      #aumenta o ícone se o mouse estiver em cima
      if hover:
        icone = pygame.transform.scale(botao["icone"], (130, 130))
      else:
        icone = botao["icone"]
      iconeretangulo = icone.get_rect(center=botao["pos"])
      self.tela.blit(icone, iconeretangulo)
      botao["rect"] = iconeretangulo
      
      #desenha o texto do botão quando o mouse estiver em cima
      if hover:
        texto_surf = fonte(24).render(botao["texto"], True, (255, 215, 0))
        texto_rect = texto_surf.get_rect(center=(botao["pos"][0], botao["pos"][1] - 80))
        self.tela.blit(texto_surf, texto_rect)

if __name__ == "__main__":
  pygame.init()
  tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  pygame.display.set_caption("Ouro e Cachaça")
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