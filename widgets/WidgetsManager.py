import pygame

class WidgetsManager:
    def __init__(self, surface):
        self.widgets = []
        self.surface = surface
        pass
    
    def add_widget(self, widget):
        if widget not in self.widgets:
            self.widgets.append(widget)
        pass

    def set_surface(self, surface):
        self.surface = surface
        for widget in self.widgets:
            widget.set_surface(surface)
        return
    
    def get_surface(self):
        return self.surface
    
    def handle_event(self, event, position):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for widget in self.widgets:
                widget.on_click(position)
        if event.type == pygame.MOUSEMOTION:
            for widget in self.widgets:
                widget.on_hover(position)
        if event.type == pygame.MOUSEBUTTONUP:
            for widget in self.widgets:
                widget.on_release(position)
        return
    
    def draw(self):
        if self.surface == None:
            return
        for widget in self.widgets:
            widget.draw()
        pass