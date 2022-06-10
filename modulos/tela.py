import PySimpleGUI as sg
import botao

def carregar_tela():
    sg.theme("Dark")
    color = (sg.theme_background_color(), sg.theme_background_color())
    botao_voltar, botao_play, botao_pause, botao_avancar, botao_stop= carregar_botoes()

    layout = [[sg.Text("Nome Musica", pad=(137,15))],
              [sg.Image("../imagens/capa.png",pad=(25,15))],
              [sg.Button('',image_data= botao_voltar ,button_color=color, border_width=0),
               sg.Button('',image_data=botao_avancar,button_color=color, border_width=0),
               sg.Button('',image_data=botao_play,button_color=color, border_width=0),
               sg.Button('',image_data=botao_pause,button_color=color, border_width=0),
               sg.Button('',image_data=botao_stop,button_color=color, border_width=0)]
    ]

    janela = sg.Window("MP3 Player", layout, size=(400, 600), finalize=True)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED:
            break

    janela.close()

def carregar_botoes():
    botao_voltar = botao.Botao("../imagens/voltar.png")
    botao_play = botao.Botao("../imagens/play.png")
    botao_pause = botao.Botao("../imagens/pause.png")
    botao_avancar = botao.Botao("../imagens/proxima.png")
    botao_stop = botao.Botao("../imagens/stop.png")

    botao_voltar_base_64 = botao_voltar.resize_da_imagem_para_base64(65,65)
    botao_play_base_64 = botao_play.resize_da_imagem_para_base64(65,65)
    botao_pause_base_64 = botao_pause.resize_da_imagem_para_base64(65,65)
    botao_avancar_base_64 = botao_avancar.resize_da_imagem_para_base64(65, 65)
    botao_stop_base_64 = botao_stop.resize_da_imagem_para_base64(65,65)

    return botao_voltar_base_64, botao_play_base_64, botao_pause_base_64, botao_avancar_base_64, botao_stop_base_64



if __name__ == "__main__":
    carregar_tela()




