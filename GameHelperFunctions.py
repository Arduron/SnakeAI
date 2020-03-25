#import numpy as np
import math

def getCurrentDirection(snake):
    if snake.x[0] > snake.x[1]:
        return [1.0,0]
    elif snake.x[0] < snake.x[1]:
        return [-1.0,0]
    elif snake.y[0] > snake.y[1]:
        return [0,1.0]
    else:
        return [0,-1.0]

def getAppleDirection(snake, apple):
    appleVector = [1,2]
    appleVector[0] = apple.x - snake.x[0]
    appleVector[1] = apple.y - snake.y[0]
    return appleVector

def getBlocked(snake, wall, step, game):
    direction = getCurrentDirection(snake)
    #Variablen für Koordinaten der Blöcke in der jeweiligen Richtung, immer mit [x1,x2,(x3),y1,y2,(y3)]
    leftBackBlocks = [0,0,0,0,0,0]
    leftBlocks = [0,0,0,0,0,0]
    leftFrontBlocks = [0,0,0,0,0,0]
    frontBlocks = [0,0,0,0,0,0]
    rightFrontBlocks = [0,0,0,0,0,0]
    rightBlocks = [0,0,0,0,0,0]
    rightBackBlocks = [0,0,0,0,0,0]

    for i in range(1, int(len(frontBlocks) / 2) + 1):
        leftBlocks[i-1] = snake.x[0] + direction[1] * step * i
        leftBlocks[i+2] = snake.y[0] - direction[0] * step * i
        frontBlocks[i-1] = snake.x[0] + direction[0] * step * i
        frontBlocks[i+2] = snake.y[0] + direction[1] * step * i
        rightBlocks[i-1] = snake.x[0] - direction[1] * step * i
        rightBlocks[i+2] = snake.y[0] + direction[0] * step * i

    for i in range(1, int(len(leftFrontBlocks) / 2) + 1):
        leftBackBlocks[i-1] = snake.x[0] + ((-1) * direction[0] + direction[1]) * step * i
        leftBackBlocks[i+2] = snake.y[0] + ((-1) * direction[0] - direction[1]) * step * i
        leftFrontBlocks[i-1] = snake.x[0] + (direction[0] + direction[1]) * step * i
        leftFrontBlocks[i+2] = snake.y[0] + ((-1) * direction[0] + direction[1]) * step * i
        rightFrontBlocks[i-1] = snake.x[0] + (direction[0] - direction[1]) * step * i
        rightFrontBlocks[i+2] = snake.y[0] + (direction[0] + direction[1]) * step * i
        rightBackBlocks[i-1] = snake.x[0] + ((-1) * direction[0] - direction[1]) * step * i
        rightBackBlocks[i+2] = snake.y[0] + (direction[0] - direction[1]) * step * i
    
    blockedResult = [0,0,0] #index 0 for left, 1 for front, 2 for right 
    blockedDirResult = [0,0,0,0,0,0,0] #left0, front1, right2, leftBack3, leftFront4, rightFront5, rightBack6

    # Kollision mit Wand checken, erst für nicht-diagonale Richtungen
    for i in range(0,wall.length):
        if game.isCollision(leftBlocks[0], leftBlocks[3], wall.x[i], wall.y[i], step-1):
            # Wenn direkter Block besetzt, sind alle Strahlen in dieser Richtung besetzt
            blockedResult[0] = 1
            blockedDirResult[0] = 1
            blockedDirResult[3] = 1
            blockedDirResult[4] = 1
        elif game.isCollision(leftBlocks[1], leftBlocks[4], wall.x[i], wall.y[i], step-1) or \
            game.isCollision(leftBlocks[2], leftBlocks[5], wall.x[i], wall.y[i], step-1):
            # Wenn direkter Block nicht besetzt, aber zweiter Block, sind auch alle Strahlen in dieser Richtung besetzt
            blockedDirResult[0] = 1
            blockedDirResult[3] = 1
            blockedDirResult[4] = 1
        if game.isCollision(frontBlocks[0], frontBlocks[3], wall.x[i], wall.y[i], step-1):
            blockedResult[1] = 1
            blockedDirResult[1] = 1
            blockedDirResult[4] = 1
            blockedDirResult[5] = 1
        elif game.isCollision(frontBlocks[1], frontBlocks[4], wall.x[i], wall.y[i], step-1) or\
            game.isCollision(frontBlocks[2], frontBlocks[5], wall.x[i], wall.y[i], step-1):
            blockedDirResult[1] = 1
            blockedDirResult[4] = 1
            blockedDirResult[5] = 1
        if game.isCollision(rightBlocks[0], rightBlocks[3], wall.x[i], wall.y[i], step-1):
            blockedResult[2] = 1
            blockedDirResult[2] = 1
            blockedDirResult[5] = 1
            blockedDirResult[6] = 1
        elif game.isCollision(rightBlocks[1], rightBlocks[4], wall.x[i], wall.y[i], step-1) or\
            game.isCollision(rightBlocks[2], rightBlocks[5], wall.x[i], wall.y[i], step-1):
            blockedDirResult[2] = 1
            blockedDirResult[5] = 1
            blockedDirResult[6] = 1  
        #Die Diagonalen nach hinten müssen separat gecheckt werden:
        if blockedDirResult[3] == 0:
            if (game.isCollision(leftBackBlocks[0], leftBackBlocks[3], wall.x[i], wall.y[i], step-1)) or \
                (game.isCollision(leftBackBlocks[1], leftBackBlocks[4], wall.x[i], wall.y[i], step-1)) or \
                    game.isCollision(leftBackBlocks[2], leftBackBlocks[5], wall.x[i], wall.y[i], step-1):
                blockedDirResult[3] = 1
        if blockedDirResult[6] == 0:
            if (game.isCollision(rightBackBlocks[0], rightBackBlocks[3], wall.x[i], wall.y[i], step-1)) or \
                (game.isCollision(rightBackBlocks[1], rightBackBlocks[4], wall.x[i], wall.y[i], step-1)) or \
                    game.isCollision(rightBackBlocks[2], rightBackBlocks[5], wall.x[i], wall.y[i], step-1):
                blockedDirResult[6] = 1

    # Jetzt das Ganze für Kollision mit Schlange, hier muss jeder Block einzeln gecheckt werden
    for i in range(1,snake.length):
        #Erst für die direkten nicht-diagonalen Blocks:
        if game.isCollision(leftBlocks[0], leftBlocks[3], snake.x[i], snake.y[i], step-1):
                blockedResult[0] = 1
        if game.isCollision(frontBlocks[0], frontBlocks[3], snake.x[i], snake.y[i], step-1):
                blockedResult[1] = 1
        if game.isCollision(rightBlocks[0], rightBlocks[3], snake.x[i], snake.y[i], step-1):
                blockedResult[2] = 1
        #Jetzt für die indirekten, nicht-diagonalen:
        if game.isCollision(leftBlocks[1], leftBlocks[4], snake.x[i], snake.y[i], step-1) or\
            game.isCollision(leftBlocks[2], leftBlocks[5], snake.x[i], snake.y[i], step-1):
                blockedDirResult[0] = 1
        if game.isCollision(frontBlocks[1], frontBlocks[4], snake.x[i], snake.y[i], step-1) or\
            game.isCollision(frontBlocks[2], frontBlocks[5], snake.x[i], snake.y[i], step-1):
                blockedDirResult[1] = 1
        if game.isCollision(rightBlocks[1], rightBlocks[4], snake.x[i], snake.y[i], step-1) or\
            game.isCollision(rightBlocks[2], rightBlocks[5], snake.x[i], snake.y[i], step-1):
                blockedDirResult[2] = 1
    
    #Jetzt für die diagonalen:
    k = 0
    while (blockedDirResult[3] == 0 and k < 3):
        for i in range(1,snake.length):
            if game.isCollision(leftBackBlocks[k], leftBackBlocks[k+3], snake.x[i], snake.y[i], step-1):
                blockedDirResult[3] = 1
                break
        k = k + 1
    k = 0
    while (blockedDirResult[4] == 0 and k < 3):
        for i in range(1,snake.length):
            if game.isCollision(leftFrontBlocks[k], leftFrontBlocks[k+3], snake.x[i], snake.y[i], step-1):
                blockedDirResult[4] = 1
                break
        k = k + 1    
    k = 0
    while (blockedDirResult[5] == 0 and k < 3):
        for i in range(1,snake.length):
            if game.isCollision(rightFrontBlocks[k], rightFrontBlocks[k+3], snake.x[i], snake.y[i], step-1):
                blockedDirResult[5] = 1
                break
        k = k + 1
    k = 0
    while (blockedDirResult[6] == 0 and k < 3):
        for i in range(1,snake.length):
            if game.isCollision(rightBackBlocks[k], rightBackBlocks[k+3], snake.x[i], snake.y[i], step-1):
                blockedDirResult[6] = 1
                break
        k = k + 1
    # Gesamt-Result ist eine Liste mit erst den direkten und dann den Strahlen
    result = blockedResult + blockedDirResult    
    return result
           
def angle_with_apple(snakedir, appledir):
    angle = math.atan2(appledir[1] * snakedir[0] - appledir[0] * snakedir[1], appledir[1] * snakedir[1] + appledir[0] * snakedir[0])/ math.pi
    angle = round(angle * 4.0) / 4.0
    #print(angle)
    return angle 












