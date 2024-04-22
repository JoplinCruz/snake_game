from win32api import GetKeyState
from random import randrange
from snakeCustomWall import wall as customwall
import time



class Snake:
    
    def __init__(self, *, width: int | None=52, heigth: int | None=20, speed: int | None=8) -> None:
        
        self.key = GetKeyState

        self.head_pos = [7, 7]  # coordinate x, y
        self.offset = [1, 1]    # coordinate x, y
        
        self.wall = customwall(width, heigth)
        self.width = width
        self.heigth = heigth
        self.speed = speed
        
        self.clearscreen = '\033[2J'
        self.hiddencursor = '\033[?25l'
        self.showcursor = '\033[?25h'
        self.locate = '\033[{};{}H'
        
        self.snakehead = "☻"
        self.snakebody = "○"
        self.clear = " "
        self.move = "stand_by"

        self.rate = .1

        self.release = [0, 1]
        self.velocity = 0
        
        self.tail = 4
        
        self.body_pos = [[7, 7]] * (self.tail+1) # coordinate [x, y]

        
    def gameboard(self) -> None:
        for i in range(len(self.wall)):
            for j in range(len(self.wall[i])):
                if self.wall[i][j] == 1:
                    print(self.locate.format(i + self.offset[1], j + self.offset[0]) + "▓")   # ░▒▓█
        print(self.locate.format(self.offset[1], self.offset[0] + (len(self.wall[0]) // 2) - 12) + "|===|__SNAKE__GAME__|===|", end="")
        print(self.locate.format(self.offset[1] + len(self.wall) - 1, self.offset[0] + (len(self.wall[0]) // 2) - 12) + "|---< SCORE:        >---|", end="")
    
    def gamescore(self, score: int) -> None:
        print(self.locate.format(self.offset[1] + len(self.wall) - 1, self.offset[0] + (len(self.wall[0]) // 2) + 1), score, end="")
    
    def blankscreen(self) -> None:
        print(self.clearscreen)
    
    def cursoroff(self) -> None:
        print(self.hiddencursor)
    
    def cursoron(self) -> None:
        print(self.showcursor)
    
    def apple(self, apple) -> None:
        print(self.locate.format(apple[1] + self.offset[1], apple[0] + self.offset[0]) + "♥", end="")
    
    
    def snake(self) -> None:
        print(self.locate.format(self.head_pos[1] + self.offset[1], self.head_pos[0] + self.offset[0]) + self.snakehead, end="")

    def snaketail(self, body_pos) -> None:
        print(self.locate.format(body_pos[1] + self.offset[1], body_pos[0] + self.offset[0]) + self.snakebody, end="")

    def cleartrail(self, body_pos) -> None:
        print(self.locate.format(body_pos[1] + self.offset[1], body_pos[0] + self.offset[0]) + self.clear, end="")
    
    
    def verifybody(self, apple) -> bool:
        if apple in self.body_pos:
            self.generateapple()
        return True
        
    def generateapple(self) -> (list[int, int] | None):
        x_quarter = len(self.wall[0]) // 2
        y_quarter = len(self.wall) // 2
        
        if self.head_pos[0] < x_quarter:
            x_apple = randrange(x_quarter, (x_quarter * 2) - 2)
        else:
            x_apple = randrange(2, x_quarter)
        
        if self.head_pos[1] < y_quarter:
            y_apple = randrange(y_quarter, (y_quarter * 2) - 1)
        else:
            y_apple = randrange(1, y_quarter)
        
        apple = [x_apple, y_apple]
        
        if self.verifybody(apple):
            return apple
    
    
    def gameover(self, score) -> None:
        # self.blankscreen()
        self.cursoron()
        print(self.locate.format(self.offset[1] + (len(self.wall) // 2) - 1, self.offset[0] + (len(self.wall[0]) // 2) - 9) + "<<  GAME  OVER  >>", end="")
        # print(self.locate.format(self.offset[1] + (len(self.wall) // 2) - 2, self.offset[0] + (len(self.wall[0]) // 2) - 10) + "<< YOUR SCORE: {} >>".format(score), "\n\n")
        print(self.locate.format(self.offset[1] + (len(self.wall)), 1), end="")
        time.sleep(5)
    
    
    def startgame(self) -> None:
        
        self.blankscreen()
        self.cursoroff()
        self.gameboard()
        
        score = 0
        counter = 0
        
        apple = self.generateapple()
        self.gamescore(score)
        
        while True:
            
            up = self.key(0x26)
            right = self.key(0x27)
            down = self.key(0x28)
            left = self.key(0x25)
            
            esc = self.key(0x1b)
            
            self.cleartrail(self.body_pos[counter - self.tail - 1])
            self.snakebody = "·"; self.snaketail(self.body_pos[counter - self.tail]); self.snakebody = "○"
            
            self.body_pos[counter] = [int(self.head_pos[0]), int(self.head_pos[1])]
            
            
            if (right not in self.release) and (self.move != "left"):
                self.move = "right"
                self.snakehead = "►"
                self.rate = 0.1
                self.velocity = 1
            
            if (down not in self.release) and (self.move != "up"):
                self.move = "down"
                self.snakehead = "▼"
                self.rate = 0.2
                self.velocity = 1
            
            if (left not in self.release) and (self.move != "right"):
                self.move = "left"
                self.snakehead = "◄"
                self.rate = 0.1
                self.velocity = 1
            
            if (up not in self.release) and (self.move != "down"):
                self.move = "up"
                self.snakehead = "▲"
                self.rate = 0.2
                self.velocity = 1
            
            if esc not in self.release:
                return False
            
            
            match self.move:
                case "right":
                    self.head_pos[0] += self.velocity
                    if self.wall[self.head_pos[1]][self.head_pos[0]] == 1:
                        self.head_pos[0] = 2
                case "down":
                    self.head_pos[1] += self.velocity
                    if self.wall[self.head_pos[1]][self.head_pos[0]] == 1:
                        self.head_pos[1] = 1
                case "left":
                    self.head_pos[0] -= self.velocity
                    if self.wall[self.head_pos[1]][self.head_pos[0]] == 1:
                        self.head_pos[0] = len(self.wall[self.head_pos[1]]) - 3
                case "up":
                    self.head_pos[1] -= self.velocity
                    if self.wall[self.head_pos[1]][self.head_pos[0]] == 1:
                        self.head_pos[1] = len(self.wall) - 2
            
                
            if self.velocity == 1:
                
                self.snaketail(self.body_pos[counter])
                
                if self.head_pos in self.body_pos[:counter] or self.head_pos in self.body_pos[counter + 1:]:
                    self.snakehead = "*"; self.snake()
                    self.gameover(score)
                    return False
                
                
                if self.head_pos == apple:
                    counter += 1
                    score += 10
                    self.tail += 1
                    self.body_pos.insert(counter, [int(self.head_pos[0]), int(self.head_pos[1])])
                    apple = self.generateapple()
                    # self.apple(apple)
                    self.gamescore(score)
            
            self.apple(apple)
            self.snake()
            
            
            if (counter >= self.tail) or (self.velocity == 0):
                counter = 0
            else:
                counter += 1
            
            
            time.sleep(self.rate / self.speed)


if __name__ == "__main__":
    snake = Snake(width=52,
                  heigth=18,
                  speed=3)
    snake.startgame()
