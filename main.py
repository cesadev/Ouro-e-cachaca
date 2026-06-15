import pygame

from cenas.cena_introducao import CenaIntroducao
from cenas.batalha import CenaCombate
from cenas.cena_base import CenaBase
from cenas.fases import fases_do_jogo
from cenas.batalha import Carta

def main():
    pygame.init()
    
    LARGURA, ALTURA = 1536, 864
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Meu Jogo - RPG")
    relogio = pygame.time.Clock()
    cena_atual = CenaIntroducao(tela)

    rodando = True
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

        if proxima == "mapa":
            print("Tutorial")
            deck_provisorio = [Carta("Capelobo", 1, 3, None, 1, 1)]
            cena_atual = CenaCombate(tela, deck_provisorio, fases_do_jogo["boss_1"])
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()