from board import Board, ROWS, SEPARATOR
from node import Node


def main():
    rows = []
    for row in range(ROWS):
        rows.append(input("Row " + str(row + 1) + ": "))
    b = Board(SEPARATOR.join(rows))
    n = Node(b)
    moves = n.solution()
    if moves is None:
        moves = n.find_optimum()
    move_nr = 1
    for src, target in moves:
        print("{0:3}: Move {1} from Row {2}, Col {3} to Row {4}, Col {5}".format(
            move_nr, b.grid[src[0]][src[1]], src[0] + 1, src[1] + 1, target[0] + 1, target[1] + 1))
        b = b.move_card(src, target)
        move_nr += 1
    if b.solved():
        print("Solved in {0} moves".format(len(moves)))


if __name__ == '__main__':
    main()  # pragma: no cover
