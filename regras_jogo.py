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
    if not atacante.socando or atacante.dano_aplicado:
        return
    mask_soco, xs, ys = atacante.get_mascara_soco()
    mask_corpo, xc, yc = alvo.get_mascara_corpo()
    if mask_soco.overlap(mask_corpo, (int(xc - xs), int(yc - ys))):
        alvo.vida -= atacante.ataque
        atacante.dano_aplicado = True
        print(f'Jogador {alvo.tipo} levou {atacante.ataque} de dano | Vida: {alvo.vida}')

def checar_fim_de_jogo(jogador_um, jogador_dois):
    if jogador_um.vida <= 0:
        return "dois"
    if jogador_dois.vida <= 0:
        return "um"
    return None
