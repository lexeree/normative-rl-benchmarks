import game


def eatBlueGhost(state, action):
    return state.killedBlue

def eatOrangeGhost(state, action):
    return state.killedOrange

def eatPowerPellet(state, action):
    for pos in state.getCapsules():
        dx = pos[0] - game.Actions.getSuccessor(state.getPacmanPosition(), action)[0]
        dy = pos[1] - game.Actions.getSuccessor(state.getPacmanPosition(), action)[1]
        return dx < 1.0 and dx > -1.0 and dy < 1.0 and dy > -1.0

def lose(state, action):
    blue = False
    orange = False
    if not state.data.agentStates[1].isScared():
        dx = state.getGhostPosition(1)[0] - game.Actions.getSuccessor(state.getPacmanPosition(), action)[0]
        dy = state.getGhostPosition(1)[1] - game.Actions.getSuccessor(state.getPacmanPosition(), action)[1]
        blue = dx < 2.0 and dx > -2.0 and dy < 2.0 and dy > -2.0
    if not state.data.agentStates[2].isScared():
        dx = state.getGhostPosition(2)[0] - game.Actions.getSuccessor(state.getPacmanPosition(), action)[0]
        dy = state.getGhostPosition(2)[1] - game.Actions.getSuccessor(state.getPacmanPosition(), action)[1]
        orange = dx < 2.0 and dx > -2.0 and dy < 2.0 and dy > -2.0
    return blue or orange

def stayStill(state, action):
    return action == 'Stop'

def score0(state, action):
    return state.data.score == 0

def scoreGreater200(state, action):
    return state.data.score > 200

def scoreGreater500(state, action):
    return state.data.score > 500

def westSide(state, action):
    return state.data.layout.width/2 > state.getPacmanPosition()[0]