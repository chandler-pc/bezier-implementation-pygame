import pygame
from manager import WidgetsManager
from button import Button
from slider import Slider
from bernstein import BernsteinBezierWindow

class BezierWindow:
    def __init__(self, width = 800, height = 600, background_color = (201, 124, 242)):
        self.isRun = True
        self.width = width
        self.height = height
        self.background_color = background_color
        self.fps = 0
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.widgets_manager = WidgetsManager(self.screen)
        pygame.display.set_caption("Bezier")
        self.__create_widgets()

    def __create_bezier(self, method):
        self.isRun = False
        if method == "Bernstein":
            BernsteinBezierWindow().run()

    def __create_widgets(self):
        w = self.width
        h = self.height
        button_width = w/3
        button_height = h/6
        button_bernstein = Button(self.widgets_manager, (w/2 - button_width/2,200), (button_width, button_height), border_radius=10)
        button_bernstein.set_text("Bernstein")
        button_bernstein.set_font_data(pygame.font.SysFont("Calibri", 50), (0, 0, 0))
        button_casteljau = Button(self.widgets_manager, (w/2 - button_width/2,350), (button_width, button_height), border_radius=10)
        button_casteljau.set_text("DeCasteljau")
        button_casteljau.set_font_data(pygame.font.SysFont("Calibri", 50), (0, 0, 0))
        button_bernstein.bind("release", lambda: self.__create_bezier("Bernstein"))

    def __events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            self.widgets_manager.handle_event(event, pygame.mouse.get_pos())
        return
    
    def __draw(self):
        self.screen.fill(self.background_color)
        self.widgets_manager.draw()
        pygame.display.flip()
        pygame.display.update()
        return

    def run(self):
        while self.isRun:
            self.__events()
            self.__draw()

if __name__ == "__main__":
    window = BezierWindow()
    window.run()
