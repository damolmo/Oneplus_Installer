import os
import pygame
import json
import sys
import ctypes
try:
    import lzma
except ImportError:
    from backports import lzma
import struct
import hashlib
import bz2
import sys
import argparse
os.system("pip install bsdiff4")
import bsdiff4
import io
import os.path
import shutil
import subprocess
# from https://android.googlesource.com/platform/system/update_engine/+/refs/heads/master/scripts/update_payload/
import update_metadata_pb2

## Screen properties
pygame.init()
width, height = 640, 480
fpsClock = pygame.time.Clock()
WIN = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
if sys.platform == "win32":
    HWND = pygame.display.get_wm_info()['window']
    SW_MAXIMIZE = 3
    ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = "#ed3237"


## Application Values
FPS = 60
clock = pygame.time.Clock()
small_font = pygame.font.Font(None, 30)
normal_font = pygame.font.Font(None, 25)
large_font = pygame.font.Font(None, 50)
mini_font = pygame.font.Font(None, 18)

## App External Data
my_data = open("devices.json")
oneplus_app_data = json.load(my_data)

## App partitions resource
my_partitions = open("partitions.json")
device_partitions = json.load(my_partitions)

## App Internal Info
icon = pygame.image.load('Assets/logo/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Oneplus Installer")

## Assets
# Logo
oneplus_header_logo = pygame.image.load(os.path.join('Assets/logo', "logo.png"))
oneplus_logo_alpha = pygame.transform.scale(pygame.image.load(os.path.join('Assets/logo', "logo_alpha.png")), (200, 200))
label = pygame.transform.scale(pygame.image.load(os.path.join('Assets/logo', "label.png")), (260, 45))

# Cursor
left_arrow = pygame.transform.scale(pygame.image.load(os.path.join('Assets/cursor', "left.png")), (57, 79))
right_arrow = pygame.transform.scale(pygame.image.load(os.path.join('Assets/cursor', "right.png")), (57, 79))

## Devices
ONEPLUS_ONE_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_ONE.png")), (244, 290))
ONEPLUS_TWO_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_TWO.png")), (244, 290))
ONEPLUS_X_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_X.png")), (244, 290))
ONEPLUS_3_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_3.png")), (244, 290))
ONEPLUS_3T_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_3T.png")), (244, 290))
ONEPLUS_5_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_5.png")), (244, 290))
ONEPLUS_5T_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_5T.png")), (244, 290))
ONEPLUS_6_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_6.png")), (244, 290))
ONEPLUS_6T_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_6T.png")), (244, 290))
ONEPLUS_7_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_7.png")), (244, 290))
ONEPLUS_7_PRO_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_7_PRO.png")), (244, 290))
ONEPLUS_7T_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_7T.jpg")), (244, 290))
ONEPLUS_7T_PRO_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_7T_PRO.png")), (244, 290))
ONEPLUS_8_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_8.jpeg")), (244, 290))
ONEPLUS_8_PRO_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_8_PRO.jpeg")), (244, 290))
ONEPLUS_8T_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_8T.png")), (244, 290))
ONEPLUS_9_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_9.png")), (244, 290))
ONEPLUS_9_PRO_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_9_PRO.png")), (244, 290))
ONEPLUS_9R_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_9R.png")), (244, 290))
ONEPLUS_9RT_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_9RT.png")), (260, 300))
ONEPLUS_NORD_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD.jpeg")), (244, 290))
ONEPLUS_NORD_CE_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_CE.png")), (260, 310))
ONEPLUS_NORD_2_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_2.png")), (234, 290))
ONEPLUS_NORD_2T_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_2T.png")), (260, 310))
ONEPLUS_NORD_CE_2_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_CE_2.png")), (234, 290))
ONEPLUS_NORD_N100_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_N100.png")), (244, 290))
ONEPLUS_NORD_N20_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_N20.png")), (244, 290))
ONEPLUS_NORD_N200_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_NORD_N200.png")), (285, 290))
ONEPLUS_10_PRO_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_10_PRO.png")), (285, 290))
ONEPLUS_10R_RENDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets/devices', "ONEPLUS_10R.png")), (285, 290))

# Music
swipe_sound = pygame.mixer.Sound("music/swipe.mp3")

# Animation
animation_000 = pygame.image.load(os.path.join('Assets/logo/animation', "frame_000_delay-0.03s.gif"))
animation_485 = pygame.image.load(os.path.join('Assets/logo/animation', "frame_485_delay-0.03s.gif"))

# Android
android_bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets/android', "background.png")), (400, 600))
smartphone_bg = pygame.image.load(os.path.join('Assets/android', 'smartphone.png'))
