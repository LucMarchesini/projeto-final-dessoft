def colisao_corpo(jogador_um, jogador_dois):
    mask1, x1, y1 = jogador_um.get_mascara_corpo()
    mask2, x2, y2 = jogador_dois.get_mascara_corpo()
    if mask1.overlap(mask2, (int(x2 - x1), int(y2 - y1))):
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
        jogador.x -= 5

def aplicar_dano(atacante, alvo):
    if not atacante.atacando or atacante.dano_aplicado:
        return
    mask_golpe, xg, yg = atacante.get_mascara_ataque()
    if mask_golpe is None:
        return
    mask_corpo, xc, yc = alvo.get_mascara_corpo()
    if mask_golpe.overlap(mask_corpo, (int(xc - xg), int(yc - yg))):
        dano = atacante.DANOS_ATAQUE[atacante.estado_ataque]
        alvo.sofrer_dano(dano)
        atacante.dano_aplicado = True
        print(f'Jogador {alvo.tipo} levou {dano} ({atacante.estado_ataque}) | Vida: {alvo.vida}')

def aplicar_dano_projetil(projetil, alvo):
    if not projetil.ativo:
        return
    mask_proj, xp, yp = projetil.get_mascara()
    mask_corpo, xc, yc = alvo.get_mascara_corpo()
    if mask_proj.overlap(mask_corpo, (int(xc - xp), int(yc - yp))):
        alvo.sofrer_dano(projetil.dano)
        projetil.ativo = False
        print(f'Jogador {alvo.tipo} levou {projetil.dano} (super) | Vida: {alvo.vida}')

def checar_fim_de_jogo(jogador_um, jogador_dois):
    if jogador_um.vida <= 0:
        return "dois"
    if jogador_dois.vida <= 0:
        return "um"
    return None
