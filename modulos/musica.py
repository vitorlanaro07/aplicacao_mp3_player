import PIL.ImageTransform
from mutagen.mp3 import MP3
from PIL import Image, ImageTransform
from io import BytesIO
import base64
import os

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
        buffer = self.__capa
        capa = BytesIO(buffer)
        imagem = Image.open(capa).resize((335,375))
        imagem.save(os.getcwd()+"/modulos/cache/capa.png")


    def duracao(self):
        tempo = int(self.duracao_segundos_total)
        tempo %= 3600
        minutos = tempo // 60
        tempo %= 60
        segundos = tempo
        return minutos, segundos

#
#
# musica = Musica("../musicas/01 - Oxalá.mp3")
# #
# print(musica.capa)





