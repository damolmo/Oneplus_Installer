from resources import *
from download import *
import os
import json
import threading
import os.path
import time

# This is the device selector

# Global variables
vec = pygame.math.Vector2

def vec_to_int(vector):
    return int(vector.x), int(vector.y)

def write_json () :
    data = json.dumps(oneplus_app_data)
    with open('devices.json', 'w') as save:
        save.write(data)

class Device :

    def __init__(self) :
        pygame.init()
        self.running = True
        self.screen = WIN
        self.rect = self.screen.get_rect()
        self.mouse = vec()
        self.mouse_visible = True
        self.clock = pygame.time.Clock()
        self.phones_list_img = [
                            ONEPLUS_6_RENDER, ONEPLUS_6T_RENDER, ONEPLUS_7_RENDER, ONEPLUS_7_PRO_RENDER, ONEPLUS_7T_RENDER,
                            ONEPLUS_7T_PRO_RENDER, ONEPLUS_8_RENDER, ONEPLUS_8_PRO_RENDER, ONEPLUS_8T_RENDER, ONEPLUS_9_RENDER, ONEPLUS_9_PRO_RENDER,
                            ONEPLUS_9R_RENDER, ONEPLUS_9RT_RENDER, ONEPLUS_NORD_RENDER, ONEPLUS_NORD_CE_RENDER, ONEPLUS_NORD_2_RENDER, ONEPLUS_NORD_2T_RENDER,
                            ONEPLUS_NORD_CE_2_RENDER, ONEPLUS_NORD_N100_RENDER, ONEPLUS_NORD_N20_RENDER, ONEPLUS_NORD_N200_RENDER, ONEPLUS_10_PRO_RENDER, ONEPLUS_10R_RENDER
                            ]

        self.phones_list_str = [
                            "ONEPLUS 6", "ONEPLUS 6T", "ONEPLUS 7", "ONEPLUS 7PRO", "ONEPLUS 7T",
                            "ONEPLUS 7TPRO", "ONEPLUS 8", "ONEPLUS 8PRO", "ONEPLUS 8T", "ONEPLUS 9", "ONEPLUS 9PRO",
                            "ONEPLUS 9R", "ONEPLUS 9RT", "ONEPLUS NORD", "ONEPLUS NORDCE", "ONEPLUS NORD2", "ONEPLUS NORD2T",
                            "ONEPLUS NORD CE 2", "ONEPLUS N100", "ONEPLUS N20", "ONEPLUS N200", "ONEPLUS 10PRO", "ONEPLUS 10R"
                            ]

        self.choosing_phone = True

        self.left_arrow_rect = pygame.Rect(30, 410, 57, 79)
        self.right_arrow_rect = pygame.Rect(1150, 410, 57, 79)

        self.next_5 = False
        self.previous_5 = True
        self.next_counter = 0
        self.count = 0


        self.first_phone_rect = pygame.Rect(200, 280, 244, 290)
        self.second_phone_rect = pygame.Rect(500, 280, 244, 290)
        self.third_phone_rect = pygame.Rect(800, 280, 244, 290)

        self.myDownload = ''
        self.current_device = ''

    def check_click(self, mouse) :
        if self.left_arrow_rect.collidepoint(mouse) :

            swipe_sound.play()

            if self.count == 1 :
                self.next_5 = False
                self.previous_5 = True
                self.count = 0

            elif self.count == 2 :
                self.next_5 = True
                self.previous_5 = False
                self.count = 1

            elif self.count == 3 :
                self.next_5 = True
                self.previous_5= False
                self.count = 2

            elif self.count == 4 :
                self.next_5 = True
                self.previous_5 = False
                self.count = 3

            elif self.count == 5 :
                self.next_5 = True
                self.previous_5 = False
                self.count = 4

            elif self.count == 6 :
                self.next_5 = True
                self.previous_5 = False
                self.count = 5

            elif self.count == 7 :
                self.next_5 = True
                self.previous_5 = False
                self.count = 6

        elif self.right_arrow_rect.collidepoint(mouse) :

            swipe_sound.play()

            if self.count == 0 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 1

            elif self.count == 1 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 2

            elif self.count == 2 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 3

            elif self.count == 3 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 4


            elif self.count == 4 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 5

            elif self.count == 5 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 6


            elif self.count == 6 :
                self.previous_5 = False
                self.next_5 = True
                self.count = 7


        elif self.first_phone_rect.collidepoint(mouse) :
            if self.count == 0 :
                self.current_device = self.phones_list_str[0]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 1 :
                self.current_device = self.phones_list_str[3]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 2 :
                self.current_device = self.phones_list_str[6]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 3 :
                self.current_device = self.phones_list_str[9]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 4 :
                self.current_device = self.phones_list_str[12]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 5 :
                self.current_device = self.phones_list_str[15]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 6 :
                self.current_device = self.phones_list_str[18]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 7 :
                self.current_device = self.phones_list_str[21]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


        elif self.second_phone_rect.collidepoint(mouse) :

            if self.count == 0 :
                self.current_device = self.phones_list_str[1]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 1 :
                self.current_device = self.phones_list_str[4]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 2 :
                self.current_device = self.phones_list_str[7]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 3 :
                self.current_device = self.phones_list_str[10]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 4 :
                self.current_device = self.phones_list_str[13]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 5 :
                self.current_device = self.phones_list_str[16]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 6 :
                self.current_device = self.phones_list_str[19]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 7 :
                self.current_device = self.phones_list_str[22]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 8 :
                self.current_device = self.phones_list_str[25]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 9 :
                self.current_device = self.phones_list_str[28]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


        elif self.third_phone_rect.collidepoint(mouse) :
            if self.count == 0 :
                self.current_device = self.phones_list_str[2]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False

            elif self.count == 1 :
                self.current_device = self.phones_list_str[5]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 2 :
                self.current_device = self.phones_list_str[8]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 3 :
                self.current_device = self.phones_list_str[11]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 4 :
                self.current_device = self.phones_list_str[14]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 5 :
                self.current_device = self.phones_list_str[17]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 6 :
                self.current_device = self.phones_list_str[20]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


            elif self.count == 7 :
                self.current_device = self.phones_list_str[23]
                self.myDownload =  oneplus_app_data["DEVICES"][self.current_device]["URL"]
                self.choosing_phone = False


    def choosing_controller(self) :

        while self.choosing_phone :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    self.check_click(event.pos)

    def choosing_window(self) :

        while self.choosing_phone :

            self.screen.fill(BLACK)

            # Logo
            self.screen.blit(oneplus_logo_alpha, (520,20))

            # Text
            text = small_font.render("Choose your OnePlus device", 1, WHITE) 
            self.screen.blit(text, (470, 220) )

            # Cursor

            self.screen.blit(left_arrow, (30, 410))
            self.screen.blit(right_arrow, (1150, 410))

            # Show 5 phones on display

            width = 200
            count = 0

            for phone in self.phones_list_img :
                if self.previous_5 :
                    if self.count == 0 :
                        if count < 3 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1


                if self.next_5 :
                    if self.count == 1 :
                        if count >= 3 and count < 6 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

                    elif self.count == 2 :
                        if count >=6 and count < 9 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

                    elif self.count == 3 :
                        if count >=9 and count < 12 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

                    elif self.count == 4 :
                        if count >=12 and count < 15 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

                    elif self.count == 5 :
                        if count >=15 and count < 18 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

                    elif self.count == 6 :
                        if count >=18 and count < 21 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

                    elif self.count == 7 :
                        if count >=21 and count < 24 :

                            # Draw phones on display
                            self.screen.blit(phone, (width, 280))

                            # Draw phone name on display
                            self.screen.blit(label, (width, 580))
                            phone_model = normal_font.render(self.phones_list_str[count].replace("ONEPLUS", ""), 1, WHITE)
                            self.screen.blit(phone_model, (width + 185, 592))

                            # Increase counters
                            width += 300
                            count +=1

                        else :
                            count +=1

            # Cursor rect

            #pygame.draw.rect(self.screen, WHITE, self.left_arrow_rect)
            #pygame.draw.rect(self.screen, WHITE, self.right_arrow_rect,)

            # Phones rect
            #pygame.draw.rect(self.screen, WHITE, self.first_phone_rect)
            #pygame.draw.rect(self.screen, WHITE, self.second_phone_rect)
            #pygame.draw.rect(self.screen, WHITE, self.third_phone_rect)

            pygame.display.update()

    def choose_your_phone(self) :

        # Create new threads
        thread_1 = threading.Thread(target=self.choosing_window, name="ui")
        thread_2 = threading.Thread(target=self.choosing_controller, name="mouse")

        # Start both threads
        thread_1.start()
        thread_2.start()

        # Start controller to avoid UI freeze
        start = self.choosing_controller()

        # Wait for threads to end
        while self.choosing_phone :
            thread_1.join()
            thread_2-join()

        # Save phone details into JSON variables
        device = self.current_device.replace(" ", "_")
        oneplus_app_data["CURRENT_DEVICE"]["NAME"] = device
        oneplus_app_data["CURRENT_DEVICE"]["URL"] = self.myDownload
        write_json()

        # Create a download class object
        download = Download()
        download.start_download_process()

        pygame.quit()
