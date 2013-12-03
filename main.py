"""
This is a test program to teach my teenage son to program Android
games in Python for his mobile phone.

Additional information is available at:
  http://github.com/codetricity/json_loader

Follow my son's progress:
http://pychildren.blogspot.com

"""


import json, pygame, sys
import pprint
from json_loader import *

###############################
## Change RUNTEST to False to 
## Turn off red squares over the
## objects with collision.

RUNTEST = True

###############################
## Map section
## Change the filename to use another
## test map or create your own map.
## use tilesets with 32x32 pixels
## ############################

# small map with no collision
# json_filename = "maps/map.json"

#larger map with collision
json_filename = "maps/larger_map.json"

# json_filename = "maps/test_map.json"

#################################
## Player image.  Change to use 
## boy.png or any other graphic of
## similar size
#################################
player_filename = "img/girl.png"

def main():
    pygame.init()

    mapdict = load_map(json_filename)
    if RUNTEST:
        run_test(mapdict)

    SCREENSIZE = (480, 320)
    SCREEN = pygame.display.set_mode(SCREENSIZE)
    starting_position = [-220,-200]

    pos = starting_position
    direction = "stop"




    tilesets = Tileset(mapdict)

    tileset_images = tilesets.load()
    # tiles = tilesets.slice_tiles(tileset_images)
    # try out new method of storing tiles from the tilesets into
    # a dictionary
    tileset_image_dict = tilesets.slice_tiles2(tileset_images)

    # layers = Layer(mapdict, tiles)
    layers = Layer(mapdict, tileset_image_dict)

    # this controls the speed of the player moving around the screen
    layers.speed = 3

    # the default screensize is 480, 320
    layers.screensize = SCREENSIZE
    combined_layers = layers.load2()

    # combined_layers = layers.load()

    collision_list = layers.load_collision()
    for rect in collision_list:
        rect.centerx += starting_position[0]
        rect.centery += starting_position[1]
    layers.calculate_map_boundary()

    event_handler = EventHandler()


    player = pygame.image.load(player_filename).convert_alpha()
    player_rect = player.get_rect(center = SCREEN.get_rect().center)



    while True:
        for event in pygame.event.get():
            event_handler.quit_game(event)
            direction = event_handler.set_direction(event, direction)

        pos, collision_list = layers.update_pos(pos, direction, collision_list)

        SCREEN.blit(combined_layers, pos)

        if RUNTEST:
            for rect in collision_list:
                tile = pygame.Surface((32, 32))
                tile.fill((255, 0, 0))
                tile.set_alpha(70)
                SCREEN.blit(tile, rect)

        SCREEN.blit(player, player_rect)

        pygame.display.update()




if __name__ == "__main__":
    main()
