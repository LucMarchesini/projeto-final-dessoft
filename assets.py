import pygame
import constantes as C

def carregar_assets():
    assets = {}

    assets['inicial'] = pygame.image.load('assets/sprites/tela_inicial.png').convert()
    assets['inicial'] = pygame.transform.scale(assets['inicial'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['background'] = pygame.image.load('assets/sprites/background.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['jogador_um'] = pygame.image.load(r'assets/sprites/Brawler-Girl/Idle/idle1.png').convert_alpha()
    assets['jogador_um'] = pygame.transform.scale(assets['jogador_um'], (450, 300))

    assets['jogador_dois'] = assets['jogador_um']

    assets['jogador_um_soco'] = pygame.image.load(r'assets/sprites/Brawler-Girl/Jab/jab3.png').convert_alpha()
    assets['jogador_um_soco'] = pygame.transform.scale(assets['jogador_um_soco'], (450, 300))

    assets['jogador_dois_soco'] = assets['jogador_um_soco']

    assets['tela_ranking'] = pygame.image.load('assets/sprites/tela_ranking.png').convert()
    assets['tela_ranking'] = pygame.transform.scale(assets['tela_ranking'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['tela_configuracoes'] = pygame.image.load('assets/sprites/tela_configuracoes.png').convert()
    assets['tela_configuracoes'] = pygame.transform.scale(assets['tela_configuracoes'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['tela_personagem'] = pygame.image.load('assets/sprites/tela_personagem.png').convert()
    assets['tela_personagem'] = pygame.transform.scale(assets['tela_personagem'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    return assets