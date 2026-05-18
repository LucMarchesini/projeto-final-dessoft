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
personagem_p1 = C.BRAWLER_GIRL
personagem_p2 = C.ENEMY_PUNK

while rodando:
    if estado == C.MENU:
        resultado = T.tela_inicial(tela, assets)
        if resultado is not None:
            estado = resultado

    elif estado == C.PERSONAGEM:
        resultado = T.tela_personagem(tela, assets)
        estado = resultado[0]
        if estado in (C.TUTORIAL, C.JOGO):
            personagem_p1, personagem_p2 = resultado[1], resultado[2]

    elif estado == C.TUTORIAL:
        estado = T.tela_tutorial(tela, assets)

    elif estado == C.JOGO:
        jogador_um = J.Jogador(
            x=C.P1_START[0],
            y=C.P1_START[1],
            controles=C.P1_CONTROLES,
            assets=assets,
            personagem=personagem_p1,
            tipo="um",
            virado=True,
            vida=100,
            ataque=10,
            estado=C.NORMAL
        )
        jogador_dois = J.Jogador(
            x=C.P2_START[0],
            y=C.P2_START[1],
            controles=C.P2_CONTROLES,
            assets=assets,
            personagem=personagem_p2,
            tipo="dois",
            virado=False,
            vida=100,
            ataque=5,
            estado=C.NORMAL
        )
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
