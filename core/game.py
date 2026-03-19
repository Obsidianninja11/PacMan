# This is the main gameloop file that initializes Pygame and runs the game.
import pygame
import json
from pathlib import Path
from core.sceneManager import sceneHandler

# The rest is code where you implement your game using the Scenes model
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "data" / "usrSettings.json"

with SETTINGS_PATH.open("r") as f:
    settings = json.load(f)

pygame.init()
pygame.joystick.init()

flags = pygame.FULLSCREEN if settings["fullscreen"] else pygame.RESIZABLE
width = settings["width"]
height = settings["height"]
screen = pygame.display.set_mode((width, height), flags)
clock = pygame.time.Clock()
fps = settings["fps"]
STEPS = 10 # How many ticks it takes per tile

# TODO: Put into settings file
key_map = {
    "up": (pygame.K_UP, pygame.K_w),
    "down": (pygame.K_DOWN, pygame.K_s),
    "left": (pygame.K_LEFT, pygame.K_a),
    "right": (pygame.K_RIGHT, pygame.K_d)
}

class TitleScene(sceneHandler):
    def __init__(self):
        sceneHandler.__init__(self)

    def processInput(self, events, pressed_keys):
        for event in events:
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or 
                event.type == pygame.JOYAXISMOTION or
                event.type == pygame.JOYBUTTONDOWN):
                # Move to the next scene when the user pressed Enter
                self.changeScene(GameScene())

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))

class XYPair():
    # TODO: Switch to using floats for smooth movement
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: "XYPair") -> "XYPair":
        return XYPair(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "XYPair") -> "XYPair": # Prob not needed
        return XYPair(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: int):
        return XYPair(self.x * multiplier, self.y * multiplier)
    
    def __mod__(self, modulus: "XYPair"):
        return XYPair(self.x % modulus.x, self.y % modulus.y)

    # String representation, e.g. when printing
    def __repr__(self):
        # :>2 means right align with length 2 (pad with spaces)
        return f"(x:{self.x:>2}, y:{self.y:>2})"

# TODO: Move into its own file
class GameScene(sceneHandler):
    grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
            [0,0,0,0,0,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,1,0,0,0,0,0],
            [1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1],
            [0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
            [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
            [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
            [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

    GRID_WIDTH = len(grid[0])
    GRID_HEIGHT = len(grid)

    tiles = {}
    try:
        for i in range(16):
            tiles[i] = pygame.image.load(Path(__file__).resolve().parent.parent / "assets" / "4x4" / f"tile_{i:02}.png")
        tiles["blue"] = pygame.image.load(Path(__file__).resolve().parent.parent / "assets" / "blue.png")
        tiles["pacman"] = pygame.image.load(Path(__file__).resolve().parent.parent / "assets" / "pacman.png")
    except Exception as e:
        print(f"Error loading image: {e}")
        pygame.quit()
    
    image_grid = []
    for y in range(GRID_HEIGHT):
        image_grid.append([])
        for x in range(GRID_WIDTH):
            if (grid[y][x] == 1):
                # TODO: Terrible code to detect the correct tile to use
                index = (grid[y-1][x] == 0 or y == 0)*8 + (grid[y][(x+1) % GRID_WIDTH] == 0 or x == (GRID_WIDTH - 1))*4 + (grid[(y+1) % GRID_HEIGHT][x] == 0 or y == (GRID_HEIGHT - 1))*2 + (grid[y][x-1] == 0 or x == 0)
                image_grid[y].append(tiles[index])
            else:
                image_grid[y].append(tiles[0])

    step = 0
    curr_dir = XYPair(1, 0)
    desired_dir = curr_dir
    angle = -45

    coord = XYPair(1, 1)

    def isValidMove(self, coord: XYPair):
        # TODO: Allow indexing directly with coord?
        return self.grid[int(coord.y) % self.GRID_HEIGHT][int(coord.x) % self.GRID_WIDTH] == 0

    def __init__(self):
        sceneHandler.__init__(self)

    def processInput(self, events, pressed_keys):
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        # Move to the next scene when the user pressed Delete
                        self.changeScene(TitleScene())
                case pygame.JOYBUTTONDOWN:
                    # for _ in range(event.button - len(joystick_controls["button_pressed"]) + 1):
                    #     joystick_controls["button_pressed"].append(False)
                    
                    # joystick_controls["button_pressed"][event.button] = True
                    print(f"Game: Button {event.button} pressed on joystick {event.instance_id}")
                case pygame.JOYBUTTONUP:
                    # for _ in range(event.button - len(joystick_controls["button_pressed"]) + 1):
                    #     joystick_controls["button_pressed"].append(False)
            
                    # joystick_controls["button_pressed"][event.button] = False
                    print(f"Game: Button {event.button} released on joystick {event.instance_id}")

                case pygame.JOYAXISMOTION:
                    # print(event)
                    # joystick_controls["axis"][event.axis] = event.value
                    # if event.axis == 0:
                    #     self.desired_dir = [round(event.value), 0]
                    # else:
                    #     self.desired_dir = [0, round(event.value)]
                    if event.value != 0:
                        if (event.axis == 0):
                            self.desired_dir = XYPair(round(event.value), 0)
                        elif (event.axis == 1):
                            self.desired_dir = XYPair(0, round(event.value))
                    print(f"Game: Axis {event.axis} moved to {event.value} on joystick {event.instance_id}  {self.desired_dir}")

        if any(pressed_keys[key] for key in key_map["up"]):
            self.desired_dir = XYPair(0, -1)
        elif any(pressed_keys[key] for key in key_map["down"]):
            self.desired_dir = XYPair(0, 1)
        elif any(pressed_keys[key] for key in key_map["left"]):
            self.desired_dir = XYPair(-1, 0)
        elif any(pressed_keys[key] for key in key_map["right"]):
            self.desired_dir = XYPair(1, 0)

        self.step = (self.step + 1) % STEPS
        if self.step != 0:
            return
    
        # print(f"{self.desired_dir=} {self.curr_dir=}")
        # print(f"{self.coord + self.curr_dir = }")
        if self.isValidMove(self.coord + self.desired_dir):
            self.curr_dir = self.desired_dir

        if self.isValidMove(self.coord + self.curr_dir):
            if (self.curr_dir.x != 0):
                self.coord.x = (self.coord.x + self.curr_dir.x) % self.GRID_WIDTH
                # self.y_pos = int(self.y_pos)
            elif (self.curr_dir.y != 0):
                # self.x_pos = int(self.x_pos)
                self.coord.y = (self.coord.y + self.curr_dir.y) % self.GRID_HEIGHT

        self.angle = (self.curr_dir.y + 2 if self.curr_dir.x == 0 else self.curr_dir.x + 3) * 90

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        screen.fill((10, 10, 10))
        image_scale = min(width // self.GRID_WIDTH, height // self.GRID_HEIGHT) # TODO: Use xypair?
        center_offset = (width - image_scale * self.GRID_WIDTH) // 2
        for y, row in enumerate(self.image_grid):
            for x, image in enumerate(row):
                screen.blit(pygame.transform.scale(image, (image_scale, image_scale)), (image_scale * x + center_offset, image_scale * y))

        pacman = pygame.transform.rotate(pygame.transform.scale(self.tiles["pacman"], (image_scale, image_scale)), self.angle - 45)
        rect = pacman.get_rect() # I multiply the steps by 0 to temporarily disable the smooth movement
        rect.center = (image_scale * (self.coord.x + 0.5) + center_offset, image_scale * (self.coord.y + 0.5))# tiles["pacman"].get_rect().center
        screen.blit(pacman, rect)

active_scene = TitleScene()

while active_scene != None:
    pressed_keys = pygame.key.get_pressed()

    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        match event.type:
            case pygame.QUIT:
                quit_attempt = True
            case pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                # elif event.key == pygame.K_F4 and alt_pressed: # I don't think this is necessary because alt+f4 should close the window and trigger pygame.QUIT
                #     quit_attempt = True
            case pygame.VIDEORESIZE:
                width = event.size[0]
                height = event.size[1]
            case pygame.JOYDEVICEADDED:
                print("Main: Joystick added")
                joysticks = []
                for i in range(pygame.joystick.get_count()):
                    joy = pygame.joystick.Joystick(i)
                    joy.init()
                    joysticks.append(joy)
                    print(f"Main: Initialized joystick {i}: {joy.get_name()}")
            case pygame.JOYDEVICEREMOVED:
                print("Main: Joystick removed")

        if quit_attempt:
            active_scene.endGame() # Also should exit here I think? since it causes an error when the scene tries to render # There are some things maybe we want to do when it quits like saving and stuff
        else:
            filtered_events.append(event)

    # TODO: Pass argument containing game data (e.g. screen dimensions, key map, etc.)
    active_scene.processInput(filtered_events, pressed_keys)
    active_scene.gameUpdate()
    active_scene.sceneRender(screen)

    active_scene = active_scene.next_scene
    pygame.display.flip()
    clock.tick(fps)
