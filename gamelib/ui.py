"""
UI elements such as buttons and labels etc.
"""

import pygame

class UI:
    """
    UI class for updating, drawing and creating the objects
    """
    def __init__(self):
        self.buttons: dict[str, Button] = {}
        self.labels: dict[str, Label] = {}
        self.overlays: dict[str, Overlay] = {}
        
    def create_button(
                self,
                button_name: str,
                click_event,pos: pygame.Vector2, 
                text: str='button', 
                text_size: float=35, 
                text_color: pygame.Color=(0, 0, 0), 
                background: bool=True, 
                padding: float=0, 
                background_size=pygame.Vector2(150, 50), 
                background_color: pygame.Color=(200, 200, 200),
                border_radius: int=0,
                toggle_colors: tuple[pygame.Color, pygame.Color] | None=None,
                state: bool=True
            ) -> Button:
        
        button = Button(
            click_event,
            pos,
            text,
            text_size,
            text_color,
            background,
            padding,
            background_size,
            background_color,
            border_radius,
            toggle_colors,
            state
            )
        
        self.buttons[button_name] = button
        return button
    
    def create_label(
            self,
            label_name: str,
            pos: pygame.Vector2,
            text: str='label',
            text_size: float=35,
            text_color: pygame.Color=(0, 0, 0),
            background: bool=True,
            padding: float=0,
            background_size=pygame.Vector2(0, 0),
            background_color: pygame.Color=(200, 200, 200),
            border_radius=0
            ) -> Label:
        
        label = Label(
            pos,
            text,
            text_size,
            text_color,
            background,
            padding,
            background_size,
            background_color,
            border_radius
            )
        
        self.labels[label_name] = label
        return label
    
    def create_overlay(self, overlay_name: str, size: pygame.Vector2, color: pygame.Color=(128, 128, 128), alpha: int=255):
        overlay = Overlay(size, color, alpha)
        self.overlays[overlay_name] = overlay
        return overlay
        
    def draw(self, screen):
        for overlay in self.overlays.values():
            overlay.draw(screen)
        for label in self.labels.values():
            label.draw(screen)
        for button in self.buttons.values():
            button.draw(screen)
        
            
    def update(self, mouse_buttons, mouse_pos):
        for button in self.buttons.values():
            button.update(mouse_buttons, mouse_pos)

class Label:
    def __init__(self, pos: pygame.Vector2, text: str, text_size: float=35, text_color: pygame.Color=(0, 0, 0), background: bool=False, padding=0, background_size=pygame.Vector2(0, 0), background_color: pygame.Color=(255, 0, 255), border_radius=0):
        self.pos = pygame.Vector2(pos)

        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.background = background
        self.background_size = pygame.Vector2(background_size)
        self.padding = padding
        self.background_color = background_color
        self.border_radius = border_radius

        self.font = pygame.font.Font(None, self.text_size)

        self.text_surf = self.font.render(
            self.text,
            True,
            self.text_color,
        )
        if self.background_size.length_squared() == 0:
            width = self.text_surf.get_width() + self.padding * 2
            height = self.text_surf.get_height() + self.padding * 2
        else:
            width, height = self.background_size

        self.background_rect = pygame.Rect(
            self.pos.x,
            self.pos.y,
            width,
            height,
        )
        
        
        
    def draw(self, screen):
        if self.background:
            pygame.draw.rect(
                screen,
                self.background_color,
                self.background_rect,
                border_radius=self.border_radius
            )
        if self.background_size.length_squared() == 0:
            text_pos = self.pos + pygame.Vector2(
                self.padding,
                self.padding,
            )
        else:
            text_pos = self.text_surf.get_rect(center=self.background_rect.center)

        screen.blit(self.text_surf, text_pos)
        
    def update_text(self, text):
        self.text = text
        self.text_surf = self.font.render(
            self.text,
            True,
            self.text_color,
        )

        if self.background_size.length_squared() == 0:
            width = self.text_surf.get_width() + self.padding * 2
            height = self.text_surf.get_height() + self.padding * 2
        else:
            width, height = self.background_size

        self.background_rect = pygame.Rect(
            self.pos.x,
            self.pos.y,
            width,
            height,
        )
        
    def update_shape(self, new_x=None, new_y=None, new_size=None):
        self.pos = pygame.Vector2(
            self.pos.x if new_x is None else new_x,
            self.pos.y if new_y is None else new_y
        )
        if new_size is not None:
            width, height = new_size
        else:
            width, height = self.background_rect.width, self.background_rect.height
        self.background_rect = pygame.Rect(
            self.pos.x,
            self.pos.y,
            width,
            height,
        )
        
    def set_center(self, pos):
        self.background_rect.center = pos
        self.pos = pygame.Vector2(self.background_rect.topleft)
        
class Button(Label):
    def __init__(self, click_event, pos, text, text_size, text_color, background, padding, background_size, background_color, border_radius, toggle_colors, state):
        super().__init__(pos, text, text_size, text_color, background, padding, background_size, background_color, border_radius)
        self.click_event = click_event
        self.hovered = False
        self.mouse_clicked = False
        self.mouse_down = False
        self.toggle = True if toggle_colors is not None else False
        if self.toggle:
            self.toggle_colors = toggle_colors
            self.state = state if isinstance(state, bool) else False
        
    def draw(self, screen):
        if not self.toggle:
            color = self.background_color
        else:
            color = self.toggle_colors[self.state]
        if self.mouse_down and self.hovered:
            color = [val/1.1 for val in [*color]]
        elif self.hovered:
            color = [min(255, val+(self.hovered*30)) for val in [*color]]
        if self.background:
            pygame.draw.rect(
                screen,
                color,
                self.background_rect,
                border_radius=self.border_radius
            )
            
        if self.background_size.length_squared() == 0:
            text_pos = self.pos + pygame.Vector2(
                self.padding,
                self.padding,
            )
        else:
            text_pos = self.text_surf.get_rect(center=self.background_rect.center)

        screen.blit(self.text_surf, text_pos)
        
    def update(self, mouse_buttons, mouse_pos):
        self.hovered = self.background_rect.collidepoint(mouse_pos)
        mouse_down = mouse_buttons[0]
        
        if mouse_down and not self.mouse_clicked:
                self.mouse_clicked = self.hovered
                
        if not mouse_down and self.mouse_down:
            if self.hovered and self.mouse_clicked and self.click_event:
                if self.toggle:
                    self.state = not self.state
                    self.click_event(self.state)
                else:
                    self.click_event()
            self.mouse_clicked = False
        self.mouse_down = mouse_down
        
    def get_state(self):
        if not self.toggle:
            raise AttributeError(f'Button {self.text} is not toggleable')
        else:
            return self.state

class Overlay:  # add ability to change color, alpha
    def __init__(self, size, color: pygame.Color=(128, 128, 128), alpha: int=255):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.color = color
        self.alpha = alpha
        self.surface.fill((*self.color, self.alpha))
    
    def draw(self, screen):
        screen.blit(self.surface, (0, 0))
        
    def resize(self, new_size):
        self.surface = pygame.Surface(new_size, pygame.SRCALPHA)
        self.surface.fill((*self.color, self.alpha))
        
if __name__ == "__main__":
    import random
    pygame.init()
    clock = pygame.time.Clock()
    ui = UI()
    button = ui.create_button("button", lambda: print('hello', random.randint(100, 200)), (100, 100), "click me", 50, (200, 200, 200), True, 10, (0, 0), (100, 100, 100))
    toggle_button = ui.create_button("togglebutton", lambda x: print(x), (300, 100), "click me", 50, (200, 200, 200), True, 10, (0, 0), (100, 100, 100), 15, ((255, 0, 0), (0, 255, 0)))
    label = ui.create_label("label", (100, 300), "text:\n210394", 50, (200, 200, 200), True, 10, (0, 0), (100, 100, 255), 20)
    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:
        mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouse_pos = pygame.mouse.get_pos()
        ui.labels["label"].update_text(f'text {random.randint(100000, 99999999)}')
        ui.update(mouse_buttons, mouse_pos)
        screen.fill((30, 30, 30))
        ui.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    