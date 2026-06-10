import time

from pixel_text_screen import PixelTextScreen


def main():
    # Create a screen we can draw on. The window opens in its own process.
    screen = PixelTextScreen()

    pixel_data = [[0 for _ in range(screen.pixel_width)] for _ in range(screen.pixel_height)]
    pixel_data[6][25] = 1
    pixel_location = [6, 25]

    try: 
        while True:
            screen.update_pixels(pixel_data)

            # TODO: improve input system
            input_key = input()
            match input_key:
                case 'w':
                    pixel_data[pixel_location[0]][pixel_location[1]] = 0
                    pixel_location = [pixel_location[0] - 1, pixel_location[1]]
                    pixel_data[pixel_location[0]][pixel_location[1]] = 1
                case 'd': 
                    pixel_data[pixel_location[0]][pixel_location[1]] = 0
                    pixel_location = [pixel_location[0], pixel_location[1] + 1]
                    pixel_data[pixel_location[0]][pixel_location[1]] = 1
                case 'a': 
                    pixel_data[pixel_location[0]][pixel_location[1]] = 0
                    pixel_location = [pixel_location[0], pixel_location[1] - 1]
                    pixel_data[pixel_location[0]][pixel_location[1]] = 1
                case 's':
                    pixel_data[pixel_location[0]][pixel_location[1]] = 0
                    pixel_location = [pixel_location[0] + 1, pixel_location[1]]
                    pixel_data[pixel_location[0]][pixel_location[1]] = 1
                case _:
                    continue

            # time.sleep(0.5)
    except KeyboardInterrupt: 
        print("Terminating")
    except Exception as error:
        print("Something went wrong.", error)
    
    screen.terminate()


if __name__ == "__main__":
    main()
