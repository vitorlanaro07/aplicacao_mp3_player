import PySimpleGUI as sg
import os
import time
from pygame import mixer
from aplicacao_mp3_player.modulos import botao, musica

mixer.init()

def carregar_tela():
    musicas = ["02 Leis Próprias (Acústico).mp3", "01 - Oxalá.mp3"]
    x=1
    sg.theme("Dark")
    color = (sg.theme_background_color(), sg.theme_background_color())

    #carrega imagens dos botões
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop, botao_pastas = carregar_botoes()

    #carrega a musica
    nova_musica = musica.Musica(os.getcwd()+"/musicas/"+musicas[x]) #

    #carrega os metadados da musica
    tempo_total = time.strftime("%M:%S", time.gmtime(nova_musica.duracao_segundos_total))
    print(tempo_total)


    artista, nome_musica = nova_musica.artista, nova_musica.titulo
    nova_musica.capa




    #Carrega o estado atual, para quando a musica tocar pela primeira vez
    #o sistema reconheça quando é play e quando é unpause
    estado_atual = False

    layout_colum = [[sg.Text(text="{} - {}".format(artista, nome_musica))], #sg.Button("", image_data= botao_pastas, button_color=color, border_width=0)
              [sg.Image(os.getcwd()+"/modulos/cache/capa.png",)],
              [sg.Text(text="00:00", key="-TEMPO-"), sg.Text("/") ,sg.Text(text=tempo_total)],
              [sg.Canvas(background_color="#b8b3ad",size=(370,0))],#nova_musica.duracao_segundos_total, s=(150,3)),nova_musica.duracao_segundos_total, s=(150,3)),
              [sg.Button('', image_data=botao_voltar, button_color=color, border_width=0,key="BACK"),
               sg.Button('', image_data=botao_avancar, button_color=color, border_width=0, key='NEXT'),
               sg.Button('', image_data=botao_play, button_color=color, border_width=0, key='PLAY'),
               sg.Button('', image_data=botao_pause, button_color=color, border_width=0,key="PAUSE"),
               sg.Button('', image_data=botao_stop, button_color=color, border_width=0,key="STOP")]
    ]

    layout = [[sg.Column(layout_colum, element_justification="center")]]

    janela = sg.Window("MP3 Player", layout, size=(415, 550), finalize=True, grab_anywhere=True)
    teste = False
    while True:
        evento, valores = janela.read(timeout=1000)
        if evento == sg.WIN_CLOSED:
            break

        if evento == "PLAY" and not estado_atual:
            estado_atual = play_musica()
        else:
            mixer.music.unpause()

        if evento == "PAUSE":
            mixer.music.pause()

        if mixer.music.get_busy() == True:
            tempo = mixer.music.get_pos() / 1000
            tempo_atual_musica = time.strftime("%M:%S", time.gmtime(tempo))
            janela["-TEMPO-"].update(tempo_atual_musica)

    janela.close()


def play_musica():
    mixer.music.load(os.getcwd() + "/musicas/01 - Oxalá.mp3")
    mixer.music.play(-1)
    return True

def carregar_botoes():
    botao_voltar = botao.Botao(os.getcwd()+"/imagens/voltar.png")
    botao_play = botao.Botao(os.getcwd()+"/imagens/play.png")
    botao_pause = botao.Botao(os.getcwd()+"/imagens/pause.png")
    botao_avancar = botao.Botao(os.getcwd()+"/imagens/proxima.png")
    botao_stop = botao.Botao(os.getcwd()+"/imagens/stop.png")
    botao_pastas = botao.Botao(os.getcwd()+"/imagens/pastas.png")

    botao_voltar_base_64 = botao_voltar.resize_da_imagem_para_base64(65,65)
    botao_play_base_64 = botao_play.resize_da_imagem_para_base64(65,65)
    botao_pause_base_64 = botao_pause.resize_da_imagem_para_base64(65,65)
    botao_avancar_base_64 = botao_avancar.resize_da_imagem_para_base64(65, 65)
    botao_stop_base_64 = botao_stop.resize_da_imagem_para_base64(65,65)
    botao_pastas_base_64 = botao_pastas.resize_da_imagem_para_base64(40,40)

    return botao_voltar_base_64, botao_play_base_64, botao_pause_base_64, botao_avancar_base_64, botao_stop_base_64, botao_pastas_base_64


if __name__ == "__main__":
    carregar_tela()

