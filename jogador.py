import pygame
import constantes as C
from projetil import Projetil

_ATAQUES_CORPO = [C.SOCO, C.CHUTE, C.SOCO_FORTE]
_TODOS_ATAQUES = _ATAQUES_CORPO + [C.SUPER]

class Jogador:
    def __init__(self, x, y, controles, assets, personagem, tipo, virado, vida, ataque, estado):
        self.x = x
        self.y = y

        self.vida   = vida
        self.ataque = ataque

        # --- Sistema de ataque ---
        self.atacando      = False
        self.estado_ataque = None
        self.frames_ataque = 0
        self.dano_aplicado = False
        self.projetil_a_disparar = None

        estados_p = assets["personagens"][personagem]
        self.DURACOES_ATAQUE = {
            t: len(estados_p[t]) * C.ANIM_VELOCIDADE for t in _TODOS_ATAQUES
        }
        self.DANOS_ATAQUE = {
            C.SOCO:       ataque,
            C.CHUTE:      int(ataque * 1.5),
            C.SOCO_FORTE: ataque * 2,
            C.SUPER:      ataque * 3,
        }
        self.COOLDOWNS_ATAQUE = {
            C.SOCO:       30,
            C.CHUTE:      40,
            C.SOCO_FORTE: 60,
            C.SUPER:      120,
        }
        self.cooldowns  = {t: 0    for t in _TODOS_ATAQUES}
        self.disponivel = {t: True for t in _TODOS_ATAQUES}

        # --- Hurt ---
        self.frames_hurt  = 0
        self.DURACAO_HURT = len(estados_p[C.HURT]) * C.ANIM_VELOCIDADE

        # --- Animação ---
        self.frame_anim    = 0
        self.contador_anim = 0
        self.estado        = estado
        self.personagem    = personagem

        # --- Física ---
        self.vel_y   = 0
        self.no_chao = True
        self.agachado = False

        self.controles = controles
        self.assets    = assets
        self.tipo      = tipo
        self.virado    = virado
        self.hitboxes  = C.DIC_HITBOXES

    # ------------------------------------------------------------------
    # Atualização principal
    # ------------------------------------------------------------------

    def atualizar(self, teclas):
        # Agachar (somente no chão, sem estar atacando)
        tecla_agachar = self.controles.get("agachar")
        self.agachado = (
            bool(tecla_agachar)
            and self.no_chao
            and not self.atacando
            and teclas[tecla_agachar]
        )

        # Movimento bloqueado ao agachar
        delta_x = 0
        if not self.agachado:
            if teclas[self.controles["direita"]]:
                delta_x += C.VELOCIDADE
            if teclas[self.controles["esquerda"]]:
                delta_x -= C.VELOCIDADE

        if teclas[self.controles["pulo"]] and self.no_chao and not self.agachado:
            self.vel_y   = C.IMPULSO_PULO
            self.no_chao = False

        # Decrementar cooldowns
        for t in _TODOS_ATAQUES:
            if self.cooldowns[t] > 0:
                self.cooldowns[t] -= 1

        # Liberar flag quando tecla solta
        for t in _TODOS_ATAQUES:
            tecla = self.controles.get(t)
            if tecla and not teclas[tecla]:
                self.disponivel[t] = True

        # Disparar novo ataque (bloqueado ao agachar)
        if not self.atacando and not self.agachado:
            for t in _TODOS_ATAQUES:
                tecla = self.controles.get(t)
                if tecla and teclas[tecla] and self.disponivel[t] and self.cooldowns[t] == 0:
                    self.atacando      = True
                    self.estado_ataque = t
                    self.frames_ataque = self.DURACOES_ATAQUE[t]
                    self.cooldowns[t]  = self.COOLDOWNS_ATAQUE[t]
                    self.disponivel[t] = False
                    if t == C.SUPER:
                        direcao = 1 if self.virado else -1
                        px = self.x + C.SPRITE_LARGURA if self.virado else self.x
                        py = self.y + 110
                        self.projetil_a_disparar = Projetil(px, py, direcao,
                                                            self.DANOS_ATAQUE[C.SUPER])
                    break

        # Contar frames do ataque
        if self.frames_ataque > 0:
            self.frames_ataque -= 1
        else:
            self.atacando      = False
            self.estado_ataque = None
            self.dano_aplicado = False

        if self.frames_hurt > 0:
            self.frames_hurt -= 1

        self.vel_y += C.GRAVIDADE
        self.x += delta_x
        self.y += self.vel_y

        if self.y >= C.Y_CHAO:
            self.y   = C.Y_CHAO
            self.vel_y  = 0
            self.no_chao = True

        self._atualizar_animacao(self._calcular_estado(delta_x))

    def sofrer_dano(self, quantidade):
        self.vida -= quantidade
        if self.vida > 0:
            self.frames_hurt = self.DURACAO_HURT

    # ------------------------------------------------------------------
    # Animação
    # ------------------------------------------------------------------

    def _calcular_estado(self, delta_x):
        estados_disp = self.assets["personagens"][self.personagem]
        if self.atacando and self.estado_ataque:
            return self.estado_ataque
        if self.frames_hurt > 0:
            return C.HURT
        if not self.no_chao and C.PULANDO in estados_disp:
            return C.PULANDO
        if self.agachado:
            return C.NORMAL   # usa animação idle, sprite desenhado comprimido
        if delta_x != 0:
            return C.ANDANDO
        return C.NORMAL

    def _atualizar_animacao(self, novo_estado):
        if novo_estado != self.estado:
            self.estado        = novo_estado
            self.frame_anim    = 0
            self.contador_anim = 0
            return

        # Pulo: frame mapeado pela velocidade vertical (0=subindo → último=caindo)
        if self.estado == C.PULANDO:
            n = len(self.assets["personagens"][self.personagem][C.PULANDO])
            t = max(0.0, (self.vel_y - C.IMPULSO_PULO) / (-C.IMPULSO_PULO * 2))
            self.frame_anim = min(int(t * n), n - 1)
            return

        self.contador_anim += 1
        if self.contador_anim >= C.ANIM_VELOCIDADE:
            self.contador_anim = 0
            n = len(self.assets["personagens"][self.personagem][self.estado])
            self.frame_anim = (self.frame_anim + 1) % n

    # ------------------------------------------------------------------
    # Colisão
    # ------------------------------------------------------------------

    def get_mascara_corpo(self):
        key = self.estado if self.virado else self.estado + "_flip"
        return self.assets["mascaras"][self.personagem][key], self.x, self.y

    def get_mascara_ataque(self):
        """Retorna a máscara delta do golpe atual (None para super)."""
        if self.estado_ataque not in _ATAQUES_CORPO:
            return None, None, None
        key = self.estado_ataque + "_delta" if self.virado else self.estado_ataque + "_delta_flip"
        mascara = self.assets["mascaras"][self.personagem].get(key)
        if mascara is None:
            return None, None, None
        return mascara, self.x, self.y

    def atualizar_direcao(self, outro_x):
        self.virado = self.x < outro_x

    def get_hitbox_jogador(self):
        offset   = C.mundo_p_tela(*C.HITBOX_OFFSET)
        size     = C.mundo_p_tela(*C.HITBOX_SIZE)
        offset_x = offset[0] if self.virado else C.SPRITE_LARGURA - offset[0] - size[0]
        h = size[1]
        if self.agachado:
            novo_h = int(h * 0.6)
            return pygame.Rect(self.x + offset_x, self.y + offset[1] + h - novo_h, size[0], novo_h)
        return pygame.Rect(self.x + offset_x, self.y + offset[1], size[0], h)

    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------

    def desenhar(self, tela):
        frames = self.assets["personagens"][self.personagem][self.estado]
        sprite = frames[min(self.frame_anim, len(frames) - 1)]
        if not self.virado:
            sprite = pygame.transform.flip(sprite, True, False)
        if self.agachado:
            orig_h = sprite.get_height()
            novo_h = int(orig_h * 0.6)
            sprite = pygame.transform.scale(sprite, (sprite.get_width(), novo_h))
            tela.blit(sprite, (self.x, self.y + orig_h - novo_h))
        else:
            tela.blit(sprite, (self.x, self.y))
