import pygame
from widget import Widget

class Button(Widget):
    def __init__(self, widget_manager, position, size, text = "" , color = (200, 200, 200), border_radius = 0):
        pygame.font.init()   
        super().__init__(widget_manager)
        self.pos = position
        self.size = size
        self.text = text
        self.color = color
        self.normal_color = color
        self.hover_color = (220, 220, 220)
        self.click_color = (160,160,160)
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_color = (0, 0, 0)
        self.rect = None
        self.is_pressed = False
        self.border_radius = border_radius
        return
    
    def set_text(self, text):
        self.text = text
        return
    def set_border_radius(self, border_radius):
        self.border_radius = border_radius
        return
    
    def set_font(self, font):
        self.font = font
        return
    
    def set_font_color(self, font_color):
        self.font_color = font_color
        return

    def set_font_data(self, font, font_color = (0, 0, 0)):
        self.font = font
        self.font_color = font_color
        return
    
    def set_colors(self, normal, hover = (255, 255, 255), click = (255, 255, 255)):
        self.normal_color = normal
        self.hover_color = hover
        self.click_color = click
        return
    
    def on_click(self,pos):
        if self.rect == None:
            return
        if not self.rect.collidepoint(pos):
            return
        self.is_pressed = True
        self.color = self.click_color
        self.on_click_func()
        return
    
    def on_hover(self, pos):
        if self.rect == None:
            return
        if not self.rect.collidepoint(pos):
            self.color = self.normal_color
            if self.is_pressed:
                self.is_pressed = False
            return
        if not self.is_pressed:
            self.color = self.hover_color
        self.on_hover_func()
        return
    
    def on_release(self, pos):
        if not self.rect.collidepoint(pos):
            return
        self.is_pressed = False
        self.color = self.hover_color
        self.on_release_func()
        return
    
    def draw(self):
        self.rect = pygame.draw.rect(self.surface, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]),border_radius=self.border_radius)
        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect()
        text_rect.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        self.surface.blit(text, text_rect)
        return