import pygame
import constantes as C

class Jogador:
    def __init__(self, x, y, controles, assets, personagem, tipo, vida, ataque, estado):
        self.x = x
        self.y = y

        self.vida = vida
        self.ataque = ataque
        self.soco_disponivel = True
        self.frames_soco = 0
        self.DURACAO_SOCO = 10
        self.cooldown_soco = 0            # <-- novo
        self.COOLDOWN_SOCO = 30
        self.dano_aplicado = False
        
        self.estado = estado
        self.personagem = personagem

        self.vel_y = 0
        self.no_chao = True
        self.socando = False                # temporário

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

        # Cooldown conta regressivamente
        if self.cooldown_soco > 0:
            self.cooldown_soco -= 1

        # Soco só dispara se cooldown zerou
        if teclas[self.controles["soco"]] and self.soco_disponivel and self.cooldown_soco == 0:
            self.socando = True
            self.estado = C.SOCO
            self.soco_disponivel = False
            self.frames_soco = self.DURACAO_SOCO
            self.cooldown_soco = self.COOLDOWN_SOCO  # inicia o cooldown

        if not teclas[self.controles["soco"]]:
            self.soco_disponivel = True

        if self.frames_soco > 0:
            self.frames_soco -= 1
        else:
            self.socando = False
            self.estado = C.NORMAL
            self.dano_aplicado = False

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
        sprite = self.assets["personagens"][self.personagem][self.estado]
        tela.blit(sprite, (self.x, self.y))