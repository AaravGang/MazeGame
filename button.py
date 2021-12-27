import pygame as pg

# Simple button class
class Button(object):
    def __init__(self, rect, color, function, **kwargs):
        self.rect = pg.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.process_kwargs(kwargs)

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "click_sound": None,
            "hover_sound": None,
            "image": None,
            "clicked_image": None,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            return self.on_click(event)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return self.on_release(event)

    def on_click(self, event):

        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                return self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            self.clicked = False
            return self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self, surface):
        """Update needs to be called every frame in the main loop."""
        color = self.color
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color

        elif self.hovered and self.hover_color:
            color = self.hover_color

        surface.fill(color, self.rect.inflate(-4, -4))

        if self.image:
            surface.blit(self.image, self.rect)

