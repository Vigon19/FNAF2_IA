

def Draw(App):
	if not App.options.is_finished():
		print("-----DRAW OPTIONS----")
		App.options.update(App)
	else:
		if not App.menu.start_game:
			App.menu.update(App)
		else:
			if App.ia_control and not App.finish_train:
				
				App.ia.run_model(App)
				App.finish_train=True
			else:
				App.game.updater(App)