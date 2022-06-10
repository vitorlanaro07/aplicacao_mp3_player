from mutagen.mp3 import MP3

from PIL import Image

class Musica:
    def __init__(self, diretorio):
        self.__diretorio = diretorio
        self.__musica = MP3(diretorio)
        self.__duracao = self.__musica.info.length
        self.__titulo = self.__musica.get("TIT2")
        self.__ano = self.__musica.get("TDRC")
        self.__artista = self.__musica.get("TPE1")
        self.__capa = self.__musica.get("APIC:").data

    @property
    def diretorio(self):
        return self.__diretorio

    @property
    def duracao_segundos_total(self):
        return self.__duracao

    @property
    def titulo(self):
        return self.__titulo


    @property
    def ano(self):
        return self.__ano


    @property
    def artista(self):
        return self.__artista


    @property
    def capa(self):
        return self.__capa


    def duracao(self):
        tempo = int(self.duracao_segundos_total)
        tempo %= 3600
        minutos = tempo // 60
        tempo %= 60
        segundos = tempo
        return minutos, segundos

"""
                              Para Testes

# musica = Musica("../musicas/02 Leis Próprias (Acústico).mp3")
# minutos, segundo = musica.duracao()
# print("{} - {}. Tempo: {:02}:{:02}".format(musica.artista, musica.titulo, minutos, segundo))

"""


