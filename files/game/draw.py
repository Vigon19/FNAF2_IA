import pygame
from files.modoIA.fnaf2_gym_RL import FNAF2Env
from files.modoIA.ia_model import Trainer
import files.utils as f

def Draw(App):
	if not App.warning_init.is_finished():
		App.warning_init.update(App)
	
	else:
		if not App.menu.start_game:
			App.menu.update(App)
		else:
			if App.ia_control:
				trainer = Trainer(App)
				trainer.train_model()
			else:
				App.game.updater(App)