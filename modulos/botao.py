import os
from PIL import Image
import base64
from io import BytesIO

class Botao:
    def __init__(self, diretorio):
        self.__diretorio = diretorio
        self.__imagem = Image.open(diretorio)


    @property
    def diretorio(self):
        return self.__diretorio

    @property
    def imagem(self):
        return self.__imagem

    def resize_da_imagem_para_base64(self, largura, altura):
        nova_resolucao = (largura, altura)
        buffer = BytesIO()
        self.imagem.resize((nova_resolucao)).save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())


