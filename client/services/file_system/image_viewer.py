from terminalpainter import Canvas, Painter
import os

class ImageViewer:
    def __init__(self, image):
        self.image = image
        terminal_width = os.get_terminal_size().columns
        factor = self.image.size[0] / terminal_width
        self.width = int(self.image.size[0] / factor)
        self.height = int(self.image.size[1] / factor)
        self.image = self.image.resize((self.width, self.height))

    def run(self):
        canvas = Canvas((self.width, self.height))
        painter = Painter()
        painter.paint_image(canvas, 0, 0,self.image)
        canvas.paint()