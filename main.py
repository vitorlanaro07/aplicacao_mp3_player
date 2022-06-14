import PySimpleGUI as sg
import os
import time
from pygame import mixer
from aplicacao_mp3_player.modulos import botao, musica

mixer.init()

def carregar_tela():
    musica_pausada = False
    musica_atual = 0
    sg.theme("DarkAmber")
    color = (sg.theme_background_color(), sg.theme_background_color())

    #carrega imagens dos botões
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop, botao_pastas = carregar_botoes()

    #Carrega Playlist
    playlist = carregar_playlist()

    titulo, tempo_total, tempo_total_segundo = carregar_dados_das_musicas(musica_atual, playlist)
    if playlist[musica_atual].capa:
        new_capa = os.getcwd()+"/modulos/cache/capa.png"
    else:
        new_capa = os.getcwd()+"/modulos/cache/capa_vazia.png"

    layout_colum = [[sg.Text(musica_atual,key="-ATUAL-"), sg.Text("/"),sg.Text(len(playlist)-1)],
                    [sg.Text(titulo,key="TITULO")], #sg.Button("", image_data= botao_pastas, button_color=color, border_width=0)
                    [sg.Image(new_capa, key= "CAPA")],
                    [sg.Text(text="00:00", key="-TEMPO-"), sg.Text("/") ,sg.Text(text=tempo_total, key="TEMPO_TOTAL")],
                    [sg.ProgressBar(tempo_total_segundo,relief="RELIEF_SUNKEN" ,bar_color="Black",orientation='h',s=(23, 6), k='-PBAR-', pad=(0,10))],
                    [sg.Button('', image_data=botao_voltar, button_color=color, border_width=0,key="BACK"),
                   sg.Button('', image_data=botao_avancar, button_color=color, border_width=0, key='NEXT'),
                   sg.Button('', image_data=botao_play, button_color=color, border_width=0, key='PLAY'),
                   sg.Button('', image_data=botao_pause, button_color=color, border_width=0,key="PAUSE"),
                   sg.Button('', image_data=botao_stop, button_color=color, border_width=0,key="STOP")]
                    ]

    layout = [[sg.Column(layout_colum, element_justification="center")]]

    janela = sg.Window("MP3 Player", layout, size=(415, 585), finalize=True, grab_anywhere=True)

    while True:
        evento, valores = janela.read(timeout=1000)
        if evento == sg.WIN_CLOSED:
            break

        if mixer.music.get_busy() == True:
            tempo = mixer.music.get_pos() / 1000
            tempo_atual_musica = time.strftime("%M:%S", time.gmtime(tempo))
            janela["-TEMPO-"].update(tempo_atual_musica)
            janela["-PBAR-"].update(tempo)

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
            try:
                musica_atual += 1
                altera_musica(musica_atual, playlist, janela)
            except:
                musica_atual = 0
                altera_musica(musica_atual, playlist, janela)

        if evento == "BACK":
            if not musica_atual <= 0:
                musica_atual -=1
                altera_musica(musica_atual, playlist, janela)
            else:
                print(musica_atual)
                musica_atual = len(playlist) - 1
                altera_musica(musica_atual, playlist, janela)


    janela.close()

def altera_musica(musica_atual, playlist, janela):
    mixer.music.unload()
    mixer.music.load(playlist[musica_atual].diretorio)
    mixer.music.play()

    titulo, tempo_total, tempo_total_segundos = carregar_dados_das_musicas(musica_atual, playlist)

    if playlist[musica_atual].capa:
        new_capa = os.getcwd()+"/modulos/cache/capa.png"
    else:
        new_capa = os.getcwd()+"/modulos/cache/capa_vazia.png"

    janela["-ATUAL-"].update(musica_atual)
    janela["TITULO"].update(titulo)
    janela["TEMPO_TOTAL"].update(tempo_total)
    janela["CAPA"].update(new_capa)


    #carrega os metadados da musica (titulo, tempo da musica)
def carregar_dados_das_musicas(musica_atual, playlist):
    tempo_total = time.strftime("%M:%S", time.gmtime(playlist[musica_atual].duracao_segundos_total))
    titulo = playlist[musica_atual].titulo
    tempo_total_segundo = int(playlist[musica_atual].duracao_segundos_total)

    return titulo, tempo_total, tempo_total_segundo


#Busca o diretorio das musicas e cria os objetos música
def carregar_playlist():
    all_music = os.listdir(os.getcwd()+"/musicas/")
    playlist = []
    for music in all_music:
        try:
            playlist.append(musica.Musica_Com_Metadados(os.getcwd()+"/musicas/" + music))
        except:
            playlist.append(musica.Musica_Sem_Metadados(os.getcwd()+"/musicas/" + music, music))
    return playlist


def play_musica(playlist,musica_atual):
    mixer.music.load(playlist[musica_atual].diretorio)
    #mixer.music.queue(playlist[musica_atual + 1].diretorio)
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

