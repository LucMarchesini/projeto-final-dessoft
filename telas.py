import pygame
import constantes as C
from jogador import Jogador
import regras_jogo as RJ

C.P1_START = C.mundo_p_tela(*C.P1_START)
C.P2_START = C.mundo_p_tela(*C.P2_START)

def tela_ranking(tela, assets):
    while True:
        tela.blit(assets['tela_ranking'], (0, 0))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

def tela_configuracoes(tela, assets):
    while True:
        tela.blit(assets['tela_configuracoes'], (0, 0))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

def tela_personagem(tela, assets):
    personagens = list(assets["personagens"].keys())
    sel_p1 = 0
    sel_p2 = min(1, len(personagens) - 1)
    confirmado_p1 = False
    confirmado_p2 = False
    fonte = assets["font_text"]
    fonte_titulo = assets["font_title"]

    while True:
        tela.blit(assets['tela_personagem'], (0, 0))

        # Dark panels behind each side
        painel = pygame.Surface((460, 420), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 160))
        tela.blit(painel, (20, 130))
        tela.blit(painel, (800, 130))

        # Title
        titulo = fonte_titulo.render("SELECIONE SEU PERSONAGEM", True, C.BRANCO)
        tela.blit(titulo, (C.LARGURA_JANELA // 2 - titulo.get_width() // 2, 50))

        # VS
        vs = fonte_titulo.render("VS", True, C.VERMELHO)
        tela.blit(vs, (C.LARGURA_JANELA // 2 - vs.get_width() // 2, 300))

        # P1 preview
        p1_nome = personagens[sel_p1]
        p1_sprite = assets["personagens"][p1_nome][C.NORMAL][0]
        tela.blit(p1_sprite, (25, 150))
        p1_label = fonte.render(f"< {p1_nome} >", True, C.BRANCO)
        tela.blit(p1_label, (25 + (450 - p1_label.get_width()) // 2, 460))
        cor_p1 = C.VERDE if confirmado_p1 else C.BRANCO
        p1_hint = fonte.render("PRONTO!" if confirmado_p1 else "SETA ESQUERDA/DIREITA + ESPACO", True, cor_p1)
        tela.blit(p1_hint, (25 + (450 - p1_hint.get_width()) // 2, 495))

        # P2 preview (facing left)
        p2_nome = personagens[sel_p2]
        p2_sprite = pygame.transform.flip(assets["personagens"][p2_nome][C.NORMAL][0], True, False)
        tela.blit(p2_sprite, (805, 150))
        p2_label = fonte.render(f"< {p2_nome} >", True, C.BRANCO)
        tela.blit(p2_label, (805 + (450 - p2_label.get_width()) // 2, 460))
        cor_p2 = C.VERDE if confirmado_p2 else C.BRANCO
        p2_hint = fonte.render("PRONTO!" if confirmado_p2 else "A/D + F", True, cor_p2)
        tela.blit(p2_hint, (805 + (450 - p2_hint.get_width()) // 2, 495))

        esc_hint = fonte.render("ESC - Voltar", True, C.BRANCO)
        tela.blit(esc_hint, (C.LARGURA_JANELA // 2 - esc_hint.get_width() // 2, 670))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return (C.SAIR, None, None)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return (C.MENU, None, None)
                if not confirmado_p1:
                    if evento.key == pygame.K_LEFT:
                        sel_p1 = (sel_p1 - 1) % len(personagens)
                    elif evento.key == pygame.K_RIGHT:
                        sel_p1 = (sel_p1 + 1) % len(personagens)
                    elif evento.key == pygame.K_SPACE:
                        confirmado_p1 = True
                if not confirmado_p2:
                    if evento.key == pygame.K_a:
                        sel_p2 = (sel_p2 - 1) % len(personagens)
                    elif evento.key == pygame.K_d:
                        sel_p2 = (sel_p2 + 1) % len(personagens)
                    elif evento.key == pygame.K_f:
                        confirmado_p2 = True

        if confirmado_p1 and confirmado_p2:
            return (C.TUTORIAL, personagens[sel_p1], personagens[sel_p2])

        pygame.display.flip()

def tela_tutorial(tela, assets):
    fonte_titulo = assets["font_title"]
    fonte        = assets["font_text"]

    controles_p1 = [
        ("← →",        "Mover"),
        ("↑",           "Pular"),
        ("SPACE",       "Soco rápido"),
        ("Z",           "Chute"),
        ("X",           "Soco forte"),
        ("C",           "Super (Fireball)"),
    ]
    controles_p2 = [
        ("A  D",        "Mover"),
        ("W",           "Pular"),
        ("F",           "Soco rápido"),
        ("G",           "Chute"),
        ("H",           "Soco forte"),
        ("J",           "Super (Fireball)"),
    ]

    while True:
        tela.blit(assets['background'], (0, 0))

        # Overlay escuro
        overlay = pygame.Surface((C.LARGURA_JANELA, C.ALTURA_JANELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        # Título
        titulo = fonte_titulo.render("CONTROLES", True, C.BRANCO)
        tela.blit(titulo, (C.LARGURA_JANELA // 2 - titulo.get_width() // 2, 40))

        # Painéis
        for label, controles, px in [("JOGADOR 1", controles_p1, 130),
                                      ("JOGADOR 2", controles_p2, 730)]:
            painel = pygame.Surface((420, 380), pygame.SRCALPHA)
            painel.fill((255, 255, 255, 20))
            tela.blit(painel, (px - 20, 130))

            cab = fonte.render(label, True, C.VERDE)
            tela.blit(cab, (px, 140))

            pygame.draw.line(tela, C.VERDE, (px, 178), (px + 380, 178), 2)

            for i, (tecla, acao) in enumerate(controles):
                y = 195 + i * 48
                t_tecla = fonte.render(tecla, True, C.BRANCO)
                t_acao  = fonte.render(acao,  True, (200, 200, 200))
                tela.blit(t_tecla, (px, y))
                tela.blit(t_acao,  (px + 130, y))

        # Rodapé
        rodape = fonte.render("Pressione qualquer tecla para lutar!", True, C.BRANCO)
        tela.blit(rodape, (C.LARGURA_JANELA // 2 - rodape.get_width() // 2, 660))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return C.PERSONAGEM
                return C.JOGO

def tela_inicial(tela, assets):
    tela.blit(assets['inicial'], (0, 0))

    botao_jogar = pygame.Rect(360, 285, 560, 80)
    botao_ranking = pygame.Rect(360, 375, 560, 80)
    botao_configuracoes = pygame.Rect(360, 465, 560, 80)
    botao_sair = pygame.Rect(360, 555, 560, 80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return C.SAIR
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if botao_jogar.collidepoint(event.pos):
                return C.PERSONAGEM
            elif botao_ranking.collidepoint(event.pos):
                return C.RANKING
            elif botao_configuracoes.collidepoint(event.pos):
                return C.CONFIG
            elif botao_sair.collidepoint(event.pos):
                return C.SAIR

def tela_luta(tela, assets, clock, jogador_um, jogador_dois):
    # lista de (Projetil, alvo) ativos na tela
    projeteis = []

    while True:
        clock.tick(C.FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

        teclas = pygame.key.get_pressed()
        jogador_um.atualizar(teclas)
        jogador_dois.atualizar(teclas)

        # Coletar projéteis recém disparados
        for jogador, alvo in [(jogador_um, jogador_dois), (jogador_dois, jogador_um)]:
            if jogador.projetil_a_disparar:
                projeteis.append((jogador.projetil_a_disparar, alvo))
                jogador.projetil_a_disparar = None

        # Atualizar e checar dano dos projéteis
        for proj, alvo in projeteis:
            proj.atualizar()
            RJ.aplicar_dano_projetil(proj, alvo)
        projeteis = [(p, a) for p, a in projeteis if p.ativo]

        RJ.colisao_corpo(jogador_um, jogador_dois)
        RJ.limites_tela(jogador_um, C.LARGURA_JANELA)
        RJ.limites_tela(jogador_dois, C.LARGURA_JANELA)
        jogador_um.atualizar_direcao(jogador_dois.x)
        jogador_dois.atualizar_direcao(jogador_um.x)

        RJ.aplicar_dano(jogador_um, jogador_dois)
        RJ.aplicar_dano(jogador_dois, jogador_um)

        vencedor = RJ.checar_fim_de_jogo(jogador_um, jogador_dois)
        if vencedor:
            print(f'Jogador {vencedor} venceu!')
            return C.MENU

        # Desenho
        tela.blit(assets['background'], (0, 0))
        jogador_um.desenhar(tela)
        jogador_dois.desenhar(tela)
        for proj, _ in projeteis:
            proj.desenhar(tela)

        if C.DEBUG:
            ZONAS_DEBUG = {C.SOCO: C.ZONA_SOCO, C.CHUTE: C.ZONA_CHUTE,
                           C.SOCO_FORTE: C.ZONA_SOCO_FORTE}
            for jogador in [jogador_um, jogador_dois]:
                mask_c, mx, my = jogador.get_mascara_corpo()
                surf_c = mask_c.to_surface(setcolor=(0, 255, 0, 80), unsetcolor=(0, 0, 0, 0))
                tela.blit(surf_c, (int(mx), int(my)))
            for jogador in [jogador_um, jogador_dois]:
                if jogador.atacando and jogador.estado_ataque in ZONAS_DEBUG:
                    mask_s, mx, my = jogador.get_mascara_ataque()
                    if mask_s:
                        surf_s = mask_s.to_surface(setcolor=(255, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
                        tela.blit(surf_s, (int(mx), int(my)))
                        zx, zy, zl, za = ZONAS_DEBUG[jogador.estado_ataque]
                        if not jogador.virado:
                            zx = C.SPRITE_LARGURA - zx - zl
                        pygame.draw.rect(tela, (255, 165, 0),
                                         (int(mx) + zx, int(my) + zy, zl, za), 2)

        pygame.display.update()