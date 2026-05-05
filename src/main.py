import pygame
import random
# --- Inicialização ---
pygame.init()

# --- Janela ---
largura_janela = 1280
altura_janela = 720
tela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Corner Fight")

# --- Clock (controla FPS) ---
clock = pygame.time.Clock()
FPS = 60
# --- Definição para o jogo continuar
rodando = True
altura_jogador = 300
largura_jogador = 450
# --- Inicialização dos assets (sem animações por enquanto)
assets = {}
assets['background'] = pygame.image.load('sprites/background.png').convert()
assets['background'] = pygame.transform.scale(assets['background'], (largura_janela,altura_janela))
assets['jogador_um'] = pygame.image.load('sprites\Brawler-Girl\Idle\idle1.png').convert_alpha()
assets['jogador_um'] = pygame.transform.scale(assets['jogador_um'], (largura_jogador, altura_jogador))
# --- Cores ---
cores={
    'Preto': (0, 0, 0),
    'Branco': (255, 255, 255)
}

# --- Loop principal ---
jogador_um_x = 0
jogador_um_y = 300
velocidade_x = 0
while rodando:
    clock.tick(FPS)

    # 1. Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 2. Update (lógica do jogo vai aqui)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        jogador_um_x += 5
    if teclas[pygame.K_LEFT]:
        jogador_um_x -= 5
    jogador_um_x += velocidade_x
    # 3. Draw
    tela.fill(cores['Preto'])
    tela.blit(assets['background'], (0, 0))
    tela.blit(assets['jogador_um'], (jogador_um_x, jogador_um_y))
    pygame.display.update()

# --- Finalização ---
pygame.quit()