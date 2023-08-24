import pygame

class BernsteinCurve:
    def __init__(self,screen, initial_points = []):
        self.points = initial_points
        self.n = len(initial_points) - 1
        self.factorials = {-1 : 1,0:1}
        self.result = []
        self.screen = screen
        self.t_value = 1.0
        self.step = 0.001
        self.calculate()
        return
    
    def clear(self):
        self.points.clear()
        self.n = -1
        self.result.clear()
        self.calculate()
    
    def addPoint(self, point):
        self.points.append(point)
        print(len(self.points))
        self.n += 1
        self.factorials[self.n] = self.__factorial(self.n)
        self.calculate()
        return
    
    def removePoint(self, point):
        if point in self.points:
            self.points.remove(point)
            self.n -= 1
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
        if self.factorials.get(n) == None:
            self.factorials[n] = n * self.__factorial(n-1)
        return self.factorials[n]
    
    def get_last_point(self):
        return self.points[len(self.points)-1]
    
    def draw(self, show_lines, show_points, show_point_t, show_bezier):
        if show_lines:
            for i in range(len(self.points)-1):
                pygame.draw.aaline(self.screen, (0,0,0), self.points[i].getPos(), self.points[i+1].getPos(), 2)
        if show_points:
            if self.points != []:
                for p in self.points:
                    p.draw(self.screen)

        if show_point_t:
            if self.points != []:
                pygame.draw.circle(self.screen, (0, 0, 255), self.result[int((self.t_value//self.step) - 1)], 5)          

        if show_bezier:
            for i in range(len(self.result)-1):
                pygame.draw.aaline(self.screen, (255,0,0), self.result[i], self.result[i+1], 2)
        return