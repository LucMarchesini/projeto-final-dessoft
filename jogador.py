import pygame
import constantes as C
from assets import carregar_assets

assets = carregar_assets()

class Jogador:
    def __init__(self, x, y, controles, assets, estado, tipo):
        self.x = x
        self.y = y

        self.vel_y = 0
        self.no_chao = True                 # futuramente isso será removido
        self.estado = estado                # pulando, socando, no chão, pulando + socando etc

        self.controles = controles
        self.assets = assets
        self.tipo = tipo

    def atualizar(self, teclas):
        delta_x = 0

        # Movimento Horizontal
        if teclas[self.controles["direita"]]:
            delta_x += C.VELOCIDADE
        if teclas[self.controles["esquerda"]]:
            delta_x -= C.VELOCIDADE
        
        # Pulo
        if teclas[self.controles["pulo"]] and self.no_chao:
            self.vel_y = C.IMPULSO_PULO
            self.no_chao = False
        
        # Soco
        self.socando = teclas[self.controles["soco"]]

        # Gravidade
        self.vel_y += C.GRAVIDADE

        # Movimento
        self.x += self.delta_x
        self.y += self.vel_y

        # Colisão com o chão

        if self.y >= C.Y_CHAO:
            self.y = C.Y_CHAO
            self.vel_y = 0
            self.no_chao = True
    
    def get_hitbox_jogador(self):
        offset = C.P1_HITBOX_OFFSET if self.tipo == "um" else C.P2_HITBOX_OFFSET
        size = C.P1_HITBOX_SIZE if self.tipo == "um" else C.P2_HITBOX_SIZE

        return pygame.Rect(
            self.x + offset[0],
            self.y + offset[1],
            size[0],
            size[1]
        )

    def get_hitbox_soco(self):
        offset = C.P1_SOCO_OFFSET if self.tipo == "um" else C.P2_SOCO_OFFSET
        size = C.P1_SOCO_SIZE if self.tipo == "um" else C.P2_SOCO_SIZE

        return pygame.Rect(
            self.x + offset[0],
            self.y + offset[1],
            size[0],
            size[1]
        )
    
    def desenhar(self, tela):
        sprite = assets["personagens"][self.estado]
        tela.blit(sprite, (self.x, self.y))
    
    