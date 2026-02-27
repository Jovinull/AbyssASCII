import pygame
import sys
import time

class RetroEngine:
    def __init__(self, width=80, height=40, font_size=16):
        pygame.init()
        self.width = width
        self.height = height
        
        # Load a monospaced font
        try:
            self.font = pygame.font.SysFont("Courier New", font_size, bold=True)
        except:
            self.font = pygame.font.SysFont("monospace", font_size, bold=True)
            
        self.char_w, self.char_h = self.font.size("A")
        self.screen_width = width * self.char_w
        self.screen_height = height * self.char_h
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ABYSS ASCII - Retro Terminal")
        
        # Grid to store (char, color)
        self.grid = [[" " for _ in range(width)] for _ in range(height)]
        self.colors = [[(255, 255, 255) for _ in range(width)] for _ in range(height)]
        
        # CRT Scanlines surface
        self.scanlines = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        for y in range(0, self.screen_height, 2):
            pygame.draw.line(self.scanlines, (0, 0, 0, 50), (0, y), (self.screen_width, y))
            
        self.clock = pygame.time.Clock()
        
    def clear_grid(self):
        self.grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.colors = [[(255, 255, 255) for _ in range(self.width)] for _ in range(self.height)]

    def add_text(self, x, y, text, color=(255, 255, 255)):
        for i, char in enumerate(text):
            if 0 <= x + i < self.width and 0 <= y < self.height:
                self.grid[y][x+i] = char
                self.colors[y][x+i] = color

    def render(self):
        self.screen.fill((0, 0, 0))
        
        # Render characters to a temporary surface for glow effect
        glow_surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        for y in range(self.height):
            for x in range(self.width):
                char = self.grid[y][x]
                if char != " ":
                    color = self.colors[y][x]
                    char_surf = self.font.render(char, True, color)
                    # Main text
                    self.screen.blit(char_surf, (x * self.char_w, y * self.char_h))
                    # Glow (blit with transparency)
                    glow_color = (*color, 100)
                    glow_char = self.font.render(char, True, glow_color)
                    glow_surf.blit(glow_char, (x * self.char_w - 1, y * self.char_h))
                    glow_surf.blit(glow_char, (x * self.char_w + 1, y * self.char_h))
                    glow_surf.blit(glow_char, (x * self.char_w, y * self.char_h - 1))
                    glow_surf.blit(glow_char, (x * self.char_w, y * self.char_h + 1))

        # Blit glow surface
        self.screen.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Apply Scanlines
        self.screen.blit(self.scanlines, (0, 0))
        
        pygame.display.flip()

    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "0"
                    if pygame.K_0 <= event.key <= pygame.K_9:
                        return chr(event.key)
                    if event.key == pygame.K_RETURN:
                        return "enter"
                    # Add arrow keys mapping if needed
                    if event.key == pygame.K_w or event.key == pygame.K_UP: return "1"
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT: return "2"
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN: return "3"
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: return "4"
            
            self.render() # Keep rendering while waiting
            self.clock.tick(30)

    def get_input_text(self, prompt_x, prompt_y, prompt_text, color=(255, 255, 255)):
        input_str = ""
        while True:
            self.clear_grid()
            # In a real scenario, we'd want to keep the current state, 
            # but for this simple version we'll just draw the prompt and current input
            self.add_text(prompt_x, prompt_y, prompt_text + input_str + "_", color)
            self.render()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return input_str
                    elif event.key == pygame.K_BACKSPACE:
                        input_str = input_str[:-1]
                    else:
                        if event.unicode.isprintable():
                            input_str += event.unicode
            self.clock.tick(30)
