class CenaBase:
    """
    Classe mãe para todas as telas do jogo.
    Nenhuma cena deve alterar a estrutura básica desses métodos.
    """
    def __init__(self, tela):
        self.tela = tela
        # Quando essa variável mudar, o jogo sabe que tem que trocar de tela
        self.proxima_cena = self 

    def processar_eventos(self, eventos):
        """
        Recebe a lista de eventos do Pygame (cliques, teclas).
        Cada cena filha vai definir o que fazer com os cliques aqui.
        """
        pass

    def atualizar(self, dt):
        """
        Atualiza a lógica da tela (movimentação, IA, turnos).
        'dt' é o delta time (tempo desde o último frame), bom para animações fluidas.
        """
        pass

    def desenhar(self):
        """
        Renderiza tudo na tela.
        """
        pass

    def mudar_cena(self, nova_cena):
        """
        Função auxiliar para trocar de tela.
        """
        self.proxima_cena = nova_cena