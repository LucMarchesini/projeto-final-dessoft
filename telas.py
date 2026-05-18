import pygame
import math
import constantes as C
from jogador import Jogador
import regras_jogo as RJ

C.P1_START = C.mundo_p_tela(*C.P1_START)
C.P2_START = C.mundo_p_tela(*C.P2_START)

# ── Paleta ───────────────────────────────────────────────────────────────────
_FUNDO       = (6,  3, 14)
_PAINEL      = (18, 10, 32)
_BORDA       = (50, 28, 80)
_VERMELHO    = (190, 20, 35)
_VERMELHO_BR = (240, 50, 70)
_DOURADO     = (200, 145,  0)
_DOURADO_BR  = (255, 195, 30)
_BRANCO      = (255, 255, 255)
_CINZA       = (130, 120, 150)
_CINZA_CL    = (185, 180, 200)
_VERDE_NEON  = (0,  210,  80)
_AZUL_P1     = (30, 110, 225)
_AZUL_P1_BR  = (70, 155, 255)

# ── Helpers ──────────────────────────────────────────────────────────────────

def _fundo(tela):
    tela.fill(_FUNDO)
    t = pygame.time.get_ticks()
    offset = (t // 30) % 90
    for i in range(-5, 22):
        x = i * 90 + offset
        pygame.draw.line(tela, (16, 8, 30), (x, 0), (x + 250, C.ALTURA_JANELA), 1)
    scan = pygame.Surface((C.LARGURA_JANELA, C.ALTURA_JANELA), pygame.SRCALPHA)
    for y in range(0, C.ALTURA_JANELA, 3):
        pygame.draw.line(scan, (0, 0, 0, 28), (0, y), (C.LARGURA_JANELA, y))
    tela.blit(scan, (0, 0))


def _sombra(tela, fonte, txt, x, y, cor, cor_s=(0, 0, 0), d=3):
    tela.blit(fonte.render(txt, True, cor_s), (x + d, y + d))
    tela.blit(fonte.render(txt, True, cor), (x, y))


def _centralizar_x(fonte, txt, ref_x=None):
    ref_x = ref_x if ref_x is not None else C.LARGURA_JANELA // 2
    return ref_x - fonte.size(txt)[0] // 2


def _separador(tela, y, cor=None, largura=400):
    cor = cor or _DOURADO
    cx = C.LARGURA_JANELA // 2
    pygame.draw.line(tela, cor, (cx - largura, y), (cx + largura, y), 2)
    pts = [(cx, y - 6), (cx + 7, y), (cx, y + 6), (cx - 7, y)]
    pygame.draw.polygon(tela, cor, pts)


def _painel(tela, rect, cor_borda=None):
    surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    surf.fill((*_PAINEL, 210))
    tela.blit(surf, rect.topleft)
    pygame.draw.rect(tela, cor_borda or _BORDA, rect, 2, border_radius=6)


def _botao(tela, fonte, txt, rect, hover=False):
    cor_bg  = (28, 14, 50) if not hover else (55, 8, 20)
    cor_brd = _DOURADO_BR  if hover     else _BORDA
    cor_txt = _DOURADO_BR  if hover     else _CINZA_CL
    pygame.draw.rect(tela, cor_bg, rect, border_radius=4)
    pygame.draw.rect(tela, cor_brd, rect, 2, border_radius=4)
    if hover:
        pygame.draw.rect(tela, _VERMELHO_BR,
                         (rect.x, rect.y + 10, 5, rect.h - 20), border_radius=2)
    surf = fonte.render(txt, True, cor_txt)
    tela.blit(surf, (rect.centerx - surf.get_width() // 2,
                     rect.centery - surf.get_height() // 2))


def _barra_vida(tela, x, y, w, vida, vida_max, invertida=False):
    h    = 28
    prop = max(0.0, min(1.0, vida / vida_max))
    bw   = int(w * prop)

    pygame.draw.rect(tela, (20, 12, 30), (x, y, w, h))

    if prop > 0.5:
        cor = (30, 185, 55)
    elif prop > 0.25:
        cor = (220, 160, 10)
    else:
        cor = _VERMELHO_BR

    if bw > 0:
        bx = x + w - bw if invertida else x
        pygame.draw.rect(tela, cor, (bx, y, bw, h))
        brilho = tuple(min(255, c + 55) for c in cor)
        pygame.draw.rect(tela, brilho, (bx, y, bw, max(1, h // 4)))

    pygame.draw.rect(tela, _DOURADO, (x, y, w, h), 2)


# ─────────────────────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def tela_inicial(tela, assets):
    fonte_btn   = assets["font_text"]
    fonte_sub   = assets["font_small"]
    fonte_giant = pygame.font.SysFont(C.FONTE_PADRAO, 96, bold=True)

    CX = C.LARGURA_JANELA // 2
    botoes = [
        (pygame.Rect(CX - 200, 290, 400, 58), "JOGAR",         C.PERSONAGEM),
        (pygame.Rect(CX - 200, 365, 400, 58), "RANKING",       C.RANKING),
        (pygame.Rect(CX - 200, 440, 400, 58), "CONFIGURAÇÕES", C.CONFIG),
        (pygame.Rect(CX - 200, 515, 400, 58), "SAIR",          C.SAIR),
    ]

    while True:
        _fundo(tela)

        # Título
        t_c = fonte_giant.render("CORNER", True, _VERMELHO)
        t_f = fonte_giant.render("FIGHT",  True, _DOURADO_BR)
        total = t_c.get_width() + 18 + t_f.get_width()
        ox = CX - total // 2
        tela.blit(fonte_giant.render("CORNER", True, (0, 0, 0)), (ox + 4, 124))
        tela.blit(fonte_giant.render("FIGHT",  True, (0, 0, 0)), (ox + t_c.get_width() + 22, 124))
        tela.blit(t_c, (ox, 120))
        tela.blit(t_f, (ox + t_c.get_width() + 18, 120))

        _separador(tela, 232)
        sub = fonte_sub.render("2-PLAYER FIGHTING GAME", True, _CINZA)
        tela.blit(sub, (CX - sub.get_width() // 2, 242))

        mouse = pygame.mouse.get_pos()
        for rect, txt, _ in botoes:
            _botao(tela, fonte_btn, txt, rect, hover=rect.collidepoint(mouse))

        rodape = fonte_sub.render("© 2025 DESSOFT", True, (50, 45, 65))
        tela.blit(rodape, (CX - rodape.get_width() // 2, C.ALTURA_JANELA - 32))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for rect, _, estado in botoes:
                    if rect.collidepoint(evento.pos):
                        return estado
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.SAIR


# ─────────────────────────────────────────────────────────────────────────────
# SELEÇÃO DE PERSONAGEM
# ─────────────────────────────────────────────────────────────────────────────
def tela_personagem(tela, assets):
    personagens   = list(assets["personagens"].keys())
    sel_p1        = 0
    sel_p2        = min(1, len(personagens) - 1)
    confirmado_p1 = False
    confirmado_p2 = False
    fonte_titulo  = assets["font_title"]
    fonte         = assets["font_text"]
    fonte_small   = assets["font_small"]
    fonte_vs      = pygame.font.SysFont(C.FONTE_PADRAO, 72, bold=True)

    CX       = C.LARGURA_JANELA // 2
    P1_RECT  = pygame.Rect(30,  120, 480, 430)
    P2_RECT  = pygame.Rect(C.LARGURA_JANELA - 510, 120, 480, 430)
    ARROW_Y  = P1_RECT.y + 375

    while True:
        _fundo(tela)

        # Título
        _sombra(tela, fonte_titulo, "SELECIONE SEU PERSONAGEM",
                _centralizar_x(fonte_titulo, "SELECIONE SEU PERSONAGEM"), 28,
                _BRANCO, d=4)
        _separador(tela, 108, cor=_VERMELHO)

        # ── P1 ────────────────────────────────────────────────
        borda_p1 = _VERDE_NEON if confirmado_p1 else _AZUL_P1_BR
        _painel(tela, P1_RECT, cor_borda=borda_p1)

        cab1 = fonte.render("JOGADOR 1", True, _AZUL_P1_BR)
        tela.blit(cab1, (P1_RECT.x + 16, P1_RECT.y + 10))
        pygame.draw.line(tela, _AZUL_P1,
                         (P1_RECT.x + 8, P1_RECT.y + 48),
                         (P1_RECT.right - 8, P1_RECT.y + 48), 1)

        p1_nome   = personagens[sel_p1]
        p1_sprite = assets["personagens"][p1_nome][C.NORMAL][0]
        tela.blit(p1_sprite, (P1_RECT.x + 15, P1_RECT.y + 54))

        cor_arr1 = _CINZA if confirmado_p1 else _DOURADO_BR
        pygame.draw.polygon(tela, cor_arr1,
                            [(P1_RECT.x + 30, ARROW_Y + 14),
                             (P1_RECT.x + 52, ARROW_Y),
                             (P1_RECT.x + 52, ARROW_Y + 28)])
        pygame.draw.polygon(tela, cor_arr1,
                            [(P1_RECT.right - 30, ARROW_Y + 14),
                             (P1_RECT.right - 52, ARROW_Y),
                             (P1_RECT.right - 52, ARROW_Y + 28)])
        n1 = fonte.render(p1_nome, True, _DOURADO_BR)
        tela.blit(n1, (P1_RECT.centerx - n1.get_width() // 2, ARROW_Y + 4))

        if confirmado_p1:
            pronto = fonte.render("✓ PRONTO!", True, _VERDE_NEON)
            tela.blit(pronto, (P1_RECT.centerx - pronto.get_width() // 2, P1_RECT.bottom - 42))
        else:
            h1 = fonte_small.render("← → escolher  |  ESPAÇO confirmar", True, _CINZA)
            tela.blit(h1, (P1_RECT.centerx - h1.get_width() // 2, P1_RECT.bottom - 40))

        # ── P2 ────────────────────────────────────────────────
        borda_p2 = _VERDE_NEON if confirmado_p2 else _VERMELHO_BR
        _painel(tela, P2_RECT, cor_borda=borda_p2)

        cab2 = fonte.render("JOGADOR 2", True, _VERMELHO_BR)
        tela.blit(cab2, (P2_RECT.x + 16, P2_RECT.y + 10))
        pygame.draw.line(tela, _VERMELHO,
                         (P2_RECT.x + 8, P2_RECT.y + 48),
                         (P2_RECT.right - 8, P2_RECT.y + 48), 1)

        p2_nome   = personagens[sel_p2]
        p2_sprite = pygame.transform.flip(assets["personagens"][p2_nome][C.NORMAL][0], True, False)
        tela.blit(p2_sprite, (P2_RECT.x + 15, P2_RECT.y + 54))

        cor_arr2 = _CINZA if confirmado_p2 else _DOURADO_BR
        pygame.draw.polygon(tela, cor_arr2,
                            [(P2_RECT.x + 30, ARROW_Y + 14),
                             (P2_RECT.x + 52, ARROW_Y),
                             (P2_RECT.x + 52, ARROW_Y + 28)])
        pygame.draw.polygon(tela, cor_arr2,
                            [(P2_RECT.right - 30, ARROW_Y + 14),
                             (P2_RECT.right - 52, ARROW_Y),
                             (P2_RECT.right - 52, ARROW_Y + 28)])
        n2 = fonte.render(p2_nome, True, _DOURADO_BR)
        tela.blit(n2, (P2_RECT.centerx - n2.get_width() // 2, ARROW_Y + 4))

        if confirmado_p2:
            pronto2 = fonte.render("✓ PRONTO!", True, _VERDE_NEON)
            tela.blit(pronto2, (P2_RECT.centerx - pronto2.get_width() // 2, P2_RECT.bottom - 42))
        else:
            h2 = fonte_small.render("A / D escolher  |  F confirmar", True, _CINZA)
            tela.blit(h2, (P2_RECT.centerx - h2.get_width() // 2, P2_RECT.bottom - 40))

        # VS central
        vs_surf = fonte_vs.render("VS", True, _VERMELHO)
        vsx = CX - vs_surf.get_width() // 2
        vsy = 310
        tela.blit(fonte_vs.render("VS", True, (0, 0, 0)), (vsx + 4, vsy + 4))
        tela.blit(vs_surf, (vsx, vsy))

        esc = fonte_small.render("ESC - Voltar", True, _CINZA)
        tela.blit(esc, (CX - esc.get_width() // 2, C.ALTURA_JANELA - 32))

        pygame.display.flip()

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


# ─────────────────────────────────────────────────────────────────────────────
# TUTORIAL / CONTROLES
# ─────────────────────────────────────────────────────────────────────────────
def tela_tutorial(tela, assets):
    fonte_titulo = assets["font_title"]
    fonte        = assets["font_text"]
    fonte_small  = assets["font_small"]

    controles_p1 = [
        ("← →",   "Mover"),
        ("↑",     "Pular"),
        ("↓",     "Agachar"),
        ("SPACE", "Soco rápido"),
        ("Z",     "Chute"),
        ("X",     "Soco forte"),
        ("C",     "Super  (Fireball)"),
    ]
    controles_p2 = [
        ("A  D",  "Mover"),
        ("W",     "Pular"),
        ("S",     "Agachar"),
        ("F",     "Soco rápido"),
        ("G",     "Chute"),
        ("H",     "Soco forte"),
        ("J",     "Super  (Fireball)"),
    ]

    PAINEL_H = 60 + len(controles_p1) * 52

    while True:
        tela.blit(assets['background'], (0, 0))
        overlay = pygame.Surface((C.LARGURA_JANELA, C.ALTURA_JANELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 195))
        tela.blit(overlay, (0, 0))

        CX = C.LARGURA_JANELA // 2

        _sombra(tela, fonte_titulo, "CONTROLES",
                _centralizar_x(fonte_titulo, "CONTROLES"), 28,
                _DOURADO_BR, d=4)
        _separador(tela, 108, cor=_DOURADO)

        for label, controles, px, cor_cab, cor_lin in [
            ("JOGADOR 1", controles_p1, 120, _AZUL_P1_BR,  _AZUL_P1),
            ("JOGADOR 2", controles_p2, 695, _VERMELHO_BR, _VERMELHO),
        ]:
            p_rect = pygame.Rect(px, 122, 450, PAINEL_H)
            _painel(tela, p_rect, cor_borda=cor_lin)

            cab = fonte.render(label, True, cor_cab)
            tela.blit(cab, (p_rect.x + 16, p_rect.y + 10))
            pygame.draw.line(tela, cor_lin,
                             (p_rect.x + 8,    p_rect.y + 50),
                             (p_rect.right - 8, p_rect.y + 50), 1)

            for i, (tecla, acao) in enumerate(controles):
                ky = p_rect.y + 62 + i * 52
                badge = pygame.Rect(p_rect.x + 12, ky, 88, 32)
                pygame.draw.rect(tela, (38, 18, 58), badge, border_radius=4)
                pygame.draw.rect(tela, _BORDA, badge, 1, border_radius=4)
                tk = fonte_small.render(tecla, True, _DOURADO_BR)
                tela.blit(tk, (badge.centerx - tk.get_width() // 2,
                               badge.centery - tk.get_height() // 2))
                ta = fonte.render(acao, True, _CINZA_CL)
                tela.blit(ta, (p_rect.x + 114, ky + 2))

        rodape = fonte.render("Pressione qualquer tecla para lutar!", True, _CINZA_CL)
        tela.blit(rodape, (CX - rodape.get_width() // 2, C.ALTURA_JANELA - 44))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return C.PERSONAGEM
                return C.JOGO


# ─────────────────────────────────────────────────────────────────────────────
# RANKING
# ─────────────────────────────────────────────────────────────────────────────
def tela_ranking(tela, assets):
    fonte_titulo = assets["font_title"]
    fonte        = assets["font_text"]
    fonte_small  = assets["font_small"]
    CX = C.LARGURA_JANELA // 2

    while True:
        _fundo(tela)
        _sombra(tela, fonte_titulo, "RANKING",
                _centralizar_x(fonte_titulo, "RANKING"), 60, _DOURADO_BR, d=4)
        _separador(tela, 150, cor=_DOURADO)

        p = pygame.Rect(CX - 310, 175, 620, 360)
        _painel(tela, p)
        msg = fonte.render("Nenhuma partida registrada ainda.", True, _CINZA)
        tela.blit(msg, (CX - msg.get_width() // 2, p.centery - msg.get_height() // 2))

        esc = fonte_small.render("ESC — Menu principal", True, _CINZA)
        tela.blit(esc, (CX - esc.get_width() // 2, C.ALTURA_JANELA - 38))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES
# ─────────────────────────────────────────────────────────────────────────────
def tela_configuracoes(tela, assets):
    fonte_titulo = assets["font_title"]
    fonte        = assets["font_text"]
    fonte_small  = assets["font_small"]
    CX = C.LARGURA_JANELA // 2

    while True:
        _fundo(tela)
        _sombra(tela, fonte_titulo, "CONFIGURAÇÕES",
                _centralizar_x(fonte_titulo, "CONFIGURAÇÕES"), 60, _DOURADO_BR, d=4)
        _separador(tela, 150, cor=_DOURADO)

        p = pygame.Rect(CX - 310, 175, 620, 360)
        _painel(tela, p)
        msg = fonte.render("Em breve.", True, _CINZA)
        tela.blit(msg, (CX - msg.get_width() // 2, p.centery - msg.get_height() // 2))

        esc = fonte_small.render("ESC — Menu principal", True, _CINZA)
        tela.blit(esc, (CX - esc.get_width() // 2, C.ALTURA_JANELA - 38))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU


# ─────────────────────────────────────────────────────────────────────────────
# VITÓRIA
# ─────────────────────────────────────────────────────────────────────────────
def tela_vitoria(tela, assets, vencedor):
    fonte_huge  = assets["font_huge"]
    fonte       = assets["font_text"]
    fonte_small = assets["font_small"]
    CX   = C.LARGURA_JANELA // 2
    tick = 0

    while True:
        tick += 1
        tela.blit(assets['background'], (0, 0))
        overlay = pygame.Surface((C.LARGURA_JANELA, C.ALTURA_JANELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 205))
        tela.blit(overlay, (0, 0))

        # Texto pulsante
        pulse    = abs(math.sin(tick * 0.05)) * 50
        cor_venc = (int(200 + pulse), int(30 + pulse * 0.4), int(30 + pulse * 0.4))
        msg      = f"JOGADOR {vencedor.upper()} VENCEU!"
        _sombra(tela, fonte_huge, msg,
                _centralizar_x(fonte_huge, msg), C.ALTURA_JANELA // 2 - 120,
                cor_venc, d=5)

        _separador(tela, C.ALTURA_JANELA // 2 + 15, cor=_DOURADO)

        h1 = fonte.render("ENTER  —  Jogar novamente", True, _BRANCO)
        h2 = fonte.render("ESC    —  Menu principal",  True, _CINZA_CL)
        tela.blit(h1, (CX - h1.get_width() // 2, C.ALTURA_JANELA // 2 + 40))
        tela.blit(h2, (CX - h2.get_width() // 2, C.ALTURA_JANELA // 2 + 88))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return C.PERSONAGEM
                if evento.key == pygame.K_ESCAPE:
                    return C.MENU


# ─────────────────────────────────────────────────────────────────────────────
# HUD
# ─────────────────────────────────────────────────────────────────────────────
def _hud(tela, assets, j1, j2):
    fonte = assets["font_small"]
    CX    = C.LARGURA_JANELA // 2
    BAR_W = 490
    BAR_Y = 16

    _barra_vida(tela, 16, BAR_Y, BAR_W, j1.vida, 100)
    n1 = fonte.render(j1.personagem, True, _AZUL_P1_BR)
    tela.blit(n1, (18, BAR_Y + 32))

    _barra_vida(tela, C.LARGURA_JANELA - 16 - BAR_W, BAR_Y, BAR_W,
                j2.vida, 100, invertida=True)
    n2 = fonte.render(j2.personagem, True, _VERMELHO_BR)
    tela.blit(n2, (C.LARGURA_JANELA - 16 - BAR_W + BAR_W - n2.get_width() - 2, BAR_Y + 32))

    vs = fonte.render("VS", True, _DOURADO)
    tela.blit(vs, (CX - vs.get_width() // 2, BAR_Y + 4))


# ─────────────────────────────────────────────────────────────────────────────
# LUTA
# ─────────────────────────────────────────────────────────────────────────────
def tela_luta(tela, assets, clock, jogador_um, jogador_dois):
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

        for jogador, alvo in [(jogador_um, jogador_dois), (jogador_dois, jogador_um)]:
            if jogador.projetil_a_disparar:
                projeteis.append((jogador.projetil_a_disparar, alvo))
                jogador.projetil_a_disparar = None

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
            return tela_vitoria(tela, assets, vencedor)

        # Desenho
        tela.blit(assets['background'], (0, 0))
        jogador_um.desenhar(tela)
        jogador_dois.desenhar(tela)
        for proj, _ in projeteis:
            proj.desenhar(tela)

        _hud(tela, assets, jogador_um, jogador_dois)

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
