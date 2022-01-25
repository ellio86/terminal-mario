import win32gui, win32con, curses, sys, time
CURSES_COLORS = [curses.COLOR_WHITE, curses.COLOR_BLACK, curses.COLOR_RED, curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_CYAN, curses.COLOR_YELLOW]
FRAMERATE = 60
KEY_LEFT = "a"
KEY_RIGHT = "d"
KEY_DOWN = "s"
KEY_JUMP = " "
KEY_SPRINT = "\\"

mario_sprite = [[9,9,9,9,9,3,3,3,3,3,3,9,9,9,9,9,9],
                [9,9,9,9,3,3,3,3,3,3,3,3,3,3,9,9,9],
                [9,9,9,9,2,2,2,2,8,8,2,8,9,9,9,9,9],
                [9,9,9,2,2,8,2,8,8,8,2,8,8,8,9,9,9],
                [9,9,9,2,2,8,2,2,8,8,8,2,8,8,8,9,9],
                [9,9,9,2,2,2,8,8,8,8,2,2,2,2,9,9,9],
                [9,9,9,9,9,8,8,8,8,8,8,8,8,9,9,9,9],
                [9,9,9,9,2,2,2,3,2,2,2,9,9,9,9,9,9],
                [9,9,9,2,2,2,2,3,2,2,3,2,2,2,9,9,9],
                [9,9,2,2,2,2,2,3,3,3,3,2,2,2,2,9,9],
                [9,9,8,8,8,2,3,8,3,3,8,3,2,8,8,9,9],
                [9,9,8,8,8,8,3,3,3,3,3,3,8,8,8,9,9],
                [9,9,8,8,8,3,3,3,3,3,3,3,3,8,8,9,9],
                [9,9,9,9,3,3,3,3,9,3,3,3,3,9,9,9,9],
                [9,9,9,2,2,2,2,9,9,9,2,2,2,2,9,9,9],
                [9,9,2,2,2,2,2,9,9,9,2,2,2,2,2,9,9]]

mario_walking = [
                [[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,3,3,3,3,3,9,9,9,9,9,9],
                 [9,9,9,9,3,3,3,3,3,3,3,3,3,9,9,9],
                 [9,9,9,9,2,2,2,8,8,2,8,9,9,9,9,9],
                 [9,9,9,2,8,2,8,8,8,2,8,8,8,9,9,9],
                 [9,9,9,2,8,2,2,8,8,8,2,8,8,8,9,9],
                 [9,9,9,2,2,8,8,8,8,2,2,2,2,9,9,9],
                 [9,9,9,9,9,8,8,8,8,8,8,8,9,9,9,9],
                 [9,9,9,9,2,2,2,3,2,2,9,9,9,9,9,9],
                 [9,9,9,2,2,2,2,3,3,2,2,9,9,9,9,9],
                 [9,9,9,2,2,2,3,3,8,3,3,9,9,9,9,9],
                 [9,9,9,2,2,2,2,3,3,3,3,9,9,9,9,9],
                 [9,9,9,3,2,2,8,8,3,3,3,9,9,9,9,9],
                 [9,9,9,9,3,2,8,8,3,3,9,9,9,9,9,9],
                 [9,9,9,9,9,3,3,3,2,2,2,9,9,9,9,9],
                 [9,9,9,9,9,2,2,2,2,9,9,9,9,9,9,9]],
                
                 [[9,9,9,9,9,3,3,3,3,3,9,9,9,9,9,9],
                 [9,9,9,9,3,3,3,3,3,3,3,3,3,9,9,9],
                 [9,9,9,9,2,2,2,8,8,2,8,9,9,9,9,9],
                 [9,9,9,2,8,2,8,8,8,2,8,8,8,9,9,9],
                 [9,9,9,2,8,2,2,8,8,8,2,8,8,8,9,9],
                 [9,9,9,2,2,8,8,8,8,2,2,2,2,9,9,9],
                 [9,9,9,9,9,8,8,8,8,8,8,8,9,9,9,9],
                 [9,9,9,9,9,9,2,2,3,3,2,9,9,9,9,9],
                 [9,9,9,9,9,2,2,2,2,3,2,8,8,9,9,9],
                 [9,9,9,8,8,2,2,2,2,2,2,8,8,8,9,9],
                 [9,9,8,8,8,3,2,2,2,2,2,8,8,9,9,9],
                 [9,9,9,2,2,3,3,3,3,3,3,3,9,9,9,9],
                 [9,9,9,2,3,3,3,3,3,3,3,3,9,9,9,9],
                 [9,9,2,2,3,3,9,9,3,3,3,9,9,9,9,9],
                 [9,9,2,9,9,9,9,2,2,2,9,9,9,9,9,9],
                 [9,9,9,9,9,9,9,9,2,2,2,9,9,9,9,9]],
                 
                 [[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,3,3,3,3,3,9,9,9,9,9,9],
                 [9,9,9,9,3,3,3,3,3,3,3,3,3,9,9,9],
                 [9,9,9,9,2,2,2,8,8,2,8,9,9,9,9,9],
                 [9,9,9,2,8,2,8,8,8,2,8,8,8,9,9,9],
                 [9,9,9,2,8,2,2,8,8,8,2,8,8,8,9,9],
                 [9,9,9,2,2,8,8,8,8,2,2,2,2,9,9,9],
                 [9,9,9,9,9,8,8,8,8,8,8,8,9,9,9,9],
                 [9,9,9,9,2,2,2,3,2,2,9,9,9,9,9,9],
                 [9,9,9,2,2,2,2,3,3,2,2,9,9,9,9,9],
                 [9,9,9,2,2,2,3,3,8,3,3,9,9,9,9,9],
                 [9,9,9,2,2,2,2,3,3,3,3,9,9,9,9,9],
                 [9,9,9,3,2,2,8,8,3,3,3,9,9,9,9,9],
                 [9,9,9,9,3,2,8,8,3,3,9,9,9,9,9,9],
                 [9,9,9,9,9,3,3,3,2,2,2,9,9,9,9,9],
                 [9,9,9,9,9,2,2,2,2,9,9,9,9,9,9,9]],
                 
                 [[9,9,9,9,9,3,3,3,3,3,9,9,9,9,9,9],
                 [9,9,9,9,3,3,3,3,3,3,3,3,3,9,9,9],
                 [9,9,9,9,2,2,2,8,8,2,8,9,9,9,9,9],
                 [9,9,9,2,8,2,8,8,8,2,8,8,8,9,9,9],
                 [9,9,9,2,8,2,2,8,8,8,2,8,8,8,9,9],
                 [9,9,9,2,2,8,8,8,8,2,2,2,2,9,9,9],
                 [9,9,9,9,9,8,8,8,8,8,8,8,9,9,9,9],
                 [9,9,2,2,2,2,3,2,2,2,3,9,9,9,9,9],
                 [8,8,2,2,2,2,3,3,2,2,2,3,2,8,8,8],
                 [8,8,8,9,2,2,3,3,3,3,3,3,3,2,8,8],
                 [8,8,9,9,3,3,3,8,3,3,3,8,9,9,2,9],
                 [9,9,9,3,3,3,3,3,3,3,3,3,3,2,2,9],
                 [9,9,3,3,3,3,3,3,3,3,3,3,3,2,2,9],
                 [9,2,2,3,3,3,9,9,9,9,3,3,3,2,2,9],
                 [9,2,2,2,9,9,9,9,9,9,9,9,9,9,9,9],
                 [9,9,2,2,2,9,9,9,9,9,9,9,9,9,9,9]],
                 
                 [[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
                 [9,9,9,9,9,3,3,3,3,3,9,9,9,9,9,9],
                 [9,9,9,9,3,3,3,3,3,3,3,3,3,9,9,9],
                 [9,9,9,9,2,2,2,8,8,2,8,9,9,9,9,9],
                 [9,9,9,2,8,2,8,8,8,2,8,8,8,9,9,9],
                 [9,9,9,2,8,2,2,8,8,8,2,8,8,8,9,9],
                 [9,9,9,2,2,8,8,8,8,2,2,2,2,9,9,9],
                 [9,9,9,9,9,8,8,8,8,8,8,8,9,9,9,9],
                 [9,9,9,9,2,2,2,3,2,2,9,9,9,9,9,9],
                 [9,9,9,2,2,2,2,3,3,2,2,9,9,9,9,9],
                 [9,9,9,2,2,2,3,3,8,3,3,9,9,9,9,9],
                 [9,9,9,2,2,2,2,3,3,3,3,9,9,9,9,9],
                 [9,9,9,3,2,2,8,8,3,3,3,9,9,9,9,9],
                 [9,9,9,9,3,2,8,8,3,3,9,9,9,9,9,9],
                 [9,9,9,9,9,3,3,3,2,2,2,9,9,9,9,9],
                 [9,9,9,9,9,2,2,2,2,9,9,9,9,9,9,9]],
                 
                 ]

brick_sprite = [[8,1,1,1,1,1,1,1,1,2,8,1,1,1,1,8],
                [1,8,8,8,8,8,8,8,8,2,1,8,8,8,8,2],
                [1,8,8,8,8,8,8,8,8,2,1,8,8,8,8,2],
                [1,8,8,8,8,8,8,8,8,2,1,8,8,8,8,2],
                [1,8,8,8,8,8,8,8,8,2,1,2,8,8,8,2],
                [1,8,8,8,8,8,8,8,8,2,8,2,2,2,2,8],
                [1,8,8,8,8,8,8,8,8,2,1,1,1,1,1,2],
                [1,8,8,8,8,8,8,8,8,2,1,8,8,8,8,2],
                [1,8,8,8,8,8,8,8,8,2,1,8,8,8,8,2],
                [1,8,8,8,8,8,8,8,8,2,1,8,8,8,8,2],
                [2,2,8,8,8,8,8,8,2,1,8,8,8,8,8,2],
                [1,1,2,2,8,8,8,8,2,1,8,8,8,8,8,2],
                [1,8,1,1,2,2,2,2,1,8,8,8,8,8,8,2],
                [1,8,8,8,1,1,1,2,1,8,8,8,8,8,8,2],
                [1,8,8,8,8,8,8,2,1,8,8,8,8,8,2,2],
                [8,2,2,2,2,2,2,8,1,2,2,2,2,2,2,8],]

hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

class Surface:
    def __init__(self, width: int = 230, height: int = 66, background_color:int = 0) -> None:
        self._width = width
        self._height = height
        self.grid = [[background_color for _ in range(self._width)] for _ in range(self._height)]
        
        
class Sprite:
    def __init__(self, pixel_array:list[list[int]]) -> None:
        self.pixel_array = pixel_array
        self.width = len(pixel_array[0])
        self.height = len(pixel_array)
        self.center = (0, 0)    # Top Left
        self.animations = {}
        self.animations["default"] = pixel_array
        self.current_animation = "default"
        self.current_frame = 0
    
    def place(self, surface: Surface, x_pos, y_pos):
        """ Draw Sprite to surface """
        for x, line in enumerate(self.pixel_array):
            for y, pixel in enumerate(line):
                try:
                    surface.grid[x + x_pos][y + y_pos] = pixel if pixel != 9 else surface.grid[x + x_pos][y + y_pos]
                except IndexError:
                    pass
                
    def add_animation(self, animation_array: list[list[list[int]]], title: str) -> None:
        self.animations[title] = animation_array
        
    def change_animation(self, animation):
        if animation in self.animations:
            self.current_frame = 0
            self.current_animation = animation
            
    def next_frame(self):
        if len(self.animations[self.current_animation]) - 1 == self.current_frame:
            self.pixel_array = self.animations[self.current_animation][0]
            self.current_frame = 0
        else:
            self.pixel_array = self.animations[self.current_animation][self.current_frame + 1]
            self.current_frame += 1
        
        
class GameObject:
    def __init__(self, sprite, x_pos, y_pos):
        self.sprite = Sprite(sprite)
        self.hitbox_width = self.sprite.width
        self.hitbox_height = self.sprite.height
        self.x_pos = x_pos
        self.y_pos = y_pos
        
class Mario(GameObject):
    def __init__(self, sprite, x_pos, y_pos):
        super().__init__(sprite, x_pos, y_pos)
        self.x_vel = 0
        self.y_vel = 0
        self.x_speed = 0x0000
        self.y_speed = 0  
        self.direction = "R"
        self.__max_walk_speed = 0x1900
        self.__max_sprint_speed = 0x2900
        
    def update_pos(self):
        self.x_pos += self.x_speed // 0x1000 if self.x_speed >= 0 else self.x_speed // 0x1000 + 1
        
    def accelerate(self, speed: int, sprinting: bool, turning: bool):
        if abs(self.x_speed + speed) > self.__max_walk_speed and not sprinting and not turning:
            self.x_speed = -self.__max_walk_speed if speed < 0 else self.__max_walk_speed
            
        elif abs(self.x_speed + speed) > self.__max_sprint_speed and not turning:
            self.x_speed = -self.__max_sprint_speed if speed < 0 else self.__max_sprint_speed
        else:
            self.x_speed += speed
class Block(GameObject):
    def __init__(self, sprite, x_pos, y_pos):
        super().__init__(sprite, x_pos, y_pos)
        

def play_game():
    def _play_game(stdscr):
        stdscr.clear()
        stdscr.nodelay(True)
        curses.start_color()
        if not curses.has_colors():
            raise Exception
        for n, color in enumerate (CURSES_COLORS, 1):
            curses.init_pair(n, color, color)
        stdscr.clear()
        stdscr.refresh()
        key_left = "a"
        key_right = "d"
        key_down = "s"
        key_jump = " "
        key_sprint = "\\"
        
        
        bg_color = 7
        surf = Surface(background_color=bg_color)
        player = Mario(mario_sprite, 25, 34)
        player.sprite.add_animation(mario_walking, "walking")
        bricks = [Block(brick_sprite, x, 50) for x in range(0, 256, 16)]
        playing = True
        frame = 0
        code=0
        code_list = []

        prev_time = time.perf_counter()
        while playing:
            # Limit FPS to FRAMERATE
            if time.perf_counter() - prev_time >= 1/FRAMERATE:
                prev_time = time.perf_counter()
                if frame == 60:
                    frame = 0
                frame += 1
                
                
                if len(code_list) == 11:
                    code_list.pop(0)
                    
                ## USER INPUT
                code = stdscr.getch()
                code_list.append(code)
                if code != -1:
                    match chr(code):
                        case "d":
                            if player.direction == "R":
                                if player.x_speed < 0x0630:
                                    player.accelerate(0x0630, False, False)
                                else:
                                    player.accelerate(0x0098, False, False)
                            else:
                                player.accelerate(0x0098, False, True)
                            
                            player.direction = "R"
                            if player.sprite.current_animation != "walking":
                                player.sprite.change_animation("walking")
                                
                        
                        case "a":
                            if player.direction == "L":
                                if player.x_speed > -0x0630:
                                    player.accelerate(-0x0630, False, False)
                                else:
                                    player.accelerate(-0x0098, False, False)
                            else:
                                player.accelerate(-0x0098, False, True)
                                
                            player.direction = "L"
                        
                if all(code == -1 for code in code_list):
                    if player.direction == "R":
                        player.accelerate(-0x00D0, False, False)
                        if player.x_speed < 0:
                            player.x_speed = 0
                    else:
                        player.accelerate(0x00D0, False, False)
                        if player.x_speed > 0:
                            player.x_speed = 0
                        
                    player.sprite.change_animation("idle")    
                
                else:
                    if frame % 15 == 0:
                        player.sprite.next_frame()
                     
                player.update_pos()
                stdscr.refresh()
                    

                
                
                ## PLACE SPRITES
                surf.grid = [[7 for _ in range(230)] for _ in range(66)]
                player.sprite.place(surf, player.y_pos, player.x_pos)
                for brick in bricks:
                    brick.sprite.place(surf,  brick.y_pos, brick.x_pos)
                ## DRAW TO SCREEN
                for x, line in enumerate(surf.grid):
                    for y, pixel in enumerate(line):
                            try:    
                                stdscr.addstr(x, y, "_", curses.color_pair(pixel)) 
                            except curses.error:
                                pass
                            
                ## Info and debug
                
            try:
                stdscr.addstr(0, 0, f"{time.perf_counter()}")
                stdscr.addstr(1, 0, f"{frame=}")
                stdscr.addstr(2, 0, f"{hex(player.x_speed)=}")
                stdscr.addstr(3, 0, f"{player.x_pos=}")
                stdscr.addstr(4, 0, f"{player.direction=}")
                stdscr.addstr(5, 0, f"{code}")
                stdscr.addstr(6, 0, f"{all(c == -1 for c in code_list)}")
                
                
            except curses.error:
                pass
            stdscr.refresh()
            

    return curses.wrapper(_play_game)

if __name__ == "__main__":
    print(play_game())
