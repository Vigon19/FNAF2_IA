import pygame, math
from files.ui.button import Button

class MusicBoxButton:
    def __init__(self, App, position:list):
        self.charge = 21
        self.fake_charge = 0
        self.position = position
        button_size = [App.assets.music_box_button_off.get_width(), App.assets.music_box_button_off.get_height()]
        self.button = Button(position, button_size, App.assets.music_box_button_off)
        self.timer = pygame.time.get_ticks()
        self.timer_sound = pygame.time.get_ticks()
        self.warning_timer = pygame.time.get_ticks()
        self.recharging_time = False
        self.times_out = False
        self.descharge_ticks = 2000
        self.warning_index = 0
        self.warning_ticks = 500


    def update(self, App):

        self.button.update(App.surface, App.mouse_hitbox)
        App.surface.blit(App.assets.music_box_label, [self.position[0] + 10, self.position[1] + 10])
        App.surface.blit(App.assets.clicknhold, [self.position[0], self.position[1] + 72])
        

        mouse_click = pygame.mouse.get_pressed()
        
        if App.ia_control is False:
            if self.button.mouse_hovered:
                if mouse_click[0]:
                    self.button.sprite = App.assets.music_box_button_on
                    self.recharge_time(App)
                    if not pygame.mixer.Channel(3).get_busy() and pygame.time.get_ticks() - self.timer_sound > 450:
                        pygame.mixer.Channel(3).play(App.assets.charge)
                        self.timer_sound = pygame.time.get_ticks()

            if not self.button.mouse_hovered or not mouse_click[0]:
                self.button.sprite = App.assets.music_box_button_off
                if self.recharging_time:
                    self.timer = pygame.time.get_ticks()
                    self.recharging_time = False
        else:
            if App.ia.music_box:
                self.button.sprite = App.assets.music_box_button_on
                self.recharge_time(App)
                if not pygame.mixer.Channel(3).get_busy() and pygame.time.get_ticks() - self.timer_sound > 450:
                    pygame.mixer.Channel(3).play(App.assets.charge)
                    self.timer_sound = pygame.time.get_ticks()
            if App.ia.music_box is False:
                self.button.sprite = App.assets.music_box_button_off
                if self.recharging_time:
                    self.timer = pygame.time.get_ticks()
                    self.recharging_time = False
        if self.charge != 0:
            # Draw timer
            App.surface.blit(App.assets.music_box_timer_sprites[self.charge-1], [self.position[0] - 100, self.position[1]])

    def run_time(self, App):
        if pygame.time.get_ticks() - self.timer > self.descharge_ticks and not self.charge == 0 and not self.recharging_time:
            self.charge -= 1
            self.timer = pygame.time.get_ticks()

        if self.charge == 0:
            self.times_out = True


    def recharge_time(self, App):
        puppet = App.objects.Animatronics.animatronics_in_game["PUPPET"]
        if not self.recharging_time:
            self.timer = pygame.time.get_ticks()
            self.recharging_time = True

        if self.recharging_time:
            if pygame.time.get_ticks() - self.timer > self.descharge_ticks - (900 + ((puppet.aggresivity + 1)*54)) / ((puppet.aggresivity + 1) * 0.167):
                if not self.charge >= 21:
                    self.charge += 1
                self.timer = pygame.time.get_ticks()

            self.warning_timer = pygame.time.get_ticks()
            self.warning_index = -1

    def warning_sign(self, App):
        if self.charge < 10 and not self.times_out:
            if self.warning_index != -1:
                if (not App.objects.open_monitor_button.inCamera or App.objects.open_monitor_button.quitting_camera):
                    App.surface.blit(App.assets.warn_big[self.warning_index], (530, App.dimentions[1] - 130))
                else:
                    App.surface.blit(App.assets.warn_small[self.warning_index], (954 - 55,515 - 110))

            # Warning index
            if pygame.time.get_ticks() - self.warning_timer > self.warning_ticks:
                if self.warning_index == -1:
                    if self.charge >= 5:
                        self.warning_index = 0
                    else:
                        self.warning_index = 1
                else:
                    self.warning_index = -1
                self.warning_timer = pygame.time.get_ticks()

            if self.charge >= 5:
                self.warning_ticks = 500
            else:
                self.warning_ticks = 200
        else:
            self.warning_timer = pygame.time.get_ticks()