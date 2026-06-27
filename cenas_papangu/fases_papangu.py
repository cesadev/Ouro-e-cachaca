fases_do_jogo = {
    "boss_papangu": {
        "nome": "Papangu",
        "mensagem_inicio": "O Papangu chegou! Esconda seu rosto e cuidado com suas cartas!",
        "obstaculos_iniciais": [], 
        "script_inimigo": {
            1: [
                {"acao": "jogar_carta", "carta": {"nome": "Saci", "vida": 2, "dano": 1}, "slot": 0}
            ],
            2: [
                {"acao": "jogar_carta", "carta": {"nome": "Mula Sem Cabeça", "vida": 3, "dano": 2}, "slot": 2}
            ],
            3: [
                # Habilidade de assustar a cada 3 rodadas
                {"acao": "ataque_especial", "nome": "Susto do Papangu", "efeito": "virar_cartas", "dano_direto": 1}
            ],
            4: [],
            5: [
                {"acao": "jogar_carta", "carta": {"nome": "Bicho Papão", "vida": 4, "dano": 2}, "slot": 1}
            ],
            6: [
                {"acao": "ataque_especial", "nome": "Susto do Papangu", "efeito": "virar_cartas", "dano_direto": 1}
            ]
        }
    }
}