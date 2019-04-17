import sys
import json
import time
import random


grid = []
isMyMove = False



def makeMove():
    min = 0
    max = len(grid)

    isMoveAvailable = False
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                isMoveAvailable = True

    if isMoveAvailable == False :
        return -1

    isValid = False

    while(isValid == False):
        try:
            move = random.randint(1, len(grid[0]))
            for i in range(len(grid[0])):
                if grid[i][move] == 0:
                    isValid = True
                    return move
        except:
            sys.stderr.write("Finding new index")




# print("Something to print")
while True:

    try:
        for line in sys.stdin:
            # sys.stderr.write(line)
            str_input = json.loads(line)
            grid = str_input["grid"]
            move = makeMove()
            move1 = {}
            move1["move"] = move
            someStr = json.dumps(move1) + "\n"
            print(someStr)
            sys.stdout.flush()
            break;
    except Exception as e:
        sys.stderr.write(b"Error")
    # if r == 'b\n':
    #     i=0
    #     # print("exiting")
    #     # break
    # else:
    #     try:
    #         str_input = json.loads(r)
    #         grid = str_input["grid"]
    #         move = makeMove()
    #         move1 = {}
    #         move1["move"] = move
    #         someStr = json.dumps(move1) + "\n"
    #         print(someStr.encode())
    #         # sys.stdout.write
    #         sys.stdout.flush()
    #     except:
    #         # print(r)
    #         i = 0



