import pygame
from widget import Widget

class Slider(Widget):
    def __init__(self, widget_manager,position,size,min,max,value = 0, color = (200, 200, 200),circle_slide = False, border_radius = 0, dtype = "float"):
        super().__init__(widget_manager)
        self.pos = position
        self.size = size
        self.color = color
        self.normal_color = color
        self.value = value
        self.min = min
        self.max = max
        self.slide = None
        self.is_pressed = False
        self.border_radius = border_radius
        self.pivot = (self.size[1]+10)/2
        self.slider_pos = self.pos[0] - self.pivot + (self.value/(self.max - self.min)) * self.size[0]
        self.font = pygame.font.SysFont("Calibri", 40)
        self.dtype = dtype
        if circle_slide:
            self.slider_radius = (self.size[1]+10)//2
        else:
            self.slider_radius = 0
        return
    
    def on_click(self, pos):
        if self.slide == None:
            return
        if not self.slide.collidepoint(pos):
            return
        self.is_pressed = True
        self.on_click_func()
        return
    
    def on_hover(self, pos):
        if self.slide == None:
            return
        if not self.slide.collidepoint(pos):
            self.is_pressed = False
            return
        if self.is_pressed:
            self.slider_pos = pos[0] - self.pivot
            if self.slider_pos < self.pos[0] - self.pivot:
                self.slider_pos = self.pos[0] - self.pivot
            if self.slider_pos > self.pos[0] + self.size[0] - self.pivot :
                self.slider_pos = self.pos[0] + self.size[0] - self.pivot
            self.value = round(float(((self.slider_pos+self.pivot-self.pos[0])/self.size[0]) * (self.max - self.min)),2)
            if self.dtype == "int":
                self.value = int(self.value)
        self.on_hover_func()
        return
    
    def on_release(self, pos):
        if self.slide == None:
            return
        if not self.slide.collidepoint(pos):
            return
        self.is_pressed = False
        self.on_release_func()
        return
    
    def get_value(self):
        return self.value
    
    def draw(self):
        pygame.draw.rect(self.surface, self.normal_color, (self.pos, self.size),border_radius=100)
        self.slide = pygame.draw.rect(self.surface, (255, 255, 255), (self.slider_pos, self.pos[1] - 5, self.size[1]+10, self.size[1]+10),border_radius=self.slider_radius)
        #show text with the value
        text = self.font.render(str(self.value), True, (0, 0, 0))
        text_rect = text.get_rect()
        self.surface.blit(text, (self.pos[0] + self.size[0] + 20, self.pos[1] - text_rect.height/2 + self.size[1]/2))
        return