# Install python packages
apt install python3-full python3-pip python3-venv
# Create virtual environment if one doesn't exist.
if [ -d "bin"]; then 
    echo "Virtual environment exists"
else 
    echo "Virtual environment doesn't exist, creating"
    python3 -m venv .
fi

# Change directory to existing venv
cd ./bin

# Install requirements
#./pip install -r ../requirements.txt; 

# Run main
python3 ../solver.py --puzzle_name /home/andrew/Documents/repositories/sudoku-solver/start-states/9x9-solvable.xml --solve_on_startup;