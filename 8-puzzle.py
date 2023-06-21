import heapq

# Class representing the puzzle state
class PuzzleState:
    def __init__(self, board, parent=None, move=""):
        self.board = board
        self.parent = parent
        self.move = move
        self.cost = 0
        self.heuristic = 0

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def calculate_cost(self, target):
        # Calculate the Manhattan distance heuristic
        self.heuristic = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != target[i][j]:
                    self.heuristic += 1

    def get_next_states(self):
        blank_pos = self.find_blank()
        moves = []

        # Generate possible moves
        if blank_pos[0] > 0:
            moves.append("U")
        if blank_pos[0] < 2:
            moves.append("D")
        if blank_pos[1] > 0:
            moves.append("L")
        if blank_pos[1] < 2:
            moves.append("R")

        next_states = []
        for move in moves:
            new_board = [row[:] for row in self.board]
            new_blank_pos = list(blank_pos)

            if move == "U":
                new_blank_pos[0] -= 1
            elif move == "D":
                new_blank_pos[0] += 1
            elif move == "L":
                new_blank_pos[1] -= 1
            elif move == "R":
                new_blank_pos[1] += 1

            # Swap blank position with the adjacent tile
            new_board[blank_pos[0]][blank_pos[1]], new_board[new_blank_pos[0]][new_blank_pos[1]] = \
                new_board[new_blank_pos[0]][new_blank_pos[1]], new_board[blank_pos[0]][blank_pos[1]]

            next_state = PuzzleState(new_board, parent=self, move=move)
            next_states.append(next_state)

        return next_states

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return [i, j]

    def print_moves(self):
        if self.parent:
            self.parent.print_moves()
        print("Move:", self.move)
        self.print_board()

    def print_board(self):
        for row in self.board:
            print(row)
        print()

# A* algorithm for solving the puzzle
def solve_puzzle(initial, target):
    # Initialize the priority queue
    open_list = []
    heapq.heappush(open_list, initial)

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.board == target:
            print("Puzzle solved!")
            current_state.print_moves()
            break

        next_states = current_state.get_next_states()
        for next_state in next_states:
            next_state.calculate_cost(target)
            next_state.cost = current_state.cost + 1
            heapq.heappush(open_list, next_state)

# Example usage
initial_state = PuzzleState([[1, 2, 3], [0, 4, 6], [7, 5, 8]])
target_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

solve_puzzle(initial_state, target_state)
