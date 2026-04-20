# Sudoku Solver
This is a project I did in college that I've decided to upload and refine as a personal project to 1) realize how far I've come since college and 2) practice Python where I don't get practice anymore. 

## Program Operating Procedure
### 1. Resolve the parsed arguments.
The following arguments can be passed to the program:
* `--puzzle_name` : String; The file path/name of the XML file detailing the puzzle's parameters. 
* `--solve_on_startup` : Boolean; Whether to solve the puzzle on startup.
* `--time_delay` : Float; Delay, in seconds, between each solving step.
* `--solution_name` : String; Name of the output XML file solution.
* `--exit_on_solve` : Boolean; Whether to exit program on solving the puzzle.

### 2. Load the solution and create the GUI.
### 3. Process the steps.
Regardless of how many steps are specified (or completing the entire puzzle), the logic remains the same. 
1. Iterate through the grid and find a solved cell.
1. Use the solved cell to eliminate its number from all adjoining cells in the same:
   * row
   * column
   * box
1. Find the next solved cell, repeat steps 2 and 3.
1. After iterating through the final cell, check if the puzzle has been solved. If not, start over! 

Eventually: Implement pigeon-hole solving. 