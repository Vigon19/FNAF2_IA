import pygame
from files.ui.button import Button

class CameraButton:
    def __init__(self, App, draw_box=False):
        spr_monitor_dims = [App.assets.monitor_button.get_width(), App.assets.monitor_button.get_height()]
        self.monitor_button = Button((510, App.dimentions[1] - spr_monitor_dims[1]- 20), [spr_monitor_dims[0], spr_monitor_dims[1] + 500], sprite=App.assets.monitor_button, draw_box=draw_box)
        self.inCamera = False
        self.camera_being_pressed = False
        self.quitting_camera = False
        self.entering_camera = False

    def update(self, App, canInteract=True):
        self.monitor_button.update(App.surface, App.mouse_hitbox)

        if App.ia_control:
            self.handle_ia_control(App)
            self.animation_ia_control(App, canInteract=canInteract)
            
        else:
            self.handle_user_control(App, canInteract)
            self.animation_user_control(App, canInteract=canInteract)

        if self.inCamera and not self.quitting_camera:
            # Force quit mask
            App.objects.mask_button.inMask = False
            App.objects.mask_button.entering_mask = False
            App.objects.mask_button.quitting_mask = True
            App.animations.mask.sprite_num = 0
            if App.ia_control is True:
                App.ia.put_mask=False

        if App.animations.monitor.sprite_num == 0 and self.quitting_camera:
            self.quitting_camera = False
            if App.ia_control is True:
                App.ia.open_monitor=False
        

    def handle_user_control(self, App, canInteract=True):
        if canInteract or not App.objects.mask_button.entering_mask:
            if App.objects.battery.charge == 0 or App.objects.office.animatronic_in_office:
                self.quitting_camera = True
                if self.monitor_button.mouse_hovered:
                    if not self.camera_being_pressed:
                        App.assets.error_sound.play()
                        self.camera_being_pressed = True
                else:
                    self.camera_being_pressed = False

    def handle_ia_control(self, App):
        if App.ia.open_monitor:
            # Lógica para abrir el monitor en modo IA
            if not self.inCamera:
                self.entering_camera = True
                App.animations.monitor.update(App.surface)

                # Get in camera
                if App.animations.monitor.sprite_num == len(App.animations.monitor.sprites) - 1:
                    if not App.objects.battery.charge == 0:
                        self.inCamera = True
                        App.objects.camera.static_animation = True
                        self.entering_camera = False
                        App.assets.camera_sound_1.play()
                    App.animations.monitor.desactivate = True

                    self.camera_being_pressed = True
        else:
            # Lógica para cerrar el monitor en modo IA
            if self.inCamera:
                self.quitting_camera = True

                if not self.camera_being_pressed:
                    self.camera_being_pressed = True

                if self.quitting_camera:
                    App.animations.monitor.desactivate = False

                    if not App.objects.music_box.times_out:
                        pygame.mixer.Channel(2).set_volume(0)

                    App.animations.monitor.update(App.surface, reversed=True)
                    # Get off camera
                    if App.animations.monitor.sprite_num == 0:
                        self.inCamera = False
                        self.camera_being_pressed = True
                        self.quitting_camera = False
                        App.assets.camera_sound_2.play()


    def animation_user_control(self, App, canInteract=True):
        # Monitor animation
        if not self.inCamera:
            if (self.monitor_button.mouse_hovered and canInteract) or self.entering_camera:
                if not self.camera_being_pressed:
                    self.entering_camera = True
                    App.animations.monitor.update(App.surface)

                    # Get in camera
                    if App.animations.monitor.sprite_num == len(App.animations.monitor.sprites) - 1:
                        if not App.objects.battery.charge == 0:
                            self.inCamera = True
                            App.objects.camera.static_animation = True
                            self.entering_camera = False
                            App.assets.camera_sound_1.play()
                        App.animations.monitor.desactivate = True

                        self.camera_being_pressed = True
            else:
                self.camera_being_pressed = False

        else:
            if self.monitor_button.mouse_hovered or self.quitting_camera:
                if not self.camera_being_pressed:
                    self.quitting_camera = True

            else:
                self.camera_being_pressed = False

            if self.quitting_camera:
                App.animations.monitor.desactivate = False

                if not App.objects.music_box.times_out:
                    pygame.mixer.Channel(2).set_volume(0)

                App.animations.monitor.update(App.surface, reversed=True)
                # Get off camera
                if App.animations.monitor.sprite_num == 0:
                    self.inCamera = False
                    self.camera_being_pressed = True
                    self.quitting_camera = False
                    App.assets.camera_sound_2.play()
                    if App.ia_control:
                        App.ia.open_monitor=False

    def animation_ia_control(self, App, canInteract=True):
        # Monitor animation
        if not self.inCamera and App.ia_control:
            if (App.ia.open_monitor and canInteract) or self.entering_camera:
                if not self.camera_being_pressed:
                    self.entering_camera = True
                    App.animations.monitor.update(App.surface)

                    # Get in camera
                    if App.animations.monitor.sprite_num == len(App.animations.monitor.sprites) - 1:
                        if not App.objects.battery.charge == 0:
                            self.inCamera = True
                            App.objects.camera.static_animation = True
                            self.entering_camera = False
                            App.assets.camera_sound_1.play()
                        App.animations.monitor.desactivate = True

                        self.camera_being_pressed = True
            else:
                self.camera_being_pressed = False

        else:
            if App.ia.open_monitor or self.quitting_camera:
                if not self.camera_being_pressed:
                    self.quitting_camera = True

            else:
                self.camera_being_pressed = False

            if self.quitting_camera:
                App.animations.monitor.desactivate = False

                if not App.objects.music_box.times_out:
                    pygame.mixer.Channel(2).set_volume(0)

                App.animations.monitor.update(App.surface, reversed=True)
                # Get off camera
                if App.animations.monitor.sprite_num == 0:
                    self.inCamera = False
                    self.camera_being_pressed = True
                    self.quitting_camera = False
                    App.assets.camera_sound_2.play()
                    if App.ia_control:
                        App.ia.open_monitor=False