import pygame
import constantes as C

class Jogador:
    def __init__(self, x, y, controles, assets, tipo, vida, ataque):
        #posição
        self.x = x
        self.y = y

        #combate
        self.vida = vida
        self.ataque = ataque
        self.soco_disponivel = True

        #física
        self.vel_y = 0
        self.no_chao = True
        self.socando = False

        #importações gerais
        self.controles = controles
        self.assets = assets
        self.tipo = tipo

    def atualizar(self, teclas):
        delta_x = 0

        if teclas[self.controles["direita"]]:
            delta_x += C.VELOCIDADE
        if teclas[self.controles["esquerda"]]:
            delta_x -= C.VELOCIDADE

        if teclas[self.controles["pulo"]] and self.no_chao:
            self.vel_y = C.IMPULSO_PULO
            self.no_chao = False

        if teclas[self.controles["soco"]]:
            if self.soco_disponivel:
                self.socando = True
                self.soco_disponivel = False  # bloqueia até soltar
            else:
                self.socando = False
                self.soco_disponivel = True  # libera quando soltar o botão
        self.vel_y += C.GRAVIDADE
        self.x += delta_x
        self.y += self.vel_y

        if self.y >= C.Y_CHAO:
            self.y = C.Y_CHAO
            self.vel_y = 0
            self.no_chao = True

    def get_hitbox_jogador(self):
        offset = C.P1_HITBOX_OFFSET if self.tipo == "um" else C.P2_HITBOX_OFFSET
        size = C.P1_HITBOX_SIZE if self.tipo == "um" else C.P2_HITBOX_SIZE
        return pygame.Rect(self.x + offset[0], self.y + offset[1], size[0], size[1])

    def get_hitbox_soco(self):
        offset = C.P1_SOCO_OFFSET if self.tipo == "um" else C.P2_SOCO_OFFSET
        size = C.P1_SOCO_SIZE if self.tipo == "um" else C.P2_SOCO_SIZE
        return pygame.Rect(self.x + offset[0], self.y + offset[1], size[0], size[1])

    def desenhar(self, tela):
        if self.socando:
            sprite = self.assets['jogador_um_soco'] if self.tipo == "um" else self.assets['jogador_dois_soco']
        else:
            sprite = self.assets['jogador_um'] if self.tipo == "um" else self.assets['jogador_dois']
        tela.blit(sprite, (self.x, self.y))