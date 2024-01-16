
import files.utils as f
from files.modoIA.modo_ia import ModoIa

def Draw(App):
	if not App.options.is_finished():
		App.options.update(App)
	else:
		if not App.menu.start_game:
			App.menu.update(App)
		else:
			if App.ia_control and not App.finish_train:
				
				App.ia.train_model(App)
				App.finish_train=True
			else:
				App.game.updater(App)