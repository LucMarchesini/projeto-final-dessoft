import pygame
import constantes as C

class Projetil:
    def __init__(self, x, y, direcao, dano):
        self.x      = float(x)
        self.y      = float(y)
        self.direcao = direcao  # 1 = direita, -1 = esquerda
        self.dano   = dano
        self.ativo  = True

    def atualizar(self):
        self.x += C.PROJETIL_VELOCIDADE * self.direcao
        if self.x < -C.PROJETIL_RAIO or self.x > C.LARGURA_JANELA + C.PROJETIL_RAIO:
            self.ativo = False

    def desenhar(self, tela):
        cx, cy = int(self.x), int(self.y)
        r = C.PROJETIL_RAIO
        pygame.draw.circle(tela, (255, 100,   0), (cx, cy), r)
        pygame.draw.circle(tela, (255, 210,   0), (cx, cy), r - 7)
        pygame.draw.circle(tela, (255, 255, 180), (cx, cy), r - 14)

    def get_mascara(self):
        r    = C.PROJETIL_RAIO
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255, 255), (r, r), r)
        return pygame.mask.from_surface(surf), self.x - r, self.y - r
