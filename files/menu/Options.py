import pygame
from files.save.save import save, read
from files.menu.menu import Menu
from files.modoIA.modo_ia import ModoIa
from files.modoIA.env_RL import envRL


class Options:
    def __init__(self):
        self.finish_options = False
        self.timer = pygame.time.get_ticks()
        self.alpha = 255
        self.intro_state=-1
        self.introduccion_proyecto = pygame.image.load("sprites/menu/logos/intro_proyecto_2.png").convert_alpha()
    def update(self, App):
        dims = App.options_image.get_rect()
        dims_proyecto = App.introduccion_proyecto.get_rect()
        App.options_image.set_alpha(self.alpha)

        if App.loaded:
            App.surface.blit(App.options_image, (App.dimentions[0]/2 - dims.w/2, App.dimentions[1]/2 - dims.h/2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                
                App.ia_control=True
                
                self.finish(App)
            elif keys[pygame.K_2]:
                
                App.only_detection=True
                
                self.finish(App)
                
            elif keys[pygame.K_3]:
                self.finish(App)
        else:
            App.surface.blit(self.introduccion_proyecto, (App.dimentions[0]/2 - dims_proyecto.w/2, App.dimentions[1]/2 - dims_proyecto.h/2))
    def is_finished(self): return self.finish_options
    def set_finish(self,bool): self.finish_options = bool
    def finish(self, App):
        """ Change to menu and load everything from the save file """
        if not self.finish_options:
            data = read(App)

            App.menu = Menu(App)
            
            if data:
                App.menu.inNight = data["Night"]
                App.menu.played_once = data["Played"]
                App.menu.custom_night_menu.completed_nights = data["Custom"]
                App.menu.cutscenes_data = data["Cutscenes"]
                App.menu.start_state=5
            self.finish_options = True
            
