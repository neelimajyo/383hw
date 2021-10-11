import random
import math


BOT_NAME = "INSERT NAME FOR YOUR BOT HERE OR IT WILL THROW AN EXCEPTION" #+ 19 


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None
        # print("****************************\n")
        # print("INSIDE GET MOVE\n")
        # print("TYPE OF STATE:\n",type(state.successors()))
        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
       # print("****************************\n")
       # print("STATE TYPE INSIDE MINIMAX:\n",type(state))
        
      #  print("STATE: SUCCESSORS",len(state.successors()))
        if len(state.successors())==0:
            return state.utility()
        
        #means current state is a max player
        if(state.next_player() == -1):
           # print("STATE IS MAX PLAYER")
            bestVal = float('-inf')
            nextMoves = state.successors()
            for move in nextMoves:
               # print("TYPE OF MOVE:",move[1])
                #value = self.minimax(state.next_player(),move)
                value = self.minimax(move[1])
                bestVal = max(value,bestVal)
            return bestVal
        
        #means current state is a min player
        else:
            #print("STATE IS MIN PLAYER\n")
            bestVal = float('+inf')
            nextMoves = state.successors()
            for move in nextMoves:
                #value = self.minimax(state.next_player(),move)
                value = self.minimax(move[1])
                bestVal = min(value,bestVal)
        return bestVal
        #
        # Fill this in!
        #
       # return 42  # Change this line!


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        
        # reached terminal state


        # Fill this in!
        #
        return 9  # Change this line!

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in constant time for all states!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """
        #
        # Fill this in!
        #
        return state.utility() # Change this line!


class MinimaxPruneAgent(MinimaxAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def pruning(self,state,alpha,beta,parent):
        # #reached terminal node
        if len(state.successors())==0:
            return state.utility()
        
        #means current state is a max player
        if(state.next_player() == -1):
            bestVal = float('-inf')
            nextMoves = state.successors()
            for move in nextMoves:
                # print("TYPE OF MOVE:",move[1])
                #value = self.minimax(state.next_player(),move)
                value = self.pruning(move[1],alpha,beta,state)
                bestVal = max(value,bestVal)
                alpha = max(alpha,bestVal)
                if(beta<= alpha):
                    break  
            return bestVal
        
        #means current state is a min player
        else:
            #print("STATE IS MIN PLAYER\n")
            bestVal = float('+inf')
            nextMoves = state.successors()
            for move in nextMoves:
                #value = self.minimax(state.next_player(),move)
                value = self.pruning(move[1],alpha,beta,state)
                bestVal = min(value,bestVal)
                beta = min(beta,value)
                if(beta<=alpha):
                    break
                
        return bestVal
        
    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not use a depth limit like MinimaxHeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        #
        # Fill this in!
        #
        alpha = float('-inf')
        beta = float('+inf')
        bestVal = 0
        nextMoves = state.successors()
        for move in nextMoves:
            val = self.pruning(move[1],alpha,beta,state)
            #state is min player
            if(move[1].next_player() == -1):
                bestVal = min(bestVal,val)
            else:
                bestVal = max(bestVal,val)
        return bestVal
        #return 13  # Change this line!


# N.B.: The following class is provided for convenience only; you do not need to implement it!

class OtherMinimaxHeuristicAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""
        #
        # Fill this in, if it pleases you.
        #
        return 26  # Change this line, unless you have something better to do.
