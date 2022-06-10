from modulos import tela, botao
import os, glob



def main():
    janela = tela.Tela()

    while True:
        evento, valores = janela
        if evento == sg.WIN_CLOSED:
            break
    self.janela.close()
    display = tela.Tela()

def seleciona_as_musicas():
    pastas_de_musicas = os.chdir("musicas/")    #diretorio
    todas_musicas = []
    for musicas in glob.glob("*.mp3"):
        todas_musicas.append(musicas)

    return todas_musicas




if __name__ == "__main__":
    main()