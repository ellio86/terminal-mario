import win32gui, win32con, curses, sys

mario_sprite = [[9,9,9,3,3,3,3,3,3,9,9,9,9],
                [9,9,3,3,3,3,3,3,3,3,3,3,9],
                [9,9,2,2,2,2,8,8,2,8,9,9,9],
                [9,2,2,8,2,8,8,8,2,8,8,8,9],
                [9,2,2,8,2,2,8,8,8,2,8,8,8],
                [9,2,2,2,8,8,8,8,2,2,2,2,9],
                [9,9,9,8,8,8,8,8,8,8,8,9,9],
                [9,9,2,2,2,3,2,2,2,9,9,9,9],
                [9,2,2,2,2,3,2,2,3,2,2,2,9],
                [2,2,2,2,2,3,3,3,3,2,2,2,2],
                [8,8,8,2,3,8,3,3,8,3,2,8,8],
                [8,8,8,8,3,3,3,3,3,3,8,8,8],
                [8,8,8,3,3,3,3,3,3,3,3,8,8],
                [9,9,3,3,3,3,9,3,3,3,3,9,9],
                [9,2,2,2,2,9,9,9,2,2,2,2,9],
                [2,2,2,2,2,9,9,9,2,2,2,2,2]]

hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

class Surface:
    def __init__(self, width: int = 230, height: int = 70, background_color:int = 0) -> None:
        self._width = width
        self._height = height
        self.grid = [[background_color for _ in range(self._width)] for _ in range(self._height)]
        
        
class Sprite:
    def __init__(self, pixel_array:list[list[int]]) -> None:
        self.pixel_array = pixel_array
        self.width = len(pixel_array[0])
        self.height = len(pixel_array)
        self.center = (0, 0)    # Top Left
    
    def place(self, surface: Surface, xpos, ypos):
        """ Draw Sprite to surface """
        for x, line in enumerate(self.pixel_array):
            for y, pixel in enumerate(line):
                try:
                    surface.grid[x + xpos][y + ypos] = pixel
                except IndexError:
                    pass
                

class Player:
    def __init__(self, sprite):
        self.sprite = Sprite(sprite)

def play_game():
    def _play_game(stdscr):
        curses.start_color()
        if not curses.has_colors():
            raise Exception
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        stdscr.clear()
        stdscr.refresh()
        bg_color = 7
        surf = Surface(background_color=bg_color)
        player = Player(mario_sprite)
        playing = True
        while playing:
            ## PLACE SPRITES
            player.sprite.place(surf, 50, 25)
            
            ## DRAW TO SCREEN
            for x, line in enumerate(surf.grid):
                for y, pixel in enumerate(line):
                        try:    
                            stdscr.addstr(x, y, "_", curses.color_pair(pixel)) if pixel != 9 else stdscr.addstr(x, y, "_", curses.color_pair(bg_color))
                        except curses.error:
                            pass
                        
            stdscr.refresh()

    return curses.wrapper(_play_game)

if __name__ == "__main__":
    print(play_game())
