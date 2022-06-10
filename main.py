import PySimpleGUI as sg
import os
from pygame import mixer
from aplicacao_mp3_player.modulos import botao, musica

def carregar_tela():
    musicas = ["01 Ogum (Acústico).mp3", "01 - Oxalá.mp3"]
    x=0
    sg.theme("Dark")
    color = (sg.theme_background_color(), sg.theme_background_color())
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop, botao_pastas = carregar_botoes()
    nova_musica = musica.Musica(os.getcwd()+"/musicas/"+musicas[x]) #
    artista, nome_musica = nova_musica.artista, nova_musica.titulo
    nova_musica.capa
    mixer.init()

    layout = [[sg.Text(text="{} - {}".format(artista, nome_musica),pad=(50,20))], #sg.Button("", image_data= botao_pastas, button_color=color, border_width=0)
              [sg.Image(os.getcwd()+"/modulos/cache/capa.png",pad=(25,15),)],
              [sg.Button('', image_data=botao_voltar, button_color=color, border_width=0,key="BACK"),
               sg.Button('', image_data=botao_avancar, button_color=color, border_width=0, key='NEXT'),
               sg.Button('', image_data=botao_play, button_color=color, border_width=0, key='PLAY'),
               sg.Button('', image_data=botao_pause, button_color=color, border_width=0,key="PAUSE"),
               sg.Button('', image_data=botao_stop, button_color=color, border_width=0,key="STOP")]
    ]

    janela = sg.Window("MP3 Player", layout, size=(400, 600), finalize=True)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED:
            break
        if evento == "PLAY":
            mixer.music.load(os.getcwd()+"/musicas/"+musicas[0])
            mixer.music.play(-1)
        if evento == "PAUSE":
            mixer.music.pause()
        if evento == "NEXT:":
            mixer.music.stop()
            mixer.music.load(os.getcwd()+"/musicas/"+musicas[1])
            mixer.music.play(-1)
        print(evento, valores)
        janela.refresh()

    janela.close()


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

