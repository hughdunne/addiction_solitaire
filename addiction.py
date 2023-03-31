from board import Board, format_slot, ROWS, SEPARATOR
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
        print("{0:3}: Move {1} from {2} to {3}".format(
            move_nr, b.grid[src[0]][src[1]], format_slot(src), format_slot(target)))
        b = b.move_card(src, target)
        move_nr += 1
    if b.solved():
        print("Solved in {0} moves".format(len(moves)))


if __name__ == '__main__':
    main()  # pragma: no cover
