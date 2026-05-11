import pygame

# --- Janela ---
LARGURA_JANELA = 1280
ALTURA_JANELA = 720
FPS = 60
TITULO = "Corner Fight"

# --- Telas ---
MENU = "menu"
JOGO = "jogo"
RANKING = "ranking"
CONFIG = "configuracoes"
SAIR = "sair"

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

# --- Jogador 1 ---
P1_CONTROLES = {
    "direita": pygame.K_RIGHT,
    "esquerda": pygame.K_LEFT,
    "pulo": pygame.K_UP,
    "soco": pygame.K_SPACE
}
P1_START_X = 0
P1_START_Y = 420
P1_HITBOX_OFFSET = (160, 80)
P1_HITBOX_SIZE = (110, 220)
P1_SOCO_OFFSET = (282, 132)
P1_SOCO_SIZE = (80, 25)

# --- Jogador 2 ---
P2_CONTROLES = {
    "direita": pygame.K_d,
    "esquerda": pygame.K_a,
    "pulo": pygame.K_w,
    "soco": pygame.K_f
}
P2_START_X = 500
P2_START_Y = 420
P2_HITBOX_OFFSET = (160, 80)
P2_HITBOX_SIZE = (110, 220)
P2_SOCO_OFFSET = (282, 132)
P2_SOCO_SIZE = (80, 25)

# --- Debug ---
DEBUG = True