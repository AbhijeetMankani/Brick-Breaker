from math import floor
from time import perf_counter, sleep
from tkinter import Canvas, Tk

import keyboard
from pyautogui import moveTo

from classes import *

FPS = 25

c_width, c_height = 963, 600

a_random_var = 3.14

brickGap = 2
brickCol = 12
brickRow = 18
brickCounter = brickCol * 14
brickWidth, brickHeight = 80, 20

brickGrid = [None] * (brickCol * brickRow)

# Initializing The Tkinter canvas
root = Tk()
root.title("Game")
canvas = Canvas(root, width=c_width, height=c_height)
canvas['bg'] = '#000000'
canvas.pack()

font = ('Algerian', 30, 'bold italic')
start_text_box = canvas.create_text(c_width / 2,
                                    c_height / 2,
                                    fill="#FFFFFF",
                                    text="Press Enter to Start The Game",
                                    font=font)
game_started = False
continue_ = True


def start_game():
    canvas.delete(start_text_box)
    game_started = True


score = 0
score_text = "Score: " + str(score)
score_box = canvas.create_text(c_width - 100,
                               50,
                               fill="#FFFFFF",
                               text=score_text)
started = False
total_time = 120
time_left = total_time
time_text = "Time: " + str(time_left)
time_box = canvas.create_text(c_width / 2, 50, fill="#FFFFFF", text=time_text)

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (c_width / 2)
y = (hs / 2) - (c_height / 2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (c_width, c_height, x, y))

prev_mouse_x = mouse_x = c_width / 2

ball = Ball(c_width / 2 + 1, c_height - 100, 0, 10, canvas)
sleep_for_ball = True
paddle = Paddle(431.5, canvas)

speed_text = "Speed: " + str(ball.speedY)
speed_box = canvas.create_text(100, 50, fill="#FFFFFF", text=speed_text)

canvas.update()


def motion(event):
    '''To get mouse's X Position'''
    global mouse_x
    mouse_x = event.x


root.bind('<Motion>', motion)


def awake_ball(event):
    '''Makes the ball move again, after being reset, or after the game starts'''
    global sleep_for_ball, start_time, started, time_left, time_box, info
    sleep_for_ball = False

    if (not (started) and game_started):
        started = True
        start_time = perf_counter()
        time_left = total_time
        time_text = "Time: " + str(time_left)
        canvas.itemconfigure(time_box, text=time_text)
    try:
        canvas.delete(info)
    except:
        pass


root.bind('<Button-1>', awake_ball)


def brickTileToIndex(TileCol, TileRow):
    '''Converts Row-Column Location to Index'''
    return (TileCol + brickCol * TileRow)


def brickPresent(TileCol, TileRow):
    '''Checks if brick's present value is 1(it is present) or not(it is removed)'''
    brickIndex = brickTileToIndex(TileCol, TileRow)
    return (brickGrid[brickIndex].present == 1)


def resetBricks():
    '''Resets The Brick wall '''
    global brickGrid, brickCounter
    for col in range(brickCol):
        for row in range(brickRow):
            index = brickTileToIndex(col, row)
            brickGrid[index] = Brick(col, row, 1, brickWidth * col,
                                     brickHeight * row, canvas)
    for i in range(brickCol * 3):
        brickGrid[i].delete(canvas)  # remove the brick
    for i in range(brickCol * (brickRow - 1), brickCol * brickRow):
        brickGrid[i].delete(canvas)  # remove the brick
    brickCounter = brickCol * brickRow


def reset():
    '''Rests The Ball, and Paddle Position, is called when ball falls down'''
    global sleep_for_ball, score
    sleep_for_ball = True
    paddle.movement(canvas, (c_width / 2) - (paddle.width / 2) - paddle.x, 0)
    ball.movement(canvas, paddle.x + paddle.width / 2 + 1 - ball.x,
                  c_height - 100 - ball.y)
    ball.speedX = 0
    moveTo(ws / 2, hs / 2)
    if (game_started):
        '''-5 score on ball falling down'''
        score -= 5
    score_text = "Score: " + str(score)
    canvas.itemconfigure(score_box, text=score_text)


resetBricks()


def removeAndBounceOffBrick():
    '''Removes the brick that the ball collides with, and bounce off of it'''
    global ball, brickCounter, score, score_text, score_box
    Col = floor(ball.x / brickWidth)
    Row = floor(ball.y / brickHeight)

    if (Col < 0 or Col >= brickCol or Row < 0 or Row >= brickRow):
        return  # bail out of function to avoid illegal array positioning usage error to occur
    else:
        brickIndex = brickTileToIndex(Col, Row)
        # so we know the area we've overlaped has a brick present and not already broken
        if (brickGrid[brickIndex].present == 1):
            prevBallX = ball.x - ball.speedX
            prevBallY = ball.y - ball.speedY
            prevCol = floor(prevBallX / brickWidth)
            prevRow = floor(prevBallY / brickHeight)

            BothTestsFailed = True

            if (prevCol != Col):  # Ball came in horizontally
                adjacentBrickIndex = brickTileToIndex(prevCol, Row)
                # make sure reflecting side is not blocked off
                if (brickGrid[adjacentBrickIndex].present != 1):
                    BothTestsFailed = False
                    ball.speedX *= -1

            if (prevRow != Row):  # Ball came in vertically
                adjacentBrickIndex = brickTileToIndex(Col, prevRow)
                # make sure reflecting side is not blocked off
                if (brickGrid[adjacentBrickIndex].present != 1):
                    BothTestsFailed = False
                    ball.speedY *= -1
            if (BothTestsFailed):
                ball.speedX *= -1
                ball.speedY *= -1
            brickCounter -= 1
            score += 2
            # +2 Score for every brick broken
            score_text = "Score: " + str(score)
            canvas.itemconfigure(score_box, text=score_text)
            brickGrid[brickIndex].delete(canvas)  # remove the brick
            if (brickCounter <= 5):
                for i in brickGrid:
                    i.delete(canvas)
                resetBricks()
                score += 50
                # +50 Score on removing all bricks except 6
                score_text = "Score: " + str(score)
                canvas.itemconfigure(score_box, text=score_text)


def speed_increment(event):
    '''You can decrease the speed of the ball, making 
		it more likely to lose points, but possibly have a higher max score.'''
    if (sleep_for_ball):
        ball.speedY += 1
        ball.speedY = min(ball.speedY, ball.max_speed)
        speed_text = "Speed: " + str(ball.speedY)
        canvas.itemconfigure(speed_box, text=speed_text)
        canvas.update()


def speed_decrement(event):
    '''You can decrease the speed of the ball, making 
		it less likely to lose points, but have a lower possible max score.'''
    if (sleep_for_ball):
        ball.speedY -= 1
        ball.speedY = max(ball.speedY, ball.min_speed)
        speed_text = "Speed: " + str(ball.speedY)
        canvas.itemconfigure(speed_box, text=speed_text)
        canvas.update()


root.bind('<F>', speed_increment)
root.bind('<S>', speed_decrement)
root.bind('<f>', speed_increment)
root.bind('<s>', speed_decrement)


def move():
    '''Defines the basic physical movement of ball, according to speed, 
	bounces it off the walls and resets the ball when it goes below paddle'''
    global ball, brickCounter, paddle, mouse_x, prev_mouse_x, sleep_for_ball, speed_text, info, continue_
    if (not (sleep_for_ball)):
        ball.movement(canvas, ball.speedX, ball.speedY)
        if (ball.x <= 10 or ball.x >= c_width - 10):
            ball.speedX *= -1
        if (ball.y <= 0):
            ball.speedY *= -1
        if (ball.y >= c_height - 20):
            if (ball.x >= paddle.x - paddle.width / 2 - 10
                    and ball.x <= paddle.x + paddle.width / 2 + 10):
                ball.speedY *= -1
                X = ball.x - (paddle.x)
                ball.speedX = X * 0.35
            else:
                reset()
        removeAndBounceOffBrick()
        continue_ = False
    elif (not continue_):
        info = canvas.create_text(
            c_width / 2,
            3 * c_height / 4,
            text="Left Click to Continue\nor Press F/S to change speed",
            font=font,
            justify="center",
            fill='#FFFFFF')
        root.update()
        continue_ = True

    paddle.movement(canvas, mouse_x - paddle.x, 0)
    prev_mouse_x = mouse_x


root.geometry(str(c_width) + 'x' + str(c_height))


def call():
    '''Place holder function, which is run every frame, to calculate current postion of things'''
    global time_left, time_box, started, game_started, start_time, canvas
    if (game_started):
        move()

        curr_time = perf_counter()
        if (started and time_left > 0):
            time_left = round(total_time - (curr_time - start_time))
            time_text = "Time: " + str(time_left)
            canvas.itemconfigure(time_box, text=time_text)
        if (time_left <= 0):
            ball.speedY = 0
            ball.speedX = 0
            sleep_for_ball = True
            for i in brickGrid:
                i.delete(canvas)
                font = ('Algerian', 40, 'bold italic')
            canvas.create_text(c_width / 2, c_height / 2, text="Your Final Score is " + str(score), font=font, justify="center", fill="#FFFFFF")
            font = ('Algerian', 20, 'bold italic')
            canvas.create_text(c_width / 2, 4 * c_height / 5, text="Press 'E' to exit", font=font, justify="center", fill="#FFFFFF")
    if (not (game_started)):
        # Runs one time, at the start of game, to give the user instructions
        keyboard.wait('enter')
        canvas.delete(start_text_box)

        font = ('Algerian', 15, 'bold italic')
        info = canvas.create_text(c_width / 2, 3 * c_height / 4, text="Left Click to Start Moving", font=font, justify="center", fill='#FFFFFF')
        root.update()
        sleep(2)
        canvas.itemconfigure(info, text="Move your cursor to control paddle")
        root.update()
        sleep(2)
        canvas.itemconfigure(info, text="You have 2 minutes to score as many\npoints as possible")
        root.update()
        sleep(3)
        canvas.itemconfigure(info, text='''Press F or S to\nincrease/decrese you ball speed\n(You can only change the speed while the ball is still)''')
        root.update()
        sleep(5)
        canvas.itemconfigure(info, text="Press E at any time to exit the program.")
        root.update()
        sleep(3)
        canvas.delete(info)
        root.update()
        reset()
        started = False
        game_started = True
        time_left = total_time


while 1:
    # The Clock which runs everything FPS frames per second
    call()
    root.update_idletasks()
    root.update()
    sleep(1 / FPS)

    if keyboard.is_pressed('E'):
        exit()
