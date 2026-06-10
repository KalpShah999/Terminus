import time

from pixel_text_screen import PixelTextScreen


def main():
    # Create a screen we can draw on. The window opens in its own process.
    screen = PixelTextScreen()

    pixel_data = [[0 for _ in range(screen.pixel_width)] for _ in range(screen.pixel_height)]
    
    text_data = [[0 for _ in range(screen.pixel_height)]] # Length is screen.pixel_height
    text_data.append([0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
    text_data.append([0, 0, 0, 1, 1, 0, 0, 0, 0, 0])
    text_data.append([0, 0, 0, 0, 1, 1, 0, 0, 0, 0])
    text_data.append([0, 0, 0, 0, 0, 1, 1, 0, 0, 0])
    text_data.append([0, 0, 0, 0, 0, 0, 1, 1, 0, 0])

    try: 
        while True:
            # Each iteration, start from left to right 
            for y in range(len(pixel_data)):
                for x in range(len(pixel_data[y])):
                    if (x < len(pixel_data[y]) - 1):
                        pixel_data[y][x] = pixel_data[y][x+1]
                    elif (len(text_data) > 0):
                        pixel_data[y][x] = text_data[0][y] 
                    else: 
                        pixel_data[y][x] = 0
            if (len(text_data) > 0): text_data.pop(0)

            screen.update_pixels(pixel_data)

            time.sleep(0.1)
    except KeyboardInterrupt: 
        print("Terminating")
    except Exception as error:
        print("Something went wrong.", error)
    
    screen.terminate()


if __name__ == "__main__":
    main()
