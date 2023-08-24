from widgets.Widget import Widget
import pygame

class Checkbox(Widget):
    def __init__(self, widget_manager, position, size, text = 'Checkbox', value = True, color = (200, 200, 200)):
        super().__init__(widget_manager)
        self.pos = position
        self.size = size
        self.text = text
        self.value = value
        self.color = color
        self.normal_color = color
        self.is_pressed = False
        self.font = pygame.font.SysFont("Calibri", self.size[1])
        self.text_color = (0, 0, 0)

    def on_click(self, pos):
        if self.box.collidepoint(pos):
            self.value = not self.value
        self.on_click_func()

    def get_value(self):
        return self.value

    def draw(self):
        self.box = pygame.draw.rect(self.surface, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.surface.blit(self.text_surface, (self.pos[0] + self.size[0] + 10, self.pos[1] + self.size[1]//2 - self.text_surface.get_height()//2))
        if self.value:
            pygame.draw.line(self.surface, (0, 0, 0), (self.pos[0], self.pos[1]), (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), 2)
            pygame.draw.line(self.surface, (0, 0, 0), (self.pos[0] + self.size[0], self.pos[1]), (self.pos[0], self.pos[1] + self.size[1]), 2)
        return
