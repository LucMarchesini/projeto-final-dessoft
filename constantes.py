import pygame

# --- Janela ---
LARGURA_JANELA = 1280
ALTURA_JANELA = 720
FPS = 60
TITULO = "Corner Fight"

# --- Telas ---
MENU = "menu"
JOGO = "jogo"
PERSONAGEM = "personagem"
RANKING = "ranking"
CONFIG = "configuracoes"
SAIR = "sair"

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
NORMAL = "normal"
SOCO = "soco"

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

# Região dentro do sprite onde o soco pode acertar (personagem olhando para a direita).
# (x, y, largura, altura) em pixels. Ajuste observando o overlay vermelho no DEBUG.
ZONA_SOCO = (260, 85, 185, 90)

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
    "direita": pygame.K_RIGHT,
    "esquerda": pygame.K_LEFT,
    "pulo": pygame.K_UP,
    "soco": pygame.K_SPACE
}
P1_START = (-640, 300)

# --- Jogador 2 ---
P2_CONTROLES = {
    "direita": pygame.K_d,
    "esquerda": pygame.K_a,
    "pulo": pygame.K_w,
    "soco": pygame.K_f
}
P2_START = (-140, 300)

# --- Debug ---
DEBUG = True