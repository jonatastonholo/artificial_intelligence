# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    
    

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
#     
#     print("successorGameState = ");
#     print(successorGameState);
#     print("***\n");
#     print("newPos = ");
#     print(newPos);
#     print("***\n");
#     print("oldFood = ");
#     print(oldFood);
#     print("***\n");
#     print("newGhostStates = ");
#     print(newGhostStates);
#     print("***\n");
#     print("newScaredTimes = ");
#     print(newScaredTimes);
#     print("\n---------------------");

    oldFoodList=oldFood.asList()
   
    oldFoodList.sort(lambda x,y: util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))
    foodScore=util.manhattanDistance(newPos, oldFoodList[0])
    
    GhostPositions=[Ghost.getPosition() for Ghost in newGhostStates]
    if len(GhostPositions) == 0 : GhostScore = 0
    else: 
        GhostPositions.sort(lambda x,y: compare(x,y,newPos))
        if util.manhattanDistance(newPos, GhostPositions[0])==0: return -99 
        else:
            GhostScore=2*(-1.0)/util.manhattanDistance(newPos, GhostPositions[0])
    if foodScore==0: score=2.0+GhostScore
    else: score=GhostScore+1.0/float(foodScore)
    
    return score
        
def compare(x,y,newPos):
    if (util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))<0: return -1
    else: 
        if (util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))>0: return 1
        else:
            return 0



def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

## Artificial Intelligence: A Modern Approach 2nd Ed. pg126
##
## function MINIMAX-DECISION (state) returns an action
##    return arg max a E ACTIONS (s) MIN-VALUE (RESULT (state, a))

##    for each op in OPERATORSfgame] do
##        VALUE[op] - MINIMAX-VALUE(APPLY(op, game), game)
##    end
##    return the op with the highest VALUE[op]


  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    numOfAgent=gameState.getNumAgents();
    depth=numOfAgent*self.depth
    LegalActions=gameState.getLegalActions(0)
    
    # FOR DEPTH>4 IS BETTER
    if Directions.STOP in LegalActions: 
        LegalActions.remove(Directions.STOP)
        
        
    listNextStates=[gameState.generateSuccessor(0,action) for action in LegalActions ]
    
    VALUE=[self.MINlMAX_VALUE(numOfAgent,1,nextGameState,depth-1) for nextGameState in listNextStates] 
    
    Max=max(VALUE)
    listMax=[]
    for i in range(0,len(VALUE)):
        if VALUE[i]==Max:
            listMax.append(i)
    i = random.randint(0,len(listMax)-1)
        
    action=LegalActions[listMax[i]]
    return action #return the op with the highest VALUE[op]


# function MINlMAX_VALUE(state, game) returns a utility value
#     if TERMINAL-TEST[game](state) then
#         return UTILITY[game](state)
#     else if MAX is to move in state then
#         return the highest MINIMAX-VALUE of SUCCESSORS(state)
#     else
#         return the lowest MINIMAX-VALUE of SUCCESSORS(state)
  def MINlMAX_VALUE(self,numOfAgent,agentIndex, gameState, depth):
    
    if (gameState.isLose() or gameState.isWin() or depth==0): #TERMINAL-TEST
        return self.evaluationFunction(gameState) #UTILITY
    else:
        listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex) ]
        
        if (agentIndex==0): # PACMAN IS INDEX 0 (MAX)
            return max([self.MINlMAX_VALUE(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates] )
        else :
            return min([self.MINlMAX_VALUE(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates])


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  INF = 999999;
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    
    numOfAgent=gameState.getNumAgents();
    depth=numOfAgent*self.depth
    LegalActions=gameState.getLegalActions(0)
    
    # FOR DEPTH>4 IS BETTER
    if Directions.STOP in LegalActions: 
        LegalActions.remove(Directions.STOP)
        
        
    listNextStates=[gameState.generateSuccessor(0,action) for action in LegalActions ]
    
    VALUE=[self.MINlMAX_VALUE(numOfAgent,1,nextGameState,depth-1, -self.INF, self.INF) for nextGameState in listNextStates] 
    
    Max=max(VALUE)
    listMax=[]
    for i in range(0,len(VALUE)):
        if VALUE[i]==Max:
            listMax.append(i)
    i = random.randint(0,len(listMax)-1)
        
    action=LegalActions[listMax[i]]
    return action #return the op with the highest VALUE[op]
    
    
    
    util.raiseNotDefined()
    
  def MINlMAX_VALUE(self,numOfAgent,agentIndex, gameState, depth, alfa=(-INF,), beta=(INF,)):
    
    if (gameState.isLose() or gameState.isWin() or depth==0): #TERMINAL-TEST
        return self.evaluationFunction(gameState) #UTILITY
    else:            
        listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex) ]
            
        ## Artificial Intelligence, 3rd ed pg 170 Adaptation
        ##MAX_VALUE
        if (agentIndex==0): # PACMAN IS INDEX 0 (MAX)
            v = -self.INF;
            v =max([self.MINlMAX_VALUE(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1,alfa,beta) for nextState in listNextStates] );
            
            if (v >= beta):
                return v;
            else:
                alfa = max(alfa,v);
                return v;
        ## Artificial Intelligence, 3rd ed pg 170 Adaptation
        ##MIN_VALUE
        else :
            v = self.INF;
            v =min([self.MINlMAX_VALUE(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1, alfa, beta) for nextState in listNextStates])
            
            if (v <= alfa):
                return v;
            else:
                beta = max(beta,v);
                return v;


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    
    numOfAgent=gameState.getNumAgents();
    depth=numOfAgent*self.depth
    LegalActions=gameState.getLegalActions(0)
    
    # FOR DEPTH>4 IS BETTER
    if Directions.STOP in LegalActions: 
        LegalActions.remove(Directions.STOP)
        
        
    listNextStates=[gameState.generateSuccessor(0,action) for action in LegalActions ]
    
    VALUE=[self.EXPECTIMAX_VALUE(numOfAgent,1,nextGameState,depth-1) for nextGameState in listNextStates] 
    
    Max=max(VALUE)
    listMax=[]
    for i in range(0,len(VALUE)):
        if VALUE[i]==Max:
            listMax.append(i)
    i = random.randint(0,len(listMax)-1)
        
    action=LegalActions[listMax[i]]
    return action #return the op with the highest VALUE[op]
    
    util.raiseNotDefined()
    
## Adaptation from https://courses.cs.washington.edu/courses/cse473/11au/slides/cse473au11-adversarial-search.pdf (pg 30)
  def EXPECTIMAX_VALUE(self,numOfAgent,agentIndex, gameState, depth):
    
    if (gameState.isLose() or gameState.isWin() or depth==0): #TERMINAL-TEST
        return self.evaluationFunction(gameState) #UTILITY
    else:
        listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex) ]
        
        if (agentIndex==0): # PACMAN IS INDEX 0 (MAX)
            return max([self.EXPECTIMAX_VALUE(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates] )
        else :
            chanceList=[self.EXPECTIMAX_VALUE(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates]
            return sum(chanceList)/len(chanceList)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
  
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return - float("inf")
        
    score = scoreEvaluationFunction(currentGameState)
    newFood = currentGameState.getFood()
    foodPos = newFood.asList()
    closestfood = float("inf")
    for pos in foodPos:
        dist = util.manhattanDistance(pos, currentGameState.getPacmanPosition())
        if (dist < closestfood):
            closestfood = dist
    numghosts = currentGameState.getNumAgents() - 1
    i = 1
    disttoghost = float("inf")
    while i <= numghosts:
        nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
        disttoghost = min(disttoghost, nextdist)
        i += 1
    score += max(disttoghost, 4) * 2
    score -= closestfood * 1.5
    capsulelocations = currentGameState.getCapsules()
    score -= 4 * len(foodPos)
    score -= 3.5 * len(capsulelocations)
    return score

  
  
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

