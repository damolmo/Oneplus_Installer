from resources import *
import payload as Payload_
import threading
import wget
from zipfile import ZipFile
import shutil

# Global variables
vec = pygame.math.Vector2

def vec_to_int(vector):
    return int(vector.x), int(vector.y)

class Download :

    def __init__(self) :
        pygame.init()
        self.running = True
        self.screen = WIN
        self.rect = self.screen.get_rect()
        self.mouse = vec()
        self.mouse_visible = True
        self.clock = pygame.time.Clock()
        self.downloading = True
        self.initial_bootanimation = True
        self.progress_message = ''
        self.extracting = False
        self.path = ''

    def oneplus_animation(self) :

        if self.initial_bootanimation :
            for animations in range(0, 100) :
                if animations <= 9 :
                    animation = pygame.image.load(os.path.join('Assets/logo/animation', "frame_00%d_delay-0.03s.gif" % animations))

                else :
                    animation = pygame.image.load(os.path.join('Assets/logo/animation', "frame_0%d_delay-0.03s.gif" % animations))

                # 1+ Logo Animation
                self.draw_screen(animation)
                self.clock.tick(60)

            self.initial_bootanimation = False

        # Starts animation loop

        while self.downloading:
            for animations in range(101, 425) :

                animation = pygame.image.load(os.path.join('Assets/logo/animation', "frame_%d_delay-0.03s.gif" % animations))

                # 1+ Logo Animation
                self.draw_screen(animation)
                self.clock.tick(60)


                # Reset the animations counter while true
                if animations == 425 :
                    animations = 80


    def bar_progress(self, current, total, width=80):
      self.progress_message = "Progress: %d%%" % (current / total * 100)
      # Don't use print() as it will print in new line every time.
      sys.stdout.write("\r" + self.progress_message)
      sys.stdout.flush()

    def extracting_window(self) :

        while self.extracting :
            self.draw_screen(animation_485)


    def draw_screen(self, animation) :

        self.screen.fill(BLACK)

        # Show Oneplus animation on download
        self.screen.blit(animation, (0,-150))

        # Current device message
        if self.downloading :
            dialog = small_font.render("Downloading OTA for %s" % oneplus_app_data["CURRENT_DEVICE"]["NAME"], 1, WHITE)
            self.screen.blit(dialog, (450, 400))

            # Show download progress on display
            text = small_font.render(self.progress_message, 1, WHITE)
            self.screen.blit(text, (575, 450))

        if self.extracting :
            self.screen.blit(animation, (0, -150))
            dialog = small_font.render("Extracting OTA file...", 1, WHITE)
            self.screen.blit(dialog, (550, 400))


        pygame.display.update()


    def download_ota_file(self) :

        # Current device path
        device = oneplus_app_data["CURRENT_DEVICE"]["NAME"]
        path = ("downloads/%s" % device)

        # Create a folder for the OTA device
        try :
            os.mkdir(path)

        except FileExistsError as error :
            shutil.rmtree(path)
            os.mkdir(path)

        # File
        ota_path = path 
        path = path + '/' + 'ota.zip'


        # Download choosed OTA file
        #wget.download(oneplus_app_data["CURRENT_DEVICE"]["URL"], path, bar=self.bar_progress)
        file = os.system("cd binaries & wget.exe -O ota.zip %s" % (oneplus_app_data["CURRENT_DEVICE"]["URL"]))

        os.system("cd binaries & move ota.zip ../%s" % path)

        self.downloading = False
        self.extracting = True
        self.path = path


    def extract_file(self) :

        output = 'downloads' + '/' + oneplus_app_data["CURRENT_DEVICE"]["NAME"] + '/' + 'output'

        try: 
            path = os.mkdir(output) 

        except FileExistsError as error :
            shutil.rmtree(output)
            path = os.mkdir(output)

        with ZipFile(self.path) as ota:
            ota.extractall(output) #Extracts the downloaded file into a subdir 

        self.extracting = False

    def check_click(self, mouse) :
        print("Downloading...")

    def download_controller(self) :

        while self.downloading :

            for event in pygame.event.get() :

                if event.type == pygame.QUIT :
                    self.running = False
                    self.downloading = False

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    self.check_click(event.pos)

    def extracting_controller(self) :

        while self.extracting :

            for event in pygame.event.get() :

                if event.type == pygame.QUIT :
                    self.running = False
                    self.downloading = False

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    self.check_click(event.pos)


    def start_download_process(self) :

        # Download

        # Create new threads
        thread_display_animation = threading.Thread(target=self.oneplus_animation, name="animation")
        thread_download_file = threading.Thread(target=self.download_ota_file, name="ota")
        thread_controller = threading.Thread(target=self.download_controller, name="controller") 

        # Start all threads
        thread_display_animation.start()
        thread_download_file.start()
        thread_controller.start()

        # Start controller thread to avoid UI freeze
        start = self.download_controller()

        # Wait for all threads to end
        while self.downloading :
            thread_display_animation.join()
            thread_controller.join()
            thread_download_file.join()

        # Extract


        # Create new threads
        thread_display_animation = threading.Thread(target=self.extracting_window, name="animation")
        thread_extract_file = threading.Thread(target=self.extract_file, name="ota")
        thread_controller = threading.Thread(target=self.extracting_controller, name="controller") 

        # Start all threads
        thread_display_animation.start()
        thread_extract_file.start()
        thread_controller.start()

        # Start controller thread to avoid UI freeze
        start = self.extracting_controller()

        # Wait for all threads to end
        while self.extracting :
            thread_display_animation.join()
            thread_extract_file.join()
            thread_download_file.join()

        Payload_.start_extraction()


