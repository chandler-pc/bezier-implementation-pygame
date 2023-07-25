import pygame
from button import Button
from checkbox import Checkbox

from manager import WidgetsManager
from slider import Slider

class BezierPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collide = None
        self.color = (0, 0, 0)
        return
    
    def set_color(self, color):
        self.color = color
        return

    def move(self, x, y):
        self.x = x
        self.y = y
        return
    
    def getIsSelecting(self, pos):
        return self.collide.collidepoint(pos) if self.collide != None else False

    def getPos(self):
        return [self.x, self.y]

    def draw(self, screen):
        self.collide = pygame.draw.circle(screen, self.color, (self.x, self.y), 5)
        return
    
class BezierBernsteinCurve:
    def __init__(self,screen, initial_points):
        self.points = initial_points
        self.n = len(initial_points) - 1
        self.factorials = []
        for i in range(self.n+1):
            self.factorials.append(self.__factorial(i))
        self.result = []
        self.screen = screen
        self.t_value = 1.0
        self.step = 0.001
        self.calculate()
        return
    
    def clear(self):
        self.points.clear()
        self.n = -1
        self.factorials.clear()
        self.result.clear()
        for i in range(self.n+1):
            self.factorials.append(self.__factorial(i))
        self.calculate()
    
    def addPoint(self, point):
        self.points.append(point)
        self.n += 1
        self.factorials.append(self.__factorial(self.n))
        self.calculate()
        return
    
    def removePoint(self, point):
        if point in self.points:
            self.points.remove(point)
            self.n -= 1
            self.factorials.pop()
            self.calculate()
        return

    def calculate(self):
        t = 0
        self.result.clear()
        while t <= self.t_value:
            sx = 0
            sy = 0
            for i in range(self.n+1):
                b = (self.factorials[self.n] / (self.factorials[i] * self.factorials[self.n - i])) * (t ** i) * ((1 - t) ** (self.n - i))
                sx += (self.points[i].getPos()[0]) * b
                sy += (self.points[i].getPos()[1]) * b
            self.result.append([sx, sy])
            t += self.step

    def set_t_value(self, t_value):
        self.t_value = t_value
        self.calculate()
        return

    def __factorial(self, n):
        if n == 0:
            return 1
        for i in range(1,n):
            n *= i
        return n
    
    def get_last_point(self):
        return self.points[len(self.points)-1]

    def draw_point_t(self, draw_point_t):
        if not draw_point_t or len(self.points) == 0:
            return
        pygame.draw.circle(self.screen, (0, 0, 255), self.result[int((self.t_value//self.step) - 1)], 5)

    def draw_points(self, draw_points):
        if not draw_points:
            return
        for p in self.points:
            p.draw(self.screen)
        return
    
    def draw_lines(self,draw_lines):
        if not draw_lines:
            return
        for i in range(len(self.points)-1):
            pygame.draw.line(self.screen, (255, 255, 255), self.points[i].getPos(), self.points[i+1].getPos(),1)
        return
    
    def draw_bezier(self, draw_bezier):
        if not draw_bezier:
            return
        for i in range(len(self.result)-1):
            pygame.draw.line(self.screen, (230, 0, 0), self.result[i], self.result[i+1],2)
        return
    
class BezierWindow:
    def __init__(self,fps = 60):
        pygame.init()
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
        self.curve = None
        self._create_widgets()
    
    def _create_widgets(self):
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
        button_clear = Button(self.widgets_manager, (10, 10), (100, 50), border_radius=10)
        button_clear.set_text("Clear")
        button_clear.bind("click", lambda: self.curve.clear())
        return
    
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
        if self.curve == None:
            self.curve = self.curve_class(self.screen,[new_point])
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
        if event.key == pygame.K_l:
            self.show_lines = not self.show_lines
        if event.key == pygame.K_c:
            self.curve.clear()

    def _draw(self):
        self.screen.fill((125, 125, 125))
        self.curve.draw_lines(self.draw_lines)
        self.curve.draw_bezier(self.draw_bezier)
        self.curve.draw_points(self.draw_points)
        self.curve.draw_point_t(self.draw_point_t)
        self.widgets_manager.draw()
        
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
        return
    
class BernsteinBezierWindow(BezierWindow):
    def __init__(self,fps = 60):
        super().__init__(fps)
        self.curve = BezierBernsteinCurve(self.screen,[])
        pygame.display.set_caption("Bernstein Bezier Curve")

    def _draw(self):
        super()._draw()
        pygame.display.flip()