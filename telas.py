import pygame
import constantes as C

def tela_ranking(tela, assets):
    while True:
        tela.blit(assets['tela_ranking'], (0, 0))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

def tela_configuracoes(tela, assets):
    while True:
        tela.blit(assets['tela_configuracoes'], (0, 0))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

def tela_personagem(tela, assets):
    while True:
        tela.blit(assets['tela_personagem'], (0, 0))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

def tela_inicial(tela, assets):
    tela.blit(assets['inicial'], (0, 0))

    botao_jogar = pygame.Rect(360, 285, 560, 80)
    botao_ranking = pygame.Rect(360, 375, 560, 80)
    botao_configuracoes = pygame.Rect(360, 465, 560, 80)
    botao_sair = pygame.Rect(360, 555, 560, 80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return C.SAIR
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if botao_jogar.collidepoint(event.pos):
                return C.JOGO
            elif botao_ranking.collidepoint(event.pos):
                return C.RANKING
            elif botao_configuracoes.collidepoint(event.pos):
                return C.CONFIG
            elif botao_sair.collidepoint(event.pos):
                return C.SAIR

def loop_jogo(tela, assets, clock):  # <-- assinatura corrigida
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

    while rodando:
        clock.tick(C.FPS)

        hit_box_um = pygame.Rect(jogador_um_x + C.P1_HITBOX_OFFSET[0], jogador_um_y + C.P1_HITBOX_OFFSET[1], *C.P1_HITBOX_SIZE)
        hit_box_soco = pygame.Rect(jogador_um_x + C.P1_SOCO_OFFSET[0], jogador_um_y + C.P1_SOCO_OFFSET[1], *C.P1_SOCO_SIZE)
        hit_box_dois = pygame.Rect(jogador_dois_x + C.P2_HITBOX_OFFSET[0], jogador_dois_y + C.P2_HITBOX_OFFSET[1], *C.P2_HITBOX_SIZE)
        hit_box_soco_dois = pygame.Rect(jogador_dois_x + C.P2_SOCO_OFFSET[0], jogador_dois_y + C.P2_SOCO_OFFSET[1], *C.P2_SOCO_SIZE)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

        delta_x_um = 0
        delta_x_dois = 0
        teclas = pygame.key.get_pressed()

        # Jogador 1
        if teclas[pygame.K_RIGHT]:
            delta_x_um += C.VELOCIDADE
        if teclas[pygame.K_LEFT]:
            delta_x_um -= C.VELOCIDADE
        if teclas[pygame.K_UP] and no_chao_um:
            vel_y_um = C.IMPULSO_PULO
            no_chao_um = False
        socando_um = teclas[pygame.K_SPACE]

        vel_y_um += C.GRAVIDADE
        jogador_um_y += vel_y_um
        if jogador_um_y >= C.Y_CHAO:
            jogador_um_y = C.Y_CHAO
            vel_y_um = 0
            no_chao_um = True

        # Jogador 2
        if teclas[pygame.K_d]:
            delta_x_dois += C.VELOCIDADE
        if teclas[pygame.K_a]:
            delta_x_dois -= C.VELOCIDADE
        if teclas[pygame.K_w] and no_chao_dois:
            vel_y_dois = C.IMPULSO_PULO
            no_chao_dois = False
        socando_dois = teclas[pygame.K_f]

        vel_y_dois += C.GRAVIDADE
        jogador_dois_y += vel_y_dois
        if jogador_dois_y >= C.Y_CHAO:
            jogador_dois_y = C.Y_CHAO
            vel_y_dois = 0
            no_chao_dois = True

        jogador_um_x += delta_x_um
        jogador_dois_x += delta_x_dois

        # Desenho
        tela.blit(assets['background'], (0, 0))

        if socando_um:
            pygame.draw.rect(tela, C.VERDE, hit_box_um)
            pygame.draw.rect(tela, C.VERMELHO, hit_box_soco)
            tela.blit(assets['jogador_um_soco'], (jogador_um_x, jogador_um_y))
        else:
            pygame.draw.rect(tela, C.VERDE, hit_box_um)
            tela.blit(assets['jogador_um'], (jogador_um_x, jogador_um_y))

        if socando_dois:
            pygame.draw.rect(tela, C.VERDE, hit_box_dois)
            pygame.draw.rect(tela, C.VERMELHO, hit_box_soco_dois)
            tela.blit(assets['jogador_dois_soco'], (jogador_dois_x, jogador_dois_y))
        else:
            pygame.draw.rect(tela, C.VERDE, hit_box_dois)
            tela.blit(assets['jogador_dois'], (jogador_dois_x, jogador_dois_y))

        pygame.display.update()

    return C.MENU