import pygame

class Carta:
    def __init__(self, nome, poder, vida, imagem=None, custo_sangue=0, valor_sacrificio=None, selos=None):
        self.nome = nome
        self.poder = poder
        self.dano = poder  
        self.vida = vida
        self.custo_sangue = custo_sangue
        self.valor_sacrificio = valor_sacrificio

        # Lista de selos que a carta tem (seja de fábrica ou adicionado depois)
        self.selos = selos.copy() if selos is not None else []
        
        self.imagem = imagem

        if self.imagem is not None:
            self.rect = self.imagem.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, 144, 176)

    # ==========================================
    # NOVO MÉTODO GENÉRICO PARA QUALQUER SELO
    # ==========================================
    def adicionar_novo_selo(self, nome_selo_logica, nome_arquivo_imagem):
        """
        Carimba QUALQUER selo novo diretamente na arte da carta e adiciona ele na lógica.
        """
        try:
            # Puxa o selo dinamicamente baseado no nome do arquivo que você mandar
            caminho = f"selos/{nome_arquivo_imagem}"
            img_temp = pygame.image.load(caminho).convert_alpha()
            img_selo = pygame.transform.scale(img_temp, (30, 30))
            
            if self.imagem is not None:
                # Copia a imagem só para essa carta
                self.imagem = self.imagem.copy()
                
                pos_selo_x = 8
                pos_selo_y = 25
                
                # O PULO DO GATO SUPREMO:
                # Ele multiplica o recuo pela quantidade de selos que a carta já tem!
                # 0 selos = pos_x fica 8
                # 1 selo  = pos_x vai para 43 (8 + 35)
                # 2 selos = pos_x vai para 78 (8 + 70)
                # Assim, todos os selos ficam perfeitamente lado a lado!
                pos_selo_x += 35 * len(self.selos)
                
                # Funde (Blit) o selo na imagem da carta!
                self.imagem.blit(img_selo, (pos_selo_x, pos_selo_y))
            
            # Adiciona na lista para o jogo saber que agora a carta tem esse poder
            self.selos.append(nome_selo_logica)
            
        except FileNotFoundError:
            print(f"AVISO: Imagem '{nome_arquivo_imagem}' não encontrada na pasta selos!")

    def desenhar(self, tela, posicao_x, posicao_y):
        self.rect.topleft = (posicao_x, posicao_y)
        
        if self.imagem is not None:
            tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(tela, (255, 255, 255), self.rect) 
            pygame.draw.rect(tela, (0, 0, 0), self.rect, 3)
        
    def copy(self):
        """Retorna uma cópia real da instância da carta"""
        # Como o método adicionar_novo_selo já altera a imagem (self.imagem) 
        # e a lista de selos (self.selos), a cópia vai herdar as tatuagens naturalmente!
        return Carta(
            self.nome, self.poder, self.vida, self.imagem, 
            self.custo_sangue, self.valor_sacrificio, self.selos
        )