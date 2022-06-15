import PySimpleGUI as sg
import os
import time
import decimal
from pygame import mixer, display, event, USEREVENT
from aplicacao_mp3_player.modulos import botao, musica

mixer.init()
display.init()

def carregar_tela():
    musica_pausada = False
    musica_atual = 0
    playlist = []
    sg.theme("DarkAmber")
    color = (sg.theme_background_color(), sg.theme_background_color())

    #carrega imagens dos botões
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop, botao_pastas = carregar_botoes()

    new_capa = os.getcwd()+"/modulos/cache/capa_vazia.png"

    layout_colum = [[sg.Text("0",key="-ATUAL-"), sg.Text("/"),sg.Text("0", key="-TOTAL-")],
                    [sg.Text("",key="TITULO")],
                    [sg.Image(new_capa, key= "CAPA")], #sg.Slider(range=(0, 100), size=(15, 15), visible=True, orientation="v")],
                    [sg.Text(text="00:00", key="-TEMPO-"), sg.Text("/") ,sg.Text(text="00:00" , key="TEMPO_TOTAL")],
                    [sg.ProgressBar(max_value=99,bar_color="Black",orientation='h',s=(23, 6), k='-PBAR-', pad=(0,10))],
                    [sg.Button('', image_data=botao_voltar, button_color=color, border_width=0,key="BACK"),
                   sg.Button('', image_data=botao_avancar, button_color=color, border_width=0, key='NEXT'),
                   sg.Button('', image_data=botao_play, button_color=color, border_width=0, key='PLAY'),
                   sg.Button('', image_data=botao_pause, button_color=color, border_width=0,key="PAUSE"),
                   sg.Button('', image_data=botao_stop, button_color=color, border_width=0,key="STOP")]
                    ]

    layout = [  [sg.Menu([["Opções",["Selecionar Pasta", "Selecionar Musica"]],["Sair"]],pad=(40,0))],
                [sg.Column(layout_colum, element_justification="center")]
                ]

    janela = sg.Window("MP3 Player", layout, size=(420, 600), finalize=True, grab_anywhere=True)

    while True:
        evento, valores = janela.read(timeout=1000)
        print(evento,valores)
        if evento in (sg.WIN_CLOSED , "Sair", None):
            break

        if mixer.music.get_busy() == True:
            porcenteagem = get_porcentagem(playlist, musica_atual)
            tempo = mixer.music.get_pos() / 1000
            tempo_atual_musica = time.strftime("%M:%S", time.gmtime(tempo))
            janela["-TEMPO-"].update(tempo_atual_musica)
            janela["-PBAR-"].update(tempo * porcenteagem)

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
        if event.get() == USEREVENT:
            print("OK")

        if evento == "Selecionar Pasta":
            pasta_ou_musica = sg.popup_get_folder('Escolha a pasta das músicas', keep_on_top=True)
            playlist, musica_atual = carrega_pasta_ou_musica(str(pasta_ou_musica), musica_atual, playlist, janela, "pasta")

        if evento == "Selecionar Musica":
            pasta_ou_musica = sg.popup_get_file('Escolha sua música', keep_on_top=True)
            playlist, musica_atual = carrega_pasta_ou_musica(str(pasta_ou_musica), musica_atual, playlist, janela, "musica")

    janela.close()


#Tenho que verificar se a playlist está vazia
def carrega_pasta_ou_musica(pasta_ou_musica, musica_atual, playlist, janela, tipo):
    if tipo == "pasta":
        playlist = carregar_playlist(str(pasta_ou_musica), tipo, playlist)
    else:
        playlist = carregar_playlist(str(pasta_ou_musica),tipo, playlist)

    titulo, tempo_total, tempo_total_segundos = carregar_dados_das_musicas(musica_atual, playlist)
    update_dados(titulo, tempo_total, tempo_total_segundos, playlist, musica_atual, janela)

    return playlist, musica_atual


def update_dados(titulo, tempo_total, tempo_total_segundos, playlist, musica_atual, janela):
    try:
        if playlist[musica_atual].capa:
            new_capa = os.getcwd()+"/modulos/cache/capa.png"
        else:
            new_capa = os.getcwd()+"/modulos/cache/capa_vazia.png"

        janela["-ATUAL-"].update(musica_atual)
        janela["-TOTAL-"].update(len(playlist) - 1)
        janela["TITULO"].update(titulo)
        janela["TEMPO_TOTAL"].update(tempo_total)
        janela["CAPA"].update(new_capa)
        janela["-PBAR-"].update(tempo_total_segundos)
    except:
        pass

def get_porcentagem(playlist, musica_atual):
    porcenteagem = decimal.Decimal(100) / decimal.Decimal(playlist[musica_atual].duracao_segundos_total)
    return float(porcenteagem)

def altera_musica(musica_atual, playlist, janela):
    mixer.music.unload()
    mixer.music.load(playlist[musica_atual].diretorio)
    mixer.music.play()

    titulo, tempo_total, tempo_total_segundos = carregar_dados_das_musicas(musica_atual, playlist)

    update_dados(titulo, tempo_total, tempo_total_segundos, playlist, musica_atual, janela)



    #carrega os metadados da musica (titulo, tempo da musica)
def carregar_dados_das_musicas(musica_atual, playlist):
    try:
        tempo_total = time.strftime("%M:%S", time.gmtime(playlist[musica_atual].duracao_segundos_total))
        titulo = playlist[musica_atual].titulo
        tempo_total_segundo = int(playlist[musica_atual].duracao_segundos_total)
    except:
        titulo, tempo_total, tempo_total_segundo = "", "00:00", 0


    return titulo, tempo_total, tempo_total_segundo


#Busca o diretorio das musicas e cria os objetos música
def carregar_playlist(diretorio, tipo, playlist):

    if tipo == "pasta":
        try:
            all_music = os.listdir(diretorio)
            for music in all_music:
                try:
                    playlist.append(musica.Musica_Com_Metadados(os.getcwd()+"/musicas/" + music))
                except:
                    playlist.append(musica.Musica_Sem_Metadados(os.getcwd()+"/musicas/" + music, music))
        except:
            pass
    else:
        try:
            playlist.append(musica.Musica_Com_Metadados(diretorio))
        except:
            playlist.append(musica.Musica_Sem_Metadados(diretorio,"teste"))

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

