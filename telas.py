import pygame
import constantes as C
from jogador import Jogador
import regras_jogo as RJ

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

def loop_jogo(tela, assets, clock):
    jogador_um = Jogador(
        x=C.P1_START_X,
        y=C.P1_START_Y,
        controles=C.P1_CONTROLES,
        assets=assets,
        tipo="um",
        vida=100,
        ataque=100
    )
    jogador_dois = Jogador(
        x=C.P2_START_X,
        y=C.P2_START_Y,
        controles=C.P2_CONTROLES,
        assets=assets,
        tipo="dois",
        vida=100,
        ataque=5
    )

    while True:
        clock.tick(C.FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return C.SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return C.MENU

        teclas = pygame.key.get_pressed()
        jogador_um.atualizar(teclas)
        jogador_dois.atualizar(teclas)
        RJ.colisao_corpo(jogador_um, jogador_dois)
        RJ.limites_tela(jogador_um, C.LARGURA_JANELA)
        RJ.limites_tela(jogador_dois, C.LARGURA_JANELA)
        # Hitboxes
        hb_um = jogador_um.get_hitbox_jogador()
        hb_soco_um = jogador_um.get_hitbox_soco()
        hb_dois = jogador_dois.get_hitbox_jogador()
        hb_soco_dois = jogador_dois.get_hitbox_soco()

        RJ.aplicar_dano(jogador_um, jogador_dois, hb_soco_um, hb_dois)
        RJ.aplicar_dano(jogador_dois, jogador_um, hb_soco_dois, hb_um)

        vencedor = RJ.checar_fim_de_jogo(jogador_um, jogador_dois)
        if vencedor:
            print(f'Jogador {vencedor} venceu!')
            return C.MENU  # por enquanto volta ao menu, depois pode virar tela de vitória
        # Desenho
        tela.blit(assets['background'], (0, 0))

        if C.DEBUG:
            pygame.draw.rect(tela, C.VERDE, hb_um, 2)
            pygame.draw.rect(tela, C.VERDE, hb_dois, 2)
            if jogador_um.socando:
                pygame.draw.rect(tela, C.VERMELHO, hb_soco_um, 2)
            if jogador_dois.socando:
                pygame.draw.rect(tela, C.VERMELHO, hb_soco_dois, 2)

        jogador_um.desenhar(tela)
        jogador_dois.desenhar(tela)

        pygame.display.update()