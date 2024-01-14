import pygame
from files.modoIA.fnaf2_gym_RL import FNAF2Env
from files.modoIA.ia_model import Trainer
from files.modoIA.loaded_model import TestModel
import files.utils as f
from files.modoIA.modoIA import MODO_IA
def Draw(App):
	if not App.warning_init.is_finished():
		App.warning_init.update(App)
	
	else:
		if not App.menu.start_game:
			App.menu.update(App)
		else:
			if App.ia_control and not App.finish_train:
				print(f"IF {App.finish_train}")
				App.ia=MODO_IA(App)
				App.env=FNAF2Env(App)
				test=TestModel(App)
				test.run_model()
				App.finish_train=True
			else:
				print(f"ELSE {App.finish_train}")
				App.game.updater(App)