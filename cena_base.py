class CenaBase:
    """
    Classe mãe para todas as telas do jogo.
    Nenhuma cena deve alterar a estrutura básica desses métodos.
    """
    def __init__(self, tela):
        self.tela = tela
        #Troca de tela sempre que essa variável mudar
        self.proxima_cena = self 

    def processar_eventos(self, eventos):
        """
        Recebe a lista de eventos do Pygame (cliques, teclas, etc).
        Toda cena filha vai ter que passar suas configurações exatamente aqui.
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