import pygame

from cenas.cena_introducao import CenaIntroducao
from cenas.batalha import CenaCombate
from cenas.cena_base import CenaBase
from cenas.fases import fases_do_jogo
from cenas.batalha import Carta
from cenas.menu import Menu
from cenas.tutorial import CenaTutorial
from cenas.mapa import CenaMapa
from cenas.comprar_cartas import CenaEscolhaCarta
from cenas.inventario import CenaInventario
from cenas.mochila import CenaMochila

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
    pygame.display.set_caption("Ouro e Cachaça")
    relogio = pygame.time.Clock()

    cena_atual = Menu(tela)

    vida_player_global = 2
    nivel_batalha_global = 1
    nodo_atual_global = 0
    
    try:
        img_capelobo = pygame.image.load("assets/Capelobo.png").convert_alpha()
    except FileNotFoundError:
        img_capelobo = None
        print("AVISO: Imagem do Capelobo não encontrada! Verifica o nome na pasta assets.")

    try:
        img_curupira = pygame.image.load("assets/curupira.png").convert_alpha()
    except FileNotFoundError:
        img_curupira = None
        print("AVISO: Imagem do Curupira não encontrada! Verifica o nome na pasta assets.")

    try:
        img_caboclo = pygame.image.load("assets/caboclo.png").convert_alpha()
    except FileNotFoundError:
        img_caboclo = None
        print("AVISO: Imagem do Caboclo não encontrada! Verifica o nome na pasta assets.")

    #cartas iniciais (globais)
    deck_jogador_global = [
        Carta("Capelobo", 1, 3, img_capelobo, 1, 1),
        Carta("Curupira", 2, 2, img_curupira, 2, 1),
        Carta("Capelobo", 1, 3, img_capelobo, 1, 1),
        Carta("Caboclo", 1, 1, img_caboclo, 1, 1),
        Carta("Caboclo", 1, 1, img_caboclo, 1, 1)
    ]

    itens_jogador_global = []

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
            if isinstance(cena_atual, CenaCombate):
                vida_player_global = cena_atual.vida_player
                if cena_atual.resultado == "vitoria":
                    nivel_batalha_global += 1

            # aqui é onde salva a posição do mapa
            if isinstance(cena_atual, CenaMapa):
                if hasattr(cena_atual, 'nodo_atual'):
                    nodo_atual_global = cena_atual.nodo_atual

            if hasattr(cena_atual, 'carta_escolhida') and cena_atual.carta_escolhida is not None:
                deck_jogador_global.append(cena_atual.carta_escolhida)
                print(f"Carta adicionada ao baralho: {cena_atual.carta_escolhida.nome}")
                cena_atual.carta_escolhida = None

            if hasattr(cena_atual, 'itens_adquiridos') and cena_atual.itens_adquiridos:
                itens_jogador_global.extend(cena_atual.itens_adquiridos) 
                for item in cena_atual.itens_adquiridos:
                    print(f"Item adicionado na mochila: {item.nome}")
                cena_atual.itens_adquiridos = []

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
        
        if proxima == "mapa":
            nova_cena = CenaMapa(tela, nodo_atual_global) 
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "inventario":
            nova_cena = CenaInventario(tela, deck_jogador_global)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "comprar_cartas": 
            nova_cena = CenaEscolhaCarta(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "mochila": 
            nova_cena = CenaMochila(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "combate":
            # montagem dinamica do boss
            nome_fase = f"boss_{nivel_batalha_global}"
            
            if nome_fase in fases_do_jogo:
                dados_da_fase = fases_do_jogo[nome_fase]
            
            # tela de zerar o jogo, dps adiciono aqui embaixo a tela de zerar, por enquanto ele vai ficar no loop de, caso terminou as batalhas, vai pra fase1.
            else:
                dados_da_fase = fases_do_jogo["boss_1"] 

            nova_cena = CenaCombate(tela, deck_jogador_global, dados_da_fase, vida_player_global)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None
        
        if proxima == "game_over":
            
            # a tela de perder as duas vidas
            # nova_cena = CenaGameOver(tela) 
            # efeito_transicao(tela, nova_cena)
            # cena_atual = nova_cena
            proxima = None
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()