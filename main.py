import os
import time

import pygame as pg
from modulos import botao, musicas


def main():
    janela.fill(color[0])
    pg.draw.rect(janela, color[1], desenho)
    iniciar_mixer()
    musica = "musicas/sound.mp3"
    musica_inicializou = False
    janela.blit(imagem_capa_musica, (30, 50))
    # aplicacao
    rodando = True
    pausou = False

    while rodando:
        pos = pg.mixer.music.get_pos() / 1000
        print("Tempo:", pos)
        if not pausou:
            if botao_start.draw(janela):
                inicializar(musica)
        if botao_pause.draw(janela):
            pausar()
            pausou = True
            print("Pause")




        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False

        pg.display.update()
    pg.quit()

pg.init()

#constantes
desenho =((30,50),(335,375))
color = ((90, 178, 219), (90, 213, 219))

#janela
janela_largura = 400
janela_altura = 600
janela = pg.display.set_mode((janela_largura, janela_altura))
pg.display.set_caption("Mp3 Player")

#botoes
imagem_botao_start = pg.image.load("imagens/botao-play.png").convert_alpha()
imagem_botao_avancar = pg.image.load("imagens/avanco-rapido.png").convert_alpha()
imagem_botao_retroceder = pg.image.load("imagens/voltar.png").convert_alpha()
imagem_botao_pausa = pg.image.load("imagens/botao-de-pausa.png").convert_alpha()
imagem_capa_musica = pg.image.load("imagens/capa.png").convert_alpha()

botao_retroceder = botao.Botao(imagem_botao_retroceder, 0.55, 0, 470)
botao_avancar = botao.Botao(imagem_botao_avancar, 0.55, 100, 470)
botao_start = botao.Botao(imagem_botao_start, 0.55, 200, 470)
botao_pause = botao.Botao(imagem_botao_pausa,0.55, 300, 470)




def inicializar (musica):
    pg.mixer.music.load(musica)
    pg.mixer.music.play(0)
    pos = pg.mixer.music.get_pos()/1000
    print(pos)

def pausar ():
    pg.mixer.music.pause()


def get_mixer_args():
    pg.mixer.init()
    freq, size, chan = pg.mixer.get_init()
    return freq, size, chan

def iniciar_mixer():
    BUFFER = 3072
    FREQ, SIZE, CHAN = get_mixer_args()
    pg.mixer.init(FREQ, SIZE, CHAN, BUFFER)
    print("Mixer inicilizado")


if __name__ == "__main__":
    main()