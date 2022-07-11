import os
os.system("pip install pyperclip")
os.system("pip install pygame")
os.system("pip install google")
os.system("pip install protobuf")
import pyperclip
import pygame
import wget
import json
import threading
import os.path
import time
from datetime import date
from datetime import datetime
from pathlib import Path
import urllib.request
import platform
from os.path import exists

pygame.font.init() # Import font
pygame.mixer.init() # Import sounds

# Local imports
from resources import *
from device import *

# Global variables
vec = pygame.math.Vector2

def vec_to_int(vector):
    return int(vector.x), int(vector.y)

def write_json () :
    data = json.dumps(oneplus_app_data)
    with open('resource.json', 'w') as save:
        save.write(data)


# This is the application home screen

class Main :

    def __init__(self) :
        pygame.init()
        self.running = True
        self.screen = WIN
        self.rect = self.screen.get_rect()
        self.mouse = vec()
        self.mouse_visible = True
        self.clock = pygame.time.Clock()
        self.start = False
        

    def check_click(self, mouse) :

        if self.rect.collidepoint(mouse) :
            self.start = True
            choosing_device = Device()
            choosing_device.choose_your_phone()

    def main_controller(self) :

        while not self.start :

            for event in pygame.event.get() :

                if event.type == pygame.QUIT :
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    self.check_click(event.pos)


    def main_window(self) :

        while not self.start :

            self.screen.fill(RED)
            self.screen.blit(oneplus_header_logo, (400, 100))

            title = large_font.render("Press to Start", 1, WHITE)
            self.screen.blit(title, (520, 500))
            pygame.display.update()


    def start_app(self) :

        # Create two initial theads
        # Display and controller

        thread_1 = threading.Thread(target=self.main_window, name="ui")
        thread_2 = threading.Thread(target = self.main_controller, name="controller")

        # Start both threads
        thread_1.start()
        thread_2.start()

        # Init controller to avoid freeze of UI
        start = self.main_controller()

        # Wait for both thread to end
        while not self.start :
            thread_1.join()
            thread_2.join()


start = Main()
start.start_app()




