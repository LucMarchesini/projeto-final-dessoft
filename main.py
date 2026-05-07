import pygame
import random
import constantes as C
from assets import carregar_assets
import telas as T

pygame.init()

tela = pygame.display.set_mode((C.LARGURA_JANELA, C.ALTURA_JANELA))                 # Cria a janela do jogo com o tamanho definido dentro dos parênteses
pygame.display.set_caption("Corner Fight")                                      # Cria o título da janela

clock = pygame.time.Clock()                                                     # Cria um objeto de controle de tempo, usado para limitar os quadros por segundo
FPS = 60                                                                        # Define a variável FPS

# --- Carrega todos os assets uma vez só ---
assets = carregar_assets()

# --- Funções (recebem assets como parâmetro) ---
def tela_inicial(assets):
    botao_jogar = pygame.Rect(*C.BOTAO_JOGAR_POS, C.BOTAO_LARGURA, C.BOTAO_ALTURA)
    botao_ranking = pygame.Rect(*C.BOTAO_RANKING_POS, C.BOTAO_LARGURA, C.BOTAO_ALTURA)
    botao_configuracoes = pygame.Rect(*C.BOTAO_CONFIG_POS, C.BOTAO_LARGURA, C.BOTAO_ALTURA)
    botao_sair = pygame.Rect(*C.BOTAO_SAIR_POS, C.BOTAO_LARGURA, C.BOTAO_ALTURA)

    while True:
        tela.blit(assets['inicial'], (0, 0))

        pygame.draw.rect(tela, (0, 255, 0), botao_jogar, 3)                     # exibe a hitbox do botão de play 
        pygame.draw.rect(tela, (0, 255, 0), botao_ranking, 3)                   # exibe a hitbox do botão de ranking
        pygame.draw.rect(tela, (0, 255, 0), botao_configuracoes, 3)             # exibe a hitbox do botão de configurações
        pygame.draw.rect(tela, (0, 255, 0), botao_sair, 3)                      # exibe a hitbox do botão de sair

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if botao_jogar.collidepoint(event.pos):
                        loop_jogo(assets)
                    elif botao_ranking.collidepoint(event.pos):
                        T.tela_ranking(tela, assets)
                    elif botao_configuracoes.collidepoint(event.pos):
                        T.tela_configuracoes(tela, assets)
                    elif botao_sair.collidepoint(event.pos):
                        return C.SAIR

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
        hit_box_um = pygame.Rect(jogador_um_x + C.P1_HITBOX_OFFSET[0], jogador_um_y + C.P1_HITBOX_OFFSET[1], *C.P1_HITBOX_SIZE) 
        hit_box_soco = pygame.Rect(jogador_um_x + C.P1_SOCO_OFFSET[0], jogador_um_y + C.P1_SOCO_OFFSET[1], *C.P1_SOCO_SIZE)   #depois cada um vai ter que virar uma variavel, porque vai variar os sprites
        hit_box_dois = pygame.Rect(jogador_dois_x + C.P2_HITBOX_OFFSET[0], jogador_dois_y + C.P2_HITBOX_OFFSET[1], *C.P2_HITBOX_SIZE)
        hit_box_soco_dois = pygame.Rect(jogador_um_x + C.P1_SOCO_OFFSET[0], jogador_um_y + C.P1_SOCO_OFFSET[1], *C.P1_SOCO_SIZE)   #depois cada um vai ter que virar uma variavel, porque vai variar os sprites
        
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

# -- Loop Principal Atualizado ---
estado = C.MENU
rodando = True

while rodando:
    if estado == C.MENU:
        estado = T.tela_inicial(tela, assets)

    elif estado == C.JOGO:
        estado = T.tela_jogo(tela, assets)

    elif estado == C.RANKING:
        estado = T.tela_ranking(tela, assets)

    elif estado == C.CONFIG:
        estado = T.tela_configuracoes(tela, assets)

    elif estado == C.SAIR:
        rodando = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

# --- Execução ---
tela_inicial(assets)
pygame.quit()