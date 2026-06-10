import queue

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor


# This file is the actual on-screen window. It is meant to run inside its own
# separate process, so it can run the GUI event loop without ever blocking your
# main program (and without stealing the terminal from input()).
#
# Your main program never touches _Window directly. Instead it sends small
# "command" messages over a queue. Each message is a tuple whose first item
# says what kind of command it is:
#     ("circle", x, y, radius, color)   color is a string like "#ff8800"
#     ("clear",)
#     ("close",)


class _Window(QWidget):

    def __init__(self, command_queue, width, height, background):
        super().__init__()
        self.command_queue = command_queue
        self.background = QColor(background)

        # The circles we currently need to draw. Each one is a tuple of
        # (x, y, radius, QColor). "clear" empties this list.
        self.circles = []

        self.setWindowTitle("PixelText Visualizer")
        self.setFixedSize(width, height)

        # A timer makes Qt call _check_queue many times per second so we can
        # pick up new drawing commands from the main program.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check_queue)
        self.timer.start(16)  # about 60 times per second

    def _check_queue(self):
        # Take every command waiting in the queue and update our circle list.
        # We only repaint once, at the end, and only if something changed.
        changed = False
        while True:
            try:
                message = self.command_queue.get_nowait()
            except queue.Empty:
                break
            changed = True
            self._handle_message(message)

        if changed:
            self.update()

    def _handle_message(self, message):
        # The first item of the tuple tells us what to do.
        command = message[0]

        if command == "circle":
            _, x, y, radius, color = message
            self.circles.append((x, y, radius, QColor(color)))
        elif command == "clear":
            self.circles.clear()
        elif command == "close":
            self.close()

    def paintEvent(self, event):
        # Qt calls this whenever the window needs to be redrawn. We fill the
        # background and then draw every circle currently in our list.
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.background)
        painter.setPen(Qt.PenStyle.NoPen)

        for x, y, radius, color in self.circles:
            painter.setBrush(color)
            painter.drawEllipse(QPointF(x, y), float(radius), float(radius))


def run_window(command_queue, width, height, background):
    # This is the function the separate process actually starts in. It builds
    # the Qt application and window, then hands control over to Qt's event
    # loop, which runs until the window is closed.
    app = QApplication([])
    window = _Window(command_queue, width, height, background)
    window.show()
    app.exec()
