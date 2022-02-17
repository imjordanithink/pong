import pygame
pygame.init()

# creation of the window
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# creation of window caption
pygame.display.set_caption("Pong")

# creation of MAIN LOOP or EVENT LOOP of the program wich displays the window and then draws something on it.
def main():
    run = True
    # MAIN LOOP handles everything going on in our game constantley such as collision.
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                run = False
                break
    pygame.quit()

# if __name__ == "__main__": makes sure that this file is only being ran as its own project and not being imported as a module in another project.
if __name__ == "__main__":
    main()
