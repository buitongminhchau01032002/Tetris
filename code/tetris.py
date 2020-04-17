import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 650
FPS = 60
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
GREY  = (100, 100, 100)
WHITE = (255, 255, 255)

BOARD_COLUMN = 10
BOARD_ROW = 20
SQUARESIZE = 30
BOARD_WIDTH = BOARD_COLUMN * SQUARESIZE # 300
BOARD_HEIGHT = BOARD_ROW * SQUARESIZE # 600


X_MARGIN = int((WINDOWHEIGHT - BOARD_HEIGHT)/2) # 25
Y_MARGIN = int((WINDOWHEIGHT - BOARD_HEIGHT)/2) # 25
X_SCORE = 375
Y_SCORE = 65
X_LINE = 375
Y_LINE = 325
X_SHAPENEXT = 445
Y_SHAPENEXT = 190

NUM_WIDTH = 30
NUM_HEIGHT = 40

TIME_FALL = 8

IMG_BG = pygame.image.load('img/bg.png')
IMG_Z = pygame.image.load('img/shape/Z.png')
IMG_Z_ = pygame.image.load('img/shape/Z_.png')
IMG_L = pygame.image.load('img/shape/L.png')
IMG_L_ = pygame.image.load('img/shape/L_.png')
IMG_T = pygame.image.load('img/shape/T.png')
IMG_line = pygame.image.load('img/shape/line.png')
IMG_square = pygame.image.load('img/shape/square.png')

IMG_0 = pygame.image.load('img/num/0.png')
IMG_1 = pygame.image.load('img/num/1.png')
IMG_2 = pygame.image.load('img/num/2.png')
IMG_3 = pygame.image.load('img/num/3.png')
IMG_4 = pygame.image.load('img/num/4.png')
IMG_5 = pygame.image.load('img/num/5.png')
IMG_6 = pygame.image.load('img/num/6.png')
IMG_7 = pygame.image.load('img/num/7.png')
IMG_8 = pygame.image.load('img/num/8.png')
IMG_9 = pygame.image.load('img/num/9.png')

BUTTON_WIDTH = 180
BUTTON_HEIGHT = 60
X_BUTTON = int(X_MARGIN + (BOARD_WIDTH - BUTTON_WIDTH)/2)
IMG_REPLAY = pygame.image.load('img/button/replay.png')
IMG_REPLAYHIGHLIGHT = pygame.image.load('img/button/replayHighlight.png')
IMG_BACK = pygame.image.load('img/button/back.png')
IMG_BACKHIGHLIGHT = pygame.image.load('img/button/backHighlight.png')
IMG_PLAY = pygame.image.load('img/button/play.png')
IMG_PLAYHIGHLIGHT = pygame.image.load('img/button/playHighlight.png')
IMG_QUIT = pygame.image.load('img/button/quit.png')
IMG_QUITHIGH = pygame.image.load('img/button/quitHighlight.png')

HEADING_WIDTH = 250
HEADING_HEIGHT = 120
X_HEADING = int(X_MARGIN + (BOARD_WIDTH - HEADING_WIDTH)/2)
Y_HEADING = 140
IMG_GAMEOVER = pygame.image.load('img/heading/gameover.png')
IMG_TETRIS = pygame.image.load('img/heading/tetris.png')

###### HÀM DÙNG ĐỂ RANDOM MỘT SỐ TỪ 1 ĐẾN 7. NÓ CHẠY TỐT! ĐỪNG ĐỘNG VÀO!!! ########
VALUE_RANDOM = [1, 2, 3, 4, 5, 6, 7] # Cái này dùng cho hàm rand_1_to_7
random.shuffle(VALUE_RANDOM)
def rand_1_to_7(): # Hàm này trả về một số random từ 1 đến 7
    check = []
    _sum = 0
    for i in range(8):
        _sum += i
        check.append(_sum)
    # check = [0, 1, 3, 6, 10, 15, 21, 28]
    rand = random.randint(1, 28)
    for i in range(len(check)):
        if check[i] < rand <= check[i+1]:
            val = VALUE_RANDOM[i]
            t = VALUE_RANDOM[i]
            VALUE_RANDOM.pop(i)
            VALUE_RANDOM.insert(0, t)
            return val
####################################################################################


def drawSquare(num, pos): # Vẽ những hình vuông nhỏ
    if num != 0:
        if num == 1:
            DISPLAYSURF.blit(IMG_square, pos)
        elif num == 2:
            DISPLAYSURF.blit(IMG_line, pos)
        elif num == 3:
            DISPLAYSURF.blit(IMG_T, pos)
        elif num == 4:
            DISPLAYSURF.blit(IMG_L, pos)
        elif num == 5:
            DISPLAYSURF.blit(IMG_L_, pos)
        elif num == 6:
            DISPLAYSURF.blit(IMG_Z, pos)
        elif num == 7:
            DISPLAYSURF.blit(IMG_Z_, pos)


def getXY(column, row): # Hàm lấy vị trí để vẽ dựa vào cột và hàng trên board
    return (X_MARGIN + column * SQUARESIZE, Y_MARGIN + row *  SQUARESIZE)

def addShapeToBoard(shape, board): # Hàm dùng để thêm shape vào board khi shape đã chạm đến đáy
    for row in range(4):
        for column in range(4):
            if shape.y + row >= 0 and shape.data[shape.option][row][column] != 0:
                board.data[row + shape.y][column + shape.x] = shape.data[shape.option][row][column]

def delRowsAmination(board, indexRowsDel, shape_next, score, lines): # Xoá hàng đã đủ
    indexRowsDel.reverse()
    # Hiệu ứng
    board_copy = Board()
    board_copy.data = board.data.copy()
    for index in indexRowsDel:
        board_copy.data[index] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(15):
        DISPLAYSURF.blit(IMG_BG, (0, 0))
        if i in (0, 1, 2, 3, 4,    10, 11, 12, 13, 14):
            board_copy.draw()
        else:
            board.draw()
        shape_next.draw_next()
        score.draw()
        lines.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    # Xoá và chèn thêm hàng trống
    for index in indexRowsDel:
        board.data.pop(index)
    for _ in indexRowsDel:
        board.data.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

def newShape(): # Tạo shape mới ngẫu nhiên
    data = []
    i = rand_1_to_7()
    if i == 1:
        data = Data().Z
    elif i == 2:
        data = Data().Z_
    elif i == 3:
        data = Data().T
    elif i == 4:
        data = Data().line
    elif i == 5:
        data = Data().L
    elif i == 6:
        data = Data().L_
    elif i == 7:
        data = Data().square
    return data


class Data():
    def __init__(self):
        self.square = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0]
        ]]
        self.line = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ], [
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ], [
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0]
        ]]
        self.T = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [3, 3, 3, 0],
            [0, 3, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 3, 0, 0],
            [3, 3, 0, 0],
            [0, 3, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 3, 0, 0],
            [3, 3, 3, 0],
            [0, 0, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 3, 0, 0],
            [0, 3, 3, 0],
            [0, 3, 0, 0]
        ]]
        self.L = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 4, 4, 0],
            [4, 0, 0, 0]
        ], [
            [0, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 4, 0, 0],
            [0, 4, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 4, 0],
            [4, 4, 4, 0]
        ], [
            [0, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 4, 0, 0],
            [0, 4, 4, 0]
        ]]
        self.L_ = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [5, 5, 5, 0],
            [0, 0, 5, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 5, 0],
            [0, 0, 5, 0],
            [0, 5, 5, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [5, 0, 0, 0],
            [5, 5, 5, 0]
        ], [
            [0, 0, 0, 0],
            [0, 5, 5, 0],
            [0, 5, 0, 0],
            [0, 5, 0, 0]
        ]]
        self.Z = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [6, 6, 0, 0],
            [0, 6, 6, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 6, 0],
            [0, 6, 6, 0],
            [0, 6, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [6, 6, 0, 0],
            [0, 6, 6, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 6, 0],
            [0, 6, 6, 0],
            [0, 6, 0, 0]
        ]]
        self.Z_ = [[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 7, 7, 0],
            [7, 7, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 7, 0, 0],
            [0, 7, 7, 0],
            [0, 0, 7, 0]
        ], [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 7, 7, 0],
            [7, 7, 0, 0]
        ], [
            [0, 0, 0, 0],
            [0, 7, 0, 0],
            [0, 7, 7, 0],
            [0, 0, 7, 0]
        ]]

class Shape():
    def __init__(self, data):
        self.data = data
        self.option = 0
        self.x = int((BOARD_COLUMN - 4)/2)
        self.y = -4
        self.reached = False # Kiểm tra shape đã chạm hay chưa
        self.is_fast = False # Kiểm tra có rơi nhanh hay không
    def draw(self): # Vẽ shape
        for row in range(4):
            for column in range(4):
                if self.y + row >= 0:
                    drawSquare(self.data[self.option][row][column], getXY(column + self.x, row + self.y))

    def draw_next(self): # Vẽ shape tiếp theo
        for row in range(2, 4):
            for column in range(4):
                drawSquare(self.data[self.option][row][column], (X_SHAPENEXT + column * SQUARESIZE, Y_SHAPENEXT + (row-2) * SQUARESIZE))

    def update(self, left, right, change, down, fall, board):
        if down:
            self.is_fast = True
        if left:
            self.x -= 1
            if not Shape.trueShape(self, board):
                self.x += 1
        elif right:
            self.x += 1
            if not Shape.trueShape(self, board):
                self.x -= 1
        if change:
            self.option += 1
            if self.option == 4:
                self.option = 0
            if not Shape.trueShape(self, board):
                self.option -= 1
                if self.option == -1:
                    self.option = 3
        if fall:
            self.y += 1
            if not Shape.trueShape(self, board):
                self.y -= 1
                self.reached = True
    
    def trueShape(shape, board): # Kiểm tra shape có thể nằm trên board hay không
        for row in range(4):
            for column in range(4):
                if shape.data[shape.option][row][column] != 0:
                    if shape.x + column < 0 or shape.x + column >= BOARD_COLUMN or shape.y + row >= BOARD_ROW:
                        return False
                    if shape.y + row >= 0 and board.data[shape.y + row][shape.x + column] != 0:
                        return False
        return True


class Board():
    def __init__(self):
        self.data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    def draw(self):
        for row in range(BOARD_ROW):
            for column in range(BOARD_COLUMN):
                drawSquare(self.data[row][column], getXY(column, row))
    

class Num5(): # 5 số ở Score và Lines
    def __init__(self, x, y):
        self.data = 0
        self.x = x
        self.y = y
    def add(self, val): # Cộng thêm giá trị
        self.data += val 
    def draw(self): 
        listNum = [int(x) for x in str(self.data)]
        for i in range(5 - len(listNum)):
            listNum.insert(0, None)
 
        for index, num in enumerate(listNum):
            x = self.x + (NUM_WIDTH + 10) *  index
            y = self.y
            if num == 0:
                DISPLAYSURF.blit(IMG_0, (x, y))
            elif num == 1:
                DISPLAYSURF.blit(IMG_1, (x, y))
            elif num == 2:
                DISPLAYSURF.blit(IMG_2, (x, y))
            elif num == 3:
                DISPLAYSURF.blit(IMG_3, (x, y))
            elif num == 4:
                DISPLAYSURF.blit(IMG_4, (x, y))
            elif num == 5:
                DISPLAYSURF.blit(IMG_5, (x, y))
            elif num == 6:
                DISPLAYSURF.blit(IMG_6, (x, y))
            elif num == 7:
                DISPLAYSURF.blit(IMG_7, (x, y))
            elif num == 8:
                DISPLAYSURF.blit(IMG_8, (x, y))
            elif num == 9:
                DISPLAYSURF.blit(IMG_9, (x, y))

class Button():
    def __init__(self, img, imgHighlight, x, y, width, height):
        self.img = img
        self.imgHighlight = imgHighlight
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.choose = False
    
    def draw(self, mouseXY):
        if self.x <= mouseXY[0] <= self.x + self.width and self.y <= mouseXY[1] <= self.y + self.height:
            self.choose = True
            DISPLAYSURF.blit(self.imgHighlight, (self.x, self.y))
        else:
            self.choose = False
            DISPLAYSURF.blit(self.img, (self.x, self.y))


class Heading(): 
    def __init__(self, img, x, y, width, height):
        self.img = img
        self.x = x
        self.y = y

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))

class Scenes():
    def __init__(self, option = 0):
        self.option = option
    
    def gameStart(self):
        DISPLAYSURF.blit(IMG_BG, (0, 0))
        mouseXY = [0, 0]
        mouseClicked = False
        listY = [285 + i*(BUTTON_HEIGHT + 25) for i in range(2)]
        tetrisHeading = Heading(IMG_TETRIS, X_HEADING, Y_HEADING, HEADING_WIDTH, HEADING_HEIGHT)
        playButton = Button(IMG_PLAY, IMG_PLAYHIGHLIGHT, X_BUTTON, listY[0], BUTTON_WIDTH, BUTTON_HEIGHT)
        quitButton = Button(IMG_QUIT, IMG_QUITHIGH, X_BUTTON, listY[1], BUTTON_WIDTH, BUTTON_HEIGHT)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouseXY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseXY = event.pos
                    mouseClicked = True
            tetrisHeading.draw()
            playButton.draw(mouseXY)
            quitButton.draw(mouseXY)

            if mouseClicked and playButton.choose:
                self.option = 1
                break
            elif mouseClicked and quitButton.choose:
                pygame.quit()
                sys.exit()
            else:
                mouseClicked = False
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            

    def gamePlay(self, board, score, lines):
        board.__init__()
        shape = Shape(newShape())
        shape_next = Shape(newShape())
        left = False
        right = False
        down = False
        change = False
        fall = False
        time_fall = TIME_FALL
        const_time_fast = 1 # Rơi nhanh
        score.data = 0
        lines.data = 0
        isGameover = False
        while not isGameover:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        left = True
                    elif event.key == K_RIGHT:
                        right = True
                    if event.key == K_UP:
                        change = True
                    if event.key == K_DOWN:
                        down = True
            DISPLAYSURF.blit(IMG_BG, (0, 0))
            board.draw()
            shape.draw()
            shape.update(left, right, change, down, fall, board)
            shape_next.draw_next()
            score.draw()
            lines.draw()

            if shape.reached:
                if shape.y <= -3:
                    isGameover = True
                addShapeToBoard(shape, board)
                shape = shape_next
                shape_next = Shape(newShape())
                time_fall = TIME_FALL

            indexRowsDel = []
            for row in range(len(board.data)):
                # Nếu không còn ô trống trong hàng thì thêm vào index
                if 0 not in board.data[row]:
                    indexRowsDel.append(row)
            numRowDel = len(indexRowsDel)
            if numRowDel > 0:
                delRowsAmination(board, indexRowsDel, shape_next, score, lines)
                score.add(numRowDel ** 2) # Tăng điểm
                lines.add(numRowDel) # tăng lines
            if shape.is_fast == True:
                const_time_fast = 20 # Rơi nhanh hơn 20 lần
            else:
                const_time_fast = 1
            const_time_lines = (int(lines.data/10))*0.1 # Rơi nhanh theo Lines
            if time_fall >= TIME_FALL:
                time_fall = 0
                fall = True
            else:
                fall = False
            left = False
            right = False
            down = False
            change = False
            time_fall += const_time_fast*(1 + const_time_lines) # Đếm thời gian để rơi
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        self.option = 2

    def gameOver(self, board, score, lines):
        listY = [285 + i*(BUTTON_HEIGHT + 25) for i in range(2)]
        replayButton = Button(IMG_REPLAY, IMG_REPLAYHIGHLIGHT, X_BUTTON, listY[0], BUTTON_WIDTH, BUTTON_HEIGHT)
        backButton = Button(IMG_BACK, IMG_BACKHIGHLIGHT, X_BUTTON, listY[1], BUTTON_WIDTH, BUTTON_HEIGHT)
        gameoverHeading = Heading(IMG_GAMEOVER, X_HEADING, Y_HEADING, HEADING_WIDTH, HEADING_HEIGHT)
        mouseClicked = False
        mouseXY = [0, 0]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouseXY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseXY = event.pos
                    mouseClicked = True

            gameoverHeading.draw()
            replayButton.draw(mouseXY)
            backButton.draw(mouseXY)

            if mouseClicked and replayButton.choose:
                self.option = 1
                break
            elif mouseClicked and backButton.choose:
                self.option = 0
                break
            else:
                mouseClicked = False
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.display.set_caption('TETRIS')
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    board = Board()
    score = Num5(X_SCORE, Y_SCORE)
    lines = Num5(X_LINE, Y_LINE)
    scene = Scenes(0)
    while True:
        if scene.option == 0:
            scene.gameStart()
        elif scene.option == 1:
            scene.gamePlay(board, score, lines)
        elif scene.option == 2:
            scene.gameOver(board, score, lines)



if __name__ == "__main__":
    main()