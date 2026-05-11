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