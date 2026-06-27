import pygame
from cena_base import CenaBase
from menu import Menu
from cartas import Carta
from cenas_tutorial.cena_introducao import CenaIntroducao
from cenas_tutorial.tutorial import CenaTutorial
from cenas_tutorial.mapa_tutorial import CenaMapa
from cenas_tutorial.combate_tutorial import CenaCombateTutorial

from cenas_caboclo.batalha import CenaCombate

# from cenas.fases import fases_do_jogo


from cenas_tutorial.comprar_cartas import CenaEscolhaCarta
from cenas_tutorial.creditos import CenaCreditos
from cenas_tutorial.inventario import CenaInventario
from cenas_tutorial.mochila_tutorial import CenaMochila
from cenas_tutorial.cena_opcoes import CenaOpcoes
from cenas_tutorial.cena_pause import CenaPause

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
    pygame.mixer.init()
    musica_pausada = False
    try:
        pygame.mixer.music.load("Musicas/Instrumental game.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"AVISO de áudio: não foi possível carregar a música: {e}")
    
    LARGURA, ALTURA = 1536, 864
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Ouro e Cachaça")

    nomes_cartas = ["acaua", "anhanga", "boitata", "caboclo", "capelobo", 
                    "chupa-cabra", "cobra_coral", "comadre", "cuca", 
                    "curupira", "la_ursa", "leao", "mula", "timbu","perna",
                    "cacto",] 
    imagens_cartas = {}

# mudança nome das cartas
    for nome in nomes_cartas:
        try:
            img_original = pygame.image.load(f"cartas/{nome}.png").convert_alpha()
            imagens_cartas[nome] = pygame.transform.scale(img_original, (144, 176))
        except FileNotFoundError:
            imagens_cartas[nome] = None

    
    nomes_versos = ["verso_carta", "verso_perna"] 
    imagens_versos = {}
    for nome in nomes_versos:
        try:
            img_original = pygame.image.load(f"verso/{nome}.png").convert_alpha()
            imagens_versos[nome] = pygame.transform.scale(img_original, (144, 176))
        except FileNotFoundError:
            imagens_versos[nome] = None

    # elementos de interface e cenário
    imagens_ui = {}
    
    # Carregando Copos, Campainha e o Fundo de Combate
    try:
        imagens_ui["copo1"] = pygame.transform.scale(pygame.image.load("assets/copo1.png").convert_alpha(), (80, 96))
        imagens_ui["copo2"] = pygame.transform.scale(pygame.image.load("assets/copo2.png").convert_alpha(), (80, 96))
        imagens_ui["campainha"] = pygame.transform.scale(pygame.image.load("assets/campainha.png").convert_alpha(), (120, 120))
        imagens_ui["combate"] = pygame.transform.scale(pygame.image.load("cenarios/combate.png").convert(), (LARGURA, ALTURA))
    except FileNotFoundError as e:
        print(f"AVISO de UI/Cenário: Arquivo de interface não encontrado! {e}")
        # Definindo fallbacks vazios para o jogo não quebrar caso falte algum
        imagens_ui.setdefault("copo1", None)
        imagens_ui.setdefault("copo2", None)
        imagens_ui.setdefault("campainha", None)
        imagens_ui.setdefault("fundo_combate", None)

    #  ---------------------------------------------- marcando aqui onde deixa de upar as imagens
    relogio = pygame.time.Clock()

    cena_atual = Menu(tela)

    vida_player_global = 2
    nivel_batalha_global = 1
    nodo_atual_global = 0

    #cartas iniciais (globais)
    deck_jogador_global = [
        Carta("Capelobo", 1, 2, imagens_cartas["capelobo"], 1, 1),
        Carta("Curupira", 2, 2, imagens_cartas["curupira"], 2, 1),
        Carta("Capelobo", 1, 2, imagens_cartas["capelobo"], 1, 1),
        Carta("Caboclo", 1, 1, imagens_cartas["caboclo"], 1, 1, selos=["mergulhador"]),
    ]

    itens_jogador_global = []

    rodando = True
    proxima = None
    while rodando:
        dt = relogio.tick(60)
        eventos = pygame.event.get()
        pausa_pedido = False

        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                if musica_pausada:
                    pygame.mixer.music.unpause()
                    musica_pausada = False
                else:
                    pygame.mixer.music.pause()
                    musica_pausada = True
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if not isinstance(cena_atual, (Menu, CenaPause)):
                    pausa_pedido = True

        if pausa_pedido:
            cena_atual = CenaPause(tela, cena_atual)
            eventos = []

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

        if isinstance(proxima, CenaBase):
            cena_atual = proxima
            proxima = None

        if proxima == "introducao":
            nova_cena = CenaIntroducao(tela)
            cena_atual = nova_cena
            efeito_transicao(tela, nova_cena)
            proxima = None
    
        if proxima == "cena_pergunta":
            cena_atual = CenaPerguntaTutorial(tela)
            cena_atual = nova_cena
            efeito_transicao(tela, nova_cena)
            proxima = None

        if proxima == "tutorial":
            nova_cena = CenaTutorial(tela, imagens_versos, imagens_cartas, imagens_ui)
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
            nova_cena = CenaEscolhaCarta(tela, imagens_versos, imagens_cartas, imagens_ui)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "mochila": 
            nova_cena = CenaMochila(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "creditos":
            nova_cena = CenaCreditos(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "opcoes":
            nova_cena = CenaOpcoes(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        if proxima == "pause":
            nova_cena = CenaPause(tela, cena_atual)
            cena_atual = nova_cena
            proxima = None

        if proxima == "menu":
            nova_cena = Menu(tela)
            efeito_transicao(tela, nova_cena)
            cena_atual = nova_cena
            proxima = None

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()