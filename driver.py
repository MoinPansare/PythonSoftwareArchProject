import subprocess
import time
from subprocess import PIPE, Popen
import json
import sys

class Driver:
    width = 7
    height = 7

    playerToStart = 1
    whoseTurn = 1
    gamesToPlay = 3

    grid = []

    p1 = None
    p2 = None

    justStarted = True

    gameResults = []

    def checkIfToRestart(self):
        if (self.gamesToPlay > 0):
            self.gamesToPlay -= 1
            if self.p1 != None:
                self.p1.terminate()
                self.p2.terminate()
                time.sleep(1.0)
            self.loadPlayers()
            self.initializeGame()
            self.playGame()
        else:
            print("We Are Done The Results are as follows")
            print(self.gameResults)
            sys.exit()


    def checkForWinner(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != 0:
                    currentValue = self.grid[i][j]

                    # check right 4 values Only if the current column is number of columns - 3
                    if (j < len(self.grid[i]) - 3):
                        if self.grid[i][j + 1] == currentValue and self.grid[i][j + 2] == currentValue and self.grid[i][
                            j + 3] == currentValue:
                            print("Winner")
                            print(i)
                            print(j)
                            print(self.grid[i][j])
                            return currentValue

                    # check bottom 4 values Only if current row is No. of rows -3
                    if (i < len(self.grid) - 3):
                        if self.grid[i + 1][j] == currentValue and self.grid[i + 2][j] == currentValue and self.grid[i + 3][
                            j] == currentValue:
                            print(i)
                            print(j)
                            print(self.grid[i][j])
                            print("Winner")
                            return currentValue

                    # Check Diagonal TopLeft to bottomRight only if No.of Rows and Col -3
                    if (i < len(self.grid) - 3 and j < len(self.grid[i]) - 3):
                        if self.grid[i + 1][j + 1] == self.grid[i + 2][j + 2] == self.grid[i + 3][j + 3] == currentValue:
                            print("Winner")
                            print(i)
                            print(j)
                            print(self.grid[i][j])
                            return currentValue

                    # Check Diagonal TopRight to bottomLeft only if No.of Rows and Col + 3
                    if i > 2 and j < len(self.grid[i]) - 3:
                        if self.grid[i - 1][j + 1] == self.grid[i - 2][j + 2] == self.grid[i - 3][j + 3] == currentValue:
                            print("Winner")
                            print(i)
                            print(j)
                            print(self.grid[i][j])
                            return currentValue

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    return 0

        return -1

    def initializeGame(self):
        justStarted = True
        self.grid = []
        for i in range(self.width):
            list = []
            for j in range(self.height):
                list.append(0)
            self.grid.append(list)
        return

    def loadPlayers(self):
        self.p1 = Popen(["python", "-u", "player.py"], stdin=PIPE, stdout=PIPE, bufsize=1)
        time.sleep(0.1)
        self.p2 = Popen(["python", "-u", "player.py"], stdin=PIPE, stdout=PIPE, bufsize=1)
        time.sleep(1.0)

        return

    def makeMove(self, index, playerID):
        tempIndex = self.height - 1
        while self.height >= 0:
            if self.grid[tempIndex][index] == 0:
                self.grid[tempIndex][index] = playerID
                break
            tempIndex -= 1
        return

    def stringifyGrid(self):
        toSend = {}
        toSend["grid"] = self.grid
        someString = json.dumps(toSend) + "\n"
        return someString.encode()

    def playGame(self):
        if self.justStarted == True:
            justStarted = False
            if self.playerToStart == 1:
                self.p1.stdin.write(self.stringifyGrid())
                self.p1.stdin.flush()
                time.sleep(0.5)
                # self.p1.stdin.close()
                whoseTurn = 1
            else:
                self.p2.stdin.write(self.stringifyGrid())
                self.p2.stdin.flush()
                time.sleep(0.5)
                # self.p2.stdin.close()
                whoseTurn = 2

        while (True):
            for row in self.grid:
                print(row)
            print("-----------------------------------------------")
            if self.whoseTurn == 1:
                try:
                    for line in self.p1.stdout:
                        myinput = json.loads(line)
                        myinput = myinput["move"]
                        self.makeMove(myinput, 1)
                        for row in self.grid:
                            print(row)
                        winnerResult = self.checkForWinner()
                        if winnerResult == 1:
                            self.gameResults.append(1)
                            self.checkIfToRestart()
                            break
                        else:
                            if winnerResult == -1:
                                self.gameResults.append(0)
                                self.checkIfToRestart()
                                break

                        self.p2.stdin.write(self.stringifyGrid())
                        self.p2.stdin.flush()
                        self.whoseTurn = 2
                        time.sleep(0.3)
                        break
                except Exception as e:
                    print("Error")
                    print(e)
            else:
                try:
                    for line in self.p2.stdout:
                        myinput = json.loads(line)
                        myinput = myinput["move"]
                        self.makeMove(myinput, 2)
                        for row in self.grid:
                            print(row)
                        winnerResult = self.checkForWinner()
                        if winnerResult == 2:
                            self.gameResults.append(2)
                            self.checkIfToRestart()
                            break
                        else:
                            if winnerResult == -1:
                                self.gameResults.append(0)
                                self.checkIfToRestart()
                                break
                        self.p1.stdin.write(self.stringifyGrid())
                        self.p1.stdin.flush()
                        self.whoseTurn = 1
                        time.sleep(0.3)
                        break
                except Exception as e:
                    print("Error")
                    print(e)


if __name__ == "__main__":
    myDriver = Driver()
    myDriver.loadPlayers()
    myDriver.checkIfToRestart()

