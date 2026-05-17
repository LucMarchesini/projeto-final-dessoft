import pygame
import constantes as C

class Jogador:
    def __init__(self, x, y, controles, assets, personagem, tipo, virado, vida, ataque, estado):
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
        self.virado = virado  # True = facing right, False = facing left

        self.hitboxes = C.DIC_HITBOXES

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

    def get_mascara_corpo(self):
        key = self.estado if self.virado else self.estado + "_flip"
        return self.assets["mascaras"][self.personagem][key], self.x, self.y

    def get_mascara_soco(self):
        key = C.SOCO + "_delta" if self.virado else C.SOCO + "_delta_flip"
        return self.assets["mascaras"][self.personagem][key], self.x, self.y

    def atualizar_direcao(self, outro_x):
        self.virado = self.x < outro_x

    def get_hitbox_jogador(self):
        offset = C.HITBOX_OFFSET
        size = C.HITBOX_SIZE

        offset = C.mundo_p_tela(offset[0], offset[1])
        size = C.mundo_p_tela(size[0], size[1])

        offset_x = offset[0] if self.virado else C.SPRITE_LARGURA - offset[0] - size[0]
        return pygame.Rect(self.x + offset_x, self.y + offset[1], size[0], size[1])

    def get_hitbox_soco(self):
        offset = C.SOCO_OFFSET
        size = C.SOCO_SIZE

        offset = C.mundo_p_tela(offset[0], offset[1])
        size = C.mundo_p_tela(size[0], size[1])

        offset_x = offset[0] if self.virado else C.SPRITE_LARGURA - offset[0] - size[0]
        return pygame.Rect(self.x + offset_x, self.y + offset[1], size[0], size[1])

    def desenhar(self, tela):
        sprite = self.assets["personagens"][self.personagem][self.estado]
        if not self.virado:
            sprite = pygame.transform.flip(sprite, True, False)
        tela.blit(sprite, (self.x, self.y))