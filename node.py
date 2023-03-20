class Node:
    boards_seen = set()
    best_score = 0

    def __init__(self, board, prev_move=None, parent=None):
        if prev_move is None:
            # This is root node so we reset
            Node.boards_seen = set()
            Node.best_score = 0
            self.path_from_root = []
        else:
            self.path_from_root = parent.path_from_root + [prev_move]
        self.board = board
        self.score = board.score()
        if self.score > Node.best_score:
            Node.best_score = self.score
        self.children = []

    def solution(self):
        q = [self]
        while len(q) > 0:
            curr_node = q.pop(0)
            for move in curr_node.board.valid_moves():
                child_board = curr_node.board.move_card(*move)
                str_board = str(child_board)
                if str_board not in Node.boards_seen:
                    Node.boards_seen.add(str_board)
                    child_node = Node(child_board, move, curr_node)
                    curr_node.children.append(child_node)
            if len(curr_node.children) == 0:
                if curr_node.board.solved():
                    return curr_node.path_from_root
            else:
                q += curr_node.children
        return None

    def find_optimum(self):
        # Do a breadth-first search
        q = [self]
        while len(q) > 0:
            curr_node = q.pop(0)
            if curr_node.score == Node.best_score:
                return curr_node.path_from_root
            q += curr_node.children
