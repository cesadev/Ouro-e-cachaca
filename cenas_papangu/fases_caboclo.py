fases_do_jogo = {
    "boss_1": {
        "nome": "o lenhador brabo",
        "mensagem_inicio": "Sua primeira batalha! Posicione suas cartas para sobreviver.",
        "obstaculos_iniciais": [
            {"slot": 2, "nome": "Cacto", "vida": 5, "dano": 0, "valor_sacrificio": 0}
        ],
        "script_inimigo": {
            1: [
                {"acao": "jogar_carta", "carta": {"nome": "Capelobo", "vida": 3, "dano": 1}, "slot": 0}
            ],
            2: [
                {"acao": "jogar_carta", "carta": {"nome": "Timbu", "vida": 2, "dano": 2}, "slot": 3}
            ],
            3: [],
            4: [
                {"acao": "ataque_especial", "nome": "Puxão master das trevas", "dano_direto": 1}
            ]
        }
    }
}