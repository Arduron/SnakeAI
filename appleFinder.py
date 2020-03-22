#import numpy as np
import math

def direction(blocked, appledir, snakedir):
    angle = angle_with_apple(snakedir, appledir)
    newDir = [0,0,0]
    if angle < -0.25:
        if blocked[0] == 0:
            newDir[0] = 1
        elif blocked[1] == 0:
            newDir[1] = 1
        else:
            newDir[2] = 1
    elif angle > 0.25:
        if blocked[2] == 0:
            newDir[2] = 1
        elif blocked[1] == 0:
            newDir[1] = 1
        else:
            newDir[0] = 1
    else:
        if blocked[1] == 0:
            newDir[1] = 1
        elif blocked[0] == 0:
            newDir[0] = 1
        else:
            newDir[2] = 1

    #print('Dir ' + str(newDir))
    return newDir

def getKey(snakedir, newDir):
    keyPress = [0,0,0,0] # index 0 für links, 1 hoch, 2 rechts, 3 runter
    if (snakedir[1] == -1 and newDir[0] == 1) or (snakedir[1] == 1 and newDir[2] == 1):
        keyPress[0] = 1
    if (snakedir[0] == 1 and newDir[0] == 1) or (snakedir[0] == -1 and newDir[2] == 1):
        keyPress[1] = 1
    if (snakedir[1] == 1 and newDir[0] == 1) or (snakedir[1] == -1 and newDir[2] == 1):
        keyPress[2] = 1
    if (snakedir[0] == -1 and newDir[0] == 1) or (snakedir[0] == 1 and newDir[2] == 1):
        keyPress[3] = 1
    
    return keyPress


def getCurrentDirection(snake):
    if snake.x[0] > snake.x[1]:
        return [1,0]
    elif snake.x[0] < snake.x[1]:
        return [-1,0]
    elif snake.y[0] > snake.y[1]:
        return [0,1]
    else:
        return [0,-1]

def getAppleDirection(snake, apple):
    appleVector = [1,2]
    appleVector[0] = apple.x - snake.x[0]
    appleVector[1] = apple.y - snake.y[0]
    return appleVector

def getBlocked(snake, wall, step, game):
    direction = getCurrentDirection(snake)
    front = [0,0]
    left = [0,0]
    right = [0,0]
    front[0] = snake.x[0] + direction[0] * step
    front[1] = snake.y[0] + direction[1] * step
    left[0] = snake.x[0] + direction[1] * step
    left[1] = snake.y[0] - direction[0] * step
    right[0] = snake.x[0] - direction[1] * step
    right[1] = snake.y[0] + direction[0] * step

    
    result = [0,0,0] #index 0 for left, 1 for front, 2 for right 
    for i in range(0,wall.length):
        if game.isCollision(front[0], front[1], wall.x[i], wall.y[i], step-1):
            result[1] = 1
        if game.isCollision(left[0], left[1], wall.x[i], wall.y[i], step-1):
            result[0] = 1
        if game.isCollision(right[0], right[1], wall.x[i], wall.y[i], step-1):
            result[2] = 1
    for i in range(1,snake.length):
        if game.isCollision(front[0], front[1], snake.x[i], snake.y[i], step-1):
            result[1] = 1
        if game.isCollision(left[0], left[1], snake.x[i], snake.y[i], step-1):
            result[0] = 1
        if game.isCollision(right[0], right[1], snake.x[i], snake.y[i], step-1):
            result[2] = 1
        
    return result
           
def angle_with_apple(snakedir, appledir):
    angle = math.atan2(appledir[1] * snakedir[0] - appledir[0] * snakedir[1], appledir[1] * snakedir[1] + appledir[0] * snakedir[0])/ math.pi
    angle = round(angle * 4) / 4
    #print(angle)
    return angle 












