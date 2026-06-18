from hitman.hitman import HC

WORLD = [
    [HC.EMPTY,   HC.WALL,    HC.WALL,    HC.SUIT,      HC.WALL,       HC.EMPTY,       HC.EMPTY],
    [HC.EMPTY,   HC.EMPTY,   HC.EMPTY,   HC.EMPTY,     HC.WALL,       HC.CIVIL_N,     HC.EMPTY],
    [HC.TARGET,  HC.WALL,    HC.EMPTY,   HC.EMPTY,     HC.EMPTY,      HC.WALL,        HC.EMPTY],
    [HC.WALL,    HC.WALL,    HC.EMPTY,   HC.GUARD_E,   HC.EMPTY,      HC.CIVIL_W,     HC.EMPTY],
    [HC.GUARD_W, HC.EMPTY,   HC.WALL,    HC.EMPTY,     HC.EMPTY,      HC.EMPTY,       HC.EMPTY],
    [HC.EMPTY,   HC.EMPTY,   HC.EMPTY,   HC.PIANO_WIRE,HC.WALL,       HC.EMPTY,       HC.EMPTY],
]