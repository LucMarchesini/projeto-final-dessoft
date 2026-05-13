import pygame
import constantes as C
from assets import carregar_assets
import telas as T
import jogador as J

pygame.init()

tela = pygame.display.set_mode((C.LARGURA_JANELA, C.ALTURA_JANELA))
pygame.display.set_caption(C.TITULO)

clock = pygame.time.Clock()

assets = carregar_assets()

estado = C.MENU
rodando = True

jogador_um = J.Jogador(
    x = C.P1_START[0],
    y = C.P1_START[1],
    controles=C.P1_CONTROLES,
    assets=assets,
    personagem=C.BRAWLER_GIRL,
    tipo="um",
    vida=100,
    ataque=100,
    estado=C.NORMAL
)

jogador_dois = J.Jogador(
    x = C.P2_START[0],
    y = C.P2_START[1],
    controles=C.P2_CONTROLES,
    assets=assets,
    personagem=C.ENEMY_PUNK,
    tipo="dois",
    vida=100,
    ataque=5,
    estado=C.NORMAL
)

while rodando:
    if estado == C.MENU:
        estado = T.tela_inicial(tela, assets)

    elif estado == C.JOGO:
        estado = T.tela_luta(tela, assets, clock, jogador_um, jogador_dois)

    elif estado == C.RANKING:
        estado = T.tela_ranking(tela, assets)

    elif estado == C.CONFIG:
        estado = T.tela_configuracoes(tela, assets)

    elif estado == C.SAIR:
        rodando = False

    elif estado is None:
        estado = C.MENU

    pygame.display.flip()
    clock.tick(C.FPS)

pygame.quit()