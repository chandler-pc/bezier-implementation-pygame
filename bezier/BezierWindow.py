import pygame
from bezier.BernsteinCurve import BernsteinCurve
from widgets.Button import Button
from widgets.Checkbox import Checkbox
from widgets.WidgetsManager import WidgetsManager
from widgets.Slider import Slider
from bezier.BezierPoint import BezierPoint

class BezierWindow:
    def __init__(self,screen,fps = 60):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.is_run = True
        self.move = False
        self.actualPoint = None
        self.draw_lines = True
        self.draw_bezier = True
        self.draw_point_t = True
        self.draw_points = True
        self.fps = fps
        self.widgets_manager = WidgetsManager(self.screen)
    
    def _create_widgets(self):
        button_clear = Button(self.widgets_manager, (10, 10), (100, 50), border_radius=10)
        button_clear.set_text("Clear")
        button_clear.bind("click", lambda: self.curve.clear())
        slider_t = Slider(self.widgets_manager, (10, 550), (200, 10), border_radius=10, min = 0, max = 1,circle_slide=True, value=1)
        slider_t.bind("hover", lambda: self.curve.set_t_value(slider_t.get_value()))
        checkbox_show_t = Checkbox(self.widgets_manager, (600, 550), (20, 20), value=True,text= "Show t position")
        checkbox_show_t.bind("click", lambda: self._set_draw_point_t(checkbox_show_t.get_value()))
        checkbox_show_points = Checkbox(self.widgets_manager, (600, 500), (20, 20), value=True,text= "Show points")
        checkbox_show_points.bind("click", lambda: self._set_draw_points(checkbox_show_points.get_value()))
        checkbox_show_lines = Checkbox(self.widgets_manager, (600, 450), (20, 20), value=True,text= "Show lines")
        checkbox_show_lines.bind("click", lambda: self._set_draw_lines(checkbox_show_lines.get_value()))
        checkbox_show_bezier = Checkbox(self.widgets_manager, (600, 400), (20, 20), value=True,text= "Show bezier")
        checkbox_show_bezier.bind("click", lambda: self._set_draw_bezier(checkbox_show_bezier.get_value()))


    def _set_draw_lines(self, value):
        self.draw_lines = value
        return
    
    def _set_draw_bezier(self, value):
        self.draw_bezier = value
        return
    
    def _set_draw_points(self, value):
        self.draw_points = value
        return

    def _set_draw_point_t(self, value):
        self.draw_point_t = value
        return

    def _find_point(self, pos):
        for p in self.curve.points:
            if p.getIsSelecting(pos):
                return p
        return None  
    
    def _add_point(self,event):
        new_point = BezierPoint(event.pos[0], event.pos[1])
        self.actualPoint = new_point
        self.curve.addPoint(new_point)

    def _remove_point(self, event):
        self.actualPoint = self._find_point(event.pos)
        if self.actualPoint == None:
            return
        self.curve.removePoint(self.actualPoint)

    def _on_mouse_down(self, event):
        if event.button == 1:
            self._add_point(event)
        if event.button == 2:
            self.actualPoint = self._find_point(event.pos)
            if self.actualPoint != None:
                self.move = True
        if event.button == 3:
            self._remove_point(event)

    def _on_mouse_up(self, event):
        if event.button == 2 or event.button == 1:
            self.move = False
            self.actualPoint = None

    def _on_mouse_motion(self, event):
        if self.move:
            self.actualPoint.move(event.pos[0], event.pos[1])
            self.curve.calculate()

    def _on_key_down(self, event):
        if event.key == pygame.K_c:
            self.curve.clear()
    
    def _draw(self):
        self.screen.fill((125, 125, 125))
        self._draw_curve()
        self.widgets_manager.draw()
        pygame.display.flip()
        pass
    
    def _draw_curve(self):
        pass

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
               self._on_mouse_down(event)
                
            if event.type == pygame.MOUSEBUTTONUP:
                self._on_mouse_up(event)

            if event.type == pygame.MOUSEMOTION:
                self._on_mouse_motion(event)

            if event.type == pygame.KEYDOWN:
                self._on_key_down(event)

            self.widgets_manager.handle_event(event, pygame.mouse.get_pos())
        return
    
    def run(self):
        self.clock = pygame.time.Clock()
        while self.is_run:
            self._events()
            self._draw()
            self.clock.tick(self.fps)
        pygame.quit()
        return


class BernsteinWindow(BezierWindow):
    def __init__(self,fps = 60):
        super().__init__(fps)
        self.curve = BernsteinCurve(self.screen)
        self._create_widgets()
    
    def _draw_curve(self):
        self.curve.draw(self.draw_lines, self.draw_points, self.draw_point_t, self.draw_bezier)
        