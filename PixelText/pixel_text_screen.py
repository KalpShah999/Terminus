from visualizer import Screen
import time


class PixelTextScreen():
    def __init__(self, pixel_width=50,
                       pixel_height=10,
                       pixel_radius=5,
                       window_width=700,
                       window_height=200,
                       window_margin=100,
                       background_colour=(80, 80, 80),
                       pixel_off_colour=(20, 20, 20),
                       pixel_on_colour=(255, 200, 50)):
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.pixel_radius = pixel_radius
        self.window_width = window_width
        self.window_height = window_height
        self.window_margin = window_margin
        self.background_colour = background_colour
        self.pixel_off_colour = pixel_off_colour
        self.pixel_on_colour = pixel_on_colour

        self.screen = Screen(width=window_width, height=window_height, background=background_colour)
        time.sleep(1)
    
    def update_pixel(self, coordinate: list, state: bool):
        # TODO: Check boundaries for coordinates 

        x_pos = self.window_margin + self.x_spacing * coordinate[0]
        y_pos = self.window_margin / 2 + self.y_spacing * coordinate[1]
        pixel_colour = self.pixel_on_colour if state else self.pixel_off_colour

        self.screen.draw_circle((x_pos, y_pos), self.pixel_radius, pixel_colour)

    def update_pixels(self, pixel_states: list(list)):
        self.x_spacing = (self.window_width - (self.window_margin * 2)) / (self.pixel_width - 1)
        self.y_spacing = (self.window_height - (self.window_margin)) / (self.pixel_height - 1)
        self.screen.clear()

        for y in range(len(pixel_states)):
            for x in range(len(pixel_states[y])):
                self.update_pixel((x, y), pixel_states[y][x])
    
    def terminate(self):
        self.screen.close()

        