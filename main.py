import PySimpleGUI as sg
import os
import time
from pygame import mixer
from aplicacao_mp3_player.modulos import botao, musica

mixer.init()

def carregar_tela():
    musica_pausada = False
    musica_atual = 0
    sg.theme("Dark")
    color = (sg.theme_background_color(), sg.theme_background_color())

    #carrega imagens dos botões
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop, botao_pastas = carregar_botoes()

    #carrega os dados iniciais da primeira musica
    artista, nome_musica, tempo_total, playlist = carregar_dados_das_musicas(musica_atual)

    #Carrega o estado atual, para quando a musica tocar pela primeira vez
    #o sistema reconheça quando é play e quando é unpause
    tocando = False

    layout_colum = [[sg.Text(artista,key="ARTISTA"),sg.Text(nome_musica,key="NOME_MUSICA")], #sg.Button("", image_data= botao_pastas, button_color=color, border_width=0)
              [sg.Image(os.getcwd()+"/modulos/cache/capa.png",)],
              [sg.Text(text="00:00", key="-TEMPO-"), sg.Text("/") ,sg.Text(text=tempo_total, key="TEMPO_TOTAL")],
              [sg.Canvas(background_color="#b8b3ad",size=(370,0))],#nova_musica.duracao_segundos_total, s=(150,3)),nova_musica.duracao_segundos_total, s=(150,3)),
              [sg.Button('', image_data=botao_voltar, button_color=color, border_width=0,key="BACK"),
               sg.Button('', image_data=botao_avancar, button_color=color, border_width=0, key='NEXT'),
               sg.Button('', image_data=botao_play, button_color=color, border_width=0, key='PLAY'),
               sg.Button('', image_data=botao_pause, button_color=color, border_width=0,key="PAUSE"),
               sg.Button('', image_data=botao_stop, button_color=color, border_width=0,key="STOP")]
    ]

    layout = [[sg.Column(layout_colum, element_justification="center")]]

    janela = sg.Window("MP3 Player", layout, size=(415, 550), finalize=True, grab_anywhere=True)

    while True:
        evento, valores = janela.read(timeout=1000)
        if evento == sg.WIN_CLOSED:
            break

        if mixer.music.get_busy() == True:
            tempo = mixer.music.get_pos() / 1000
            tempo_atual_musica = time.strftime("%M:%S", time.gmtime(tempo))
            janela["-TEMPO-"].update(tempo_atual_musica)

        if evento == "PLAY" and not musica_pausada:
            play_musica(playlist, musica_atual)
        elif evento == "PAUSE":
            mixer.music.pause()
            musica_pausada = True

        if musica_pausada and evento == "PLAY":
            mixer.music.unpause()
            musica_pausada = False

        if evento == "STOP":
            mixer.music.stop()

        if evento == "NEXT":
            musica_atual += 1
            mixer.music.unload()
            artista, nome_musica, tempo_total, playlist = carregar_dados_das_musicas(musica_atual)
            janela["ARTISTA"].update(artista)
            janela["NOME_MUSICA"].update(nome_musica)
            janela["TEMPO_TOTAL"].update(tempo_total)
            mixer.music.load(playlist[musica_atual].diretorio)
            mixer.music.play()

        if evento == "BACK":
            musica_atual -=1
            mixer.music.unload()
            artista, nome_musica, tempo_total, playlist = carregar_dados_das_musicas(musica_atual)
            janela["ARTISTA"].update(artista)
            janela["NOME_MUSICA"].update(nome_musica)
            janela["TEMPO_TOTAL"].update(tempo_total)
            mixer.music.load(playlist[musica_atual].diretorio)
            mixer.music.play()


    janela.close()


def carregar_dados_das_musicas(musica_atual):
    playlist = carregar_playlist()

    #carrega os metadados da musica (tempo, capa, artista e nome da musica)
    tempo_total = time.strftime("%M:%S", time.gmtime(playlist[musica_atual].duracao_segundos_total))
    artista, nome_musica = playlist[musica_atual].artista, playlist[musica_atual].titulo
    playlist[musica_atual].capa

    return artista, nome_musica,tempo_total, playlist


#Busca o diretorio das musicas e cria os objetos música
def carregar_playlist():
    all_music = os.listdir(os.getcwd() + "/musicas/")
    playlist = []
    for cancao in all_music:
        try:
            playlist.append(musica.Musica(os.getcwd() + "/musicas/" + cancao))
        except:
            pass
    return playlist




def play_musica(playlist,musica_atual):
    mixer.music.load(playlist[musica_atual].diretorio)
    mixer.music.play()
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

