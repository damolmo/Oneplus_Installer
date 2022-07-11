from resources import *
import threading
import os
import platform

# Global variables
vec = pygame.math.Vector2

def vec_to_int(vector):
    return int(vector.x), int(vector.y)

# This is the installer screen

class Installer :

    def __init__(self) :
        pygame.init()
        self.running = True
        self.screen = WIN
        self.rect = self.screen.get_rect()
        self.mouse = vec()
        self.mouse_visible = True
        self.clock = pygame.time.Clock()
        self.partitions_list = []
        self.installing = True
        self.initial_bootanimation = True
        self.current_partition = ''
        self.rebooting_system = False
        self.current_number = 5

        self.android_transfer = False
        self.my_device_model = ''
        self.android_transfered = False
        self.device_detected = False
        self.platform = platform.system()
        self.path = "downloads" + "/" + oneplus_app_data["CURRENT_DEVICE"]["NAME"] + "/" + "output"

    def oneplus_animation(self) :

        # Starts animation loop

        while not self.device_detected:
            for animations in range(101, 425) :

                animation = pygame.image.load(os.path.join('Assets/logo/animation', "frame_%d_delay-0.03s.gif" % animations))

                # 1+ Logo Animation
                self.draw_ui(animation)
                self.clock.tick(60)


                # Reset the animations counter while true
                if animations == 425 :
                    animations = 80


    def oneplus_animation_second(self) :
        while self.installing :
            for animations in range(101, 425) :

                animation = pygame.image.load(os.path.join('Assets/logo/animation', "frame_%d_delay-0.03s.gif" % animations))

                # 1+ Logo Animation
                self.draw_ui_second(animation)
                self.clock.tick(60)


                # Reset the animations counter while true
                if animations == 425 :
                    animations = 80


    def check_adb_device(self):

        while not self.device_detected :

            try:
                my_device_model = subprocess.check_output("platform-tools/%s/adb shell getprop ro.product.model" % self.platform , shell=True, )
                my_device_model = my_device_model.decode("utf-8")
                my_device_model = str(my_device_model)
                self.my_device_model = my_device_model.replace(" ", "")
                self.device_detected = True

            except subprocess.CalledProcessError as e:
                self.my_device_model = "unknown"


    def draw_ui(self, animation):

    
        # Background color
        self.screen.fill(BLACK)

        self.screen.blit(animation, (-330, 20))

        text = large_font.render("Oneplus Installer", 1, WHITE)
        self.screen.blit(text, (50, 100))

        self.screen.blit(android_bg, (600, 100))

        description = small_font.render("Please, connect your phone to your computer", 1, WHITE)
        self.screen.blit(description, (50, 170))

        description = small_font.render("The OTA Installation process will start automatically", 1, WHITE)
        self.screen.blit(description, (50, 200))

        percentage = small_font.render("Waiting for device.." , 1, WHITE)
        self.screen.blit(percentage, (220, 500))


        pygame.display.update()


    def draw_ui_second(self, animation):

    
        # Background color
        self.screen.fill(BLACK)

        self.screen.blit(animation, (-330, 20))

        text = large_font.render("Oneplus Installer", 1, WHITE)
        self.screen.blit(text, (50, 100))

        self.screen.blit(android_bg, (600, 100))

       
        description = small_font.render("We're currently installing the OTA", 1, WHITE)
        self.screen.blit(description, (50, 170))

        description = small_font.render("Please, don't disconnect your %s" % oneplus_app_data["CURRENT_DEVICE"]["NAME"], 1, WHITE)
        self.screen.blit(description, (50, 200))

        dialog = small_font.render("Installing %s" % self.current_partition , 1, WHITE)
        self.screen.blit(dialog, (220, 500))


        pygame.display.update()


    def controller(self) :

        while self.installing :

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    print("Installing...")

    def controller_second(self) :

        while not self.device_detected :

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    print("Installing...")

    def count_all_partitions(self) :

        # Counts all partitions and return a value

        count = 0

        for partitions in self.partitions_list :
            count +=1

        return count

    def install_current_partition(self, partition) :

        # Install current partition to 1+ Device

        partition_without_extension = partition.replace(".img", "")

        os.system("platform-tools/%s/fastboot flash %s %s/%s" % (self.platform, partition_without_extension , self.path, partition))


    def install_ota(self) :

        # Count all device partitions
        partitions = self.count_all_partitions()

        # Install current partition

        for partition in range(0, partitions) :
            self.current_partition = self.partitions_list[partition]
            self.install_current_partition(self.partitions_list[partition])

        self.installing = False
        #self.rebooting_system = True


    def reboot_window(self) :

        while self.rebooting_system : 

            # Background
            self.screen.fill(BLACK)

            # Countdown
            number = large_font.render("Rebooting", 1, WHITE)
            self.screen.blit(number, (350, 250))
            number = large_font.render("%d" % self.current_number, 1, WHITE)
            self.screen.blit(number, (400, 320))

            pygame.display.update()

    def countdown(self) :

        while self.rebooting_system :
            self.current_number -=1


            if self.current_number == 0 :
                self.rebooting_system = False

    def reboot_fastboot(self) :
        os.system("platform-tools/%s/adb reboot bootloader" % self.platform)

    def start_install(self) :


        # Create three new threads
        thread_1 = threading.Thread(target = self.controller_second, name ="mouse")
        thread_3 = threading.Thread(target = self.oneplus_animation, name="ui")
        thread_4 = threading.Thread(target = self.check_adb_device, name="adb")

        # Start Both Threads
        thread_3.start()
        thread_1.start()
        thread_4.start()

        start = self.controller_second()

        # Wait for both threads to end
        while not self.device_detected :
            thread_3.join()
            thread_1.join()
            thread_4.join()
        
        # Save current device partitions into a temp array
        self.partitions_list = device_partitions["PARTITIONS"]

        # Start install process

        # Create threads for user UI
        thread_1 = threading.Thread(target=self.oneplus_animation_second, name="ui")
        thread_2 = threading.Thread(target=self.controller, name="mouse")
        thread_3 = threading.Thread(target=self.install_ota, name="ota")
        thread_4 = threading.Thread(target=self.reboot_fastboot, name="fastboot")

        # Start all threads
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()

        # Start controller to avoid UI freeze
        start = self.controller()

        # Wait for all threads to end
        while self.installing :
            thread_4.join()
            thread_3.join()
            thread_1.join()
            thread_2.join()

        # Create threads for user UI
        thread_1 = threading.Thread(target=self.reboot_window, name="ui")
        thread_2 = threading.Thread(target=self.countdown, name="mouse")
        

        # Start threads
        thread_1.start()
        thread_2.start()

        # Wait for threads to end
        while self.rebooting_system :
            thread_1.join()
            thread_2.join()

        # Reboot to system
        os.system("platform-tools/%s/fastboot reboot system" % self.platform)
