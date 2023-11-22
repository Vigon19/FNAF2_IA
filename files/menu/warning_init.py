import pygame
from files.save.save import save, read
from files.menu.menu import Menu
from files.modoIA.modoIA import MODO_IA
class WarningInit:
    def __init__(self, App):
        self._finished = False
        self.timer = pygame.time.get_ticks()
        self.alpha = 255
        self.intro_state=-1
        self.introduccion_proyecto = pygame.image.load("sprites/menu/logos/intro_proyecto_2.png").convert_alpha()
    def update(self, App):
        dims = App.inital_warning.get_rect()
        dims_proyecto = App.introduccion_proyecto.get_rect()
        App.inital_warning.set_alpha(self.alpha)
        

        if App.loaded:
            App.surface.blit(App.inital_warning, (App.dimentions[0]/2 - dims.w/2, App.dimentions[1]/2 - dims.h/2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                
                self.finish(App)
            elif keys[pygame.K_2]:
                self.finish(App)
        else:
            App.surface.blit(self.introduccion_proyecto, (App.dimentions[0]/2 - dims_proyecto.w/2, App.dimentions[1]/2 - dims_proyecto.h/2))
    def is_finished(self): return self._finished

    def finish(self, App):
        """ Change to menu and load everything from the save file """
        if not self._finished:
            data = read(App)

            App.menu = Menu(App)
            App.ia=MODO_IA()
            if data:
                App.menu.inNight = data["Night"]
                App.menu.played_once = data["Played"]
                App.menu.custom_night_menu.completed_nights = data["Custom"]
                App.menu.cutscenes_data = data["Cutscenes"]
                App.menu.start_state=5
            self._finished = True