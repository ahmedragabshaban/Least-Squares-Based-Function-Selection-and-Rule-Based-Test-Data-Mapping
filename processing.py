import pandas as pd
import math
import os
from sqlalchemy import create_engine
from db_models import Base

class MyError(Exception):
    pass

class AssignmentModel:
    def __init__(self, db_name="assignment.db"):
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.best_funcs = [] 

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def load_data(self, path):
        if not os.path.exists(path):
            raise MyError(f"File not found: {path}")
        try:
            return pd.read_csv(path)
        except Exception as e:
            raise MyError(f"Failed to read CSV: {e}")

    def train(self, train_df, ideal_df):
        # Finds the 4 best ideal functions using Least Squares.
        for i in range(1, 5):
            col_train = f'y{i}'
            min_error = float('inf')
            chosen = None
            max_deviation = 0.0

            # Compare with all 50 ideal columns
            for k in range(1, 51):
                col_ideal = f'y{k}'
                
                # Calculate squared error
                diff = train_df[col_train] - ideal_df[col_ideal]
                current_error = (diff ** 2).sum()

                if current_error < min_error:
                    min_error = current_error
                    chosen = col_ideal
                    max_deviation = diff.abs().max()

            self.best_funcs.append({
                'train': col_train,
                'ideal': chosen,
                'max_dev': max_deviation
            })
            print(f"Function {col_train} -> {chosen}")

    def test(self, test_df, ideal_df):
        results = []
        
        for index, row in test_df.iterrows():
            x_val = row['x']
            y_val = row['y']
            
            match_row = ideal_df[ideal_df['x'] == x_val]
            
            if match_row.empty:
                continue

            best_match = None
            min_delta = float('inf')

            # Check the 4 selected functions
            for item in self.best_funcs:
                ideal_name = item['ideal']
                allowed_dev = item['max_dev'] * math.sqrt(2)
                
                ideal_y = match_row.iloc[0][ideal_name]
                delta = abs(y_val - ideal_y)

                if delta <= allowed_dev:
                    if delta < min_delta:
                        min_delta = delta
                        best_match = ideal_name

            if best_match:
                results.append({
                    'x': x_val,
                    'y': y_val,
                    'delta_y': min_delta,
                    'ideal_function': best_match
                })
        
        return results

    def save_all(self, train, ideal, mapped):
        print("Saving to DB...")
        train.to_sql('training_data', self.engine, if_exists='replace', index=False)
        ideal.to_sql('ideal_functions', self.engine, if_exists='replace', index=False)
        
        if len(mapped) > 0:
            df = pd.DataFrame(mapped)
            df.to_sql('test_mapping', self.engine, if_exists='replace', index=False)
