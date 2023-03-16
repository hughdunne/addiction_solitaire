from board import Board, ROWS, SEPARATOR
from node import Node


def main():
    rows = []
    for row in range(ROWS):
        rows.append(input("Row " + str(row + 1) + ": "))
    b = Board(SEPARATOR.join(rows))
    n = Node(b)
    n.get_subtree()
    moves = n.find_optimum()
    for src, target in moves:
        print("Move {0} from Row {1}, Col {2} to Row {3}, Col {4}".format(
            b.grid[src[0]][src[1]], src[0] + 1, src[1] + 1, target[0] + 1, target[1] + 1))
        b = b.move_card(src, target)
    if b.solved():
        print("Solved in {0} moves".format(len(moves)))


if __name__ == '__main__':
    main()  # pragma: no cover
