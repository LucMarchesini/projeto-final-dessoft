def checar_soco(hitbox_soco, hitbox_adversario):
    return hitbox_soco.colliderect(hitbox_adversario)
def colisao_corpo(jogador_um, jogador_dois):
    hb_um = jogador_um.get_hitbox_jogador()
    hb_dois = jogador_dois.get_hitbox_jogador()

    if hb_um.colliderect(hb_dois):
        if jogador_um.x < jogador_dois.x:
            jogador_um.x -= 5
            jogador_dois.x += 5
        else:
            jogador_um.x += 5
            jogador_dois.x -= 5
def limites_tela(jogador, largura_tela):
    hb = jogador.get_hitbox_jogador()

    if hb.left < 0:
        jogador.x += 5 
    if hb.right > largura_tela:
        jogador.x -=5 
def aplicar_dano(atacante, alvo, hb_soco, hb_alvo):
    if atacante.socando and not atacante.dano_aplicado and checar_soco(hb_soco, hb_alvo):
        alvo.vida -= atacante.ataque
        atacante.dano_aplicado = True  # <-- bloqueia qualquer dano subsequente
        print(f'Jogador {alvo.tipo} levou {atacante.ataque} de dano | Vida: {alvo.vida}')
def checar_fim_de_jogo(jogador_um, jogador_dois):
    if jogador_um.vida <= 0:
        return "dois"  # jogador dois venceu
    if jogador_dois.vida <= 0:
        return "um"    # jogador um venceu
    return None        # jogo continua