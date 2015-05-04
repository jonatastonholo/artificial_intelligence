#implementedSearches.py
############################################################################################
# Student: Jonatas Ribeiro Tonholo ** Implementations based on the 2th edition of          #
# Class: Artificial Inteligence    ** Stuart Russell and Peter Norvig's book:              #
# Course: Computer Engineering     ** Artificial Intelligence - A Modern Approach,         #
# University: CEFET-MG/Brazil      ** chapters 3 and 4.                                    #
############################################################################################
############################################################################################
# Warning: Do not copy this project, only inspire on it for the good of your own learning. #
############################################################################################
#-------------- TESTES INICIAIS --------------

class TiposBusca:
    TESTE1 = 'Profundidade'
    TESTE2 = 'Teste'

from game import Directions
s = Directions.SOUTH
w = Directions.WEST
n = Directions.NORTH
e = Directions.EAST
st = Directions.STOP

def busca_teste(tipoBusca):
    if tipoBusca == TiposBusca.TESTE1:
        return [s,n,s,n,s,n,s,st]
    elif tipoBusca == TiposBusca.TESTE2:
        return [s,s,w,s,w,w,s,w,w,st]
#---------------------------------------------



#------------------------ THE CLASS NODE -------------------------------------------------------
''' pg 72
datatype node
    components: STATE, PARENT-NODE, OPERATOR, DEPTH, PATH-COST
    
    - the state in the state space to which the node corresponds;
    - the node in the search tree that generated this node (this is called the parent node);
    - the operator that was applied to generate the node;
    - the number of nodes on the path from the root to this node (the depth of the node);
    - the path cost of the path from the initial state to the node.
    
'''
class Node:
#    def __init__(self, state, parent_node, operator, depth, cost):
    def __init__(self, state, parent_node, cost, heuristic = 0):
        self.state = state
        self.parent_node = parent_node
        #self.operator = operator
        #self.depth = depth
        self.heuristic = heuristic
        self.cost = cost
    
    def getState(self):
        return self.state[-1] #Last index of

    ''' pg 72
    The EXPAND function is responsible for calculating each of the components of the
    nodes it generates.
    '''
    def EXPAND(self,problem):
        successors = problem.getSuccessors(self.getState())
        result = []
        for successor in successors:
            if successor[0] not in self.state: #If the successor isn't himself
                result += [Node(
                                list(self.state) + [successor[0]], 
                                list(self.parent_node) + [successor[1]],
                                self.cost + successor[2] + self.heuristic,
                                )
                           ]
        return result
    
    
#-------------NON HEURISTIC SEARCHES PROBLEMS --------------------------------------------------

class DataStructureType:
    STACK = 'Stack'
    QUEUE = 'Queue'
    PRIORITY_QUEUE = 'PriorityQueue'
    PRIORITY_QUEUE_WITH_FUNCTION = 'PriorityQueueWithFunction'
    


def getNodes(dsType, problem):
        if dsType == DataStructureType.STACK:
            from util import Stack
            nodes = Stack()
            nodes.push(Node([problem.getStartState()], [], 0, 0))
            return nodes
        elif dsType == DataStructureType.QUEUE:
            from util import Queue
            nodes = Queue()
            nodes.push(Node([problem.getStartState()], [], 0, 0))
            return nodes
        elif dsType == DataStructureType.PRIORITY_QUEUE:
            from util import PriorityQueue
            nodes =  PriorityQueue()
            nodes.push(Node([problem.getStartState()], [], 0,0),0)
            return nodes

''' pg 73
    function GENERAL-SEARCH(problem, QUEUING-FN) returns a solution, or failure
        nodes <- MAKE-QUEUE(MAKE-NODE(INITIAL-STATE[probLem]))
        loop do
            if nodes is empty then return failure
            node <- REMOVE-FRONT(nodes)
            if GOAL-TEST[problem] applied to STATE(node) succeeds then return node
            nodes <- QUEUING-FN(nodes, EXPAND(node, OPERATORS[problem]))
        end
'''
def GENERAL_SEARCH(problem, queuingFn, dsType):
    nodes = getNodes(dsType,problem)
    
    while nodes:
        node = nodes.pop()
        if problem.isGoalState(node.getState()):
            return node.parent_node
        nodes = queuingFn(nodes, node.EXPAND(problem))
    return None


''' DEPTH-FlRST-SEARCH - pg 78 
    function DEPTH-FlRST-SEARCH(problem) returns a solution, or failure
        GENERAL-SEARCH(problem,ENQUEUE-AT-FRONT)
'''
def DEPTH_FlRST_SEARCH(problem):
    return GENERAL_SEARCH(problem,ENQUEUE_AT_FRONT,DataStructureType.STACK)
    #return GENERAL_SEARCH(problem,ENQUEUE_AT_FRONT,DataStructureType.QUEUE)

''' BREADTH-FlRST-SEARCH - pg 74
    function BREADTH-FlRST-SEARCH(problem) returns a solution or failure
        return GENERAL-SEARCH( problem,ENQUEUE- AT-END)
'''
def BREADTH_FlRST_SEARCH(problem):
    return GENERAL_SEARCH(problem,ENQUEUE_AT_END,DataStructureType.QUEUE)

''' UNIFORM_COST_SEARCH- pg 75-76
    function BREADTH-FlRST-SEARCH(problem) returns a solution or failure
        return GENERAL-SEARCH( problem,ENQUEUE- AT-END)
'''
def UNIFORM_COST_SEARCH(problem):
    return GENERAL_SEARCH(problem,ENQUEUE_WITH_PRIORITY,DataStructureType.PRIORITY_QUEUE)


#----------------- HEURISTIC SEARCHES PROBLEMS -------------------------------------------------

class ProblemType:
    A_STAR = 'aStar'

''' A GENERAL_FUNCTION for Heuristics problems - pg 93
    function BEST-FiRST-SEARCH(problem, EVAL-FN) returns a solution sequence
        inputs: problem, a problem
            Eval-Fn, an evaluation function
        Queueing-Fn <- a function that orders nodes by EVAL-FN
        return GENERAL-SEARCH(problem, Queueing-Fn)
'''
def BEST_FIRST_SEARCH(problem, EvalFn, heuristic):
    queuingFn = getQueuingFnHeuristicMode(EvalFn)
    n = Node([problem.getStartState()], [], 0, heuristic(problem.getStartState(), problem))
    from util import PriorityQueueWithFunction
    nodes =  PriorityQueueWithFunction(heuristicAStarQueuingFn)
    nodes.push(n)
    
    while nodes:
        node = nodes.pop()
        if problem.isGoalState(node.getState()):
            return node.parent_node
        nodes = queuingFn(nodes, node.EXPAND(problem))
    
    return None
    
'''
    Defines f(n) = g(n) + h(n)
'''
def heuristicAStarQueuingFn(node):
    Gn = node.cost
    Hn = node.heuristic
    return Gn + Hn
     
def getQueuingFnHeuristicMode(EvalFn):
    if EvalFn == ProblemType.A_STAR:
        return ENQUEUE_WITH_PRIORITY_AND_FN
    else:
        return None


''' A_STAR_SEARCH - Pg 97
    function A_STAR_SEARCH(problem) returns a solution or failure
        return BEST-FlRST-SEARCH(problem,g + h)
'''
def A_STAR_SEARCH(problem, heuristic):
    return BEST_FIRST_SEARCH(problem, ProblemType.A_STAR, heuristic)
#----------------QUEUE FUNCTIONS --------------------------------------
def ENQUEUE_AT_END(ds, elements):
    from util import Queue
    if isinstance(ds,Queue): #Force use stack FIFO Queue
        queue = ds
        for element in elements:
            queue.push(element)
    else:
        print 'ERROR: use util.Queue()'
    return queue
    

def ENQUEUE_AT_FRONT(ds, elements):
    from util import Stack
    if isinstance(ds,Stack): #Force use stack LIFO Stack
        stack = ds 
        for element in elements:
            stack.push(element)
    else:
        print 'ERROR: use util.Stack()'
    return stack

def ENQUEUE_WITH_PRIORITY(ds, elements):
    from util import PriorityQueue
    if isinstance(ds,PriorityQueue): #Force use Priority Queue
        pqueue = ds 
        for element in elements:
            pqueue.push(element,element.cost)
    else:
        print 'ERROR: use util.PriorityQueue()'
    return pqueue

def ENQUEUE_WITH_PRIORITY_AND_FN(ds, elements):
    from util import PriorityQueueWithFunction
    if isinstance(ds,PriorityQueueWithFunction): #Force use Priority Queue With Function
        pqueue = ds 
        for element in elements:
            pqueue.push(element)
    else:
        print 'ERROR: use util.PriorityQueueWithFunction()'
    return pqueue

#-------------------------------------------------------------------------
