import pygame
import constantes as C

def carregar_assets():
    assets = {}

    # --- Fontes ---
    assets["font_title"] = pygame.font.SysFont(C.FONTE_PADRAO, C.TAMANHO_TITULO, bold=True)
    assets["font_text"] = pygame.font.SysFont(C.FONTE_PADRAO, C.TAMANHO_TEXTO)

    # --- Telas ---
    assets['inicial'] = pygame.image.load('assets/sprites/tela_inicial.png').convert()
    assets['inicial'] = pygame.transform.scale(assets['inicial'], (C.LARGURA_JANELA, C.ALTURA_JANELA))
    
    assets['background'] = pygame.image.load('assets/sprites/background.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['tela_ranking'] = pygame.image.load('assets/sprites/tela_ranking.png').convert()
    assets['tela_ranking'] = pygame.transform.scale(assets['tela_ranking'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['tela_configuracoes'] = pygame.image.load('assets/sprites/tela_configuracoes.png').convert()
    assets['tela_configuracoes'] = pygame.transform.scale(assets['tela_configuracoes'], (C.LARGURA_JANELA, C.ALTURA_JANELA))

    assets['tela_personagem'] = pygame.image.load('assets/sprites/tela_personagem.png').convert()
    assets['tela_personagem'] = pygame.transform.scale(assets['tela_personagem'], (C.LARGURA_JANELA, C.ALTURA_JANELA))
    
    # --- Personagens ---
    assets["personagens"] = {}

    assets["personagens"]["Brawler-Girl"] = {}

    assets["personagens"]["Brawler-Girl"]["normal"] = pygame.image.load(r'assets/sprites/Brawler-Girl/Idle/idle1.png').convert_alpha()
    assets["personagens"]["Brawler-Girl"]["normal"] = pygame.transform.scale(assets["personagens"]["Brawler-Girl"]["normal"], (450, 300))

    assets["personagens"]["Brawler-Girl"]["soco"] = pygame.image.load(r'assets/sprites/Brawler-Girl/Jab/jab3.png').convert_alpha()
    assets["personagens"]["Brawler-Girl"]["soco"] = pygame.transform.scale(assets["personagens"]["Brawler-Girl"]["soco"], (450, 300))

    return assets