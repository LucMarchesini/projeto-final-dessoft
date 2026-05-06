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

assets['tela_ranking'] = pygame.image.load('sprites/tela_ranking.png').convert()
assets['tela_ranking'] = pygame.transform.scale(assets['tela_ranking'], (largura_janela, altura_janela))

assets['tela_configuracoes'] = pygame.image.load('sprites/tela_configuracoes.png').convert()
assets['tela_configuracoes'] = pygame.transform.scale(assets['tela_configuracoes'], (largura_janela, altura_janela))

assets['tela_personagem'] = pygame.image.load('sprites/tela_personagem.png').convert()
assets['tela_personagem'] = pygame.transform.scale(assets['tela_personagem'], (largura_janela, altura_janela))

# --- Fontes ---
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_sub   = pygame.font.SysFont("Arial", 28)

# --- Funções (recebem assets como parâmetro) ---
def tela_inicial(assets):
    botao_jogar = pygame.Rect(360, 285, 560, 80)
    botao_ranking = pygame.Rect(360, 375, 560, 80)
    botao_configuracoes = pygame.Rect(360, 465, 560, 80)
    botao_sair = pygame.Rect(360, 555, 560, 80)

    while True:
        tela.blit(assets['inicial'], (0, 0))

        pygame.draw.rect(tela, (0, 255, 0), botao_jogar, 3)                     # exibe a heatbox do botão de play 
        pygame.draw.rect(tela, (0, 255, 0), botao_ranking, 3)                   # exibe a heatbox do botão de ranking
        pygame.draw.rect(tela, (0, 255, 0), botao_configuracoes, 3)             # exibe a heatbox do botão de configurações
        pygame.draw.rect(tela, (0, 255, 0), botao_sair, 3)                      # exibe a heatbox do botão de sair

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if botao_jogar.collidepoint(event.pos):
                        loop_jogo(assets)
                    elif botao_ranking.collidepoint(event.pos):
                        tela_ranking(assets)
                    elif botao_configuracoes.collidepoint(event.pos):
                        tela_configuracoes(assets)
                    elif botao_sair.collidepoint(event.pos):
                        pygame.quit()

        pygame.display.flip()
        clock.tick(FPS)

def loop_jogo(assets):
    socando_um = False
    socando_dois = False
    rodando = True
    
    jogador_um_x = 0
    jogador_um_y = 420
    jogador_dois_x = 500
    jogador_dois_y = 420
    
    vel_y_um = 0
    vel_y_dois = 0
    no_chao_um = True
    no_chao_dois = True

    cores = {
        'Preto': (0, 0, 0),
        'Branco': (255, 255, 255)
    }
    caixa = pygame.Rect(700, 400, 50, 50)
    while rodando:
        hit_box_um = pygame.Rect(jogador_um_x+160, jogador_um_y+80, 110, 220) 
        hit_box_soco = pygame.Rect(jogador_um_x+282, jogador_um_y+132, 80, 25) #depois cada um vai ter que virar uma variavel, porque vai variar os sprites
        hit_box_dois = pygame.Rect(jogador_dois_x+160, jogador_dois_y+80, 110, 220) 
        hit_box_soco_dois = pygame.Rect(jogador_dois_x+282, jogador_dois_y+132, 80, 25) #depois cada um vai ter que virar uma variavel, porque vai variar os sprites
        
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        delta_x_um = 0
        delta_x_dois = 0
        #Jogador 1
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            delta_x_um += 5
        if teclas[pygame.K_LEFT]:
            delta_x_um -= 5
        if teclas[pygame.K_UP] and no_chao_um:
            vel_y_um = -15
            no_chao_um = False
        if teclas[pygame.K_SPACE]:
            socando_um = True
        else:
            socando_um = False
        vel_y_um += 0.8
        jogador_um_y += vel_y_um
        if jogador_um_y >= 390:
            jogador_um_y = 390
            vel_y_um = 0
            no_chao_um = True
        #jogador 2
        if teclas[pygame.K_d]:
            delta_x_dois += 5
        if teclas[pygame.K_a]:
            delta_x_dois -= 5
        if teclas[pygame.K_w] and no_chao_dois:
            vel_y_dois = -15
            no_chao_dois = False
        if teclas[pygame.K_f]:
            socando_dois = True
        else:
            socando_dois = False
        vel_y_dois += 0.8
        jogador_dois_y += vel_y_dois
        if jogador_dois_y >= 390:
            jogador_dois_y = 390
            vel_y_dois = 0
            no_chao_dois = True
        jogador_um_x+=delta_x_um
        jogador_dois_x+=delta_x_dois

        tela.blit(assets['background'], (0, 0))
        if socando_um:
            pygame.draw.rect(tela, (0, 255, 0), hit_box_um)
            pygame.draw.rect(tela, (255, 0, 0), hit_box_soco)
            tela.blit(assets['jogador_um_soco'], (jogador_um_x, jogador_um_y))

        else:
            pygame.draw.rect(tela, (0, 255, 0), hit_box_um)
            tela.blit(assets['jogador_um'], (jogador_um_x, jogador_um_y))

        if socando_dois:
            pygame.draw.rect(tela, (0, 255, 0), hit_box_dois)
            pygame.draw.rect(tela, (255, 0, 0), hit_box_soco_dois)
            tela.blit(assets['jogador_dois_soco'], (jogador_dois_x, jogador_dois_y))

        else:
            pygame.draw.rect(tela, (0, 255, 0), hit_box_dois)
            tela.blit(assets['jogador_dois'], (jogador_dois_x, jogador_dois_y))
            
        pygame.display.update()

def tela_ranking(assets):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        
        tela.blit(assets['tela_ranking'], (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

def tela_configuracoes(assets):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        
        tela.blit(assets['tela_configuracoes'], (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

def tela_personagem(assets):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

        tela.blit(assets['tela_personagem'], (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

# --- Execução ---
tela_inicial(assets)
pygame.quit()