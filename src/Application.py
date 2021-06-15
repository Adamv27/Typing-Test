import sys
import pygame
import TypeTest as tt
import pygame.freetype


class Application:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.width, self.height = [750, 400]
        pygame.display.set_caption('Typing Test')

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.colors = {'background': (50, 52, 55), 'default_text': (100, 100, 100), 'incorrect_text': (202, 71, 84),
                       'correct_text': (208, 208, 208), 'stats': (226, 183, 20)}
        self.test = tt.TypeTest(15)
        self.test.generate_test()
        self.test.text = self.test.get_text()

    def main_loop(self):
        while True:
            self.screen.fill(self.colors['background'])
            self.display_text()
            if not self.test.is_started and not self.test.is_complete:
                self.display_start()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Space bar has been pressed for the first time which begins the test
                    if event.key == pygame.K_SPACE and not self.test.is_started:
                        self.test.start()
                        continue
                    # Deleting incorrect letters
                    if event.key == pygame.K_BACKSPACE and self.test.is_started:
                        self.test.backspace()
                    elif self.test.is_started:
                        self.test.typed(event.unicode)
            if self.test.is_started:
                if self.test.is_over():
                    self.test.end()
            elif self.test.is_complete:
                self.display_stats()

            pygame.display.update()

    def display_text(self):
        font = pygame.freetype.Font(None, 30)
        font.origin = True
        # Space each letter takes during rendering
        M_ADV_X = 4

        offset = 0
        for i, line in enumerate(self.test.text):
            current = ' '.join(line)
            # Size of entire line
            text_surf_rect = font.get_rect(current)
            baseline = text_surf_rect.y

            text_surf = pygame.Surface(text_surf_rect.size)
            text_surf_rect.center = self.screen.get_rect().center
            text_surf_rect.y -= 50

            # Width of each letter in the line
            metrics = font.get_metrics(current)

            text_surf.fill(self.colors['background'])
            x = 0
            for (index, (letter, metric)) in enumerate(zip(current, metrics)):
                if index < self.test.index_on_line and self.test.current_line >= i:
                    if index not in self.test.incorrect_letters:
                        color = self.colors['correct_text']
                elif i < self.test.current_line:
                    color = self.colors['correct_text']
                else:
                    color = self.colors['default_text']

                if [index, i] in self.test.incorrect_letters:
                    color = self.colors['incorrect_text']
                font.render_to(text_surf, (x, baseline), letter, color)
                x += metric[M_ADV_X]
            text_surf_rect.y = text_surf_rect.y + offset
            offset += 30
            self.screen.blit(text_surf, text_surf_rect)

    def display_stats(self):
        wpm = self.test.get_wpm()
        accuracy = self.test.get_accuracy()

        font = pygame.font.SysFont('arial', 30)

        accuracy_text_surf = font.render('accuracy: ' + accuracy + '%', True, self.colors['stats'])
        wpm_text_surf = font.render('wpm: '+ wpm, True, self.colors['stats'])
        self.screen.blit(wpm_text_surf, (200, 250))
        self.screen.blit(accuracy_text_surf, (375, 250))

    def display_start(self):
        font = pygame.font.SysFont('arial', 34)

        text_surf = font.render('Press Space to begin', True, self.colors['stats'])
        self.screen.blit(text_surf, (250, 50))

