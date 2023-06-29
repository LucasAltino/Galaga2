import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Galaga")
pag = "inicio"

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fundo
fundo_img = pygame.image.load("fundo.png")
fundo = pygame.transform.scale(fundo_img, (largura_tela, altura_tela))

# Função para desenhar o fundo na tela
def desenhar_fundo():
    tela.blit(fundo, (0, 0))

# Jogador
jogador_img = pygame.image.load("nave.png")
jogador_largura = 40
jogador_altura = 40
jogador_x = largura_tela // 2 - jogador_largura // 2
jogador_y = altura_tela - jogador_altura - 10
jogador_velocidade = 7

# Tiro
tiro_img = pygame.image.load("tiro.png")
tiro_largura = 25
tiro_altura = 35
tiro_x = 0
tiro_y = 0
tiro_velocidade_jogador = 10
tiro_velocidade_inimigo1 = 0.5
tiro_velocidade_inimigo2 = 1.5
tiro_disparado_jogador = False
tiro_disparado_inimigo1 = False
tiro_disparado_inimigo2 = False
tiro_pronto_jogador = True
tiro_pronto_inimigo1 = True
tiro_pronto_inimigo2 = True

# Inimigos
inimigo_img = pygame.image.load("inimigo.png")
inimigo2_img = pygame.image.load("inimigo2.png")
num_inimigos = 9
inimigos = []
inimigo_largura = 40
inimigo_altura = 40
inimigo_velocidade = 3

inimigos2 = []
inimigo2_largura = 40
inimigo2_altura = 40
inimigo2_velocidade = 4

for _ in range(num_inimigos):
    inimigo_x = random.randint(0, largura_tela - inimigo_largura)
    inimigo_y = random.randint(-altura_tela, 0)
    inimigos.append([inimigo_x, inimigo_y, False])

for _ in range(num_inimigos):
    inimigo2_x = random.randint(0, largura_tela - inimigo2_largura)
    inimigo2_y = random.randint(-altura_tela, 0)
    inimigos2.append([inimigo2_x, inimigo2_y, False])

# Pontuação
score = 0
pontuacao_fonte = pygame.font.Font(None, 36)

# Função para desenhar o jogador na tela
def desenhar_jogador(x, y):
    tela.blit(pygame.transform.scale(jogador_img, (jogador_largura, jogador_altura)), (x, y))

# Função para desenhar o tiro na tela
def desenhar_tiro(x, y):
    tela.blit(pygame.transform.scale(tiro_img, (tiro_largura, tiro_altura)), (x, y))

# Função para desenhar os inimigos na tela
def desenhar_inimigos():
    for inimigo in inimigos:
        inimigo_x, inimigo_y, atingido = inimigo
        if not atingido:
            tela.blit(pygame.transform.scale(inimigo_img, (inimigo_largura, inimigo_altura)), (inimigo_x, inimigo_y))

# Função para desenhar os inimigos do tipo 2 na tela
def desenhar_inimigos2():
    for inimigo in inimigos2:
        inimigo_x, inimigo_y, atingido = inimigo
        if not atingido:
            tela.blit(pygame.transform.scale(inimigo2_img, (inimigo2_largura, inimigo2_altura)), (inimigo_x, inimigo_y))

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and tiro_pronto_jogador:
                if pag == "inicio":
                    pag = "jogo"
                else:
                    tiro_disparado_jogador = True
                    tiro_x = jogador_x + jogador_largura // 2 - tiro_largura // 2
                    tiro_y = jogador_y - tiro_altura
                    tiro_pronto_jogador = False

    # Movimentação do jogador
    teclas_pressionadas = pygame.key.get_pressed()
    if teclas_pressionadas[pygame.K_LEFT]:
        jogador_x -= jogador_velocidade
    if teclas_pressionadas[pygame.K_RIGHT]:
        jogador_x += jogador_velocidade

    # Limitar a posição do jogador dentro da tela
    if jogador_x < 0:
        jogador_x = 0
    elif jogador_x > largura_tela - jogador_largura:
        jogador_x = largura_tela - jogador_largura

    # Movimentação do tiro do jogador
    if tiro_disparado_jogador:
        tiro_y -= tiro_velocidade_jogador
        if tiro_y < 0:
            tiro_disparado_jogador = False
            tiro_pronto_jogador = True

    # Movimentação dos inimigos
    for i in range(num_inimigos):
        inimigo_x, inimigo_y, atingido = inimigos[i]
        if not atingido:
            inimigo_y += inimigo_velocidade
            if inimigo_y > altura_tela:
                inimigo_x = random.randint(0, largura_tela - inimigo_largura)
                inimigo_y = random.randint(-altura_tela, 0)
                inimigos[i] = [inimigo_x, inimigo_y, False]
            inimigos[i] = [inimigo_x, inimigo_y, atingido]

    # Movimentação dos inimigos do tipo 2
    for i in range(num_inimigos):
        inimigo2_x, inimigo2_y, atingido = inimigos2[i]
        if not atingido:
            inimigo2_y += inimigo2_velocidade
            if inimigo2_y > altura_tela:
                inimigo2_x = random.randint(0, largura_tela - inimigo2_largura)
                inimigo2_y = random.randint(-altura_tela, 0)
                inimigos2[i] = [inimigo2_x, inimigo2_y, False]
            inimigos2[i] = [inimigo2_x, inimigo2_y, atingido]

    # Colisão do tiro do jogador com os inimigos
    for i in range(num_inimigos):
        inimigo_x, inimigo_y, atingido = inimigos[i]
        if not atingido and tiro_disparado_jogador:
            if tiro_x + tiro_largura > inimigo_x and tiro_x < inimigo_x + inimigo_largura and tiro_y < inimigo_y + inimigo_altura:
                tiro_disparado_jogador = False
                tiro_pronto_jogador = True
                inimigo_x = random.randint(0, largura_tela - inimigo_largura)
                inimigo_y = random.randint(-altura_tela, 0)
                inimigos[i] = [inimigo_x, inimigo_y, True]
                score += 1

    # Colisão do tiro do jogador com os inimigos do tipo 2
    for i in range(num_inimigos):
        inimigo2_x, inimigo2_y, atingido = inimigos2[i]
        if not atingido and tiro_disparado_jogador:
            if tiro_x + tiro_largura > inimigo2_x and tiro_x < inimigo2_x + inimigo2_largura and tiro_y < inimigo2_y + inimigo2_altura:
                tiro_disparado_jogador = False
                tiro_pronto_jogador = True
                inimigo2_x = random.randint(0, largura_tela - inimigo2_largura)
                inimigo2_y = random.randint(-altura_tela, 0)
                inimigos2[i] = [inimigo2_x, inimigo2_y, True]
                score += 1
     # Verificar colisões
    jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)
    tiro_rect = pygame.Rect(tiro_x, tiro_y, tiro_largura, tiro_altura)
    for inimigo in inimigos:
        inimigo_rect = pygame.Rect(inimigo[0], inimigo[1], inimigo_largura, inimigo_altura)
        if jogador_rect.colliderect(inimigo_rect):
            rodando = False
        if tiro_disparado_jogador and tiro_rect.colliderect(inimigo_rect):
            tiro_disparado_jogador = False
            tiro_pronto_jogador = True
            inimigo[2] = True

    for inimigo2 in inimigos2:
        inimigo2_rect = pygame.Rect(inimigo2[0], inimigo2[1], inimigo2_largura, inimigo2_altura)
        if jogador_rect.colliderect(inimigo2_rect):
            rodando = False
        if tiro_disparado_jogador and tiro_rect.colliderect(inimigo2_rect):
            tiro_disparado_jogador = False
            tiro_pronto_jogador = True
            inimigo2[2] = True

    if pag == "inicio":
        # Exibir pontuação no canto superior esquerdo
        pontuacao_texto = pontuacao_fonte.render("Precione ESPAÇO para jogar! ", True, BRANCO)
        tela.blit(pontuacao_texto, (largura_tela/2 - 180, altura_tela/2 - 30))
    else:
        # Desenhar elementos na tela
        desenhar_fundo()
        desenhar_jogador(jogador_x, jogador_y)
        desenhar_jogador(jogador_x, jogador_y)
        if tiro_disparado_jogador:
            desenhar_tiro(tiro_x, tiro_y)
        desenhar_inimigos()
        desenhar_inimigos2()

        # Exibir pontuação no canto superior esquerdo
        pontuacao_texto = pontuacao_fonte.render("Pontuação: " + str(score), True, BRANCO)
        tela.blit(pontuacao_texto, (10, 10))

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)

# Encerramento do Pygame
pygame.quit()
