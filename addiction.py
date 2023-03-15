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
        print(str(b.grid[src[0]][src[1]]) + ' to Row ' + str(target[0] + 1) + ', Col ' + str(target[1] + 1))
        b = b.move_card(src, target)


if __name__ == '__main__':
    main()
