import time

from .screen import Screen


def main():
    # Create a screen we can draw on. The window opens in its own process.
    screen = Screen(width=600, height=200)

    # Give the window a moment to open before we start sending it commands.
    time.sleep(1)

    x = 50
    direction = 5
    while True:
        # Start each frame with a blank screen.
        screen.clear()

        # Draw the dot at its current position.
        screen.draw_circle((x, 100), 20, color=(255, 120, 40))

        # Move the dot, and reverse when it reaches either edge.
        x += direction
        if x >= 550 or x <= 50:
            direction = -direction

        # Wait a little so the movement is visible.
        time.sleep(0.05)


if __name__ == "__main__":
    main()
