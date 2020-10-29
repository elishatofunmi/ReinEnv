import numpy as np
from PlayersProperties import *


class network:

    def __init__(self):
        self.playersList = [
            # players A1 - A10
            'playerAKeeper',
            'playerA1',
            'playerA2',
            'playerA3',
            'playerA4',
            'playerA5',
            'playerA6',
            'playerA7',
            'playerA8',
            'playerA9',
            'playerA10',
            # players B1 - B10
            'playerBKeeper',
            'playerB1',
            'playerB2',
            'playerB3',
            'playerB4',
            'playerB5',
            'playerB6',
            'playerB7',
            'playerB8',
            'playerB9',
            'playerB10',
        ]
        return

    def sortdata(self, dictData):
        vals = list(dictData.values())
        keys = list(dictData.keys())
        vals.sort()
        sortedKeys = []
        for i in vals:
            for j in keys:
                if dictData[j] == i:
                    sortedKeys.append(j)

        return sortedKeys

    def LikePairsNearestNeighbor(self, playername, sourcePlayerCoordinate, SourcedictDataX, SourcedicDataY,
                                 milestone='short', conditionedValue=30):
        """
        dictDataX contains players of source team their respective coordinates, excluding the source player.

        dictDataY contains players of all opposing team and their respective coordinates.

        LikePairsNearestNeighbor basically wants to determine who in my team should I pass to based on the following.
        1. Long pass - long
        2. short pass - short
        3. across - across
        4. decide - decide (means, decide between across, long and short)
        5. self - self (means, hold the ball)

        conditionedValue: The value that determines the minimum distance you have to be from the opponent before you can receive the ball.

        """
        status = True
        # status is for the program to keep finding feasible team player that can hold the ball to the post.
        while status:
            playersDistanceEstimate = {}
            players = SourcedictDataX.keys()

            # compute the distance between the source players and his fellow team members
            for playee in players:
                # calculate distance
                xvalue = SourcedictDataX[playee][0] - sourcePlayerCoordinate[0]
                yvalue = SourcedictDataX[playee][1] - sourcePlayerCoordinate[1]
                xdiff = np.abs(xvalue)
                ydiff = np.abs(yvalue)
                distance = np.sqrt(pow(xdiff, 2) + pow(ydiff, 2))
                if xvalue > 0 and yvalue > 0:
                    status = True  # this is to estimate if the player is ahead or behind
                    playersDistanceEstimate[playee] = (distance, status)
                else:
                    status = False
                    playersDistanceEstimate[playee] = (distance, status)

            # let's decide players who can receive long pass, short pass or across.
            # divide into 3 categories based on the highest distance
            maxValue = max([playersDistanceEstimate[i]
                            for i in range(len(list(playersDistanceEstimate.values())))])
            GaugeA = int(maxValue/3)
            GaugeB = GaugeA * 2
            across, longpass, shortpass = {}, {}, {}
            for i, (j, k) in zip(playersDistanceEstimate.keys(), list(playersDistanceEstimate.values())):
                """
                # deciding players that can receive long pass.
                same condition for short pass

                # deciding players that can receive short pass.
                They have to be players very close to the source player
                source players based on nearest distance

                # deciding players that can receive across.
                They have to be farthest players, and must be in front of source player - random selection

                """
                if j <= GaugeA:
                    shortpass[i] = j
                elif j > GaugeA and j <= GaugeB:
                    longpass[i] = j
                else:
                    if k == True:  # player is ahead
                        across[i] = j
                    else:
                        # player is behind, don't append the player to the list of valid players to receive the ball.
                        pass

            # deciding players that can receive long pass
            sortedshort, sortedLong, sortedacross = [], [], []

            sortedLong = self.sortdata(longpass)

            # deciding players that can receive short pass
            """
            1. They have to be players very close to the source player
            source players based on nearest distance - random selection
            """

            sortedshort = self.sortdata(shortpass)

            # deciding players that can receive across
            """
            1. They have to be players not too far, not to close
            source players based on nearest distance - random selection
            """

            sortedacross = self.sortdata(across)

            targetplayer = ''

            if milestone == 'decide':
                # decide if long pass, short pass or across based on opposing obstacles

                # if no obstacle
                decision = np.random.choice(['long', 'short', 'across'])

                # else decide choice if there are obstacles

            else:
                decision = milestone
                if decision == 'across':
                    if sortedacross[-1] == '':
                        if sortedLong[-1] == '':
                            if sortedshort[-1] == '':
                                # hold the ball and move to a new position away from the enemy
                                targetplayer = 'self'
                            else:
                                # randomly select players in the category of short
                                targetplayer = np.random.choice(sortedshort)
                        else:
                            # randomly select players in the category of long
                            targetplayer = np.random.choice(sortedLong)
                    else:
                        # randomly select players in the category of across
                        targetplayer = np.random.choice(sortedacross)

                elif decision == 'long':
                    if sortedLong == '':
                        if sortedshort[-1] == '':
                            targetplayer = 'self'
                        else:
                            # randomly select players in the category of short
                            targetplayer = np.random.choice(sortedshort)
                    else:
                        # randomly select players in the category of long
                        targetplayer = np.random.choice(sortedLong)

                else:
                    if sortedshort[-1] == '':
                        targetplayer = 'self'
                    else:
                        # randomly select players in the category of short
                        targetplayer = np.random.choice(sortedshort)

            # determine if the receiving player is free within a space of 30 to hold the ball.
            # note that the enemy if within the space of 3, will automatically receive the ball.

            if targetplayer != 'self':
                playersB = SourcedicDataY.keys()

                # compute the distance between the target player and the opposing teams around.
                distanceD = {}
                selectedPlayerCoordinate = SourcedictDataX[targetplayer]
                for playee in playersB:
                    # calculate distance
                    xvalue = SourcedicDataY[playee][0] - \
                        selectedPlayerCoordinate[0]
                    yvalue = SourcedicDataY[playee][1] - \
                        selectedPlayerCoordinate[1]
                    xdiff = np.abs(xvalue)
                    ydiff = np.abs(yvalue)
                    distance = np.sqrt(pow(xdiff, 2) + pow(ydiff, 2))
                    distanceD[playee] = distance

                sortKeysB = self.sortdata(distanceD)
                if SourcedicDataY[sortKeysB[0]] > conditionedValue:
                    status = False
                    break
                else:
                    status = True
                    SourcedictDataX.pop(targetplayer)
                    # Delete selected target player from list to prevent getting selected the second time.
            else:
                targetplayer = 'self'
                status = False
                break

        return targetplayer

    def updateposition(self, playername, sourcePlayerCoordinate, SourcedictDataX, SourcedicDataY,
                       milestone='short', conditionedValue=30):
        """
        proposes a new team player to pass the ball too within the same team.
        This decides if ball should remain with self or can be passed to another player of the same team, either by
        long pass, short pass, across or randomly decide (long, short or across)
        """
        nextplayer = self.LikePairsNearestNeighbor(
            playername, sourcePlayerCoordinate, SourcedictDataX, SourcedicDataY,
            milestone='short', conditionedValue=30)

        # determine a new coordinate away from the enemey
        # draw close to your team member.
        playersDistanceEstimate = {}
        players = SourcedictDataX.keys()

        # compute the distance between the source players and his fellow team members
        for playee in players:
            # calculate distance
            xvalue = SourcedictDataX[playee][0] - sourcePlayerCoordinate[0]
            yvalue = SourcedictDataX[playee][1] - sourcePlayerCoordinate[1]
            xdiff = np.abs(xvalue)
            ydiff = np.abs(yvalue)
            distance = np.sqrt(pow(xdiff, 2) + pow(ydiff, 2))
            playersDistanceEstimate[playee] = distance

        sortmembers = self.sortdata(playersDistanceEstimate)
        # closest team member is
        nextcoordinates = SourcedictDataX[sortmembers[0]]
        nextLocation = self.linearRegression(
            sourcePlayerCoordinate[0], sourcePlayerCoordinate[1], nextcoordinates[0], nextcoordinates[1])

        # setting a new coordinate for the ball
        bal = ball()
        bal.positionx = nextLocation[0]
        bal.positiony = nextLocation[1]

        if nextplayer == 'self':
            # set a new position for the just decided target player
            self.setplayersLocation(
                defaultPlayer=playername, coordinate=nextLocation)
        else:
            # pass the ball from the source player to the destination player
            self.setplayersLocation(
                defaultPlayer=nextplayer, coordinate=nextLocation)
        return

    def linearRegression(self, x1, y1, x2, y2, NumberOfMoves=3):
        xmove, ymove = (0, 0)
        m = (y2 - y1) / (x2 - x1)
        c = y2 - (m * x2)

        xmove = x1 + NumberOfMoves
        ymove = (m * xmove) + c
        return xmove, ymove

    def setplayersLocation(self, defaultPlayer='ball', coordinate=(350, 600)):
        if defaultPlayer == 'PlayerA1':
            A1 = playerA1()
            A1.positionx = coordinate[0]
            A1. positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA2':
            A2 = playerA2()
            A2.positionx = coordinate[0]
            A2.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA3':
            A3 = playerA3()
            A3.positionx = coordinate[0]
            A3.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA4':
            A4 = playerA4()
            A4.positionx = coordinate[0]
            A4.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA5':
            A5 = playerA5()
            A5.positionx = coordinate[0]
            A5.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA6':
            A6 = playerA6()
            A6.positionx = coordinate[0]
            A6.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA7':
            A7 = playerA7()
            A7.positionx = coordinate[0]
            A7.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA8':
            A8 = playerA8()
            A8.positionx = coordinate[0]
            A8.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA9':
            A9 = playerA9()
            A9.positionx = coordinate[0]
            A9.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerA10':
            A10 = playerA10()
            A10.positionx = coordinate[0]
            A10.positiony = coordinate[1]
        elif defaultPlayer == 'playerAKeeper':
            keeperA = playerAKeeper()
            keeperA.positionx = coordinate[0]
            keeperA.positiony = coordinate[1]

        # begin for B
        elif defaultPlayer == 'PlayerB1':
            B1 = playerB1()
            B1.positionx = coordinate[0]
            B1. positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB2':
            B2 = playerB2()
            B2.positionx = coordinate[0]
            B2.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB3':
            B3 = playerB3()
            B3.positionx = coordinate[0]
            B3.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB4':
            B4 = playerB4()
            B4.positionx = coordinate[0]
            B4.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB5':
            B5 = playerA5()
            B5.positionx = coordinate[0]
            B5.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB6':
            B6 = playerB6()
            B6.positionx = coordinate[0]
            B6.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB7':
            B7 = playerB7()
            B7.positionx = coordinate[0]
            B7.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB8':
            B8 = playerB8()
            B8.positionx = coordinate[0]
            B8.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB9':
            B9 = playerB9()
            B9.positionx = coordinate[0]
            B9.positiony = coordinate[1]
        elif defaultPlayer == 'PlayerB10':
            B10 = playerB10()
            B10.positionx = coordinate[0]
            B10.positiony = coordinate[1]
        else:
            keeperB = playerBKeeper()
            keeperB.positionx = coordinate[0]
            keeperB.positiony = coordinate[1]

        return
