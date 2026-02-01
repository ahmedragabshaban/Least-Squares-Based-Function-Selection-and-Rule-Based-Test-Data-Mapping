# Python Data Assignment

This project implements a data pipeline to select ideal functions for training data and map test points based on specific criteria.

## Requirements
*   Python 3.x
*   pandas
*   sqlalchemy
*   bokeh

## Setup
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Place your CSV files (`train.csv`, `ideal.csv`, `test.csv`) in a folder named `data`.

## How to Run

**1. Run the Main Script:**
Run the main script from the terminal:
```bash
python main.py --train data/train.csv --ideal data/ideal.csv --test data/test.csv
```

**2. Run Unit Tests:**
To run the tests, execute:
```bash
python -m unittest discover tests
```
