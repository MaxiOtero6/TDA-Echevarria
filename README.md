# TDA-Echevarria

## TP1

### Run commands

#### DyC

-   `python3 -m TP1.DyC.plot`: Run plot cases for this algorithm
-   `pytest TP1/DyC/dc_test.py`: Run tests

#### Greedy

-   `python -m TP1.Greedy.plot`: Run plot cases for this algorithm
-   `pytest TP1/Greedy/greedy_test.py`: Run tests

#### Backtracking

-   `python -m TP1.Backtracking.algo`: Run algorithm and dump results
-   `pytest TP1/Backtracking/backtracking_test.py`: Run tests

#### Dinamica

-   `python -m TP1.Dinamica.dinamica`: Run algorithm and dump results
-   `pytest TP1/Dinamica/dinamica_test.py`: Run tests

## TP2

### Run commands

#### PL

-   `python3 -m TP2.`:

#### RF

-   `python -m TP2.RF.algo`: Run algorithm with base case

#### AA

-   `python -m TP2.AA.algo`: Run algorithm with predefined test cases and generate results
- The `generar_casos_prueba()` function defiens 6 test cases: basic, large items, small items, worst case, mixed and random
- Results are automatically exported to `resultados.txt`

#### AR

-   `python -m TP2.`:

## Makefile Commands

-   `make build`: Creates a Python virtual environment (.venv) and installs dependencies from requirements.txt.
-   `make test`: Activates the virtual environment and runs pytest to execute unit tests for all algorithms.
-   `make format`: Activates the virtual environment and formats Python code using Black.
-   `make lint`: Activates the virtual environment and lints Python code using Pylint.
