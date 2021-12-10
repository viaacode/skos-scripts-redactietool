#!/usr/bin/env python
# coding: utf-8

import argparse
from numpy.core.numeric import NaN

# importing packages
import pandas as pd
import re


def tidy_split(df, column, sep="|", keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.
    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row
    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()

    for i, presplit in enumerate(df[column]):
        if presplit is NaN:
            indexes.append(i)
            new_values.append(presplit)
            continue

        values = re.split('''{}(?=(?:[^'"]|'[^']*'|"[^"]*")*$)'''.format(sep), presplit)

        #values = presplit.split(sep)        
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="csv file that need normalization")
    parser.add_argument("column", nargs="+")
    parser.add_argument(
        "-s",
        "--separator",
        required=False,
        help="Character to separate value on.",
        default=",",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    for c in args.column:
        df = tidy_split(df, c, args.separator)
    print(df.to_csv())
