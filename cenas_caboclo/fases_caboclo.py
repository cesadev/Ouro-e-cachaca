fases_do_jogo = {
    "luta_1_mapa_1": {
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "acaua", "vida": 3, "dano": 2, "selos":["voar"]}, "slot": 1}],
            2: [{}],
            3: [{"acao": "jogar_carta", "carta": {"nome": "comadre", "vida": 1, "dano": 1, "selos":["ataque_triplo"]}, "slot": 2}]
        }
    },

    "luta_2_mapa_1": {
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "mula", "vida": 4, "dano": 3, "selos":[]}, "slot": 0}],
            2: [{}],
            3: [{"acao": "jogar_carta", "carta": {"nome": "comadre", "vida": 1, "dano": 1, "selos":["ataque_triplo"]}, "slot": 2}]
        }
    },

    "luta_3_mapa_1": {
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "timbu", "vida": 2, "dano": 2, "selos":["espinhos"]}, "slot": 1},
                {"acao": "jogar_carta", "carta": {"nome": "boitata", "vida": 1, "dano": 2, "selos":[]}, "slot": 3}],
            2: [{"acao": "jogar_carta", "carta": {"nome": "timbu", "vida": 2, "dano": 2, "selos":["espinhos"]}, "slot": 0}]
        }
    },

    "boss_1": {
        "nome": "caboclo de lança",
        "mensagem_inicio": "Tu veio de muito longe né menino, agora bora dançar !",
        "obstaculos_iniciais": [
            {"slot": 2, "nome": "cacto", "vida": 5, "dano": 0, "valor_sacrificio": 0}
        ],
        "script_inimigo": {
            1: [{"acao": "jogar_carta", "carta": {"nome": "capelobo", "vida": 2, "dano": 1, "selos":[]}, "slot": 0},
                {"acao": "jogar_carta", "carta": {"nome": "boitata", "vida": 1, "dano": 2, "selos":[]}, "slot": 2}],
            2: [{"acao": "jogar_carta", "carta": {"nome": "cobra_coral", "vida": 2, "dano": 2, "selos":["mortal"]}, "slot": 3}],
            3: [{"acao": "jogar_carta", "carta": {"nome": "boitata", "vida": 1, "dano": 2, "selos":[]}, "slot": 0}],
            4: [{"acao": "jogar_carta", "carta": {"nome": "capelobo", "vida": 2, "dano": 1, "selos":[]}, "slot": 0}],
            5: [{"acao": "jogar_carta", "carta": {"nome": "acaua", "vida": 3, "dano": 2, "selos":["voar"]}, "slot": 1}],
            6: [{"acao": "jogar_carta", "carta": {"nome": "cobra_coral", "vida": 2, "dano": 2, "selos":["mortal"]}, "slot": 2}],
            7: [{"acao": "jogar_carta", "carta": {"nome": "boitata", "vida": 1, "dano": 2, "selos":[]}, "slot": 3}]
        }
    }
}
