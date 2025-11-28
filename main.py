
import pygame
import sys
import os
import configparser
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.config_file = os.path.join('conf', 'conf.ini')
        self.config = configparser.ConfigParser()
        self.controls = {}
        self.screen_width = 800
        self.screen_height = 600
        self.fullscreen = False
        self.block_size = 20
        self.fps = 15
        self.bg_color = (10, 10, 10)
        self.snake_color = (0, 255, 0)
        self.food_color = (255, 0, 0)
        self.font = pygame.font.SysFont("Arial", 36)
        self.load_config()
        self.display_flags = pygame.FULLSCREEN | pygame.SCALED if self.fullscreen else 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), self.display_flags)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def load_config(self):
        try:
            if not os.path.exists(self.config_file):
                raise FileNotFoundError(f"Arquivo de configuração não encontrado em {self.config_file}")
            self.config.read(self.config_file)
            display_section = 'Display'
            self.screen_width = self.config.getint(display_section, 'width', fallback=1280)
            self.screen_height = self.config.getint(display_section, 'height', fallback=720)
            self.fullscreen = self.config.getboolean(display_section, 'fullscreen', fallback=False)
            controls_section = 'Controls'
            self.controls['UP'] = pygame.key.key_code(self.config.get(controls_section, 'up', fallback='w'))
            self.controls['DOWN'] = pygame.key.key_code(self.config.get(controls_section, 'down', fallback='s'))
            self.controls['LEFT'] = pygame.key.key_code(self.config.get(controls_section, 'left', fallback='a'))
            self.controls['RIGHT'] = pygame.key.key_code(self.config.get(controls_section, 'right', fallback='d'))
            self.controls['PAUSE'] = pygame.key.key_code(self.config.get(controls_section, 'pause', fallback='enter'))
            self.controls['EXIT'] = pygame.key.key_code(self.config.get(controls_section, 'action_b', fallback='p'))  # Tecla para sair
        except Exception as e:
            print(f"ERRO: {e}. Usando padrão.")
            self.controls = {
                'UP': pygame.K_w, 'DOWN': pygame.K_s, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d,
                'PAUSE': pygame.K_RETURN, 'EXIT': pygame.K_p
            }

    def reset_game(self):
        self.snake = [(self.screen_width // 2, self.screen_height // 2)]
        self.direction = 'RIGHT'
        self.food = self.get_random_position()
        self.score = 0
        self.running = True

    def get_random_position(self):
        x = random.randint(0, (self.screen_width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.screen_height - self.block_size) // self.block_size) * self.block_size
        return x, y

    def draw_text(self, text, size, color, x, y, center=True):
        font_obj = pygame.font.SysFont("Arial", size)
        surface = font_obj.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls['PAUSE']:
                    pygame.quit()
                    sys.exit()
                elif event.key == self.controls['UP'] and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == self.controls['DOWN'] and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == self.controls['LEFT'] and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == self.controls['RIGHT'] and self.direction != 'LEFT':
                    self.direction = 'RIGHT'

    def update(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'UP':
            head_y -= self.block_size
        elif self.direction == 'DOWN':
            head_y += self.block_size
        elif self.direction == 'LEFT':
            head_x -= self.block_size
        elif self.direction == 'RIGHT':
            head_x += self.block_size

        new_head = (head_x, head_y)

        # Colisão com bordas ou corpo
        if (head_x < 0 or head_x >= self.screen_width or head_y < 0 or head_y >= self.screen_height or new_head in self.snake):
            self.running = False
            return

        self.snake.insert(0, new_head)

        # Comer comida
        if new_head == self.food:
            self.score += 10
            self.food = self.get_random_position()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(self.bg_color)
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.snake_color, (*segment, self.block_size, self.block_size))
        pygame.draw.rect(self.screen, self.food_color, (*self.food, self.block_size, self.block_size))
        self.draw_text(f"Score: {self.score}", 28, (255, 255, 255), 10, 10, center=False)
        pygame.display.flip()

    def game_over_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("GAME OVER", 64, (255, 0, 0), self.screen_width // 2, self.screen_height // 2 - 50)
        self.draw_text(f"Score: {self.score}", 48, (255, 255, 255), self.screen_width // 2, self.screen_height // 2 + 10)
        self.draw_text("ENTER para reiniciar | 'P' para sair", 28, (200, 200, 200), self.screen_width // 2, self.screen_height // 2 + 80)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Reinicia
                        waiting = False
                        self.reset_game()
                    elif event.key == self.controls['EXIT']:  # Sai com 'P'
                        pygame.quit()
                        sys.exit()

    def run(self):
        while True:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(self.fps)
            self.game_over_screen()

if __name__ == "__main__":
    SnakeGame().run()
