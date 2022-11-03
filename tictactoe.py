"""
Tic Tac Toe Player
"""
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board, assuming X gets the first
    move in the initial game state.
    """

    # Sum of empty cells on the board
    count = 0

    # Compute the total number of empty cells on the board
    for row in board:
        count += row.count(EMPTY)

    if count % 2 == 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Set to store possible actions
    possible_actions = set()

    # Add the empty cells to the set of possible actions
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Destructure the given action
    i, j = action

    # Raise an exception if the given position is not valid
    try:
        board[i][j]
    except IndexError:
        raise Exception(f'({i}, {j}) is not a valid board position!')

    # Raise an exception if the cell is already occupied
    if board[i][j] != EMPTY:
        raise Exception(f'({i}, {j}) is already occupied!')

    # Deep copy the board so that it's left unmodified
    new_board = deepcopy(board)

    # Get the next player and update the new board
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # List to store the scores of the 1st, 2nd, and 3rd rows and columns
    rows = [0, 0, 0]
    cols = [0, 0, 0]

    # Score for the right and left diagonals
    right_dia, left_dia = 0, 0

    # Loop over each cell and calculate the scores for rows, columns, diagonals
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                continue

            # Count X as 1 and O as -1
            score = 1 if cell == X else -1

            # Update the score of diagonals and the relevant row and column
            if i == j:
                left_dia += score
            if i + j == 2:
                right_dia += score
            rows[i] += score
            cols[j] += score

            # Check if there is a winner and return the winner if there is one
            if 3 * score in {rows[i], cols[j], left_dia, right_dia}:
                return cell

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Return True if there is a winner or there are no empty cells
    if winner(board) or not any(EMPTY in row for row in board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Store the winner to reduce computation time
    winner_player = winner(board)

    # Return either -1, 0, or 1 based on the winner
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Return the action that yields the best score for the current player
    if player(board) == X:
        return max_value(board)[1]
    return min_value(board)[1]


def max_value(board):
    """
    Finds the action that yields the highest score and returns that score and
    the corresponding action.
    """

    # If the game is over, return the score and None
    if terminal(board):
        return utility(board), None

    # Set the best score to negative infinity and the best action to None
    best_score, best_action = float('-inf'), None

    # Iterate over possible actions
    for action in actions(board):

        # Find the minimum score
        score, _ = min_value(result(board, action))

        # Update the best score and action if there is a better score
        if best_score < score:
            best_score, best_action = score, action

            # Return the best score and action if best score is already 1
            if best_score == 1:
                return best_score, best_action

    return best_score, best_action


def min_value(board):
    """
    Finds the action that yields the lowest score and returns that score and
    the corresponding action.
    """

    # If the game is over, return the score and None
    if terminal(board):
        return utility(board), None

    # Set the best score to infinity and the best action to None
    best_score, best_action = float('inf'), None

    # Iterate over possible actions
    for action in actions(board):

        # Find the maximum score
        score, _ = max_value(result(board, action))

        # Update the best score and action if there is a better score
        if best_score > score:
            best_score, best_action = score, action

            # Return the best score and action if best score is already -1
            if best_score == -1:
                return best_score, best_action

    return best_score, best_action
