import pygame
try:            
    img_capelobo = pygame.image.load("assets/Capelobo.png").convert_alpha()
    img_la_ursa = pygame.image.load("assets/LaUrsa.png").convert_alpha()
    img_anhanga = pygame.image.load("assets/Anhanga.png").convert_alpha()
    img_cobra_coral = pygame.image.load("assets/cobra_coral.png").convert_alpha()
    img_leao = pygame.image.load("assets/leao.png").convert_alpha()
    img_timbu = pygame.image.load("assets/timbu.png").convert_alpha()
except FileNotFoundError:
    img_capelobo = None
    img_la_ursa = None
    img_anhanga = None
    img_leao = None
    img_cobra_coral = None
    img_timbu = None

fases_do_jogo = {
    "boss_1": {
        "nome": "o lenhador brabo",
        "obstaculos_iniciais": [
           #lembrando que o jogo terá 4 slots e eles serão de 0 a 3, aqui ta no slot 2 ou seja será no terceiro campo
            {"slot": 2, "nome": "Tronco", "vida": 5, "dano": 0, "valor_sacrificio": 0}
        ],
        "script_inimigo": {
            1: [
                {"acao": "jogar_carta", "carta": {"nome": "Capelobo", "vida": 3, "dano": 1, "imagem": img_capelobo}, "slot": 0}
            ],
            2: [
                {"acao": "jogar_carta", "carta": {"nome": "Timbu", "vida": 2, "dano": 2, "imagem": img_timbu}, "slot": 3}
            ],
            3: [], #aqui é o turno 3, um exemplo em que o chefe nao faz nada além de te encarar
            4: [
                #aqui será um exemplo de ataque especial do chefe no turno 4
                {"acao": "ataque_especial", "nome": "Puxão master das trevas", "dano_direto": 1}
            ]
        }
    }
}