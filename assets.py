import pygame
import constantes as C

def carregar_assets():
    assets = {}

    # --- Fontes ---
    assets["font_huge"]  = pygame.font.SysFont(C.FONTE_PADRAO, 80, bold=True)
    assets["font_title"] = pygame.font.SysFont(C.FONTE_PADRAO, C.TAMANHO_TITULO, bold=True)
    assets["font_text"]  = pygame.font.SysFont(C.FONTE_PADRAO, C.TAMANHO_TEXTO)
    assets["font_small"] = pygame.font.SysFont(C.FONTE_PADRAO, 20)

    # --- Telas ---
    assets['background'] = pygame.image.load('assets/sprites/background.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (C.LARGURA_JANELA, C.ALTURA_JANELA))
    
    # --- Personagens ---
    def _frames(pasta, prefixo, n):
        lista = []
        for i in range(1, n + 1):
            img = pygame.image.load(f'assets/sprites/{pasta}/{prefixo}{i}.png').convert_alpha()
            lista.append(pygame.transform.scale(img, (C.SPRITE_LARGURA, C.SPRITE_ALTURA)))
        return lista

    assets["personagens"] = {
        C.BRAWLER_GIRL: {
            C.NORMAL:     _frames("Brawler-Girl/Idle",  "idle",  4),
            C.ANDANDO:    _frames("Brawler-Girl/Walk",  "walk", 10),
            C.SOCO:       _frames("Brawler-Girl/Jab",   "jab",   3),
            C.CHUTE:      _frames("Brawler-Girl/Kick",  "kick",  5),
            C.SOCO_FORTE: _frames("Brawler-Girl/Punch", "punch", 3),
            C.SUPER:      _frames("Brawler-Girl/Punch", "punch", 3),
            C.PULANDO:    _frames("Brawler-Girl/Jump",  "jump",  4),
            C.HURT:       _frames("Brawler-Girl/Hurt",  "hurt",  2),
        },
        C.ENEMY_PUNK: {
            C.NORMAL:     _frames("Enemy-Punk/Idle",  "idle",  4),
            C.ANDANDO:    _frames("Enemy-Punk/Walk",  "walk",  4),
            C.SOCO:       _frames("Enemy-Punk/Punch", "punch", 3),
            C.CHUTE:      _frames("Enemy-Punk/Punch", "punch", 3),
            C.SOCO_FORTE: _frames("Enemy-Punk/Punch", "punch", 3),
            C.SUPER:      _frames("Enemy-Punk/Punch", "punch", 3),
            C.PULANDO:    _frames("Enemy-Punk/Idle",  "idle",  4),
            C.HURT:       _frames("Enemy-Punk/Hurt",  "hurt",  4),
        },
    }

    # --- Mascaras ---
    def _zona_mask(zona):
        surf = pygame.Surface((C.SPRITE_LARGURA, C.SPRITE_ALTURA), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255, 255), zona)
        return (pygame.mask.from_surface(surf),
                pygame.mask.from_surface(pygame.transform.flip(surf, True, False)))

    zona_soco_mask,       zona_soco_mask_flip       = _zona_mask(C.ZONA_SOCO)
    zona_soco_forte_mask, zona_soco_forte_mask_flip = _zona_mask(C.ZONA_SOCO_FORTE)
    zona_chute_mask,      zona_chute_mask_flip       = _zona_mask(C.ZONA_CHUTE)

    ZONAS_GOLPE = {
        C.SOCO:       (zona_soco_mask,       zona_soco_mask_flip),
        C.SOCO_FORTE: (zona_soco_forte_mask, zona_soco_forte_mask_flip),
        C.CHUTE:      (zona_chute_mask,      zona_chute_mask_flip),
    }

    assets["mascaras"] = {}
    for nome, estados in assets["personagens"].items():
        assets["mascaras"][nome] = {}
        for estado, frames in estados.items():
            first = frames[0]
            assets["mascaras"][nome][estado]           = pygame.mask.from_surface(first)
            assets["mascaras"][nome][estado + "_flip"] = pygame.mask.from_surface(
                pygame.transform.flip(first, True, False)
            )

        # Delta de cada golpe: último frame ∩ zona do golpe
        for tipo_golpe, (zm, zm_flip) in ZONAS_GOLPE.items():
            last       = assets["personagens"][nome][tipo_golpe][-1]
            last_flip  = pygame.transform.flip(last, True, False)
            assets["mascaras"][nome][tipo_golpe + "_delta"]      = pygame.mask.from_surface(last).overlap_mask(zm, (0, 0))
            assets["mascaras"][nome][tipo_golpe + "_delta_flip"] = pygame.mask.from_surface(last_flip).overlap_mask(zm_flip, (0, 0))

    return assets