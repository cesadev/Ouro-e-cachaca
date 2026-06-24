import sys
sys.path.append("cenas")
import pygame
from cenas.menu import Menu

pygame.init()

TELA = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cartas e Cachaça")
clock = pygame.time.Clock()

cena_atual = Menu(TELA)

while True:
  dt = clock.tick(60) / 1000
  eventos = pygame.event.get()

  cena_atual.processar_eventos(eventos)
  cena_atual.atualizar(dt)
  cena_atual.desenhar()

  if cena_atual.proxima_cena != cena_atual:
    cena_atual = cena_atual.proxima_cena

  pygame.display.update()