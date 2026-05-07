import pygame
import constantes as C

def tela_personagem(tela, assets):
    tela.blit(assets['tela_personagem'], (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return C.SAIR
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return C.MENU

    pygame.display.flip()