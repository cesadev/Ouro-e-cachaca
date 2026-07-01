fases_do_jogo = {
    "luta_1_mapa_2": {
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "caboclo", "vida": 1, "dano": 1, "selos":["mergulhador"]}, "slot": 0},
                {"acao": "jogar_carta", "carta": {"nome": "caboclo", "vida": 1, "dano": 1, "selos":["mergulhador"]}, "slot": 1},
                {"acao": "jogar_carta", "carta": {"nome": "capelobo", "vida": 2, "dano": 1, "selos":[]}, "slot": 2}],
            2: [{"acao": "jogar_carta", "carta": {"nome": "acaua", "vida": 3, "dano": 2, "selos":["voar"]}, "slot": 3}],
            3: [{"acao": "jogar_carta", "carta": {"nome": "boitata", "vida": 1, "dano": 2, "selos":[]}, "slot": 2}],
            4: [{"acao": "jogar_carta", "carta": {"nome": "caboclo", "vida": 1, "dano": 1, "selos":["mergulhador"]}, "slot": 2}],
            5: [{}],
            6: [{"acao": "jogar_carta", "carta": {"nome": "acaua", "vida": 3, "dano": 2, "selos":["voar"]}, "slot": 3}]
        }
    },

    "luta_2_mapa_2": {
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "capelobo", "vida": 2, "dano": 1, "selos":[]}, "slot": 1}],
            2: [{"acao": "jogar_carta", "carta": {"nome": "boitata", "vida": 1, "dano": 2, "selos":[]}, "slot": 1},
                {"acao": "jogar_carta", "carta": {"nome": "cobra_coral", "vida": 2, "dano": 2, "selos":["mortal"]}, "slot": 2}],
            3: [{"acao": "jogar_carta", "carta": {"nome": "curupira", "vida": 2, "dano": 3, "selos":[]}, "slot": 0}],
            4: [{"acao": "jogar_carta", "carta": {"nome": "caboclo", "vida": 1, "dano": 1, "selos":["mergulhador"]}, "slot": 3}],
            5: [{}],
            6: [{"acao": "jogar_carta", "carta": {"nome": "mula", "vida": 4, "dano": 3, "selos":[]}, "slot": 0}]
        }
    },

     "boss_2": {
        "nome": "papa-figo",
        "mensagem_inicio": "Criança mal criada... Chegou a sua hora de ir dormir...",
        "obstaculos_iniciais": [{"slot": 1, "nome": "cacto", "vida": 5, "dano": 0, "valor_sacrificio": 0}],
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "cuca", "vida": 2, "dano": 2, "selos":["escudo"]}, "slot": 0}],
            2: [{}],
            3: [{"acao": "jogar_carta", "carta": {"nome": "cuca", "vida": 2, "dano": 2, "selos":["escudo"]}, "slot": 1}],
            4: [{}],
            5: [{"acao": "jogar_carta", "carta": {"nome": "cuca", "vida": 2, "dano": 2, "selos":["escudo"]}, "slot": 2}],
            6: [{}],
            7: [{"acao": "jogar_carta", "carta": {"nome": "cuca", "vida": 2, "dano": 2, "selos":["escudo"]}, "slot": 3}],
            8: [{}],
            9: [{"acao": "jogar_carta", "carta": {"nome": "cuca", "vida": 2, "dano": 2, "selos":["escudo"]}, "slot": 0}],
            10: [{}],
            11: [{"acao": "jogar_carta", "carta": {"nome": "cuca", "vida": 2, "dano": 2, "selos":["escudo"]}, "slot": 1}]
        }
    }
}
