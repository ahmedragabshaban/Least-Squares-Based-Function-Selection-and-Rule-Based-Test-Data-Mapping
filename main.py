import argparse
import sys
from processing import AssignmentModel, MyError
from plotting import draw_charts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='train.csv')
    parser.add_argument('--ideal', default='ideal.csv')
    parser.add_argument('--test', default='test.csv')
    args = parser.parse_args()

    # Create object
    app = AssignmentModel()

    try:
        print("Start...")
        
        # Load
        train_df = app.load_data(args.train)
        ideal_df = app.load_data(args.ideal)
        test_df = app.load_data(args.test)
        
        app.create_db()

        # Select functions
        print("Training...")
        app.train(train_df, ideal_df)

        # Map points
        print("Mapping...")
        results = app.test(test_df, ideal_df)
        print("Mapped points: {}".format(len(results)))

        # Save
        app.save_all(train_df, ideal_df, results)

        # Plot
        draw_charts(train_df, ideal_df, results, app.best_funcs)
        
        print("Finished successfully.")

    except MyError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Something went wrong: {}".format(e))

if __name__ == '__main__':
    main()
