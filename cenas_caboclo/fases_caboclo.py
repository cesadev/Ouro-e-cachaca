fases_do_jogo = {
    "luta_1_mapa_1":{
        "script_inimigo": {
            1:[
                {"acao": "jogar_carta", "carta": {"nome": "Acauã", "vida": 3, "dano": 2}, "slot": 1}
            ],
            2: []
            3: [
                {"acao": "jogar_carta", "carta": {"nome": "Comadre Florzinha", "vida": 1, "dano": 1}, "slot": 2}
            ]
        }
    }
    
    "luta_2_mapa_1":{
        "script_inimigo": {
            1:[
                {"acao": "jogar_carta", "carta": {"nome": "Mula Sem-Cabeça", "vida": 4, "dano": 3}, "slot": 0}
            ],
            2: [],
            3: [
                {"acao": "jogar_carta", "carta": {"nome": "Comadre Florzinha", "vida": 1, "dano": 1}, "slot": 2}
            ]
        }
    }

    "luta_3_mapa_1":{
            "script_inimigo": {
                1:[
                    {"acao": "jogar_carta", "carta": {"nome": "Timbu", "vida": 2, "dano": 2}, "slot": 1},
                    {"acao": "jogar_carta", "carta": {"nome": "Boitatá", "vida": 1, "dano": 2}, "slot": 3}
                ],
                2: [
                     {"acao": "jogar_carta", "carta": {"nome": "Timbu", "vida": 2, "dano": 2}, "slot": 0},
                ]
            }
        }

    "boss_1": {
        "nome": "caboclo de lança",
        "mensagem_inicio": "Tu veio de muito longe né menino, agora bora dançar !",
        "obstaculos_iniciais": [
            {"slot": 2, "nome": "Cacto", "vida": 5, "dano": 0, "valor_sacrificio": 0}
        ],
        "script_inimigo": {
            1: [
                {"acao": "jogar_carta", "carta": {"nome": "Capelobo", "vida": 3, "dano": 1}, "slot": 0},
                {"acao": "jogar_carta", "carta": {"nome": "Boitatá", "vida": 1, "dano": 2}, "slot": 2}
            ],
            2: [
                {"acao": "jogar_carta", "carta": {"nome": "Cobra Coral", "vida": 2, "dano": 2}, "slot": 3}
            ],
            3: [
                {"acao": "jogar_carta", "carta": {"nome": "Boitatá", "vida": 1, "dano": 2}, "slot": 0}
            ],
            4: [
                 {"acao": "jogar_carta", "carta": {"nome": "Capelobo", "vida": 3, "dano": 1}, "slot": 0}
            ],
            5: [
                 {"acao": "jogar_carta", "carta": {"nome": "Acauã", "vida": 3, "dano": 2}, "slot": 1}
            ],
            6: [
                {"acao": "jogar_carta", "carta": {"nome": "Cobra Coral", "vida": 2, "dano": 2}, "slot": 2}
            ],
            7: [
                {"acao": "jogar_carta", "carta": {"nome": "Boitatá", "vida": 1, "dano": 2}, "slot": 3}
            ]
        }
    }
}
