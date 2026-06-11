fases_do_jogo = {
    "boss_1": {
        "nome": "o lenhador brabo",
        "obstaculos_iniciais": [
           #lembrando que o jogo terá 4 slots e eles serão de 0 a 3, aqui ta no slot 2 ou seja será no terceiro campo
            {"slot": 2, "nome": "Tronco", "vida": 5, "dano": 0, "valor_sacrificio": 0}
        ],
        "script_inimigo": {
            1: [
                {"acao": "jogar_carta", "carta": {"nome": "Lobo", "vida": 2, "dano": 2}, "slot": 0}
            ],
            2: [
                {"acao": "jogar_carta", "carta": {"nome": "Corvo", "vida": 1, "dano": 1}, "slot": 3}
            ],
            3: [], #aqui é o turno 3, um exemplo em que o chefe nao faz nada além de te encarar
            4: [
                #aqui será um exemplo de ataque especial do chefe no turno 4
                {"acao": "ataque_especial", "nome": "Puxão master das trevas", "dano_direto": 1}
            ]
        }
    }
}