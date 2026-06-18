from hitman.hitman import HC

WORLD = [
    [HC.EMPTY,   HC.WALL,    HC.EMPTY,   HC.SUIT,      HC.EMPTY,      HC.WALL,        HC.EMPTY],
    [HC.EMPTY,   HC.WALL,    HC.EMPTY,   HC.WALL,      HC.EMPTY,      HC.EMPTY,       HC.EMPTY],
    [HC.TARGET,  HC.EMPTY,   HC.EMPTY,   HC.EMPTY,     HC.CIVIL_N,    HC.WALL,        HC.EMPTY],
    [HC.WALL,    HC.EMPTY,   HC.WALL,    HC.GUARD_E,   HC.EMPTY,      HC.CIVIL_W,     HC.EMPTY],
    [HC.EMPTY,   HC.EMPTY,   HC.EMPTY,   HC.EMPTY,     HC.EMPTY,      HC.EMPTY,       HC.EMPTY],
    [HC.EMPTY,   HC.WALL,    HC.EMPTY,   HC.PIANO_WIRE,HC.EMPTY,      HC.EMPTY,       HC.EMPTY],
]