import pygame
import time
from pygame.locals import QUIT
import matplotlib.pyplot as plt
import files.game.draw as dr
from files.import_imp import import_images
from files.animations.animations_init import animations_init
from files.game.game_objects import GameObjects
from files.game.game_controller import Game
from files.menu.menu import Menu
from files.save.save import save, read
from files.menu.warning_init import WarningInit
from files.modoIA.modoIA import MODO_IA
from multiprocessing import Process, Queue
class App:
	def __init__(self, initial_dimentions=(1024, 768), caption="Five Nights at Freddy's - made with pygame"):
		self.playing = True
		self.loaded = False
		self.ia_control=False
		self.screen_queue = Queue()
		pygame.init() 
		pygame.mixer.init() 
		self.dimentions = initial_dimentions
		self.surface = pygame.display.set_mode( self.dimentions ,vsync=True)
		pygame.display.set_caption(caption) # Win's name

		# Icon
		icon = pygame.image.load("icon.ico")
		pygame.display.set_icon(icon)

		# Fps configurations
		self.clock = pygame.time.Clock()
		self.frames_per_second = 60

		self.warning_init = WarningInit(self)
		self.introduccion_proyecto = pygame.image.load("sprites/menu/logos/intro_proyecto.png").convert_alpha()
		self.inital_warning = pygame.image.load("sprites/menu/logos/4.png").convert_alpha()
		self.update(self)
		
		self.assets = import_images()
		self.scene = 0
		# Mouse
		self.mouse_hitbox = pygame.Rect((self.dimentions[0]/2,self.dimentions[1]/2), (1,1))

		# DeltaTime variables
		self.prev_time, self.now_time = 0, 0

		# Animations
		self.animations = animations_init(self)

		# Menu will be initialized in draw, and game / gameObjects in menu
		self.objects:GameObjects = None
		self.game:Game = None
		self.menu:Menu = None
		self.ia:MODO_IA = None
		self.loaded = True
		

	def get_deltatime(self):
		self.now_time = time.time()
		self.deltaTime = self.now_time - self.prev_time
		self.prev_time = self.now_time

	def loop(self):
		while self.playing == True:
			
			events = pygame.event.get()

			# Update mouse's hitbox and pressed buttons
			self.mouse_hitbox.left, self.mouse_hitbox.top = pygame.mouse.get_pos()

			# Frames per second
			self.game_fps = self.clock.tick(self.frames_per_second)

			#pygame.display.set_caption(str(round(self.clock.get_fps(), 2)) ) # Win's name

			#DeltaTime
			self.get_deltatime()

			self.game_events(events)

			self.update(events)


	def game_events(self, events):
		for event in events:
			if event.type == QUIT:
				if self.warning_init.is_finished():
					save(self)
				if self.ia_control is True:
					self.ia.detection_thread.join()
				self.playing = False
				
	def update(self, events):
		self.surface.fill((0,0,0))

		# Draw on screen
		dr.Draw(self)
		
		# Update each frame
		pygame.display.update()
