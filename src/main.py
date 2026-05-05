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

# --- Inicialização dos assets (sem animações por enquanto)
assets = {}
assets['background'] = pygame.image.load('sprites/background').convert()
assets['jogador_um'] = pygame.image.load('sprites\Brawler-Girl\Idle').convert_alpha()
assets['jogador_um'] = pygame.transform.scale(assets['jogador_um'], (20, 100))
# --- Cores ---
cores={
    'Preto': (0, 0, 0),
    'Branco': (255, 255, 255)
}

# --- Loop principal ---
while rodando:

    # 1. Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 2. Update (lógica do jogo vai aqui)

    # 3. Draw
    tela.fill(cores['Preto'])

    pygame.display.update()
    clock.tick(FPS)

# --- Finalização ---
pygame.quit()