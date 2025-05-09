#EMERY: linear scalarization multi objective RL agents


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):

    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.QValues = util.Counter()
        self.legalActions = []

    def getQValue(self, state, action):
        return self.QValues[(state, action)]

    def computeValueFromQValues(self, state):
        qvals = [self.getQValue(state, action) for action in self.legalActions]
        if not qvals:
            return 0.0
        return max(qvals)

    def getAction(self, state, train=False):
        self.legalActions = self.getLegalActions(state)
        action = None
        if not self.legalActions:
          return action
        if train:
            randomize = util.flipCoin(self.epsilon)
            if randomize:
                action = random.choice(self.legalActions)
            else:
                action = self.getPolicy(state)
        else:
          action = self.getPolicy(state)
        return action

    def update(self, state, action, nextState, reward):
        curQ = self.QValues[(state, action)]
        self.QValues[(state, action)] = (1 - self.alpha) * curQ + self.alpha * (
                    reward + self.discount * self.getValue(nextState))

    def getPolicy(self, state):
        actions = []
        self.legalActions = self.getLegalActions(state)
        if not self.legalActions:
            return None
        val = self.computeValueFromQValues(state)
        for action in self.legalActions:
            if val == self.getQValue(state, action):
                actions.append(action)
        return random.choice(actions)

    def getValue(self, state):
        qvals = [self.getQValue(state, action) for action in self.legalActions]
        if not qvals:
            return 0.0
        return max(qvals)


class PacmanAgent(QLearningAgent):

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state, train=False):
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action



class ApproximateAgent(PacmanAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        qval = 0.0
        features = self.featExtractor.getFeatures(state, action)
        for feature in features:
          qval += features[feature] * self.weights[feature]
        return qval


    def update(self, state, action, nextState, reward):
        features = self.featExtractor.getFeatures(state, action)
        difference = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
        for feature in features:
          self.weights[feature] += self.alpha * difference * features[feature]
        #print(self.weights)