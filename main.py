import pathlib
import PySimpleGUI as sg
import os
import time
import decimal
from pygame import mixer, display, event, USEREVENT
from modulos import botao, musica

mixer.init()
display.init()
mixer.music.set_endevent(USEREVENT)

def carregar_tela():
    musica_pausada = False
    musica_atual = 0
    visibilidade_volume = False
    playlist = []
    sg.theme("DarkAmber")
    color = (sg.theme_background_color(), sg.theme_background_color())
    #carrega imagens dos botões
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop, botao_volume = carregar_botoes()

    new_capa = os.getcwd()+"/modulos/cache/capa_vazia.png"

    layout_colum = [[sg.Text("0",key="-ATUAL-"), sg.Text("/"),sg.Text("0", key="-TOTAL-")],
                    [sg.Text("",key="TITULO")],
                    [sg.Image(new_capa, key= "CAPA")], #sg.Slider(range=(0, 100), size=(15, 15), visible=True, orientation="v")],
                    [sg.Text(text="00:00", key="-TEMPO-"), sg.Text("/") ,sg.Text(text="00:00" , key="TEMPO_TOTAL"),
                     sg.Button("", image_data=botao_volume, button_color=color, border_width=0, key="-BOTAO-VOLUME-"),
                     sg.Slider((0,10), default_value=10, orientation="h", visible= False, size=(10,20), enable_events=True, key="-VOLUME-")],
                    [sg.ProgressBar(max_value=99,bar_color="Black",orientation='h',s=(23, 6), k='-PBAR-', pad=(0,10))],
                    [sg.Button('', image_data=botao_voltar, button_color=color, border_width=0,key="BACK"),
                   sg.Button('', image_data=botao_avancar, button_color=color, border_width=0, key='NEXT'),
                   sg.Button('', image_data=botao_play, button_color=color, border_width=0, key='PLAY'),
                   sg.Button('', image_data=botao_pause, button_color=color, border_width=0,key="PAUSE"),
                   sg.Button('', image_data=botao_stop, button_color=color, border_width=0,key="STOP")]
                    ]

    layout = [  [sg.Menu([["Opções",["Selecionar pasta", "Selecionar musica","Limpar playslist","Sair"]]],pad=(40,0))],
                [sg.Column(layout_colum, element_justification="center")]
                ]

    janela = sg.Window("MP3 Player", layout, size=(420, 600), finalize=True, grab_anywhere=True)

    while True:
        evento, valores = janela.read(timeout=1000)
        if evento in (sg.WIN_CLOSED , "Sair", None):
            break

        #Enquanto a musica estiver tocando
        if mixer.music.get_busy() == True:
            porcenteagem = get_porcentagem(playlist, musica_atual)
            tempo = mixer.music.get_pos() / 1000
            tempo_atual_musica = time.strftime("%M:%S", time.gmtime(tempo))
            janela["-TEMPO-"].update(tempo_atual_musica)
            janela["-PBAR-"].update(tempo * porcenteagem)

        #Avança para a proxima música assim que acaba a atual
        try:
            for acabou_musica in event.get():
                if acabou_musica.type == USEREVENT:
                    mixer.music.queue(playlist[musica_atual + 1].diretorio)
                    musica_atual += 1
                    altera_musica(musica_atual, playlist, janela)
        except:
            pass

        # try:
        #     while musica_atual <= len(playlist):
        # for event in event.get():
        #     if event.type == USEREVENT:
        #         print("Ok")
        #                 # musica_atual += 1
                        # mixer.music.queue(playlist[musica_atual])
                        # print(playlist[musica_atual])
        # except:
        #     pass


        try:
            if evento == "PLAY" and not musica_pausada:
                play_musica(playlist, musica_atual)
            elif evento == "PAUSE":
                mixer.music.pause()
                musica_pausada = True
        except:
            pass


        #Se acabar a playlist e clicar em play, a playlist recomeça da primeira
        if evento == "PLAY" and musica_atual == len(playlist) - 1 and not musica_pausada:
            musica_atual = 0
            altera_musica(musica_atual, playlist, janela)

        if musica_pausada and evento == "PLAY":
            mixer.music.unpause()
            musica_pausada = False

        if evento == "STOP":
            mixer.music.stop()

        try:
            if evento == "NEXT":
                try:
                    musica_atual += 1
                    altera_musica(musica_atual, playlist, janela)
                except:
                    musica_atual = 0
                    altera_musica(musica_atual, playlist, janela)
        except:
            pass

        try:
            if evento == "BACK":
                if not musica_atual <= 0:
                    musica_atual -=1
                    altera_musica(musica_atual, playlist, janela)
                else:
                    print(musica_atual)
                    musica_atual = len(playlist) - 1
                    altera_musica(musica_atual, playlist, janela)
        except:
            pass

        try:
            if evento == "Selecionar pasta":
                pasta_ou_musica = sg.popup_get_folder('Escolha a pasta das músicas', keep_on_top=True)
                playlist, musica_atual = carrega_pasta_ou_musica(str(pasta_ou_musica + "/"), musica_atual, playlist, janela, "pasta")
        except:
            pass

        try:
            if evento == "Selecionar musica":
                pasta_ou_musica = sg.popup_get_file('Escolha sua música', keep_on_top=True)
                playlist, musica_atual = carrega_pasta_ou_musica(str(pasta_ou_musica), musica_atual, playlist, janela, "musica")
        except:
            pass

        # Limpar playlist
        if evento == "Limpar playslist":
            mixer.music.stop()
            playlist = []
            musica_atual = 0
            update_dados("", "00:00", 0, playlist, musica_atual, janela)

        # Abrir o volume
        if evento == "-BOTAO-VOLUME-":
            if not visibilidade_volume:
                janela["-VOLUME-"].update(visible=True)
                visibilidade_volume = True

            elif visibilidade_volume:
                janela["-VOLUME-"].update(visible=False)
                visibilidade_volume = False

        # Slider volume
        if evento == "-VOLUME-":
            mixer.music.set_volume(valores["-VOLUME-"] * 0.1)

    janela.close()




def carrega_pasta_ou_musica(pasta_ou_musica, musica_atual, playlist, janela, tipo):
    if tipo == "pasta":
        print(str(pasta_ou_musica))
        playlist = carregar_playlist(str(pasta_ou_musica), tipo, playlist)
    else:
        playlist = carregar_playlist(str(pasta_ou_musica),tipo, playlist)

    titulo, tempo_total, tempo_total_segundos = carregar_dados_das_musicas(musica_atual, playlist)
    update_dados(titulo, tempo_total, tempo_total_segundos, playlist, musica_atual, janela)

    return playlist, musica_atual


def update_dados(titulo, tempo_total, tempo_total_segundos, playlist, musica_atual, janela):
    try:
        try:
            if playlist[musica_atual].capa:
                new_capa = os.getcwd()+"/modulos/cache/capa.png"
            else:
                new_capa = os.getcwd()+"/modulos/cache/capa_vazia.png"
        except:
            new_capa = os.getcwd() + "/modulos/cache/capa_vazia.png"
        if len(playlist) > 0:
            janela["-ATUAL-"].update(musica_atual + 1)
            janela["-TOTAL-"].update(len(playlist))
        else:
            janela["-ATUAL-"].update(0)
            janela["-TOTAL-"].update(0)

        janela["TITULO"].update(titulo)
        janela["TEMPO_TOTAL"].update(tempo_total)
        janela["CAPA"].update(new_capa)
        janela["-PBAR-"].update(0)
        janela["-TEMPO-"].update("00:00")
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
    try:
        if tipo == "pasta":
            all_music2 = pathlib.Path(diretorio)
            for music in all_music2.glob("*.mp3"):
                print(music)
                try:
                    playlist.append(musica.Musica_Com_Metadados(music))
                except:
                    nome_da_musica = os.path.basename(music)
                    playlist.append(musica.Musica_Sem_Metadados(music, nome_da_musica))
            return playlist
        else:
            try:
                playlist.append(musica.Musica_Com_Metadados(diretorio))
                return playlist
            except:
                nome_da_musica = os.path.basename(diretorio)
                playlist.append(musica.Musica_Sem_Metadados(diretorio, nome_da_musica))
                return playlist
    except:
        pass

    return playlist

def play_musica(playlist,musica_atual):
    mixer.music.load(playlist[musica_atual].diretorio)
    try:
        for x in range(len(playlist) - 1):  # coloca na fila as restantes
            mixer.music.queue(playlist[x + 1].diretorio)
    except:
        pass
    mixer.music.play()
    return True


def carregar_botoes():
    botao_voltar = botao.Botao(os.getcwd()+"/imagens/voltar.png")
    botao_play = botao.Botao(os.getcwd()+"/imagens/play.png")
    botao_pause = botao.Botao(os.getcwd()+"/imagens/pause.png")
    botao_avancar = botao.Botao(os.getcwd()+"/imagens/proxima.png")
    botao_stop = botao.Botao(os.getcwd()+"/imagens/stop.png")
    botao_volume = botao.Botao(os.getcwd()+"/imagens/alto-falante.png")

    botao_voltar_base_64 = botao_voltar.resize_da_imagem_para_base64(65,65)
    botao_play_base_64 = botao_play.resize_da_imagem_para_base64(65,65)
    botao_pause_base_64 = botao_pause.resize_da_imagem_para_base64(65,65)
    botao_avancar_base_64 = botao_avancar.resize_da_imagem_para_base64(65, 65)
    botao_stop_base_64 = botao_stop.resize_da_imagem_para_base64(65,65)
    botao_volume_base_64 = botao_volume.resize_da_imagem_para_base64(30,30)

    return botao_voltar_base_64, botao_play_base_64, botao_pause_base_64, botao_avancar_base_64, botao_stop_base_64, botao_volume_base_64


if __name__ == "__main__":
    carregar_tela()

