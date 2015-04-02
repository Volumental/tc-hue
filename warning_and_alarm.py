import sys, pygame

class WarningAndAlarm(object):
    def __init__(self):
        pygame.init()
        self.image_position = [150, 150]
        self.screen_background = 0, 0, 0

    def trigger(self, number_of_times=5):
        self.screen = pygame.display.set_mode([400, 400])
        for i in range (0,number_of_times):
            pygame.mixer.music.load("warning_sound.wav")
            pygame.mixer.music.play(0)
            red_button_on = pygame.image.load("red_button_on.png")
            red_button_off = pygame.image.load("red_button_off.png")
            imgrect = red_button_on.get_rect()
            imgrect = imgrect.move(self.image_position)
            self.screen.fill(self.screen_background)

            while pygame.mixer.music.get_busy():
                self.screen.blit(red_button_on, imgrect)
                pygame.display.flip()
                pygame.time.wait(500)
                self.screen.blit(red_button_off, imgrect)
                pygame.display.flip()
                pygame.time.wait(500)

