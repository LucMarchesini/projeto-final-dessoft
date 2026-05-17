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

    assets["personagens"]["Enemy-Punk"] = {}

    assets["personagens"]["Enemy-Punk"]["normal"] = pygame.image.load(r'assets/sprites/Enemy-Punk/Idle/idle1.png').convert_alpha()
    assets["personagens"]["Enemy-Punk"]["normal"] = pygame.transform.scale(assets["personagens"]["Enemy-Punk"]["normal"], (450, 300))

    assets["personagens"]["Enemy-Punk"]["soco"] = pygame.image.load(r'assets/sprites/Enemy-Punk/punch/punch3.png').convert_alpha()
    assets["personagens"]["Enemy-Punk"]["soco"] = pygame.transform.scale(assets["personagens"]["Enemy-Punk"]["soco"], (450, 300))

    # --- Mascaras ---
    # Zona do soco: superfície com a região onde o braço pode acertar
    zona_surf = pygame.Surface((C.SPRITE_LARGURA, C.SPRITE_ALTURA), pygame.SRCALPHA)
    zona_surf.fill((0, 0, 0, 0))
    pygame.draw.rect(zona_surf, (255, 255, 255, 255), C.ZONA_SOCO)
    zona_mask = pygame.mask.from_surface(zona_surf)
    zona_mask_flip = pygame.mask.from_surface(
        pygame.transform.flip(zona_surf, True, False)
    )

    assets["mascaras"] = {}
    for nome, estados in assets["personagens"].items():
        assets["mascaras"][nome] = {}
        for estado, sprite in estados.items():
            assets["mascaras"][nome][estado] = pygame.mask.from_surface(sprite)
            sprite_flip = pygame.transform.flip(sprite, True, False)
            assets["mascaras"][nome][estado + "_flip"] = pygame.mask.from_surface(sprite_flip)

        # Máscara de soco = interseção do sprite de soco com a zona do braço
        mask_soco = assets["mascaras"][nome][C.SOCO]
        assets["mascaras"][nome][C.SOCO + "_delta"] = mask_soco.overlap_mask(zona_mask, (0, 0))

        mask_soco_flip = assets["mascaras"][nome][C.SOCO + "_flip"]
        assets["mascaras"][nome][C.SOCO + "_delta_flip"] = mask_soco_flip.overlap_mask(zona_mask_flip, (0, 0))

    return assets