import pygame
import constantes as C

def personagem(tela, assets):
    tela.blit(assets['tela_personagem'], (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return C.SAIR
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return C.MENU

    pygame.display.flip()

def ranking(tela, assets):
    tela.blit(assets['tela_ranking'], (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return C.SAIR   

    pygame.display.flip()

def configuracoes(tela, assets):
    tela.blit(assets['tela_configuracoes'], (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return C.SAIR

    pygame.display.flip()
