# addiction
Program to solve the addiction solitaire game.

## Prerequisites

Should work with any recent version of Python.

## Usage

    python addiction.py

You will be prompted to enter the board row by row. You can enter each card as a
two-character string where the first character is the suit and the second
character is the value, e.g. "DA" for the ace of diamonds or "S6" for the six of
spades. Cards are delimited by commas. Use an extra comma to represent a blank
space.

### Example:

![Screenshot](addiction.PNG)

    Row 1: SA,D5,S6,H3,C2,H5,C4
    Row 2: DA,S5,S3,,,,C6
    Row 3: CA,D4,D6,H4,C5,C3,S4
    Row 4: HA,H2,H6,D2,S2,,D3

The program will then output the solution, move by move:

      1: Move S4 from Row 3, Col 7 to Row 2, Col 4
      2: Move S5 from Row 2, Col 2 to Row 2, Col 5
      3: Move D2 from Row 4, Col 4 to Row 2, Col 2
      4: Move S6 from Row 1, Col 3 to Row 2, Col 6
      5: Move D6 from Row 3, Col 3 to Row 1, Col 3
      6: Move D5 from Row 1, Col 2 to Row 3, Col 3
      7: Move S2 from Row 4, Col 5 to Row 1, Col 2
      8: Move C4 from Row 1, Col 7 to Row 3, Col 7
      9: Move H6 from Row 4, Col 3 to Row 1, Col 7
     10: Move H3 from Row 1, Col 4 to Row 4, Col 3
     11: Move H4 from Row 3, Col 4 to Row 4, Col 4
     12: Move D6 from Row 1, Col 3 to Row 3, Col 4
     13: Move S3 from Row 2, Col 3 to Row 1, Col 3
     14: Move S4 from Row 2, Col 4 to Row 1, Col 4
     15: Move D3 from Row 4, Col 7 to Row 2, Col 3
     16: Move D4 from Row 3, Col 2 to Row 2, Col 4
     17: Move C2 from Row 1, Col 5 to Row 3, Col 2
     18: Move S5 from Row 2, Col 5 to Row 1, Col 5
     19: Move D5 from Row 3, Col 3 to Row 2, Col 5
     20: Move C3 from Row 3, Col 6 to Row 3, Col 3
     21: Move C6 from Row 2, Col 7 to Row 3, Col 6
     22: Move H5 from Row 1, Col 6 to Row 4, Col 5
     23: Move S6 from Row 2, Col 6 to Row 1, Col 6
     24: Move D6 from Row 3, Col 4 to Row 2, Col 6
     25: Move C4 from Row 3, Col 7 to Row 3, Col 4
     26: Move H6 from Row 1, Col 7 to Row 4, Col 6
    Solved in 26 moves

## Testing

    pytest test_addiction.py

## Notes

The program does not assume that the puzzle can be solved without shuffling.
It tries to maximize the number of cards locked in, and to do so in the
fewest moves. Since it does not take account of shuffling, it's possible
that partially solving the puzzle, then shuffling and then completing the
puzzle may result in fewer moves than the optimum solution this program finds.