class Widget:
    def __init__(self, widget_manager):
        self.widget_manager = widget_manager
        self.widget_manager.add_widget(self)
        self.surface = widget_manager.get_surface()
        return
    
    def set_surface(self, surface):
        self.surface = surface
        return
    
    def on_click(self, pos):
        pass

    def on_hover(self, pos):
        pass

    def on_release(self, pos):
        pass

    def on_motion(self, pos):
        pass
    def on_click_func(self):
        pass

    def on_hover_func(self):
        pass

    def on_release_func(self):
        pass
    
    def on_motion_func(self):
        pass

    def draw(self):
        pass

    def bind(self, event, func):
        if event == "click":
            self.on_click_func = func
        elif event == "hover":
            self.on_hover_func = func
        elif event == "release":
            self.on_release_func = func
        return