import pygame

from cenas.cena_introducao import CenaIntroducao
from cenas.batalha import CenaCombate
from cenas.cena_base import CenaBase
from cenas.fases import fases_do_jogo
from cenas.batalha import Carta
from cenas.menu import Menu
from cenas.tutorial import CenaTutorial

def efeito_transicao(tela, cena_nova):
    largura, altura = tela.get_size()
    superficie_fade = pygame.Surface((largura, altura))
    superficie_fade.fill((0, 0, 0))
    relogio = pygame.time.Clock()

    for alfa in range(0, 255, 10):
        superficie_fade.set_alpha(alfa)
        tela.blit(superficie_fade, (0, 0))
        pygame.display.update()
        relogio.tick(60)

    for alfa in range(255, 0, -10):
        cena_nova.desenhar()
        superficie_fade.set_alpha(alfa)
        tela.blit(superficie_fade, (0, 0))
        pygame.display.update()
        relogio.tick(60)    
def main():
    pygame.init()
    
    LARGURA, ALTURA = 1536, 864
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Meu Jogo - RPG")
    relogio = pygame.time.Clock()

    cena_atual = Menu(tela)

    rodando = True
    proxima = None
    while rodando:
        dt = relogio.tick(60)
        eventos = pygame.event.get()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        cena_atual.processar_eventos(eventos)
        cena_atual.atualizar(dt)
        cena_atual.desenhar()

        if hasattr(cena_atual, 'terminou') and cena_atual.terminou:
            proxima = cena_atual.proxima_cena
            cena_atual.terminou = False

        if proxima == "introducao":
                nova_cena = CenaIntroducao(tela)
                cena_atual = nova_cena
                efeito_transicao(tela, nova_cena)
                proxima = None
        
        if proxima == "tutorial":
            print("Tutorial")
            nova_cena = CenaTutorial(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()