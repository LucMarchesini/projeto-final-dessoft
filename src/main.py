import pygame
import random

pygame.init()

largura_janela = 1280
altura_janela = 720
tela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Corner Fight")

clock = pygame.time.Clock()
FPS = 60

# --- Carrega todos os assets uma vez só ---
assets = {}

assets['inicial'] = pygame.image.load('sprites/tela_inicial.png').convert()
assets['inicial'] = pygame.transform.scale(assets['inicial'], (largura_janela, altura_janela))

assets['background'] = pygame.image.load('sprites/background.png').convert()
assets['background'] = pygame.transform.scale(assets['background'], (largura_janela, altura_janela))

assets['jogador_um'] = pygame.image.load(r'sprites/Brawler-Girl/Idle/idle1.png').convert_alpha()
assets['jogador_um'] = pygame.transform.scale(assets['jogador_um'], (450, 300))

# --- Fontes ---
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_sub   = pygame.font.SysFont("Arial", 28)

# --- Funções (recebem assets como parâmetro) ---
def tela_inicial(assets):
    botao_jogar = pygame.Rect(360, 290, 560, 80)
    while True:
        tela.blit(assets['inicial'], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if botao_jogar.collidepoint(event.pos):
                        return

        pygame.display.flip()
        clock.tick(FPS)

def loop_jogo(assets):
    rodando = True
    jogador_um_x = 0
    jogador_um_y = 420
    
    gravidade = 0
    no_chao = True

    cores = {
        'Preto': (0, 0, 0),
        'Branco': (255, 255, 255)
    }

    while rodando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            jogador_um_x += 5
        if teclas[pygame.K_LEFT]:
            jogador_um_x -= 5
        if teclas[pygame.K_UP] and no_chao:
            gravidade = -15
            no_chao = False

        gravidade += 0.8
        jogador_um_y += gravidade
        if jogador_um_y >= 390:
            jogador_um_y = 390
            gravidade = 0
            no_chao = True
        hit_box_um = pygame.Rect(jogador_um_x+160, jogador_um_y+80, 110, 220) 
        tela.fill(cores['Preto'])
        tela.blit(assets['background'], (0, 0))
        pygame.draw.rect(tela, (0, 200, 0), hit_box_um)
        tela.blit(assets['jogador_um'], (jogador_um_x, jogador_um_y))
        
        pygame.display.update()

# --- Execução ---
tela_inicial(assets)
loop_jogo(assets)
pygame.quit()