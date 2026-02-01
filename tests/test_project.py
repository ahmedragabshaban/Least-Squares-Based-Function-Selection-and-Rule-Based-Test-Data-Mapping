import unittest
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processing import AssignmentModel

class TestAssignment(unittest.TestCase):
    
    def setUp(self):
        # Setup a dummy model and data before each test
        self.model = AssignmentModel("test_database.db")
        
        # Create dummy Training Data
        # y1 is constant 10
        self.train = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y1': [10.0, 10.0, 10.0],
            'y2': [20.0, 20.0, 20.0], 
            'y3': [30.0, 30.0, 30.0],
            'y4': [40.0, 40.0, 40.0]
        })
        
        # Create dummy Ideal Data
        # y5 matches y1 perfectly (constant 10)
        self.ideal = pd.DataFrame({'x': [1.0, 2.0, 3.0]})
        for i in range(1, 51):
            if i == 5:
                self.ideal[f'y{i}'] = [10.0, 10.0, 10.0]
            else:
                self.ideal[f'y{i}'] = [100.0, 100.0, 100.0] # Far away values

    def test_ideal_function_selection(self):
        # Test if the model selects y5 for y1 (Perfect match)
        self.model.train(self.train, self.ideal)
        
        # Check results
        selected = self.model.best_funcs[0]
        self.assertEqual(selected['train'], 'y1')
        self.assertEqual(selected['ideal'], 'y5')

    def test_mapping_logic(self):
        # Test if points are accepted/rejected correctly
        
        # Force a specific selection: Train y1 -> Ideal y5 (deviation 0.5)
        # Threshold will be 0.5 * sqrt(2) = approx 0.707
        self.model.best_funcs = [{
            'train': 'y1', 
            'ideal': 'y5', 
            'max_dev': 0.5
        }]
        
        # Case 1: Point with diff 0.6 (Should PASS because 0.6 < 0.707)
        pass_data = pd.DataFrame({'x': [1.0], 'y': [10.6]})
        results = self.model.test(pass_data, self.ideal)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['ideal_function'], 'y5')
        
        # Case 2: Point with diff 0.8 (Should FAIL because 0.8 > 0.707)
        fail_data = pd.DataFrame({'x': [1.0], 'y': [10.8]})
        results_fail = self.model.test(fail_data, self.ideal)
        
        self.assertEqual(len(results_fail), 0)

    def tearDown(self):
        # Remove the temporary test database
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")

if __name__ == '__main__':
    unittest.main()