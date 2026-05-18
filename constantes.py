import pygame

# --- Janela ---
LARGURA_JANELA = 1280
ALTURA_JANELA = 720
FPS = 60
TITULO = "Corner Fight"

# --- Telas ---
MENU      = "menu"
JOGO      = "jogo"
PERSONAGEM = "personagem"
TUTORIAL  = "tutorial"
RANKING   = "ranking"
CONFIG    = "configuracoes"
SAIR      = "sair"

# --- Coordenadas ---
ORIGEM_X = LARGURA_JANELA // 2
ORIGEM_Y = 0

def mundo_p_tela(x, y):
    return x + ORIGEM_X, ALTURA_JANELA - y

def tela_p_mundo(x, y):
    return x - ORIGEM_X, ALTURA_JANELA - y

# --- Fontes ---
FONTE_PADRAO = "Arial"
TAMANHO_TITULO = 64
TAMANHO_TEXTO = 28

# --- Botões ---
BOTAO_LARGURA = 560
BOTAO_ALTURA = 80

BOTAO_JOGAR_POS = (360, 285)
BOTAO_RANKING_POS = (360, 375)
BOTAO_CONFIG_POS = (360, 465)
BOTAO_SAIR_POS = (360, 555)

# --- Personagens ---
BRAWLER_GIRL = "Brawler-Girl"
ENEMY_PUNK = "Enemy-Punk"

# --- Estados ---
NORMAL     = "normal"
ANDANDO    = "andando"
PULANDO    = "pulando"
HURT       = "hurt"
SOCO       = "soco"
CHUTE      = "chute"
SOCO_FORTE = "soco_forte"
SUPER      = "super"

ANIM_VELOCIDADE = 8  # frames de jogo por frame de sprite (~7 fps)

# --- Física ---
GRAVIDADE = 0.8
IMPULSO_PULO = -23
VELOCIDADE = 5
Y_CHAO = 390

# --- Cores ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

SPRITE_LARGURA = 450
SPRITE_ALTURA = 300

# Zonas de golpe dentro do sprite (personagem olhando para a direita).
# (x, y, largura, altura). Ajuste observando o overlay no DEBUG.
ZONA_SOCO       = (260,  85, 185,  90)   # braço/soco rápido
ZONA_SOCO_FORTE = (230,  70, 220, 110)   # soco mais largo e mais alto
ZONA_CHUTE      = (210, 160, 240, 120)   # perna/chute (área baixa)

# --- Projétil ---
PROJETIL_VELOCIDADE = 10
PROJETIL_RAIO       = 22

# --- Jogadores ---                     --> transformar em dicionário futuramente
HITBOX_OFFSET = (-480, 640)
HITBOX_SIZE = (-530, 500)
SOCO_OFFSET = (-358, 588)
SOCO_SIZE = (-560, 695)

DIC_HITBOXES = {
    "HITBOX_OFFSET": (-480, 640),
    "HITBOX_SIZE": (-530, 500),
    "SOCO_OFFSET": (-358, 588),
    "SOCO_SIZE": (-560, 695)
}

# --- Jogador 1 ---
P1_CONTROLES = {
    "direita":    pygame.K_RIGHT,
    "esquerda":   pygame.K_LEFT,
    "pulo":       pygame.K_UP,
    "soco":       pygame.K_SPACE,
    "chute":      pygame.K_z,
    "soco_forte": pygame.K_x,
    "super":      pygame.K_c,
}
P1_START = (-640, 300)

# --- Jogador 2 ---
P2_CONTROLES = {
    "direita":    pygame.K_d,
    "esquerda":   pygame.K_a,
    "pulo":       pygame.K_w,
    "soco":       pygame.K_f,
    "chute":      pygame.K_g,
    "soco_forte": pygame.K_h,
    "super":      pygame.K_j,
}
P2_START = (-140, 300)

# --- Debug ---
DEBUG = False