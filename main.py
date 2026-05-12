import pygame
import constantes as C
from assets import carregar_assets
import telas as T

pygame.init()

tela = pygame.display.set_mode((C.LARGURA_JANELA, C.ALTURA_JANELA))
pygame.display.set_caption(C.TITULO)

clock = pygame.time.Clock()

assets = carregar_assets()

estado = C.MENU
rodando = True

while rodando:
    if estado == C.MENU:
        estado = T.tela_inicial(tela, assets)

    elif estado == C.JOGO:
        estado = T.tela_luta(tela, assets, clock)

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