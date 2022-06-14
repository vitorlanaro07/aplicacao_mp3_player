import os
import pygame
import time

pygame.mixer.init()
pygame.display.init()

screen = pygame.display.set_mode ( ( 420 , 240 ) )

all_music = os.listdir(os.getcwd()+"/musicas/")
playlist = []
for musica in all_music:
    playlist.append(os.getcwd()+"/musicas/"+musica)



pygame.mixer.music.load ( playlist.pop() )  # Get the first track from the playlist
pygame.mixer.music.queue ( playlist.pop() ) # Queue the 2nd song
pygame.mixer.music.set_endevent (  )    # Setup the end track event
pygame.mixer.music.play()           # Play the music
print(playlist)
running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.USEREVENT:    # A track has ended
         if len ( playlist ) > 0:       # If there are more tracks in the queue...
            pygame.mixer.music.queue ( playlist.pop() ) # Q




