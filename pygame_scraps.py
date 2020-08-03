# import the pygame module, so you can use it
import pygame
import pygame.font


# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("minimal program")

    max_x = 1200
    max_y = 800
    screen = pygame.display.set_mode((max_x, max_y))

    # define a variable to control the main loop
    running = True

    x = 0
    y = 0
    image = pygame.image.load("zonesdemo.jpg")
    #image.set_colorkey((0, 0, 0))
    # image.set_alpha(30)
    old_rect = screen.blit(image, (x, y))
    pygame.display.flip()
    loops = 0

    # text stuff
    foreground = pygame.Surface(screen.get_size())
    foreground = foreground.convert()

    if pygame.font:
        print("font here")
        font = pygame.font.Font(None, 36)
        text = font.render("Here's my test text dsfgkjdshkfghsdkjfghdsjkfhnsdnfgjksn\ndfngsdkjlfngsdkjlfgnjksdnfgjksdnfgjklsdnfgkjlnsdfgknjldsg", 1, (255, 255, 255))
        textpos = text.get_rect()
        foreground.blit(text, textpos)
        foreground.set_colorkey((0, 0, 0))
        screen.blit(foreground, (0, 0))

    # main loop
    while running:
        # print(loops)
        loops += 1
        x += 1
        y += 1
        if x > max_x:
            x = 0
        if y > max_y:
            y = 0

        screen.fill((0, 0, 0))
        screen.blit(image, (x, y))
        screen.blit(foreground, (x / 2, y / 3))
        pygame.display.flip()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

main()