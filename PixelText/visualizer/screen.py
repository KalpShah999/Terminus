import multiprocessing

from .window import run_window


def _to_hex(color):
    # Tk expects colours as text like "#ff8800", so turn an (r, g, b) tuple
    # into that format.
    r, g, b = color
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


class Screen:

    # This is the object you use from your own code. It behaves like a simple
    # screen you can draw on, but behind the scenes it launches a separate
    # process that owns the real window. Because the window lives in its own
    # process, your main program is never blocked and your terminal stays free
    # for input(). You can almost pretend it is a real, physical screen plugged
    # into your program.

    def __init__(self, width=800, height=400, background=(15, 15, 20)):
        self.width = width
        self.height = height

        # The queue is the "wire" between us and the window process: we put
        # drawing commands in, and the window process takes them out.
        self._command_queue = multiprocessing.Queue()

        # Launch the window in its own process. daemon=True means the window is
        # closed automatically when your main program ends.
        self._process = multiprocessing.Process(
            target=run_window,
            args=(self._command_queue, width, height, _to_hex(background)),
            daemon=True,
        )
        self._process.start()

    def draw_circle(self, position, radius, color=(255, 255, 255)):
        # Ask the window to draw a filled circle. position is an (x, y) point
        # measured from the top-left corner of the window.
        x, y = position
        self._command_queue.put(("circle", x, y, radius, _to_hex(color)))

    def clear(self):
        # Remove everything currently drawn so you can start a fresh frame.
        self._command_queue.put(("clear",))

    def close(self):
        # Politely ask the window to close itself.
        self._command_queue.put(("close",))
