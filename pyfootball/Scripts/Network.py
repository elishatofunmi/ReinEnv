import numpy as np


class network:

    def __init__(self):
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

    def LikePairsNearestNeighbor(self, sourcePlayerCoordinate, SourcedictDataX, SourcedicDataY, milestone='short', conditionedValue = 30):
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
        #status is for the program to keep finding feasible team player that can hold the ball to the post.
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
            playersB = SourcedicDataY.keys()
            

            # compute the distance between the target player and the opposing teams around.
            distanceD = {}
            selectedPlayerCoordinate = SourcedictDataX[targetplayer]
            for playee in playersB:
                # calculate distance
                xvalue = SourcedicDataY[playee][0] - selectedPlayerCoordinate[0]
                yvalue = SourcedicDataY[playee][1] - selectedPlayerCoordinate[1]
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
                
                #Delete selected target player from list to prevent getting selected the second time.
                
        


        return targetplayer

    def updateposition(self, sourcePlayerCoordinate, SourcedictDataX, SourcedicDataY, milestone='short'):
        """
        proposes a new team player to pass the ball too within the same team.
        This decides if ball should remain with self or can be passed to another player of the same team, either by
        long pass, short pass, across or randomly decide (long, short or across)
        """
        nextplayer = self.LikePairsNearestNeighbor(
            sourcePlayerCoordinate, SourcedictDataX, SourcedicDataY, milestone='short')

        if nextplayer == 'self':
            # determine a new coordinate away from the enemey
            pass

        else:
            # pass the ball from the source player to the destination player
            pass
        return

    def linearRegression(self, x1, y1, x2, y2, NumberOfMoves=5):
        xmove, ymove = (0, 0)
        m = (y2 - y1) / (x2 - x1)
        c = y2 - (m * x2)

        xmove = x1 + NumberOfMoves
        ymove = (m * xmove) + c
        return xmove, ymove
