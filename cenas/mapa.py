import pygame
from cenas.cena_base import CenaBase

class CenaMapa(CenaBase):
    def __init__(self, tela, nodo_atual=0):
        super().__init__(tela)

        self.nodo_atual = nodo_atual

        try:
            img = pygame.image.load("assets/fundo_tutorial_mapa.png").convert_alpha()
            self.fundo = pygame.transform.scale(img, tela.get_size())
        except FileNotFoundError:
            self.fundo = pygame.Surface(tela.get_size())
            self.fundo.fill((50, 50, 50))

        self.nos_clicaveis = [
        {"id": 0, "rect": pygame.Rect(65, 400, 80, 80), "destino": "combate", "proximos": [1]},
        {"id": 1, "rect": pygame.Rect(250, 470, 80, 80), "destino": "comprar_cartas", "proximos": [2]},
        {"id": 2, "rect": pygame.Rect(390, 310, 80, 80), "destino": "mochila", "proximos": [3]},
        {"id": 3, "rect": pygame.Rect(535, 510, 80, 80), "destino": "combate", "proximos": [4]},
        {"id": 4, "rect": pygame.Rect(665, 355, 80, 80), "destino": "comprar_cartas", "proximos": [5]},
        {"id": 5, "rect": pygame.Rect(740, 510, 80, 80), "destino": "selos", "proximos": [6]},
        {"id": 6, "rect": pygame.Rect(895, 395, 80, 80), "destino": "combate", "proximos": [7,8]},
        {"id": 7, "rect": pygame.Rect(1040, 260, 80, 80), "destino": "selos", "proximos": [9]},
        {"id": 8, "rect": pygame.Rect(1040, 530, 80, 80), "destino": "fogueira", "proximos": [9]},
        {"id": 9, "rect": pygame.Rect(1190, 400, 80, 80), "destino": "combate", "proximos": []}]
                

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                opcoes_validas = self.nos_clicaveis[self.nodo_atual]["proximos"]
                
                for no in self.nos_clicaveis:
                    if no["rect"].collidepoint(pos_mouse):
                        if no["id"] in opcoes_validas:
                            self.nodo_atual = no["id"]
                            self.proxima_cena = no["destino"] 
                            self.terminou = True 
                            return

    def atualizar(self, dt):
            pass

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        opcoes_validas = self.nos_clicaveis[self.nodo_atual]["proximos"]
        for no in self.nos_clicaveis:
            cor = (0, 255, 0) if no["id"] in opcoes_validas else (255, 0, 0)
            pygame.draw.rect(self.tela, cor, no["rect"], 3)

            rect_atual = self.nos_clicaveis[self.nodo_atual]["rect"]
            ponto_x = rect_atual.centerx
            ponto_y = rect_atual.top - 10

            pygame.draw.polygon(self.tela, (255, 255, 0), [(ponto_x - 15, ponto_y - 20), (ponto_x + 15, ponto_y - 20),(ponto_x, ponto_y)])

if __name__ == "__main__":
    pygame.init()
    tela = pygame.display.set_mode((1536, 864)) 
    pygame.display.set_caption("Teste do Mapa")
    relogio = pygame.time.Clock()
    
    cena_teste = CenaMapa(tela, 0) 
    
    rodando = True
    while rodando:
        dt = relogio.tick(60)
        eventos = pygame.event.get()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        cena_teste.processar_eventos(eventos)
        cena_teste.atualizar(dt)
        cena_teste.desenhar()

        pygame.display.flip()

    pygame.quit()