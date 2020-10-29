# General player properties
class defaultProperties:
    def __init__(self):
        self.positionx = 0
        self.positiony = 0
        return

    def setCoordinates(self, x, y):
        self.positionx = x
        self.positiony = y
        return

    def getCoordinates(self):
        return self.positionx, self.positiony


# defenders properties
class defenders(defaultProperties):
    def __init__(self):
        super().__init__(self)
        return

# mid-fielders properties


class midfielders(defaultProperties):
    def __init__(self):
        super().__init__(self)
        return


# Strikers properties
class stricker(defaultProperties):
    def __init__(self):
        super().__init__(self)
        return


# Class players A
class playerAKeeper(defaultProperties):
    def __init__(self):
        super().__init__(self)
        return


class playerA1(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA2(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA3(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA4(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA5(midfielders):
    """
    midfielders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA6(midfielders):
    """
    midfielders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA7(midfielders):
    """
    midfielders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA8(stricker):
    """
    stricker
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA9(stricker):
    """
    stricker
    """

    def __init__(self):
        super().__init__(self)
        return


class playerA10(stricker):
    """
    stricker
    """

    def __init__(self):
        super().__init__(self)
        return


# Class players B
class playerBKeeper(defaultProperties):
    def __init__(self):
        super().__init__(self)
        return


class playerB1(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB2(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB3(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB4(defenders):
    """
    defenders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB5(midfielders):
    """
    midfielders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB6(midfielders):
    """
    midfielders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB7(midfielders):
    """
    midfielders
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB8(stricker):
    """
    stricker
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB9(stricker):
    """
    stricker
    """

    def __init__(self):
        super().__init__(self)
        return


class playerB10(stricker):
    """
    stricker
    """

    def __init__(self):
        super().__init__(self)
        return
