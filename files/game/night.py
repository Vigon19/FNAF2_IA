# Nights controller

import pygame, random

class NightAIChanger:
    def __init__(self, App):
        self.animatronics_ai = {}
        self.animatronics = App.objects.Animatronics.animatronics_in_game
        self.animatronics_keys = self.animatronics.keys()
        self.get_ais(App)
        self.time = 0

    def get_ais(self, App):
        for key in self.animatronics_keys:
            self.animatronics_ai[key] = self.animatronics[key].aggresivity

    def update_ai(self, App):
        for key in self.animatronics_keys:
            self.animatronics[key].aggresivity = self.animatronics_ai[key]

    def update(self, App, nightToPlay:int):
        self.time = App.objects.gameTimer.time
        match nightToPlay:
            case 1:
                self.night_1(App)
            case 2:
                self.night_2(App)
            case 3:
                self.night_3(App)
            case 4:
                self.night_4(App)
            case 5:
                self.night_5(App)
            case 6:
                self.night_6(App)
            case 7:
                self.night_7(App)
            case _:
                print("No AI configured!")

        self.update_ai(App)

    def night_1(self, App):

        match self.time:
            case 12:
                pass

            case 1: 
                pass

            case 2:
                self.animatronics_ai["TOY_FREDDY"] = 2
                self.animatronics_ai["TOY_BONNIE"] = 2

            case 3:
                self.animatronics_ai["TOY_BONNIE"] = 3
                self.animatronics_ai["PUPPET"] = 1

            case 4: pass

            case 5: pass

    def night_2(self, App):
        self.animatronics_ai["PUPPET"] = 5
        self.animatronics_ai["MANGLE"] = 3
        self.animatronics_ai["TOY_CHICA"] = 3
        self.animatronics_ai["TOY_BONNIE"] = 3
        self.animatronics_ai["TOY_FREDDY"] = 2
        self.animatronics_ai["BALOON_BOY"] = 3
        self.animatronics_ai["FOXY"] = 1

    def night_3(self, App):

        match self.time:
            case 12:
                self.animatronics_ai["WITHERED_BONNIE"] = 1
                self.animatronics_ai["WITHERED_CHICA"] = 1
                self.animatronics_ai["FOXY"] = 2
                self.animatronics_ai["BALOON_BOY"] = 1
                self.animatronics_ai["PUPPET"] = 8

            case 1: 
                self.animatronics_ai["WITHERED_FREDDY"] = 2
                self.animatronics_ai["WITHERED_BONNIE"] = 3
                self.animatronics_ai["WITHERED_CHICA"] = 2
                self.animatronics_ai["FOXY"] = 3
                self.animatronics_ai["BALOON_BOY"] = 2
                self.animatronics_ai["TOY_BONNIE"] = 1
                self.animatronics_ai["TOY_CHICA"] = 1

            case 2:
                pass

            case 3:
                pass

            case 4: pass

            case 5: pass

    def night_4(self, App):

        match self.time:
            case 12:
                self.animatronics_ai["WITHERED_BONNIE"] = 1
                self.animatronics_ai["FOXY"] = 7
                self.animatronics_ai["BALOON_BOY"] = 3
                self.animatronics_ai["MANGLE"] = 5
                self.animatronics_ai["PUPPET"] = 9

            case 1: 
                pass

            case 2:
                self.animatronics_ai["WITHERED_FREDDY"] = 3
                self.animatronics_ai["WITHERED_CHICA"] = 4
                self.animatronics_ai["WITHERED_BONNIE"] = 4
                self.animatronics_ai["TOY_BONNIE"] = 1

            case 3:
                pass

            case 4: pass

            case 5: pass

    def night_5(self, App):

        match self.time:
            case 12:
                self.animatronics_ai["WITHERED_FREDDY"] = 2
                self.animatronics_ai["WITHERED_BONNIE"] = 2
                self.animatronics_ai["WITHERED_CHICA"] = 2
                self.animatronics_ai["FOXY"] = 5
                self.animatronics_ai["BALOON_BOY"] = 5
                self.animatronics_ai["TOY_FREDDY"] = 5
                self.animatronics_ai["TOY_BONNIE"] = 2
                self.animatronics_ai["TOY_CHICA"] = 2
                self.animatronics_ai["MANGLE"] = 1
                self.animatronics_ai["PUPPET"] = 10

            case 1: 
                self.animatronics_ai["WITHERED_FREDDY"] = 10
                self.animatronics_ai["WITHERED_BONNIE"] = 5
                self.animatronics_ai["WITHERED_CHICA"] = 5
                self.animatronics_ai["FOXY"] = 7
                self.animatronics_ai["TOY_FREDDY"] = 1
                self.animatronics_ai["MANGLE"] = 10

            case 2:
                pass

            case 3:
                pass

            case 4: pass

            case 5: pass

    def night_6(self, App):

        match self.time:
            case 12:
                self.animatronics_ai["WITHERED_FREDDY"] = 5
                self.animatronics_ai["WITHERED_BONNIE"] = 5
                self.animatronics_ai["WITHERED_CHICA"] = 5
                self.animatronics_ai["FOXY"] = 10
                self.animatronics_ai["BALOON_BOY"] = 5
                self.animatronics_ai["TOY_FREDDY"] = 0
                self.animatronics_ai["TOY_BONNIE"] = 0
                self.animatronics_ai["TOY_CHICA"] = 0
                self.animatronics_ai["MANGLE"] = 3
                self.animatronics_ai["PUPPET"] = 15
                self.animatronics_ai["GOLDEN_FREDDY"] = random.randint(1, 10)

            case 1: 
                self.animatronics_ai["GOLDEN_FREDDY"] = random.randint(1, 10)

            case 2:
                self.animatronics_ai["WITHERED_FREDDY"] = 10
                self.animatronics_ai["WITHERED_BONNIE"] = 10
                self.animatronics_ai["WITHERED_CHICA"] = 10
                self.animatronics_ai["FOXY"] = 15
                self.animatronics_ai["BALOON_BOY"] = 9
                self.animatronics_ai["TOY_FREDDY"] = 5
                self.animatronics_ai["TOY_BONNIE"] = 5
                self.animatronics_ai["TOY_CHICA"] = 5
                self.animatronics_ai["MANGLE"] = 10
                self.animatronics_ai["GOLDEN_FREDDY"] = 3

            case 3:
                pass

            case 4: pass

            case 5: pass

    def night_7(self, App):
        """ Get the data from custom night """
        for key in self.animatronics_keys:
            try:
                self.animatronics_ai[key] = App.menu.custom_night_menu.animatrionics_data[key]["aggresive"]
            except KeyError as e:
                self.animatronics_ai[key] = 20 # change
        