import pygame as pg

class Botao:
    def __init__(self, imagem, escala, x , y):
        largura = imagem.get_width()
        altura = imagem.get_height()
        self.imagem = pg.transform.scale(imagem,(int(largura * escala), int(altura * escala)))
        self.clicked = False
        self.rect = imagem.get_rect()
        self.rect.topleft = (x, y)

    def get_surface(self):
        return self.imagem

    def draw (self, janela):
        click = None
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == True and self.clicked == False:
                click = True
                self.clicked = True

        if pg.mouse.get_pressed()[0] == False:
            self.clicked = False

        janela.blit(self.imagem, ((self.rect.x), (self.rect.y)))
        return click

