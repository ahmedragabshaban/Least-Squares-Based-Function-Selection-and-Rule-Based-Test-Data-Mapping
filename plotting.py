from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
import pandas as pd

def draw_charts(train, ideal, mapped_data, models):
    output_file("plots.html")
    my_plots = []
    
    if mapped_data:
        test_df = pd.DataFrame(mapped_data)
    else:
        test_df = pd.DataFrame(columns=['x', 'y', 'ideal_function'])

    colors = ['red', 'green', 'blue', 'orange']

    for i in range(4):
        model = models[i]
        t_col = model['train']
        i_col = model['ideal']

        p = figure(title="Train {} vs Ideal {}".format(t_col, i_col), width=800, height=400)

        # Plot lines and dots
        p.scatter(train['x'], train[t_col], color="black", legend_label="Train")
        p.line(ideal['x'], ideal[i_col], color=colors[i], line_width=2, legend_label="Ideal")

        # Plot mapped points
        subset = test_df[test_df['ideal_function'] == i_col]
        if not subset.empty:
            p.scatter(subset['x'], subset['y'], color="purple", size=8, legend_label="Mapped Test")

        my_plots.append(p)

    save(column(my_plots))
    print("Plots saved.")
