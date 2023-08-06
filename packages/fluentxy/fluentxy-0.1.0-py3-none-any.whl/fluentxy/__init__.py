"""An interface to produce Pandas DataFrames from Fluent XY output files."""

from parse import parse
import numpy as np
import pandas as pd

from typing import List

__version__ = "0.1.0"


def parse_data(lines: List) -> pd.DataFrame:
    """Parse an XY-formatted datafile from Fluent and return a DataFrame."""
    axis_labels = parse('(labels "{x}" "{y}")', lines[1])
    columns = []
    for line in lines[2:]:
        if line.startswith("(("):
            columns.append(parse('((xy/key/label "{label}")', line)["label"])
    index = pd.MultiIndex.from_product([columns, [axis_labels["x"], axis_labels["y"]]])
    data = pd.DataFrame(columns=index)
    finish = False
    this_data = []
    for line in lines[2:]:
        if line.startswith("(("):
            column = parse('((xy/key/label "{label}")', line)["label"]
        # Skip blank lines
        elif not line.strip() or line.startswith(("(",)):
            continue
        elif line.startswith(")"):
            finish = True
        else:
            x, y = parse("{:g}\t{:g}", line.strip())
            this_data.append([x, y])

        if finish:
            this_data = np.array(this_data)
            data[(column, axis_labels["x"])] = this_data[:, 0]
            data[(column, axis_labels["y"])] = this_data[:, 1]
            finish = False
            this_data = []
    return data


def plot_xy(axis, df, column, x_label, y_label):
    """Plot an X-Y line plot from the given column in the df on axis."""
    axis.plot(df[(column, x_label)], df[(column, y_label)])
