from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO
import os

class Musica:
    def __init__(self, diretorio, titulo, capa, duracao):
        self._diretorio = diretorio
        self._titulo = titulo
        self._capa = capa
        self._duracao = duracao

    @property
    def diretorio(self):
        return self._diretorio

    @property
    def titulo(self):
        return self._titulo

    @property
    def capa(self):
        return self._capa

    @property
    def duracao_segundos_total(self):
        return self._duracao

    def duracao(self):
        tempo = int(self.duracao_segundos_total)
        tempo %= 3600
        minutos = tempo // 60
        tempo %= 60
        segundos = tempo
        return minutos, segundos


class Musica_Com_Metadados(Musica):
    def __init__(self, diretorio, titulo):
        self._musica = MP3(diretorio)
        super().__init__(diretorio=diretorio, titulo=titulo, capa=self._musica.get("APIC:").data, duracao=self._musica.info.length)

    @property
    def capa(self):
        buffer = super().capa
        carrega_foto = BytesIO(buffer)
        imagem = Image.open(carrega_foto).resize((335,375))
        imagem.save(os.getcwd()+"/modulos/cache/capa.png")
        return True

class Musica_Sem_Metadados(Musica):
    def __init__(self, diretorio, titulo):
        duracao = MP3(diretorio)
        super().__init__(diretorio=diretorio, titulo=titulo, capa=False, duracao=duracao.info.length)



